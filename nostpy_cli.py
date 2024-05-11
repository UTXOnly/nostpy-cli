import asyncio
import argparse
import ast

from create_event import Event
from kind4 import Kind4MessageCodec

def main():
    parser = argparse.ArgumentParser(description="Send events via WebSocket.")
    parser.add_argument("-pubkey", "--public_key", required=True, help="Public key in hexadecimal")
    parser.add_argument("-privkey", "--private_key", required=True, help="Private key in hexadecimal")
    parser.add_argument("-content", "--content", required=True, help="Encrypted content to send as event")
    parser.add_argument("-tags", "--tags", default='[]', type=ast.literal_eval, help="Tags to add to event in JSON format e.g. '[]' for no tags or '[['tag1', 'value1'], ['tag2', 'value2']]'")
    parser.add_argument("-kind", "--kind", required=True, type=int, help="Event kind")
    parser.add_argument("--relay", nargs="+", required=True, help="WebSocket relay URLs")

    args = parser.parse_args()

    if args.kind == 4:
        kind4_codec = Kind4MessageCodec(
            args.private_key, args.tags[0][1]
        )
        kind4_msg = kind4_codec.encrypt_message(args.content)
        args.content = kind4_msg

    event = Event(relays_kind4=args.relay)
    asyncio.run(event.send_event(args.public_key, args.private_key, args.content, args.kind, args.tags))

if __name__ == "__main__":
    main()