# AVM (X-Chain) API

The X-Chain, Avalanche's native platform for creating and trading assets, is an instance of the Avalanche Virtual Machine (AVM).
This API allows clients to create and trade assets on the X-Chain and other instances of the AVM.

## Format

This API uses the `json 2.0` API format.

## Endpoints

`/ext/bc/X` to interact with the X-Chain.

`/ext/bc/blockchainID` to interact with other AVM instances,
where `blockchainID` is the ID of a blockchain running the AVM.

## Methods

### avm.buildGenesis

Given a JSON representation of this Virtual Machine's genesis state, create the byte
representation of that state.

#### Endpoint

This call is made to the AVM's static API endpoint:

`/ext/vm/avm`

#### Signature

```go
avm.buildGenesis(genesisData:JSON) -> {bytes:string}
```

where `genesisData` has this form:

```json
{
"genesisData" : 
    {
        "assetAlias1": {               // Each object defines an asset
            "name": "human readable name",
            "symbol":"AVAL",           // Symbol is between 0 and 4 characters
            "initialState": {
                "fixedCap" : [         // Choose the asset type.
                    {                  // Can be "fixedCap", "variableCap", "limitedTransfer", "nonFungible"
                        "amount":1000, // At genesis, address A has
                        "address":"A"  // 1000 units of asset
                    },
                    {
                        "amount":5000, // At genesis, address B has
                        "address":"B"  // 1000 units of asset
                    },
                    ...                // Can have many initial holders
                ]
            }
        },
        "assetAliasCanBeAnythingUnique": { // Asset alias can be used in place of assetID in calls
            "name": "human readable name", // names need not be unique
            "symbol": "AVAL",              // symbols need not be unique
            "initialState": {
                "variableCap" : [          // No units of the asset exist at genesis
                    {
                        "minters": [       // The signature of A or B can mint more of
                            "A",           // the asset.
                            "B"
                        ],
                        "threshold":1
                    },
                    {
                        "minters": [       // The signatures of 2 of A, B and C can mint
                            "A",           // more of the asset
                            "B",
                            "C"
                        ],
                        "threshold":2
                    },
                    ...                    // Can have many minter sets
                ]
            }
        },
        ...                                // Can list more assets
    }
}
```

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "id"     : 1,
    "method" : "avm.buildGenesis",
    "params" : {
        "genesisData": {
            "asset1": {
                "name": "myFixedCapAsset",
                "symbol":"MFCA",
                "initialState": {
                    "fixedCap" : [
                        {
                            "amount":100000,
                            "address": "8UeduLccQuSmYiY3fGQEyotM9uXxoHoQQ"
                        },
                        {
                            "amount":100000,
                            "address": "AgVkHvvDShLumJrzXzkwuHa7rYpewj9Kg"
                        },
                        {
                            "amount":50000,
                            "address": "AwBDGsUwNdXgVc8XG2E8A8dL3bkoVbkL9"
                        },
                        {
                            "amount":50000,
                            "address": "AATN8YjgmFjC2jQRq45sEeGcBFXNYPcM8"
                        }
                    ]
                }
            },
            "asset2": {
                "name": "myVarCapAsset",
                "symbol":"MVCA",
                "initialState": {
                    "variableCap" : [
                        {
                            "minters": [
                                "AATN8YjgmFjC2jQRq45sEeGcBFXNYPcM8",
                                "FNqMDYafoDVYQ2o4a7Zd9maJAxcUEieQb"
                            ],
                            "threshold":1
                        },
                        {
                            "minters": [
                                "JJSiKQfha9Z2TiMxBZ8XdW9F6KFw8aKS4",
                                "7jJHY1vZL6AAbCFb97KMLY8nqMQVyd5JG",
                                "58pM5cEf1wMSncPdCwtQ8tbHs2xdMA4eo"
                            ],
                            "threshold":2
                        }
                    ]
                }
            }
        }
    }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/vm/avm
