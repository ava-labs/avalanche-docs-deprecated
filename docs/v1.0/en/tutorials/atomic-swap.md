# Transfer AVAX tokens between the P-Chain and X-Chain

## Introduction

AVAX tokens exist on both the X-Chain, where they can be traded, and the P-Chain, where they can be provided as a stake when validating the Default Subnet.

Avalanche supports **atomic swaps** of AVAX between the X-Chain and P-chain.
(In the future Avalanche will support more generic atomic swaps between chains.)

In this tutorial we'll send AVAX tokens from the X-Chain to the P-chain and back.

## Requirements

We assume that you've already done the [quickstart guide](../quickstart/ava-getting-started.md) and are familiar with the [Avalanche Network's architecture.](../core-concepts/overview.md)

We assume your node is connected to the Public Testnet.

## Export AVAX from the X-Chain to the P-Chain

Of course, in order to send AVAX you need to have some AVAX!
Use the [Public Tesnet Faucet](https://faucet.avax.network/) to send some AVAX to an X-Chain address you hold, just like in the quickstart guide.

To send the AVAX, call the X-Chain's [`exportAVAX`](../api/avm.md#avmexportavax) method.

Your call should look like this:

```json
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"avm.exportAVAX",
    "params" :{
        "to":"Bg6e45gxCUTLXcfUuoy3go2U6V3bRZ5jH",
        "amount": 500,
        "username":"myUsername",
        "password":"myPassword"
    }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/X
```

where `to` is the address of a P-Chain account you hold.
(See [here](../api/platform.md#platformcreateaccount) for instructions on creating a new P-Chain account)

The response should look like this:

```json
{
    "jsonrpc": "2.0",
    "result": {
        "txID": "MqEaeWc4rfkw9fhRMuMTN7KUTNpFmh9Fd7KSre1ZqTsTQG73h"
    },
    "id": 1
}
```

We can verify that this transaction was accepted by calling `getTxStatus`:

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "avm.getTxStatus",
    "params":{
        "txID":"MqEaeWc4rfkw9fhRMuMTN7KUTNpFmh9Fd7KSre1ZqTsTQG73h"
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/X
```

Which shows our transaction is accepted:

```json
{
    "jsonrpc": "2.0",
    "result": {
        "status": "Accepted"
    },
    "id": 1
}
```

We can also call [`getBalance`](../api/avm.md#avmgetbalance) to check that the AVAX was deducted from an address held by our user:

```json
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"avm.getBalance",
    "params" :{
        "address":"X-ADDRESSGOESHERE",
        "assetID":"AVAX"
    }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/X
```

(If your user controls multiple X-Chain addresses, the AVAX may have been sent from any combination of them.)

## Import AVAX to the P-Chain from the X-Chain

Our transfer isn't done just yet.
We need to call the P-Chain's [`importAVAX`](../api/platform.md#platformimportavax) method to finish the transfer.

Your call should look like this:

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.importAVAX",
    "params": {
        "username":"myUsername",
        "password":"myPassword",
        "to":"Bg6e45gxCUTLXcfUuoy3go2U6V3bRZ5jH",
        "payerNonce":1
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/P
```

where `to` is the same as in the call to `avm.exportAVAX`, and `username` controls the account specified in `to`.

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

Which we can issue to the network with `issueTx`:

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.issueTx",
    "params": {
        "tx":"1117xBwcr5fo1Ch4umyzjYgnuoFhSwBHdMCam2wRe8SxcJJvQRKSmufXM8aSqKaDmX4TjvzPaUbSn33TAQsbZDhzcHEGviuthncY5VQfUJogyMoFGXUtu3M8NbwNhrYtmSRkFdmN4w933janKvJYKNnsDMvMkmasxrFj8fQxE6Ej8eyU2Jqj2gnTxU2WD3NusFNKmPfgJs8DRCWgYyJVodnGvT43hovggVaWHHD8yYi9WJ64pLCvtCcEYkQeEeA5NE8eTxPtWJrwSMTciHHVdHMpxdVAY6Ptr2rMcYSacr8TZzw59XJfbQT4R6DCsHYQAPJAUfDNeX2JuiBk9xonfKmGcJcGXwdJZ3QrvHHHfHCeuxqS13AfU"
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/P
```

Now we can check the account's balance and verify that is has the AVAX:

```json
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
        "balance": "500"
    },
    "id": 1
}
```

Woo! We successfully moved AVAX from the X-Chain to the P-Chain.
Now we can use the AVAX held by this P-Chain account to provide a stake in order to validate the Default Subnet.

## Export AVAX from the P-Chain to the X-Chain

Now let's move AVAX on the P-Chain back to the X-Chain.

To do so, call [`platform.exportAVAX`](../api/platform.md#platformexportavax):

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.exportAVAX",
    "params": {
        "to":"G5ZGXEfoWYNFZH5JF9C4QPKAbPTKwRbyB",
        "amount":250,
        "payerNonce":2
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

where `to` is the X-Chain address (without the `X-`) the AVAX is being sent to.

This returns the unsigned transaction:

```json
{
    "jsonrpc": "2.0",
    "result": {
        "unsignedTx": "1112Y8Y5ibRqMDtby9NSdpK9u3n1yGywybAAVYnhCkFYcRzEYbR7J5Ci6SX98PmgS2LpRf5pcu6YAgLYGiTuQpiSucRcX4dv7HbVnEsrQnjcieGbgkf9PFS126hC8xce4pEZUzr9jReVdfXe3g9BSUsXLj2XcWrnD6iTgHpiC18jjyjg1wjm1Vs4TcXhG472MRvGspucJ8LuUE91WV7353Kxdc2e7Trw2Sd6iV"
    },
    "id": 1
}
```

Now we sign with the key of the account that the AVAX is being sent from:

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.sign",
    "params": {
        "tx":"1112Y8Y5ibRqMDtby9NSdpK9u3n1yGywybAAVYnhCkFYcRzEYbR7J5Ci6SX98PmgS2LpRf5pcu6YAgLYGiTuQpiSucRcX4dv7HbVnEsrQnjcieGbgkf9PFS126hC8xce4pEZUzr9jReVdfXe3g9BSUsXLj2XcWrnD6iTgHpiC18jjyjg1wjm1Vs4TcXhG472MRvGspucJ8LuUE91WV7353Kxdc2e7Trw2Sd6iV",
        "signer":"Bg6e45gxCUTLXcfUuoy3go2U6V3bRZ5jH",
        "username":"myUsername",
        "password":"myPassword"
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

This returns the signed transaction:

```json
{
    "jsonrpc": "2.0",
    "result": {
        "tx": "1112Y8Y5ibRqMDtby9NSdpK9u3n1yGywybAAVYnhCkFYcRzEYbR7J5Ci6SX98PmgS2LpRf5pcu6YAgLYGiTuQpiSucRcX4dv7HbVnEsrQnjcieGbgkf9PFS126hC8xce4pEZUzrAzm53EwXPbbF1uWemTQUfFs44xha8Yn4JtgEwT3Q42VywckUVncKvfX2wtbz3RaDvavYhxUM7TbxSMJwAo8Xq45RjKZDpmw"
    },
    "id": 1
}
```

Which we issue to the network:

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.issueTx",
    "params": {
        "tx":"1112Y8Y5ibRqMDtby9NSdpK9u3n1yGywybAAVYnhCkFYcRzEYbR7J5Ci6SX98PmgS2LpRf5pcu6YAgLYGiTuQpiSucRcX4dv7HbVnEsrQnjcieGbgkf9PFS126hC8xce4pEZUzrAzm53EwXPbbF1uWemTQUfFs44xha8Yn4JtgEwT3Q42VywckUVncKvfX2wtbz3RaDvavYhxUM7TbxSMJwAo8Xq45RjKZDpmw"
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

We can see that the AVAX was deducted from the account:

```json
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
        "nonce": "2",
        "balance": "250"
    },
    "id": 1
}
```

## Import AVAX to the X-Chain from the P-Chain

To finish our transfer from the P-Chain to the X-Chain, call `avm.importAVAX`:

```json
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"avm.importAVAX",
    "params" :{
        "username":"myUsername",
        "password":"myPassword",
        "to":"X-G5ZGXEfoWYNFZH5JF9C4QPKAbPTKwRbyB"
    }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/X
```

Note that `to` is the same address specified in our call to `platform.exportAVAX` except that we include `X-` in the address.
`username` must control the address in `to` for the transfer to succeed.

Just as before, we can call `avm.getBalance` to verify the funds were sent.

## Wrapping Up

That's it! Now you can swap AVAX back and forth between the X-Chain and P-Chain.
In the future Avalanche will support more generalized atomic swaps between chains.