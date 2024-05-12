import asyncio
import hashlib
import typing
import json
import secp256k1
import time
import websockets


class Event:
    def __init__(self, relays_kind4) -> None:
        self.relays_kind4 = relays_kind4  # List of relay URLs

    def print_color(self, text, color):
        print(f"\033[1;{color}m{text}\033[0m")

    def sign_event_id(self, event_id: str, private_key_hex: str) -> str:
        private_key = secp256k1.PrivateKey(bytes.fromhex(private_key_hex))
        sig = private_key.schnorr_sign(
            bytes.fromhex(event_id), bip340tag=None, raw=True
        )
        return sig.hex()

    def calc_event_id(self, public_key: str, created_at: int, kind_number: int, tags: list, content: str) -> str:
        data = [0, public_key, created_at, kind_number, tags, content]
        data_str = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
        return hashlib.sha256(data_str.encode("UTF-8")).hexdigest()

    def create_event(self, public_key: str, private_key_hex: str, content: str, kind: int, tags: list):
        created_at = int(time.time())
        kind
        event_id = self.calc_event_id(
            public_key, created_at, kind, tags, content
        )
        signature_hex = self.sign_event_id(event_id, private_key_hex)
        try:
            self.verify_signature(event_id, public_key, signature_hex)
        except Exception as exc:
            print(f"Error verifying sig: {exc}")
            return
        event_data = {
            "id": event_id,
            "pubkey": public_key,
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

    async def send_event(self, public_key, private_key_hex, content, kind, tags):
        try:
            event_data = self.create_event(public_key, private_key_hex, content, kind, tags)
            for ws_relay in self.relays_kind4:
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

    async def query_relays(self, query_dict):
        for relay in self.relays_kind4:
            try:
                async with websockets.connect(relay) as ws:
                    query_ws = json.dumps(("REQ", "5326483051590112", query_dict))
                    await ws.send(query_ws)
                    print(f"Query sent to relay {relay}: {query_ws}")
                    try:
                        response = json.loads(await asyncio.wait_for(ws.recv(), timeout=3))
                        print(f"Response from query is: {response}")
                        return response
                    except asyncio.TimeoutError:
                        self.print_color("No response within 1 second, continuing...", "31")
                        return
            except Exception as exc:
                self.print_color(f"Exception is {exc}, error querying {relay}", "31")