```

#### Example Response

```json
{
    "jsonrpc": "2.0",
    "result": {
        "bytes":"111TNWzUtHKoSvxohjyfEwE2X228ZDGBngZ4mdMUVMnVnjtnawW1b1zbAhzyAM1v6d7ECNj6DXsT7qDmhSEf3DWgXRj7ECwBX36ZXFc9tWVB2qHURoUfdDvFsBeSRqatCmj76eZQMGZDgBFRNijRhPNKUap7bCeKpHDtuCZc4YpPkd4mR84dLL2AL1b4K46eirWKMaFVjA5btYS4DnyUx5cLpAq3d35kEdNdU5zH3rTU18S4TxYV8voMPcLCTZ3h4zRsM5jW1cUzjWVvKg7uYS2oR9qXRFcgy1gwNTFZGstySuvSF7MZeZF4zSdNgC4rbY9H94RVhqe8rW7MXqMSZB6vBTB2BpgF6tNFehmYxEXwjaKRrimX91utvZe9YjgGbDr8XHsXCnXXg4ZDCjapCy4HmmRUtUoAduGNBdGVMiwE9WvVbpMFFcNfgDXGz9NiatgSnkxQALTHvGXXm8bn4CoLFzKnAtq3KwiWqHmV3GjFYeUm3m8Zee9VDfZAvDsha51acxfto1htstxYu66DWpT36YT18WSbxibZcKXa7gZrrsCwyzid8CCWw79DbaLCUiq9u47VqofG1kgxwuuyHb8NVnTgRTkQASSbj232fyG7YeX4mAvZY7a7K7yfSyzJaXdUdR7aLeCdLP6mbFDqUMrN6YEkU2X8d4Ck3T"
    },
    "id": 1
}
```

### avm.createAddress

Create a new address controlled by the given user.

#### Signature

```go
avm.createAddress({
    username: string,
    password:string
}) -> {address: string}
```

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "avm.createAddress",
    "params": {
        "username":"myUsername",
        "password":"myPassword"
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/X
```

#### Example Response

```json
{
    "jsonrpc": "2.0",
    "result": {
        "address": "X-EKpEPX56YA1dsaHBsW8X5nGqNSwJ7JrWH"
    },
    "id": 1
}
```

### avm.createFixedCapAsset

Create a new fixed-cap, fungible asset.
A quantity of it is created at initialization and then no more is ever created.
The asset can be sent with `avm.send`.

#### Signature

```go
avm.createFixedCapAsset({
    name: string,
    symbol: string,
    denomination: int,  
    initialHolders: []{
        address: string,
        amount: int
    },
    username: string,  
    password: string
}) -> {assetID: string}
```

* `name` is a human-readable name for the asset. Not necessarily unique.
* `symbol` is a shorthand symbol for the asset. Between 0 and 4 characters. Not necessarily unique. May be omitted.
* `denomination` determines how balances of this asset are displayed by user interfaces. If `denomination` is 0, 100 units of this asset are displayed as 100. If `denomination` is 1, 100 units of this asset are displayed as 10.0. If `denomination` is 2, 100 units of this asset are displays as .100, etc.
* In the future, performing a transaction on an AVM instance will require a transaction fee (paid in AVAX tokens). `username` and `password` denote the user paying the fee.
  That user will need to hold enough AVAX to cover the fee.
  Since there are no transaction fees right now, you can leave `username` and `password` blank.
* Each element in `initialHolders` specifies that `address` holds `amount` units of the asset at genesis.
* `assetID` is the ID of the new asset.

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     : 1,
    "method" :"avm.createFixedCapAsset",
    "params" :{
        "name": "myFixedCapAsset",
        "symbol":"MFCA",
        "initialHolders": [
            {
                "address": "X-AW87kLa9vP6TqEVsfvmLcTrroi73CQkng",
                "amount": 10000
            },
            {
                "address":"X-Gwafp5KZKPxtZbrW7RtQ7w1cQEAbVntGn",
                "amount":50000
            }
        ],
        "username":"myUsername",
        "password":"myPassword"
    }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/X
```

#### Example Response

```json
{
    "jsonrpc":"2.0",
    "id"     :1,
    "result" :{
        "assetID":"ZiKfqRXCZgHLgZ4rxGU9Qbycdzuq5DRY4tdSNS9ku8kcNxNLD"
    }
}
```

### avm.createMintTx

Create an unsigned transaction to mint more of a variable-cap asset (an asset created with `avm.createVariableCapAsset`.)

#### Signature

```go
avm.createMintTx({
    amount: int,
    assetID: string,
    to: string,
    minters: []string
}) -> {tx: string}
```

* `amount` units of `assetID` will be created and controlled by address `to`.
* `minters` are the minters that will sign this transaction before it's issued.
  `minters` must be `threshold` addresses from one of this asset's minter sets.

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     : 1,
    "method" :"avm.createMintTx",
    "params" :{
        "amount":10000000,
        "assetID":"2QbZFE7J4MAny9iXHUwq8Pz8SpFhWk3maCw4SkinVPv6wPmAbK",
        "to":"X-AHFNFP9rqditmGx4ZkSewmkyRPbBpnf22",
        "minters":[
            "X-AHFNFP9rqditmGx4ZkSewmkyRPbBpnf22",
            "X-PkGQYz92QaCSCUbY48pZ9fhXgDX2Z4hAb"
        ]
    }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/X
```

