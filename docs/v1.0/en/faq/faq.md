---
title: "FAQ"
excerpt: ""
---


This guide addresses frequently asked questions.

We are working very hard to answer everyone's questions, but there are only so many of us, so 
**please try to find the answer to your question before asking on Discord.**
Look on this page first, and if you don't find the answer here, search on Discord. 
If you're having an issue, chances are high that somebody else had the same issue.
If your question is still unanswered, ask about it on our [Discord](https://chat.avalabs.org) server.

**There is a list of known issues at the bottom of this page.**

##  Questions

### Where can I go for help?

[Discord](https://chat.avalabs.org), but please search the documentation and Discord for your issue before asking about it.

### I think something went wrong or there's a bug. What do I do?

First, re-read any instructions that you were following and make sure that you followed them correctly.
Then, re-read them again ;)  
See [known issues](#known-issues) and the #testnet-status channel of our [Discord](https://chat.avalabs.org).
If your issue is not addressed anywhere, post in the appropriate Discord channel (probably #troubleshooting.)

If, after doing the above, you think there is a bug, please make an issue on our [Github.](https://github.com/ava-labs/gecko/issues) 
Please give as much information and context as possible when describing an issue.
If someone already reported the same issue, comment with your details.

Many times, restarting your node will fix an issue.

### How do I upgrade my node?

The node is a binary program. You can either download the source code and then build the binary program, or you can download the pre-built binary.
You can do either of the below. You don't need to do both.

#### From source

First clone our Github repo (you can skip this step if you've done this before):

`git clone https://github.com/ava-labs/gecko.git`

Then move to the gecko directory:

`cd gecko`

Pull the latest code:

`git pull`

Check that your local code is up to date. Do:

`git rev-parse HEAD`

and check that the first 7 characters printed match the `Latest commit` field on our [Github.](https://github.com/ava-labs/gecko)

Now build the binary:

`./scripts/build.sh`

This should print `Build Successful`.

You can check what version you're running by doing `./build/avalanche --version`.
(Note: If this fails, your Gecko version is `0.5.1` or older.)

You can run your node with `./build/avalanche`

#### Download Binary

Go to our [releases page](https://github.com/ava-labs/gecko/releases) and select the release you want (probably the latest one.)

Under `Assets`, select the appropriate file.

For MacOS:  
Download the file named `gecko-osx-<VERSION>.zip`  
Unzip the file with `unzip gecko-osx-<VERSION>.zip`  
The resulting folder, `gecko-<VERSION>`, contains the binaries.  
You can run the node with `./gecko-<VERSION>/avalanche`

For Linux x86:  
Download the file named `gecko-linux-<VERSION>.tar.gz`  
Unzip the file with `tar -xvf gecko-linux-<VERSION>.tar.gz`  
The resulting folder, `gecko-<VERSION>`, contains the binaries.  
You can run the node with `./gecko-<VERSION>/avalanche`

Note: The Linux binaries are compiled for AMD64 (x86-64) architectures. For ARM platforms, like the Raspberry Pi, please [build from source](#from-source).

### Will restarting/upgrading my node give me a new node ID?

No.

### What version am I running?

Run `./avalanche --version`.
It will print the version of Avalanche you're running.
To see what the latest release is, see our [releases page.](https://github.com/ava-labs/gecko/releases/)

### Why am I getting a 404 when I make an API call?

First, make sure you're sending the API call to the right place/following an instruction correctly.
Then, [make sure your node is connected to peers.](#is-my-node-connected-to-peers)
Then, [make sure the chain you're sending the call to is done bootstrapping.](#is-my-node-done-bootstrapping)
If a problem persists, contact us on [Discord.](https://chat.avalabs.org)

### Where is my node's data?

By default, the node's database is at `$HOME/.gecko/db`
**If you delete this directory, it will erase the state of your node, including private keys and keystore users.**

If there is a new major release (e.g. Cascade --> Denali), your node's state will be reset.
Otherwise, upgrading Gecko will not overwrite or destroy your node's state.

The only data not in this folder is your node's staking key/certificate.
These are in `$HOME/.gecko/staking` by default.
**If you delete this directory, it will erase your node ID. This will jeopardize your validator reward.**
If your node is a validator and you delete its staking key, it will no longer be a validator when it restarts.

Upgrading Gecko will never erase or change your staking key/certificate.

### Where are my node's logs?

By default, they're in `$HOME/.gecko/logs/node`.

Logs specific to a chain are in subdirectory `chain/[CHAIN ID]` where `[CHAIN ID]` is the chain's ID.

### Can I run Gecko on a different machine but keep the node ID / state?

Yes.

To keep your node ID, you'll have to copy your staking key and certificate to the new machine.
By default, these are at `$HOME/.gecko/staking` and are named `staker.key` and `staker.crt`.
Place the staking key and certificate on the new machine at `$HOME/.gecko/staking`.

To keep your node's state (keystore users, etc.), you'll have to copy your database directory to the new machine.
By default, this is at `$HOME/.gecko/db`.
Place this directory at the same location on the new machine.

Advanced users may place the staking key and database at different locations and point to them at runtime
using [command-line arguments.](../../references/command-line-interface/)

<!-- TODO put this back once isBootstrapped is in an official release
### Is my node done bootstrapping?

Each chain bootstraps separately and finishes bootstrapping at different times.

To check whether a given chain is done bootstrapping, call API method [`info.isBootstrapped`.](../api/info.md#infoisbootstrapped)
For example, to see if the X-Chain is done bootstrapping:

```sh
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "info.isBootstrapped",
    "params":{
        "chain":"X"
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/info
```
-->

### Is my node in the validator set?

First, get your node's ID:

```sh
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "info.getNodeID",
    "params":{},
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/info
```

The response contains your node's ID:

```json
{
    "jsonrpc": "2.0",
    "result": {
        "nodeID": "ARCLrphAHZ28xZEBfUL7SVAmzkTZNe1LK"
    },
    "id": 1
}
```

Then look on the [explorer's validator page](https://explorer.avax.network/validators) and verify your node is present.

If the explorer isn't working, you can check this way:

Get the current list of validators:

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.getCurrentValidators",
    "params": {},
    "id": 4
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

and check that your node is in that list.

If it's not there, check the pending validator list:

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.getPendingValidators",
    "params": {},
    "id": 4
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

If your node is not in either list, it is not a validator and is not a pending validator.

Please note that even if your node is off, it will appear in the validator list.
In order to complete certain incentivized testnet challenges, your node must also be running and connected to other nodes.

### My node is in the validator set. How can I tell that it's actually validating?

There is no good way to tell right now. If your node is connected to peers, it should be validating.

### How can I get involved with Avalanche?

We want you to be a part of the Avalanche community!
Any contribution, no matter how small, is valued and welcome.

You can:

* [Get a grant](https://www.avalabs.org/avalanche-x) for working on a project that adds to the Avalanche ecosystem
* [Participate in our bug bounty](https://www.avalabs.org/avalanche-x/explore-open-grants/bug-bounty)
* Check out the #dev-chat channel on our [Discord.](https://chat.avalabs.org)
* Make an issue or pull request on our [Github.](https://github.com/ava-labs/gecko)

### What hardware do I need?

In general, any fairly modern computer should do.
It should have:

* CPU >= 2 GHz
* RAM >= 4 GB
* Free disk space >= 5 GB

### What software do I need?

Your operating system should be 64-bit Ubuntu >= 18.04 or MacOS >= Catalina.
Other operating systems may work but are not well tested.
We recommend using Ubuntu 18.04 because that's what we use.

You need to have Go 1.13 or 1.14 installed.
To check, do: `go version`. It should say 1.13.X or 1.14.X where X is some number.
If Go is not installed, follow one of the many online guides for doing so.

You also need to have your GOPATH set.
To check that it's set, do `echo $GOPATH`. It should print something.
If it doesn't see [here](https://www.digitalocean.com/community/tutorials/how-to-install-go-on-ubuntu-18-04) or many of the guides online about setting your GOPATH.

### Is there a browser-based wallet?

[Yes.](https://wallet.avax.network/)

### Is there an explorer?

[Yes.](https://explorer.avax.network/)

### Is there a Javascript library?

[Yes.](../../tools/avalanche.js/)

### Is my node connected to peers?

Call `info.peers`:

```sh
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"info.peers"
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/info
```

Each entry in the response contains a peer's IP address, public IP address, ID, version, and the time of the last sent and received messages exchanged with this node.
If you see none, something is wrong and you are not connected to any peers.

### How do I kill my node?

Do `CTRL + C` in the terminal window where you're running the node.

There is a known issue where sometimes this doesn't kill the node.
In that case:

Do `CTRL + Z` in the terminal window where you're running the node.
This should print something like:

```sh
[1]+  Stopped     /home/youruser/go/src/github.com/ava-labs/gecko/build/avalanche
```

Do `kill -9 %1` (or `kill -9 %2` if it printed `[2]+ Stopped`, etc.)

### Do I need to open any ports?

You don't have to. However, if you open the staking port (`9651` by default) your node will be able to connect to more peers.

### What is the `id` field in every API call? Do I need to change it?

Gecko uses the [JSON RPC 2.0 standard](https://www.jsonrpc.org/specificatio) for API calls.  
As part of this standard, each call and response has a field `id`.
This is useful in tracking which response corresponds to which request.

You do not need to change this field when making API calls.
It's OK to make many API calls with the same `id` field.

### Is there a repository of Avalanche related materials I can learn from?

In addition to this documentation, there is a [community-run repository](https://github.com/tbrunain/awesome-ava-chain) of useful links and resoucres.
Great thanks to `tbrunain` for this contribution :)

### My node prints `peer attempting to connect with newer version avalanche/<VERSION>. You may want to update your client.` Is this OK?

As long as you are [on the right network](#node-is-on-the-wrong-network), yes.

### What is AVAX's denomination?

AVAX is denomination 9, so the smallest unit of AVAX is nanoAVAX (nAVAX) at 10^-9 AVAX

## Web Wallet

### What's up with the new wallet?

Avalanche's [Web Wallet](https://wallet.avax.network) is an HD Wallet (hierarchical deterministic) based on the BIP 32, 39 and 44 standards. It follows industry best practices for security, wallet interoperability and hardware wallet integration.

### When hardware wallet integration?

There is an Avalanche-X grant for [ledger support](https://www.avalabs.org/avalanche-x/explore-open-grants/ledger-support).

### What is the HD Path?

`m / 44' / 9000'`

### My address keeps changing after each transaction. Why?

HD wallets support generating a new address for every transaction. This is a convention to increase privacy. Previous addresses may be reused and your wallet's balance will be correct.

### For the token sale should I use the address from the keygen site or the web wallet?

Use the address from [the keygen site](https://keygen.avax.network). This will guarantee the tokens you buy will be delivered to a new wallet with the correct address.

## Common Problems

### API call fails with `Failed to connect to 127.0.0.1 port 9650: Connection refused`

This means that your node is not listening for HTTP traffic on localhost port 9650.
There are a few reasons this might happen.

First, make sure that your node is actually running. If you're running the node in a terminal, **you have to be running the node in a separate tab/window from the one you're using to make the API calls.** If you do `CTRL + C` to kill your node and then make an API call, **it will fail because the node is not running.**

If you're running a node on another machine, replace `localhost` or `127.0.0.1` in the API call with the machine's IP address.

If you started your node with command-line argument `--http-port=9700` then replace `9650` in the API call with `9700` (or whatever port you specified.)

### Starting node fails with: `parsing parameters returned with error couldn't create db at ...`

There is already a node running on your machine.

### Node is on the wrong network

If you have already received funds from the faucet and can see them on the explorer, but you still can't send a transaction with your node, you may still be connected to an old test network.
Check to make sure that you are are on the right network, by calling `info.getNetworkName`:

```json
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"info.getNetworkName"
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/info
```

The expected output is:

```json
{
    "jsonrpc": "2.0",
    "result": {
        "networkID": "denali"
    },
    "id": 1
}
```

If the response is not `denali`, or the API call fails with a 404, you are not on the Denali network.

### API response says `invalid character 'â' looking for beginning of value`

You probably pasted the API call from a program that uses smart quotes.
Replace each character that looks like a quotation mark " with a quotation mark and try again.

### Starting node fails with: `cannot execute binary file: Exec format error`

You are probably using one of the [official releases](https://github.com/ava-labs/gecko/releases) on an architecture it was not build for.  
The `gecko-linux-<release>.tar.gz` is build for AMD64 (x86-64) architectures. Platforms based on ARM chips, like the Raspberry Pi, are **not** working with it.  
Instead you need to [build gecko from source](../quickstart/ava-getting-started.md#download-gecko-source-code). Keep in mind you need to use a 64-bit operating system.

## Known Issues/Bugs

This section contains bugs and issues that we're aware of.
Please also see our [Github issues.](https://github.com/ava-labs/gecko/issues)

### Node won't start with `failed to listen on consensus server at 0.0.0.0:9651: unable to listen`

To get around this, run the `avalanche` binary with `--staking-port=9652` (or `9653` or `9654` or ...)

Example: `./avalanche --staking-port=9652`

### Node won't quit with `CTRL + C`

If your node is running in an open terminal tab:

Do `CTRL + Z` in the terminal window where you're running the node.
This should print something like:

```sh
[1]+  Stopped     /home/youruser/go/src/github.com/ava-labs/gecko/build/avalanche
```

Do `kill -9 %1` (or `kill -9 %2` if it printed `[2]+ Stopped`, etc.)

If your node is running in the background:

Do `ps aux | grep ava`

The output should have a line that looks like this:

```sh
youruser 29861  8.7  0.2 1459208 34996 pts/2   Sl+  19:44   0:00 ./build/avalanche
```

Do:

`kill -9 29861` (or whatever number appears in the second column)

### Node prints a lot of messages that begin `2020-06-09T12:45:02.548-0400 [DEBUG] plugin.sh: DEBUG[06-09|12:45:02.548] `

This is a known issue. We're working on it! You can ignore these logs.

### Node prints `NAT Traversal failed ...`

This is OK. It means your node will be able to connect to less peers, but you should still be able to connect to some peers and participate in the network.
