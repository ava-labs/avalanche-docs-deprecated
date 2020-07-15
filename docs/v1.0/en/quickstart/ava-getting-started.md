---
title: "Avalanche Quickstart Guide"
excerpt: ""
---

# Quickstart Guide

The quickest way to learn about Avalanche is to run a node and interact with the network.

In this tutorial, which should take less than 10 minutes, we will:

* Install and run an Avalanche node
* Connect to the public test network
* Acquire and send AVAX, the Avalanche network's native token
* Start validating


If you run into any issues at all, **please check the [FAQ](../faq/faq.md)**
If your issue isn't addressed there, come ask for help on our [Discord Server!](https://chat.avalabs.org/)
We will work to get you through any problems.

## Requirements 

Avalanche is an incredibly lightweight protocol, so the minimum computer requirements are quite modest. 

* Hardware: CPU > 2 GHz, RAM > 3 GB, Storage > 5 GB free space.
* OS: Ubuntu == 18.04 or Mac OS X >= Catalina. (Ubuntu versions other than 18.04 may work but have not been tested.)
* Software: [Go](https://golang.org/doc/install) >= 1.13

Run `go version`. **It should be 1.13 or above.**
Run `echo $GOPATH`. **It should not be empty.**

## Run an Avalanche Node

Let's install Gecko, the Go implementation of an Avalanche node, and connect to the Avalanche Public Testnet.

### Download Gecko

The node is a binary program. You can either download the source code and then build the binary program, or you can download the pre-built binary.
You can do either of the below. You don't need to do both.

#### Download Gecko Source Code

Download the Gecko repository:

```sh
go get -v -d github.com/ava-labs/gecko/...
```

(Note to advanced users: Gecko uses Go modules, so you can actually clone the [Gecko repository](https://github.com/ava-labs/gecko) to locations other than your GOPATH.)

Change to the `gecko` directory:

```sh
cd $GOPATH/src/github.com/ava-labs/gecko
```

Build Gecko:

```sh
./scripts/build.sh
```

The binary, named `avalanche`, is in `gecko/build`. 

#### Download Gecko Binary

Go to our [releases page](https://github.com/ava-labs/gecko/releases) and select the release you want (probably the latest one.)

Under `Assets`, select the appropriate file.

For MacOS:  
Download the file named `gecko-osx-<VERSION>.zip`  
Unzip the file with `unzip gecko-osx-<VERSION>.zip`  
The resulting folder, `gecko-<VERSION>`, contains the binaries.  
You can run the node with `./gecko-<VERSION>/avalanche`

For Linux:  
Download the file named `gecko-linux-<VERSION>.tar.gz`.  
Unzip the file with `tar -xvf gecko-linux-<VERSION>.tar.gz`  
The resulting folder, `gecko-<VERSION>`, contains the binaries.  
You can run the node with `./gecko-<VERSION>/avalanche`

### Start a Node and Connect to Test Network

The Avalanche test network is a sandbox Avalanche network where AVAX tokens are free.
You can use it to play around in a low-stakes environment.

To start a node and connect it to the Avalanche test net:

```sh
./build/avalanche
```

You can use `Ctrl + C` to kill the node.

When the node starts, it has to bootstrap (catch up with the rest of the network.)
This should take a few hours.
You will see logs about bootstrapping.

When a given chain is done bootstrapping, it will print a log like this:

`INFO [06-07|19:54:06] <X Chain> /snow/engine/avalanche/transitive.go#80: bootstrapping finished with 1 vertices in the accepted frontier`

If you make an API call to a chain that is not done bootstrapping, it will hang or 404.

If your node never finishes bootstrapping, contact us on [Discord.](https://chat.avalabs.org/)

## Create a Keystore User

Avalanche nodes provide a built-in **Keystore.**
The Keystore manages users and is a lot like a wallet.
A user is a password-protected identity that a client can use when interacting with blockchains.
**You should only create a keystore user on a node that you operate, as the node operator has access to your plaintext password.**
To create a user, call `keystore.createUser`:

```sh
curl -X POST --data '{
     "jsonrpc": "2.0",
     "id": 1,
     "method": "keystore.createUser",
     "params": {
         "username": "YOUR USERNAME HERE",
         "password": "YOUR PASSWORD HERE"
     }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/keystore
```

The response should look like this:

```json
{
     "jsonrpc":"2.0",
     "result":{"success":true},
     "id":1
}
```

Now you have a user on this node.
Keystore data exists at the node level.
Users you create on one node's Keystore do not exist on
other nodes but you can import/export users to/from the Keystore.
See the [Keystore API](../api/keystore.md) to see how.

## Create an Address

Avalanche is a network of heterogeneous blockchains.
One of these blockchains is the X-Chain, which acts as a decentralized platform for creating and trading digital assets.
(Think X for eXchanging assets.)

There's a special asset on the X-Chain called the [AVAX token](../core-concepts/overview.md#the-x-chain). 
This is the native token of the Avalanche network, and transaction fees on the Avalanche network are paid in AVAX.

Let's acquire some AVAX tokens.
First, we'll need to create an address to hold them.

To create a new address on the X-Chain, call `avm.createAddress`, a method of the [X-Chain's API](../api/avm.md):

```sh
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :2,
    "method" :"avm.createAddress",
    "params" :{
        "username":"YOUR USERNAME HERE",
        "password":"YOUR PASSWORD HERE"
    }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/X
```

If this call returns a 404 or hangs, your node probably isn't finished bootstrapping.

Note that we make this request to `127.0.0.1:9650/ext/bc/X`.
The `bc/X` portion signifies that the request is being sent to the blockchain whose ID (or alias) is `X` (ie the X-Chain.)

The response should look like this:

```json
{
    "jsonrpc":"2.0",
    "id":2,
    "result" :{
        "address":"X-5TQr5hSAZ8ZKuSaYLg5sr4VwvcvwKZ1Mg"
    }
}
```

Your user now controls the address `X-5TQr5hSAZ8ZKuSaYLg5sr4VwvcvwKZ1Mg` on the X-Chain.
To tell apart addresses on different chains, the Avalanche convention is for an address to include the ID of the chain it exists on.
Hence, this address begins `X-`, denoting that it exists on the X-Chain.

## Use the Avalanche Faucet

Now let's use the Avalanche test net faucet to send some free AVAX to this address.
The faucet dispenses 20,000 nanoAVAX (nAVAX) each drop.

**This is only a test network, and AVAX on this network has no value.**

Go to the [test net faucet](https://faucet.avax.network/) and paste the address you just created to receive 20,000 nAVAX.

We can check an address's balance of a given asset by calling `avm.getBalance`, another method of the X-Chain's API.
Let's check that the faucet drip went through.

(Note: The asset ID of AVAX is AVA on nodes running Denali or earlier. The ID will change to AVAX in the next release.)

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

Note that AVAX has the special ID `AVAX`. 
Usually an asset ID is an alphanumeric string.

The response should look like this:

```json
{
    "jsonrpc":"2.0",
    "id"     :3,
    "result" :{
        "balance":20000,
        "utxoIDs": [
            {
                "txID": "x6vR85YPNRf5phpLAEC7Sd6Tq2PXWRt3AAHAK4BpjxyjRyhtu",
                "outputIndex": 0
            }
        ]
    }
}
```

## Send AVAX

Now let's send some AVAX:

(Note: The asset ID of AVAX is AVA on nodes running Denali or earlier. The ID will change to AVAX in the next release.)

```sh
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :5,
    "method" :"avm.send",
    "params" :{
        "username"   :"YOUR USERNAME HERE",
        "password"   :"YOUR PASSWORD HERE",
        "assetID"    :"AVAX",
        "amount"     :1000,
        "to"         :"X-FxgGhoAwg3dPTPhHEmjgi27ZPmvc8jQmj"
    }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/X
```

`amount` specifies the number of nAVAX to send.
A nAVAX (nanoAVAX) is the smallest increment of AVAX, and 1,000,000,000 nAVAX == 1 AVAX. 

When you send this request, the node will authenticate you using your username and password.
Then, it will look through all the private keys controlled by your user until it finds
enough nAVAX to satisfy the request.

The response should look like this:

```json
{
    "jsonrpc":"2.0",
    "id"     :5,
    "result" :{
        "txID":"2QouvFWUbjuySRxeX5xMbNCuAaKWfbk5FeEa2JmoF85RKLk2dD"
    }
}
```

`txID` is the ID of the send transaction we just sent to the network. It will be different for every invocation of `send`.

## Checking the Transaction Status

This send transaction will only take a second or two to finalize. We can check its status with `avm.getTxStatus`:

```sh
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :6,
    "method" :"avm.getTxStatus",
    "params" :{
        "txID":"2QouvFWUbjuySRxeX5xMbNCuAaKWfbk5FeEa2JmoF85RKLk2dD"
    }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/X
```

The response should look like this:

```json
{
    "jsonrpc":"2.0",
    "id"     :6,
    "result" :{
        "status":"Accepted"
    }
}
```

You might also see that `status` is `Processing` if the network has not yet finalized the transaction.

Once you see that the transaction is `Accepted`, check the balance of the `to` address to see that it has the AVAX we sent:

```sh
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :7,
    "method" :"avm.getBalance",
    "params" :{
        "address":"X-FxgGhoAwg3dPTPhHEmjgi27ZPmvc8jQmj",
        "assetID"  :"AVAX"
    }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/X
```

The response should be:

```json
{
    "jsonrpc":"2.0",
    "id"     :7,
    "result" :{
        "balance":1000
    }
}
```

In the same fashion, we could check `X-5TQr5hSAZ8ZKuSaYLg5sr4VwvcvwKZ1Mg` to see that AVAX we sent was deducted from its balance.

## Validate the Default Subnet (Stake)

[Subnets](../core-concepts/overview.md#what-are-subnets) are a powerful feature of the Avalanche network.
A Subnet is a set of validators that work to achieve consensus on a set of blockchains.

The Default Subnet is inherent to the Avalanche network, and it validates Avalanche's [built-in blockchains](../core-concepts/overview.md#built-in-blockchains).
Avalanche uses Proof-of-Stake, so to become a validator one needs to provide a stake, or bond, in AVAX tokens.

Let's add your node to the Default Subnet.

### Create a P-Chain Account

The P-Chain (Platform Chain) manages metadata about the Avalanche network, including which nodes belong to which Subnets.
The P-Chain uses an account model, so in order to validate the Default Subnet you'll need to first create an account on the P-Chain.
To do so, call [`platform.createAccount`](../api/platform.md#platformcreateaccount):

```sh
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.createAccount",
    "params": {
    	"username":"YOUR USERNAME HERE",
    	"password":"YOUR PASSWORD HERE"
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

Note that this API call is sent to the P-Chain (`127.0.0.1:9650/ext/P`) rather than the X-Chain (`127.0.0.1:9650/ext/X`) like previous API calls.

The response contains the address of your new account:

```json
{
    "jsonrpc": "2.0",
    "result": {
        "address": "Bg6e45gxCUTLXcfUuoy3go2U6V3bRZ5jH"
    },
    "id": 1
}
```

### Fund Your P-Chain Account

As mentioned before, in order validate the Default Subnet, you need to stake some AVAX tokens.
Right now, your P-Chain account has no AVAX.
AVAX tokens are transferrable between the X-Chain (where you sent funds with the faucet) and the P-Chain.
Let's send some AVAX to your P-Chain account from the X-Chain.
The minimum stake amount is 10,000 nAVAX, so make sure you have at least this much AVAX in your X-Chain addresses.
(If you need more, use the faucet a few more times.)

The first step in transferring AVAX from the X-Chain to P-Chain is to call `avm.exportAVAX`:


```sh
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"avm.exportAVAX",
    "params" :{
        "to":"Bg6e45gxCUTLXcfUuoy3go2U6V3bRZ5jH",
        "amount": 10000,
    	"username":"YOUR USERNAME HERE",
    	"password":"YOUR PASSWORD HERE"
    }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/X
```

The response contains the transaction ID.
As before, you can check the transaction's status by calling `avm.getTxStatus`.

The second and final step is to call `platform.importAVAX`:

```sh
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.importAVAX",
    "params": {
    	"username":"YOUR USERNAME HERE",
    	"password":"YOUR PASSWORD HERE",
		"to":"Bg6e45gxCUTLXcfUuoy3go2U6V3bRZ5jH",
		"payerNonce":1
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/P
```

`payerNonce` is the next unused nonce of your P-Chain account, which is 1 since your P-Chain account has not sent any transactions.

The response contains the transaction:

This call returns the transaction:

```json
{
    "jsonrpc": "2.0",
    "result": {
        "tx": "1117xBwcr5fo1Ch4umyzjYgnuoFhSwBHdMCam2wRe8SxcJJvQRKSmufXM8aSqKaDmX4TjvzPaUbSn33TAQsbZDhzcHEGviuthncY5VQfUJogyMoFGXUtu3M8NbwNhrYtmSRkFdmN4w933janKvJYKNnsDMvMkmasxrFj8fQxE6Ej8eyU2Jqj2gnTxU2WD3NusFNKmPfgJs8DRCWgYyJVodnGvT43hovggVaWHHD8yYi9WJ64pLCvtCcEYkQeEeA5NE8eTxPtWJrwSMTciHHVdHMpxdVAY6Ptr2rMcYSacr8TZzw59XJfbQT4R6DCsHYQAPJAUfDNeX2JuiBk9xonfKmGcJcGXwdJZ3QrvHHHfHCeuxqS13AfU"
    },
    "id": 1
}
```

Which you can issue to the P-Chain by calling `platform.issueTx`:

```sh
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.issueTx",
    "params": {
    	"tx":"1117xBwcr5fo1Ch4umyzjYgnuoFhSwBHdMCam2wRe8SxcJJvQRKSmufXM8aSqKaDmX4TjvzPaUbSn33TAQsbZDhzcHEGviuthncY5VQfUJogyMoFGXUtu3M8NbwNhrYtmSRkFdmN4w933janKvJYKNnsDMvMkmasxrFj8fQxE6Ej8eyU2Jqj2gnTxU2WD3NusFNKmPfgJs8DRCWgYyJVodnGvT43hovggVaWHHD8yYi9WJ64pLCvtCcEYkQeEeA5NE8eTxPtWJrwSMTciHHVdHMpxdVAY6Ptr2rMcYSacr8TZzw59XJfbQT4R6DCsHYQAPJAUfDNeX2JuiBk9xonfKmGcJcGXwdJZ3QrvHHHfHCeuxqS13AfU"
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/P
```

Now check the balance of your P-Chain account by calling `platform.getAccount`:

```sh
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.getAccount",
    "params":{
    	"address":"Bg6e45gxCUTLXcfUuoy3go2U6V3bRZ5jH"
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/P
```

The response should look like this:

```json
{
    "jsonrpc": "2.0",
    "result": {
        "address": "Bg6e45gxCUTLXcfUuoy3go2U6V3bRZ5jH",
        "nonce": "1",
        "balance": "10000"
    },
    "id": 1
}
```

Great! Now your P-Chain account has enough AVAX tokens to provide a stake.

### Get Your Node's ID

Your node is uniquely identified by its staking key.
To get your node's ID, call [`info.getNodeID:`](../api/info.md#info.getNodeID)

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

### Create the Unsigned Transaction

To add your node to the Default Subnet, you'll issue a transaction to the P-Chain.
When you add a node to the Default Subnet, you specify:

* `id`: The node ID of the node being added
* `payerNonce`: The next unused nonce of the account providing the transaction fee (the fee is currently 0) and staked AVAX tokens.
* `destination`: The address of the account the AVAX (along with a validator reward) will be returned to when the node is done validating.
* `startTime`: The Unix time the node will start validating the Default Subnet.
* `endTime`: The Unix time the node will stop validating the Default Subnet.

The place you're most likely to get tripped up is `startTime` and `endTime`.

`startTime` must be in the future relative to the time this transaction is issued.
To get the current Unix time, see [here.](https://www.unixtimestamp.com/)
Below, we use the shell command `date` to compute the Unix time 10 minutes from now.

`endTime` must be between 1 day (the minimum staking period) and 365 days (the maximum staking period) ahead of `startTime`.
Below, we use the shell command `date` to compute the Unix time 2 days from now.

(Note: If you're on a Mac, replace  `$(date` with `$(gdate`. If you don't have `gdate` installed, do `brew install coreutils`.)

Now let's create the unsigned transaction:

```sh
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.addDefaultSubnetValidator",
    "params": {
    	"id":"ARCLrphAHZ28xZEBfUL7SVAmzkTZNe1LK",
    	"payerNonce":2,
    	"destination":"Bg6e45gxCUTLXcfUuoy3go2U6V3bRZ5jH",
    	"startTime":'$(date --date="10 minutes" +%s)',
    	"endTime":'$(date --date="2 days" +%s)',
    	"stakeAmount":10000,
        "delegationFeeRate":100000
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

The response has the unsigned transaction:

```json
{
    "jsonrpc": "2.0",
    "result": {
        "unsignedTx": "111fRKBNoBhBfeGvBzvz6r9dZUKbEnUypM6tjiSyYrWM4ojSTuL2Syxv8cFLphtYaxdM1EA3Aj4yej8ABSfmjb9NMrtxQac9cnWwCER7GHSzFULB25hAtzGtJ8XhsrKcvtpAM8FwjRzg3Bg1q6V8GTKGMC219bYMETS48GMFGh4nts1Jsf246rjZ26r1Vyok8MdnoaxjQWR6cKq"
    },
    "id": 1
}
```

### Sign the Transaction

We need to sign this transaction with the key of the account that is paying the transaction fee and providing the staked tokens.

To do so, call `platform.Sign`.

```sh
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.sign",
    "params": {
    	"tx":"111fRKBNoBhBfeGvBzvz6r9dZUKbEnUypM6tjiSyYrWM4ojSTuL2Syxv8cFLphtYaxdM1EA3Aj4yej8ABSfmjb9NMrtxQac9cnWwCER7GHSzFULB25hAtzGtJ8XhsrKcvtpAM8FwjRzg3Bg1q6V8GTKGMC219bYMETS48GMFGh4nts1Jsf246rjZ26r1Vyok8MdnoaxjQWR6cKq",
    	"signer":"Bg6e45gxCUTLXcfUuoy3go2U6V3bRZ5jH",
    	"username":"YOUR USERNAME HERE",
    	"password":"YOUR PASSWORD HERE"
    },
    "id": 2
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

This returns the signed transaction:

```json
{
    "jsonrpc": "2.0",
    "result": {
        "Tx": "111fRKBNoBhBfeGvBzvz6r9dZUKbEnUypM6tjiSyYrWM4ojSTuL2Syxv8cFLphtYaxdM1EA3Aj4yej8ABSfmjb9NMrtxQac9cnWwCER7GHSzFULB4RoAjStfe26qQxhS91KvCCX3WBLmpyvNXHzgWk3uJP45cPv15RHGymFboPUcxNTwGij1NgQpKPcL4YxcDnKvNjrcQzKiXAz"
    },
    "id": 2
}
```

### Issue the Transaction

Finally, we issue the transaction to the network by calling [`platform.issueTx`](../api/platform.md#platformissuetx)

```sh
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.issueTx",
    "params": {
    	"tx":"111fRKBNoBhBfeGvBzvz6r9dZUKbEnUypM6tjiSyYrWM4ojSTuL2Syxv8cFLphtYaxdM1EA3Aj4yej8ABSfmjb9NMrtxQac9cnWwCER7GHSzFULB4RoAjStfe26qQxhS91KvCCX3WBLmpyvNXHzgWk3uJP45cPv15RHGymFboPUcxNTwGij1NgQpKPcL4YxcDnKvNjrcQzKiXAz"
    },
    "id": 3
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

Look out for errors printed by the node, which may indicate that your `startTime` is in the past, for example.
If so, try building and issuing the transaction again with corrected arguments.

### Verify Success

Now we can call [`platform.getPendingValidators`](../api/platform.md#platformgetpendingvalidators) to verify that the node has been added to the pending validator set of the Default Subnet.
A Subnet's pending validator set contains the nodes that are slated to start validating in the future.

If we don't provide any arguments, this method returns the pending validator set of the Default Subnet:

```sh
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.getPendingValidators",
    "params": {},
    "id": 4
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

The response should confirm that the node with ID `ARCLrphAHZ28xZEBfUL7SVAmzkTZNe1LK` will start validating the Default Subnet in the future.

```json
{
    "jsonrpc": "2.0",
    "result": {
        "validators": [
            {
                "id": "ARCLrphAHZ28xZEBfUL7SVAmzkTZNe1LK",
                "startTime": "1584021450",
                "endtime": "1584121156",
                "stakeAmount": "10000",
            }
        ]
    },
    "id": 4
}
```

Awesome! Now just wait until the time reaches `startTime`.
When it does, your node will start validating the Default Subnet.
You can verify this by calling [`platform.getCurrentValidators.`](../api/platform.md#platformgetcurrentvalidators) 

When the time reaches `endTime`, the P-Chain account that you specified in `destination` will receive back the staked AVAX tokens as well as a validator reward.
Then, if you want, you can rejoin the Default Subnet.

Now that your node is validating the Default Subnet, please leave it running until at least `endTime`.
We want to have as many nodes as possible participating in consensus in order to stress test the Avalanche network and achieve true decentralization.
Note that in the future you will only receive a validator reward if your node is sufficiently responsive (ie online) while validating.

## Next Steps

- [Learn more about Avalanche](../core-concepts/overview.md)
- [Create and trade a new asset](../tutorials/fixed-cap-asset.md)
- [Create a new blockchain](../tutorials/create-a-blockchain.md)
- [Create a new, custom validator set (Subnet)](../tutorials/create-a-subnet.md)
- [Explore our APIs](../api/intro-apis.md)
- [Explore reference materials](../references/cryptographic-primitives.md)
- [Read the whitepaper and other papers](../papers/index.md)