#### Example Response

```json
{
    "jsonrpc":"2.0",
    "id"     :1,
    "result" :{
        "tx":"NUPLwbt2hsYxpQg4H2o451hmTWQ4JZx2zMzM4SinwtHgAdX1JLPHXvWSXEnpecStLj"
    }
}
```

### avm.createVariableCapAsset

Create a new variable-cap, fungible asset. No units of the asset exist at initialization.
Minters can mint units of this asset using `createMintTx`, `signMintTx` and `issueTx`.
The asset can be sent with `avm.send`.

See [this tutorial](../tutorials/variable-cap-asset.md) for an example of usage.

#### Signature

```go
avm.createVariableCapAsset({
    name: string,
    symbol: string,
    denomination: int,  
    minterSets []{
        minters: []string,
        threshold: int
    },
    username: string,  
    password: string
}) -> {assetID: string}
```

* `name` is a human-readable name for the asset. Not necessarily unique.
* `symbol` is a shorthand symbol for the asset. Between 0 and 4 characters. Not necessarily unique. May be omitted.
* `denomination` determines how balances of this asset are displayed by user interfaces. If denomination is 0, 100 units of this asset are displayed as 100. If denomination is 1, 100 units of this asset are displayed as 10.0. If denomination is 2, 100 units of this asset are displays as .100, etc.
* `minterSets` is a list where each element specifies that `threshold` of the addresses
  in `minters` may together mint more of the asset by signing a minting transaction.
* In the future, performing a transaction on an AVM instance will require a transaction fee (paid in AVAX tokens). `username` and `password` denote the user paying the fee.
  That user will need to hold enough AVAX to cover the fee.
  Since there are no transaction fees right now, you can leave `username` and `password` blank.
* `assetID` is the ID of the new asset.

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     : 1,
    "method" :"avm.createVariableCapAsset",
    "params" :{
        "name":"myVariableCapAsset",
        "symbol":"MFCA",
        "minterSets":[
            {
                "minters":[
                    "X-5LC8hETB2XeTPrLGk8jjjZZVU6VzW1kXw"
                ],
                "threshold": 1
            },
            {
                "minters": [
                    "X-81XNrdH8xwRk8A9u6vAtLssiZYv7YFb6h",
                    "X-8sL4nTb2L2AZo9Bkp1TFPxxFf6GpRMsdf",
                    "X-NyiSJaddAG6GGTKHDroWs3PytbuvqfKXo"
                ],
                "threshold": 2
            }
        ],
        "username":"myUsername",
        "password":"myPassword"
    }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/X
```

#### Example Response

```json
{
    "jsonrpc":"2.0",
    "id"     :1,
    "result" :{
        "assetID":"2QbZFE7J4MAny9iXHUwq8Pz8SpFhWk3maCw4SkinVPv6wPmAbK"
    }
}
```

### avm.exportAVAX

Send AVAX from the X-Chain to an account on the P-Chain.  
After calling this method, you must call the P-Chain's [`importAVAX`](./platform.md#platformimportavax) method to complete the transfer.

#### Signature

```go
avm.exportAVAX({
    to: string,
    amount: int,
    username: string,
    password:string,
}) -> {txID: string}
```

* `to` is the ID of the P-Chain account the AVAX is sent to.
* `amount` is the amount of nAVAX to send.
* The AVAX is sent from addresses controlled by `username`

#### Example Call

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

#### Example Response

```json
{
    "jsonrpc": "2.0",
    "result": {
        "txID": "25VzbNzt3gi2vkE3Kr6H9KJeSR2tXkr8FsBCm3vARnB5foLVmx"
    },
    "id": 1
}
```

### avm.exportKey

Get the private key that controls a given address.  
The returned private key can be added to a user with `avm.importKey`.

#### Signature

```go
avm.exportKey({
    username: string,
    password:string,
    address:string
}) -> {privateKey: string}
```

* `username` must control `address`.
* `privateKey` is the string representation of the private key that controls `address`.

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"avm.exportKey",
    "params" :{
        "username" :"myUsername",
        "password":"myPassword",
        "address": "X-7u5FQArVaMSgGZzeTE9ckheWtDhU5T3KS"
    }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/X
```

