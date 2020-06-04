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

### What do I need to do to participate in the Denali testnet?

[See here.](https://medium.com/@collin.cusce/9bbfb353207b)

### Can I run a node even though I'm not participating in the Denali incentivized testnet challenges?

Yes, and we would love it if you did.

### I think something went wrong or there's a bug. What do I do?

First, re-read any instructions that you were following and make sure that you followed them correctly.
Then, re-read them again ;)  
See [known issues](#known-issues) and the #testnet-status and #denali-support channels of our [Discord](https://chat.avalabs.org).
If your issue is not addressed anywhere, post in the appropriate Discord channel (probably #denali-support or #troubleshooting.)

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
Now you can run your node with `./build/ava`

#### Download Binary

Go to our [releases page](https://github.com/ava-labs/gecko/releases) and select the release you want (probably the latest one.)

Under `Assets`, select the appropriate file.

For MacOS:  
Download the file named `gecko-osx-<VERSION>.zip`  
Unzip the file with `unzip gecko-osx-<VERSION>.zip`  
The resulting folder, `build`, contains the binaries.  
You can run the node with `./build/ava`

For Linux:  
Download the file named `gecko-linux-<VERSION>.tar.gz`. 
Unzip the file with `tar -xvf gecko-linux-<VERSION>.tar.gz`  
The resulting folder, `gecko-<VERSION>`, contains the binaries.  
You can run the node with `./gecko-<VERSION>/ava`

### Why am I getting a 404 when I make an API call?

First, make sure you're sending the API call to the right place/following an instruction correctly.
Then, [make sure your node is connected to peers.](#is-my-node-connected-to-peers)
It should be connected to at least a few peers.
Then, [make sure your node is done bootstrapping.](#is-my-node-done-bootstrapping)

### Where is my node's data?

By default, the node's database is at `$HOME/.gecko/db`
**If you delete this directory, it will erase the state of your node, including private keys and keystore users.**

If there is a new release (e.g. Cascade --> Denali), your node's state will be reset.
Otherwise, upgrading Gecko will not overwrite or destroy your node's state.

The only data not in this folder is your node's staking key/certificate.
These are in `$HOME/.gecko/staking` by default.
**If you delete this directory, it will erase your node ID. This will jeopardize your validator reward or your Denali testnet reward (if applicable.)**
If your node is a validator and you delete its staking key, it will no longer be a validator when it restarts.

Upgrading Gecko will never erase or change your staking key/certificate.

### Where are my node's logs?

By default, they're in `$HOME/.gecko/logs/node`.

Logs specific to a chain are in subdirectory `chain/[CHAIN ID]` where `[CHAIN ID]` is the chain's ID.

### Is my node done bootstrapping?

Bootstrapping can take hours!

The simplest way to check is to get a drip from the [AVA faucet](https://faucet.ava.network/) and check that your address's balance changes.

To check an address's balance, call the X-Chain's `getBalance` method:

```sh
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :3,
    "method" :"avm.getBalance",
    "params" :{
        "address":"X-5TQr5hSAZ8ZKuSaYLg5sr4VwvcvwKZ1Mg",
        "assetID"  :"AVA"
    }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/X
```

Replace `X-5TQr5hSAZ8ZKuSaYLg5sr4VwvcvwKZ1Mg` with the address you sent the drip to.

If your node reflects the drip, it's done bootstrapping. Otherwise, it is not.

As long as your folder `$HOME/.gecko/db/` keeps growing in size you should be fine.
You can check that size with:

```sh
du -hs ~/.gecko/db
```

Or check constantly with (Strg + c to quit):

```sh
watch du -hs ~/.gecko/db
```

### Is my node in the validator set?

First, get your node's ID:

```sh
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "admin.getNodeID",
    "params":{},
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/admin
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

Then look on the [explorer's validator page](https://explorer.ava.network/validators) and verify your node is present.

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
In order to complete certain incentivized testnet challenges, your node must also be on.

### My node is in the validator set. How can I tell that it's actually validating?

There is no good way to tell right now. If your node is connected to peers, it should be validating.

### How can I get involved with AVA?

You can:

* [Get a grant](https://www.avalabs.org/ava-x) for working on a project that adds to the AVA ecosystem
* [Participate in our bug bounty](https://www.avalabs.org/ava-x/explore-open-grants/bug-bounty)
* Check out the #dev-chat channel on our [Discord.](https://chat.avalabs.org)
* Make an issue or pull request on our [Github.](https://github.com/ava-labs/gecko)

### What hardware do I need?

In general, any fairly modern computer should do.
It should have:

* CPU >= 2 GHz
* RAM >= 4 GB
* Free disk space >= 5 GB

### What software do I need?

Your operating system should be Ubuntu >= 18.04 or MacOS >= Catalina.
Other operating systems may work but are not well tested.
We recommend using Ubuntu 18.04 because that's what we use.

You need to have Go 1.13 or 1.14 installed.
To check, do: `go version`. It should say 1.13.X or 1.14.X where X is some number.
If Go is not installed, follow one of the many online guides for doing so.

You also need to have your GOPATH set.
To check that it's set, do `echo $GOPATH`. It should print something.
If it doesn't see [here](https://www.digitalocean.com/community/tutorials/how-to-install-go-on-ubuntu-18-04) or many of the guides online about setting your GOPATH.

### Is there a browser-based wallet?

[Yes.](https://wallet.ava.network/)

### Is there an explorer?

[Yes.](https://explorer.ava.network/)

### Is there a Javascript library?

[Yes.](http://docs.ava.network/v1.0/en/tools/slopes/)

### Is my node connected to peers?

Call `admin.peers`:

```sh
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"admin.peers"
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/admin
```

Each entry in the response contains a peer's IP address, public IP address, ID, version, and the time of the last sent and received messages exchanged with this node. If you see none, you are not connected to any peers.
You should see at least the 5 nodes run by AVA Labs.

### How do I kill my node?

Do `CTRL + C` in the terminal window where you're running the node.

There is a known issue where sometimes this doesn't kill the node.
In that case:

Do `CTRL + Z` in the terminal window where you're running the node.
This should print something like:

```
[1]+  Stopped     /home/youruser/go/src/github.com/ava-labs/gecko/build/ava
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

### Is there a repository of AVA related materials I can learn from?

In addition to this documentation, there is a [community-run repository](https://github.com/tbrunain/awesome-ava-chain) of useful links and resoucres.
Great thanks to `tbrunain` for this contribution :)

### My node prints `peer attempting to connect with newer version avalanche/<VERSION>. You may want to update your client.` Is this OK?

As long as you are [on the right network](#node-is-on-the-wrong-network), yes.

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

If you have already received funds from the faucet and can see them on the explorer, but you still can't send a transaction with your node, you may still be connected to the Cascade test network. Check to make sure that you are are on the right network, by calling `admin.getNetworkID`:

```json
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"admin.getNetworkID"
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/admin
```

The expected output is:

```json
{
    "jsonrpc": "2.0",
    "result": {
        "networkID": "3"
    },
    "id": 1
}
```

The correct network ID for Denali is 3. If the network ID is 2, then you are on the Cascade test network and need to upgrade.

### API response says `invalid character 'â' looking for beginning of value`

You probably pasted the API call from a program that uses smart quotes.
Replace each character that looks like a quotation mark " with a quotation mark and try again.

## Known Issues/Bugs

This section contains bugs and issues that we're aware of.
Please also see our [Github issues.](https://github.com/ava-labs/gecko/issues)

### Node won't start with `failed to listen on consensus server at 0.0.0.0:9651: unable to listen`

To get around this, run the `ava` binary with `--staking-port=9652` (or `9653` or `9654` or ...)

Example: `./ava --staking-port=9652`

### Node won't quit with `CTRL + C`

If your node is running in an open terminal tab:

Do `CTRL + Z` in the terminal window where you're running the node.
This should print something like:

```
[1]+  Stopped     /home/youruser/go/src/github.com/ava-labs/gecko/build/ava
```

Do `kill -9 %1` (or `kill -9 %2` if it printed `[1]+ Stopped`, etc.)

If your node is running in the background:

Do `ps aux | grep ava`

The output should have a line that looks like this:

```
youruser 29861  8.7  0.2 1459208 34996 pts/2   Sl+  19:44   0:00 ./build/ava
```

Do:

`kill -9 29861` (or whatever number appears in the second column)

### On start, node prints `error while creating vm: Unrecognized remote plugin`

This message means your node is not running the C-Chain; it's looking in the wrong location for a binary.

To fix this, you can use the `--plugin-dir` command-line argument.

If you are in the directory containing the `ava` binary, start your node with: `./ava --plugin-dir=$(pwd)/plugins`

### Node prints `GetFailed called without sending the corresponding Get message`

This is OK. We will likely lower this log level to be less visible in the future.

### Node prints `next scheduled event is at ...`

This is OK. We will likely lower this log level to be less visible in the future.

### Node prints `NAT Traversal failed ...`

This is OK. It means your node will be able to connect to less peers, but you should still be able to connect to some peers and participate in the network.

### Node print `assertions are enabled. This may slow down execution`

This is OK.
