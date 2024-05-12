#!/usr/bin/env python3
import asyncio
import argparse
import ast

from .create_event import Event
from .kind4 import Kind4MessageCodec


async def handle_query(args):
    event = Event(relays=args.relay)

    all_args = {
        "kinds": args.kinds,
        "search": args.search,
        "since": args.since,
        "until": args.until,
        "authors": args.authors,
        "limit": args.limit,
    }

    query_dict = {key: value for key, value in all_args.items() if value is not None}
    await event.query_relays(query_dict)


async def handle_send_event(args):
    event = Event(relays=args.relay)
    if args.kind == 4:
        kind4_codec = Kind4MessageCodec(args.private_key, args.tags[0][1])
        args.content = kind4_codec.encrypt_message(args.content)
    await event.send_event(
        args.public_key, args.private_key, args.content, args.kind, args.tags
    )


def main():
    parser = argparse.ArgumentParser(description="Send and query nostr events")
    subparsers = parser.add_subparsers(
        title="commands", description="valid commands", help="additional help"
    )

    # Subparser for the "query" command
    query_parser = subparsers.add_parser("query", help="Query events")
    query_parser.add_argument(
        "-kinds",
        "--kinds",
        type=ast.literal_eval,
        help="Kinds to query e.g. '[1,9075]'",
    )
    query_parser.add_argument("-search", "--search", help="Search content and tags")
    query_parser.add_argument(
        "-since", "--since", type=int, help="Collect events since"
    )
    query_parser.add_argument(
        "-until", "--until", type=int, help="Collect events until"
    )
    query_parser.add_argument(
        "-authors", "--authors", type=str, help="List of authors e.g. []"
    )
    query_parser.add_argument(
        "-limit",
        "--limit",
        type=ast.literal_eval,
        help="Limit on number of results returned",
    )
    query_parser.add_argument(
        "--relay", nargs="+", required=True, help="WebSocket relay URLs"
    )
    query_parser.set_defaults(func=handle_query)

    # Subparser for the "send_event" command
    send_event_parser = subparsers.add_parser("send_event", help="Send an event")
    send_event_parser.add_argument(
        "-pubkey", "--public_key", required=True, help="Public key in hexadecimal"
    )
    send_event_parser.add_argument(
        "-privkey", "--private_key", required=True, help="Private key in hexadecimal"
    )
    send_event_parser.add_argument(
        "-content", "--content", help="Encrypted content to send as event"
    )
    send_event_parser.add_argument(
        "-tags",
        "--tags",
        default="[]",
        type=ast.literal_eval,
        help="Tags to add to event",
    )
    send_event_parser.add_argument("-kind", "--kind", type=int, help="Event kind")
    send_event_parser.add_argument(
        "--relay", nargs="+", required=True, help="WebSocket relay URLs"
    )
    send_event_parser.set_defaults(func=handle_send_event)

    parser.epilog = 'Example send usage: nostpy-cli send_event -pubkey "abc123..." -privkey "def456..." -content "Hello, world!" --relay "wss://example.com"'

    args = parser.parse_args()
    if hasattr(args, "func"):
        asyncio.run(args.func(args))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