#### Example Response

```json
{
    "jsonrpc":"2.0",
    "id"     :1,
    "result" :{
        "privateKey":"2w4XiXxPfQK4TypYqnohRL8DRNTz9cGiGmwQ1zmgEqD9c9KWLq"
    }
}
```

### avm.getAllBalances

Get the balances of all assets controlled by a given address.

#### Signature

```go
avm.getAllBalances({address:string}) -> {
    balances: []{
        asset: string,
        balance: int
    }
}
```

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     : 1,
    "method" :"avm.getAllBalances",
    "params" :{
        "address":"X-Go7PyA65ZUVichsQVmAt9d65h2S7Exiw"
    }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/X
```

#### Example Response

```json
{
    "jsonrpc": "2.0",
    "result": {
        "balances": [
            {
                "asset": "AVAX",
                "balance": "102"
            },
            {
                "asset": "2sdnziCz37Jov3QSNMXcFRGFJ1tgauaj6L7qfk7yUcRPfQMC79",
                "balance": "10000"
            }
        ]
    },
    "id": 1
}
```


### avm.getAssetDescription

Get information about an asset.

#### Signature

```go
avm.getAssetDescription({assetID: string}) -> {name: string, symbol: string, denomination:int}
```

* `name` is the asset's human-readable, not necessarily unique name.
* `symbol` is the asset's symbol.
* `denomination` determines how balances of this asset are displayed by user interfaces. If denomination is 0, 100 units of this asset are displayed as 100. If denomination is 1, 100 units of this asset are displayed as 10.0. If denomination is 2, 100 units of this asset are displays as .100, etc.


#### Example Call

```json
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"avm.getAssetDescription",
    "params" :{
        "assetID" :"ZiKfqRXCZgHLgZ4rxGU9Qbycdzuq5DRY4tdSNS9ku8kcNxNLD"
    }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/X
```

#### Example Response

```json
{
    "jsonrpc":"2.0",
    "id"     :1,
    "result" :{
        "name":"My asset name",
        "symbol":"MyAN"
    }
}
```

### avm.getBalance

Get the balance of an asset controlled by a given address.

#### Signature

```go
avm.getBalance({
    address:string,
    assetID: string
}) -> {balance: int}
```

#### Example Call

```json
curl -X POST --data '{
  "jsonrpc":"2.0",
  "id"     : 1,
  "method" :"avm.getBalance",
  "params" :{
      "address":"X-EKpEPX56YA1dsaHBsW8X5nGqNSwJ7JrWH",
      "assetID": "2pYGetDWyKdHxpFxh2LHeoLNCH6H5vxxCxHQtFnnFaYxLsqtHC"
  }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/X
```

#### Example Response

```json
{
    "jsonrpc":"2.0",
    "id"     :1,
    "result" :{
        "balance":"299999999999900",
        "utxoIDs":[
            {
                "txID":"WPQdyLNqHfiEKp4zcCpayRHYDVYuh1hqs9c1RqgZXS4VPgdvo",
                "outputIndex":1
            }
        ]
    }
}
```

### avm.getTx

Returns the specified transaction

#### Signature

```go
avm.getTx({txID: string}) -> {tx: string}
```
  
#### Example Call

```json
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"avm.getTx",
    "params" :{
        "txID":"2QouvFWUbjuySRxeX5xMbNCuAaKWfbk5FeEa2JmoF85RKLk2dD"
    }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/X
