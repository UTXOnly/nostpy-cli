# nostpy-cli

`nostpy-cli` is a Command Line Interface tool for sending and querying nostr events by websocket connection.

## Features

- Send events to specified relays
- Query events from specified relays
- Encode/decode kind4 messages
- Supports [NIP-50](https://github.com/nostr-protocol/nips/blob/master/50.md) searches

## Prerequisites

Before installing `nostpy-cli`, ensure you have Python 3.6 or higher installed on your system. You can check your Python version by running:

```
python3 --version
```
## Installation

### Install Using pip
To install using `pip` use the command below:
```
pip install nostpy-cli
```

### Build from source
Clone the Repository
First, clone the repository to your local machine:

```
git clone https://github.com/UTXOnly/nostpy-cli.git
cd nostpy-cli
python3 -m build
pip install .
```



## Usage
Once installed, you can run `nostpy-cli` from the command line as shown below:

### Send Event
To send an event, you would use a command similar to the following:

```
nostpy-cli send_event -pubkey "your_public_key_hex" -privkey "your_private_key_hex" -content "your plaintext message" -tags "[['tag1', 'value1']]" -kind 4 --relay "wss://yourrelayurl.com" "wss://yoursecondrelayurl.com"
```
`--pubkey` , `--priv_key` and `--relay` arguments are required, all else are optional

#### Example
* Send a kind 1 event with tags

```
nostpy-cli send_event -pubkey 5ce5b352f1ef76b1dffc5694dd5b34126137184cc9a7d78cba841c0635e17952 -privkey 2b1e4e1f26517dda57458596760bb3bd3bd3717083763166e12983a6421abc18 -content test27 -tags "[
['t', 'vvfdvfd'], ['v', 'v2']]" -kind 1 --relay wss://relay.nostpy.lol wss://relay.damus.io wss://nos.lol
```

* Send a kind 4 direct message
```
nostpy-cli send_event -pubkey 5ce5b352f1ef76b1dffc5694dd5b34126137184cc9a7d78cba841c0635e17952 -privkey 2b1e4e1f26517dda57458596760bb3bd3bd3717083763166e12983a6421abc18 -content "This is my plaintext message" -tags "[['p', '4503baa127bdfd0b054384dc5ba82cb0e2a8367cbdb0629179f00db1a34caacc']]" -kind 4 --relay wss://relay.nostpy.lol wss://relay.damus.io wss://nos.lol
```

### Query Event
To query events, use the following command:

```
nostpy-cli query --kinds "[1,9735]" --relay "wss://yourrelayurl.com"
```
`--relay` field required

#### Example
* Query an event with search
```
nostpy-cli query -kinds "[31990,1]" -search "random_search" -since 1713629501 -authors npub1g5pm4gf8hh7skp2rsnw9h2pvkr32sdnuhkcx9yte7qxmrg6v4txqqudjqv --relay wss://relay.nostpy.lol
```

### Decrypt kind4 message content
Decrypt kind4 message content by providing recipient private key hex, sender public key hex and the message ciphertext, returns the plaintext message

#### Example 
```
nostpy-cli decode -content "kP9dCG/stpEGNTjW2/aySQ==?iv=+GCHVOBAiM9X074n1vxiFg==" -priv_key 2b1e4e1f26517dda57458596760bb3bd3bd3717083763166e12983a6421abc18 -sender_pubkey 4503baa127bdfd0b054384dc5ba82cb0e2a8367cbdb0629179f00db1a34caacc 
```
### Help
To view all available commands and their options, use the help command:

```
nostpy-cli -h
```

```
usage: nostpy-cli [-h] {query,send_event,decode} ...

Send and query nostr events

options:
  -h, --help            show this help message and exit

commands:
  valid commands

  {query,send_event,decode}
                        additional help
    query               Query events
    send_event          Send an event
    decode              Decode kind4 content

Example send usage: nostpy-cli send_event -pubkey "abc123..." -privkey "def456..." -content "Hello, world!" --relay "wss://example.com"
```
## Contributing
Contributions to nostpy-cli are welcome! Please feel free to submit pull requests or open issues to report bugs or suggest enhancements.

### License
This project is licensed under the MIT License - see the LICENSE file for details.
