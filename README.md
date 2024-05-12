# nostpy-cli

`nostpy-cli` is a Command Line Interface (CLI) tool designed to handle nostpy events efficiently. This tool provides easy-to-use commands to send and query events via a WebSocket connection.

## Features

- Send events to a specified relay.
- Query events from a relay.

## Prerequisites

Before installing `nostpy-cli`, ensure you have Python 3.6 or higher installed on your system. You can check your Python version by running:

```
python3 --version
```
## Installation
### Build from source
Clone the Repository
First, clone the repository to your local machine:

```
git clone https://github.com/UTXOnly/nostpy-cli.git
cd nostpy-cli
python3 -m build
pip install .
```

### Install Using pip
To install using `pip` use the command below:
```
pip install nostpy-cli
```

## Usage
Once installed, you can run nostpy-cli from the command line. Below are some examples of how to use the CLI tool:

### Help
To view all available commands and their options, use the help command:

```
nostpy-cli -h
```
### Send Event
To send an event, you would use a command similar to the following:

```
nostpy-cli send_event --pubkey "your_public_key" --privkey "your_private_key" --content "your_encrypted_content" --tags "[['tag1', 'value1']]" --kind 4 --relay "wss://yourrelayurl.com"
```

### Query Event
To query events, use the following command:

```
nostpy-cli query --kinds "[1,9075]" --relay "wss://yourrelayurl.com"
```

## Contributing
Contributions to nostpy-cli are welcome! Please feel free to submit pull requests or open issues to report bugs or suggest enhancements.

### License
This project is licensed under the MIT License - see the LICENSE file for details.