```

#### Example Response

```json
{
    "jsonrpc":"2.0",
    "id"     :1,
    "result" :{
        "tx":"1111111vQFqEEHkkAGwJnpdAJgga28zHk9pFARHp1VWe3QM5wC7ztGA5cZAPanFWXHkhbWEbFs9qsEpNZ7QHrzucUUZqLEPrAwJZLrZBik4dEhbsTCF3nS6s2fXVzc5ar2esLFD92WVMZmJNuTUQuKjVkjag2Gy3HHYSqm6bojrG62KrazywKPhrYx8QF9AqNfYYwD3XcSUV1g46r7sQ1WqzM8nyG4qL517JS1YVuTC3aWPeN5cxP6FdvbYexwHcgaBtiQsYbCEeZ9cuJqhE2Pxx8BJFpicLN8FBexb6fzQyBLiFR7yx6v6YBjq7dtu9MBczFdNCnDE4MsG2SyPZsdUv1XxQYVVwDqgqi8Zto5esJKph72YZbrXX3SHVSZBFZXkKbTzyEQFWHCF1jC"
    }
}
```

### avm.getTxStatus

Get the status of a transaction sent to the network.

#### Signature

```go
avm.getTxStatus({txID: string}) -> {status: string}
```

`status` is one of:

* `Accepted`: The transaction is (or will be) accepted by every node
* `Processing`: The transaction is being voted on by this node
* `Rejected`: The transaction will never be accepted by any node in the network
* `Unknown`: The transaction hasn't been seen by this node
  
#### Example Call

```json
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"avm.getTxStatus",
    "params" :{
        "txID":"2QouvFWUbjuySRxeX5xMbNCuAaKWfbk5FeEa2JmoF85RKLk2dD"
    }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/X
```

#### Example Response

```json
{
    "jsonrpc":"2.0",
    "id"     :1,
    "result" :{
        "status":"Accepted"
    }
}
```

### avm.getUTXOs

Get the UTXOs that reference a given address.

#### Signature

```go
avm.getUTXOs({addresses: string}) -> {utxos: []string}
```

* `UTXOs` is a list of UTXOs such that each UTXO references at least one address in `addresses`

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"avm.getUTXOs",
    "params" :{
        "addresses":["X-xMrKg8uUECt5CS9RE9j5hizv2t2SWTbk"]
    }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/X
```

#### Example Response

```go
{
    "jsonrpc": "2.0",
    "result": {
        "utxos": [
            "3ng2kBneUGy8SY98FgNvEMPo2pgL7m9UqcTDbL4svzdNKiuTpQCewGeJyTqppjMjaimnAvQfVfBTWcy2Da2CAKMy9P3Pu6E4nqp7NbrNN1aptYTEGoeg6oMjV76QGiWn37RhFcWuboDLst778nemsE7RrNhccgnHAXCQ"
        ]
    },
    "id": 1
}
```

### avm.importAVAX

Finalize a transfer of AVAX from the P-Chain to the X-Chain.

Before this method is called, you must call the P-Chain's [`exportAVAX`](./platform.md#platformexportavax) method to initiate the transfer.

#### Signature

```go
avm.importAVAX({
    to: string,
    username: string,
    password:string,
}) -> {txID: string}
```

* `to` is the address the AVAX is sent to.
  This must be the same as the `to` argument in the corresponding call to the P-Chain's `exportAVAX`,
  except that the prepended `X-` should be included in this argument.
* `username` is the user that controls `to`.

#### Example Call

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

#### Example Response

```json
{
    "jsonrpc": "2.0",
    "result": {
        "txID": "MqEaeWc4rfkw9fhRMuMTN7KUTNpFmh9Fd7KSre1ZqTsTQG73h"
    },
    "id": 1
}
```

### avm.importKey

Give a user control over an address by providing the private key that controls the address.

#### Signature

```go
avm.importKey({
    username: string,
    password:string,
    privateKey:string
}) -> {address: string}
```

* Add `privateKey` to `username`'s set of private keys. `address` is the address `username` now controls with the private key.

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"avm.importKey",
    "params" :{
        "username" :"myUsername",
        "password":"myPassword",
        "privateKey":"2w4XiXxPfQK4TypYqnohRL8DRNTz9cGiGmwQ1zmgEqD9c9KWLq"
    }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/X
```

#### Example Response

```json
{
    "jsonrpc":"2.0",
    "id"     :1,
    "result" :{
        "address":"X-7u5FQArVaMSgGZzeTE9ckheWtDhU5T3KS"
    }
}
```

### avm.issueTx

Send a signed transaction to the network.

#### Signature

```go
avm.issueTx({tx: string}) -> {txID: string}
```

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     : 1,
    "method" :"avm.issueTx",
    "params" :{
        "tx":"6sTENqXfk3gahxkJbEPsmX9eJTEFZRSRw83cRJqoHWBiaeAhVbz9QV4i6SLd6Dek4eLsojeR8FbT3arFtsGz9ycpHFaWHLX69edJPEmj2tPApsEqsFd7wDVp7fFxkG6HmySR"
    }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/X
```

#### Example Response

```json
{
    "jsonrpc":"2.0",
    "id"     :1,
    "result" :{
        "txID":"NUPLwbt2hsYxpQg4H2o451hmTWQ4JZx2zMzM4SinwtHgAdX1JLPHXvWSXEnpecStLj"
    }
}
```

