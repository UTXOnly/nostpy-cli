# nostpy-cli

`nostpy-cli` is a Command Line Interface tool for sending and querying nostr events by websocket connection.

## Features

- Send events to a specified relays
- Query events from relays
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
Once installed, you can run nostpy-cli from the command line. Below are some examples of how to use the CLI tool:

### Send Event
To send an event, you would use a command similar to the following:

```
nostpy-cli send_event --pubkey "your_public_key" --privkey "your_private_key" --content "your plaintext message" --tags "[['tag1', 'value1']]" --kind 4 --relay "wss://yourrelayurl.com"
```
`--pubkey` , `--priv_key` and `--relay` arguments are required, all else are optional

### Query Event
To query events, use the following command:

```
nostpy-cli query --kinds "[1,9075]" --relay "wss://yourrelayurl.com"
```
`--relay` field required
### Help
To view all available commands and their options, use the help command:

```
nostpy-cli -h
```
## Contributing
Contributions to nostpy-cli are welcome! Please feel free to submit pull requests or open issues to report bugs or suggest enhancements.

### License
This project is licensed under the MIT License - see the LICENSE file for details.
