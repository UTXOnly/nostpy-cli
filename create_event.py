import asyncio
import argparse
import hashlib
import json
import secp256k1
import time
import websockets
import ast

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

    def create_event(self, public_key, private_key_hex, content, kind, tags):
        #tags = []#[["p", public_key]]
        #tags = json.loads(tags) if isinstance(tags, str) else tags
        #tags = tags or []
        created_at = int(time.time())
        kind
        event_id = self.calc_event_id(
            public_key, created_at, kind, tags, content
        )
        signature_hex = self.sign_event_id(event_id, private_key_hex)
        event_data = {
            "id": event_id,
            "pubkey": public_key,
            "kind": kind,
            "created_at": created_at,
            "tags": tags,
            "content": content,
            "sig": signature_hex,
        }
        #print(f"Event created is {event_data}")
        return event_data

    async def send_event(self, public_key, private_key_hex, content, kind, tags):
        try:
            event_data = self.create_event(public_key, private_key_hex, content, kind, tags)
            for ws_relay in self.relays_kind4:
                async with websockets.connect(ws_relay) as ws:
                    event_json = json.dumps(("EVENT", event_data))
                    print(f"Event to send is {event_json}")
                    await ws.send(event_json)
                    response = await asyncio.wait_for(ws.recv(), timeout=10)
                    print("Response:", response)
        except Exception as exc:
            print(f"Error in sending event: {exc}")

def main():
    parser = argparse.ArgumentParser(description="Send events via WebSocket.")
    parser.add_argument("-pubkey", "--public_key", required=True, help="Public key in hexadecimal")
    parser.add_argument("-privkey", "--private_key", required=True, help="Private key in hexadecimal")
    parser.add_argument("-content", "--content", required=True, help="Encrypted content to send as event")
    parser.add_argument("-tags", "--tags", default='[]', type=ast.literal_eval, help="Tags to add to event in JSON format e.g. '[]' for no tags or '[['tag1', 'value1'], ['tag2', 'value2']]'")
    parser.add_argument("-kind", "--kind", required=True, type=int, help="Event kind")
    parser.add_argument("--relay", nargs="+", required=True, help="WebSocket relay URLs")

    args = parser.parse_args()

    event = Event(relays_kind4=args.relay)
    asyncio.run(event.send_event(args.public_key, args.private_key, args.content, args.kind, args.tags))

if __name__ == "__main__":
    main()