### avm.listAddresses

List addresses controlled by the given user.

#### Signature

```go
avm.listAddresses({
    username: string,
    password: string
}) -> {addresses: []string}
```

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "avm.listAddresses",
    "params": {
        "username":"myUsername",
        "password":"myPassword"
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/X

```

#### Example Response

```json
{
    "jsonrpc": "2.0",
    "result": {
        "addresses": ["X-EKpEPX56YA1dsaHBsW8X5nGqNSwJ7JrWH"]
    },
    "id": 1
}
```

### avm.send

Send a quantity of an asset to an address.

#### Signature

```go
avm.Send({
    amount: int,
    assetID: string,
    to: string,
    username: string,
    password: string
}) -> {txID: string}
```

* Sends `amount` units of asset with ID `assetID` to address `to`.
  `amount` is denominated in the smallest increment of the asset.
  For AVAX this is 1 nAVAX (one billionth of 1 AVAX.)
* The asset is sent from addresses controlled by user `username`.
  (Of course, that user will need to hold at least the balance of the asset being sent.)

(Note: The asset ID of AVAX is AVA on nodes running Denali or earlier. The ID was changed to AVAX on the Everest release.)

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"avm.send",
    "params" :{
        "assetID" :"AVAX",
        "amount"  :10000,
        "to"      :"X-xMrKg8uUECt5CS9RE9j5hizv2t2SWTbk",
        "username":"userThatControlsAtLeast10000OfThisAsset",
        "password":"myPassword"
    }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/X
```

#### Example Response

```json
{
    "jsonrpc":"2.0",
    "id"     :1,
    "result" :{
        "txID":"2iXSVLPNVdnFqn65rRvLrsu8WneTFqBJRMqkBJx5vZTwAQb8c1"
    }
}
```

### avm.signMintTx

Sign an unsigned or partially signed transaction.

#### Signature

```go
avm.signMintTx({
    tx: string,
    minter: string,
    username: string,
    password: string
}) ->  
{tx: string}
```

* `tx` is an unsigned or partially signed mint transaction.
* `minter` is the address signing this transaction.
* `username` is the user that controls address `minter`.

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     : 1,
    "method" :"avm.signMintTx",
    "params" :{
        "tx":"1112yKaDdTb7XZXqX38X8U6ro7EC4GQdxDU48eHTcoQxPtJncHSQEMCi9n3hYaPp33K95i8sntkox5ZMHNq26DeNui4yuSQANXgFEeondXZvq65Pk1jnXbUpkJPkjX4KG1W9XQMAmCNpXs5xHzpX4THcYg3WY569Rj7cdf9Km4FQ3r3VDUAn1dpZLsCyQHeGb8Lr3ub7PGh4pn42KPAWsS6N4xCAGg1GGww2XNBxoDfu81toejPJFuqTJQg6tzgL82uT3amebb4FYQVU5B2gxH5Amevm1zsiTTfNDWui4BfB6e7jt8fc36UWYgb4MiaaApmySUe4ndt7SjFTT6taDkVNFdbUWuNEfiebrYFLpqL86mQ1XD",
        "minter":"X-xMrKg8uUECt5CS9RE9j5hizv2t2SWTbk",
        "username":"userThatControlsTheSignerAddress",
        "password":"passwordOfThatUser"
    }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/X
```

#### Example Response

```json
{
    "jsonrpc":"2.0",
    "id"     :1,
    "result" :{
        "tx":"1112yKaDdTb7XZXqX38X8U6ro7EC4GQdxDU48eHTcoQxPtJncHSQEMCi9n3hYaPp33K95i8sntkox5ZMHNq26DeNui4yuSQANXgFEeondXZvq65Pk1jnXbUpkJPkjX4KG1W9XQMAmCNpXs5xHzpX4THcYg3WY569Rj7cdf9Km4FQ3r3VDUAn1dpZLsCyQHeGb8Lr3ub7PGh4pn42KPAWsS6N4xCAGg1GGww2XNBxoDfu81toejPJFuqTJQg6tzgL82uT3amebb4FYQVU5B2gxH5Amevm1zsiTTfNDWui4BfB6e7jt8fc36UWYgb4MiaaApmySUe4ndt7SjFTT6taDkVNFdbUWuNEfiebrYFLpqL86mQ1XD"
    }
}
```
