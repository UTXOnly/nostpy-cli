import asyncio
import hashlib
import json
import secp256k1
import time
import websockets


class Event:
    """
    A class that manages cryptographic events, including their signing, verification, creation, and sending.
    Also includes querying functionality to request information from WebSocket relays.

    Attributes:
        relays (list): A list of WebSocket relays to interact with.

    Methods:
        print_color(text, color):
            Prints a message in a specified color.

        sign_event_id(event_id, private_key_hex) -> str:
            Signs an event ID using a private key in hexadecimal format.

        calc_event_id(public_key, created_at, kind_number, tags, content) -> str:
            Calculates the event ID by hashing event data.

        create_event(public_key, private_key_hex, content, kind, tags) -> dict:
            Creates an event and returns the structured event data dictionary.

        verify_signature(event_id, pubkey, sig) -> bool:
            Verifies an event signature against a public key.

        send_event(public_key, private_key_hex, content, kind, tags):
            Asynchronously sends an event to the configured WebSocket relays.

        query_relays(query_dict, timeout=5):
            Asynchronously queries the configured WebSocket relays with the specified query parameters.
    """

    def __init__(self, relays) -> None:
        self.relays = relays

    def print_color(self, text, color):
        print(f"\033[1;{color}m{text}\033[0m")

    def sign_event_id(self, event_id: str, private_key_hex: str) -> str:
        private_key = secp256k1.PrivateKey(bytes.fromhex(private_key_hex))
        sig = private_key.schnorr_sign(
            bytes.fromhex(event_id), bip340tag=None, raw=True
        )
        return sig.hex()

    def calc_event_id(
        self,
        public_key: str,
        created_at: int,
        kind_number: int,
        tags: list,
        content: str,
    ) -> str:
        data = [0, public_key, created_at, kind_number, tags, content]
        data_str = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
        return hashlib.sha256(data_str.encode("UTF-8")).hexdigest()

    def create_event(
        self, private_key_hex: str, content: str, kind: int, tags: list
    ):
        created_at = int(time.time())
        private_key = secp256k1.PrivateKey(bytes.fromhex(private_key_hex))
        public_key_hex = private_key.pubkey.serialize()[1:].hex()
        event_id = self.calc_event_id(public_key_hex, created_at, kind, tags, content)
        signature_hex = self.sign_event_id(event_id, private_key_hex)
        try:
            self.verify_signature(event_id, public_key_hex, signature_hex)
        except Exception as exc:
            print(f"Error verifying sig: {exc}")
            return
        event_data = {
            "id": event_id,
            "pubkey": public_key_hex,
            "kind": kind,
            "created_at": created_at,
            "tags": tags,
            "content": content,
            "sig": signature_hex,
        }
        return event_data

    def verify_signature(self, event_id: str, pubkey: str, sig: str) -> bool:
        try:
            pub_key = secp256k1.PublicKey(bytes.fromhex("02" + pubkey), True)
            result = pub_key.schnorr_verify(
                bytes.fromhex(event_id), bytes.fromhex(sig), None, raw=True
            )
            if result:
                self.print_color(f"Verification successful for event: {event_id}", "32")
                return True
            else:
                self.print_color(f"Verification failed for event: {event_id}", "31")
                return False
        except (ValueError, TypeError) as e:
            print(f"Error verifying signature for event {event_id}: {e}")
            return False

    async def send_event(self, private_key_hex, content, kind, tags):
        try:
            event_data = self.create_event(
                private_key_hex, content, kind, tags
            )
            for ws_relay in self.relays:
                async with websockets.connect(ws_relay) as ws:
                    event_json = ("EVENT", event_data)
                    print("Sending event:")
                    self.print_color(f"{event_json}", "32")
                    print(f"to {ws_relay}")
                    await ws.send(json.dumps(event_json))
                    response = await asyncio.wait_for(ws.recv(), timeout=10)
                    print(f"Response from {ws_relay} is : ")
                    self.print_color(f"{response}", "33")
        except Exception as exc:
            print(f"Error in sending event: {exc}")

    async def query_relays(self, query_dict, timeout=5):
        for relay in self.relays:
            try:
                async with websockets.connect(relay) as ws:
                    query_ws = json.dumps(("REQ", "5326483051590112", query_dict))
                    await ws.send(query_ws)
                    print(f"Query sent to relay {relay}: {query_ws}")

                    responses_received = 0
                    start_time = time.time()
                    response_limit = query_dict.get("limit", 3)

                    while (
                        responses_received < response_limit
                        and (time.time() - start_time) < timeout
                    ):
                        try:
                            response = await asyncio.wait_for(ws.recv(), timeout=1)
                            self.print_color(f"Response from {relay}: {response}", "32")
                            responses_received += 1
                        except asyncio.TimeoutError:
                            self.print_color(
                                "No response within 1 second, continuing...", "31"
                            )
                            break
            except Exception as exc:
                self.print_color(f"Exception is {exc}, error querying {relay}", "31")
