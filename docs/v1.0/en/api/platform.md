# Platform API

This API allows clients to interact with the P-Chain (Platform Chain), which maintains Avalanche's validator set and handles blockchain creation.

## Endpoint

```http
/ext/P
```

## Format

This API uses the `json 2.0` RPC format.  

## Methods

### platform.addDelegator

Add a delegator to the Primary Network.

A delegator stakes AVAX and specifies a validator (the delegatee) to validate on their behalf.
The delegatee has an increased probability of being sampled by other validators (weight) in proportion to the stake delegated to them.

The delegatee charges a fee to the delegator; the former receives a percentage of the delegator's validation reward (if any.)

The delegation period must be a subset of the perdiod that the delegatee validates the Primary Network.

#### Signature

```go
platform.addDelegator(
    {
        nodeID: string,
        startTime: int,
        endTime: int,
        stakeAmount: int,
        rewardAddress: string,
        changeAddr: string, (optional)
        username: string,
        password: string
    }
) -> 
{
    txID: string,
    changeAddr: string
}
```

* `nodeID` is the node ID of the delegatee.
* `startTime` is the Unix time when the delegator starts delegating.
* `endTime` is the Unix time when the delegator stops delegating (and staked AVAX is returned).
* `stakeAmount` is the amount of nAVAX the delegator is staking.
* `rewardAddress` is the address the validator reward goes to, if there is one.
* `changeAddr` is the address any change will be sent to. If omitted, change is sent to one of the addresses controlled by the user.
* `username` is the user that pays the transaction fee.
* `password` is `username`'s password.
* `txID` is the transaction ID
* `changeAddr` in the result is the address where any change was sent.

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.addDelegator",
    "params": {
        "nodeID":"NodeID-MFrZFVCXPv5iCn6M9K6XduxGTYp891xXZ",
        "rewardAddress":"P-avax1gss39m5sx6jn7wlyzeqzm086yfq2l02xkvmecy",
        "startTime":1594102400,
        "endTime":1604102400,
        "stakeAmount":100000,
        "changeAddr": "P-avax103y30cxeulkjfe3kwfnpt432ylmnxux8r73r8u",
        "username":"username",
        "password":"password"
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

#### Example Response

```json
{
    "jsonrpc": "2.0",
    "result": {
        "txID": "6pB3MtHUNogeHapZqMUBmx6N38ii3LzytVDrXuMovwKQFTZLs",
        "changeAddr": "P-avax103y30cxeulkjfe3kwfnpt432ylmnxux8r73r8u"
    },
    "id": 1
}
```

### platform.addValidator

Add a validator to the Primary Network.

#### Signature

```go
platform.addValidator(
    {
        nodeID: string,
        startTime: int,
        endTime: int,
        stakeAmount: int,
        rewardAddress: string,
        changeAddr: string, (optional)
        delegationFeeRate: float,
        username: string,
        password: string
    }
) ->
{
    txID: string,
    changeAddr: string
}
```

* `nodeID` is the node ID of the validator being added.
* `startTime` is the Unix time when the validator starts validating the Primary Network.
* `endTime` is the Unix time when the validator stops validating the Primary Network (and staked AVAX is returned).
* `stakeAmount` is the amount of nAVAX the validator is staking.
* `rewardAddress` is the address the validator reward will go to, if there is one.
* `changeAddr` is the address any change will be sent to. If omitted, change is sent to one of the addresses controlled by the user.
* `delegationFeeRate` is the percent fee this validator charges when others delegate stake to them.
  Up to 4 decimal places allowed; additional decimal places are ignored. Must be between 0 and 100, inclusive.
  For example, if `delegationFeeRate` is `1.2345` and someone delegates to this validator, then when the delegation period is over, 1.2345% of the reward goes to the validator and the rest goes to the delegator.
* `username` is the user that pays the transaction fee.
* `password` is `username`'s password.
* `txID` is the transaction ID
* `changeAddr` in the result is the address where any change was sent.

#### Example Call

In this example we use shell command `date` to compute Unix times 10 minutes and 2 days in the future.
(Note: If you're on a Mac, replace  `$(date` with `$(gdate`. If you don't have `gdate` installed, do `brew install coreutils`.)

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.addValidator",
    "params": {
        "nodeID":"NodeID-ARCLrphAHZ28xZEBfUL7SVAmzkTZNe1LK",
        "rewardAddress":"P-avax1gss39m5sx6jn7wlyzeqzm086yfq2l02xkvmecy",
        "changeAddr": "P-avax103y30cxeulkjfe3kwfnpt432ylmnxux8r73r8u",
        "startTime":'$(date --date="10 minutes" +%s)',
        "endTime":'$(date --date="2 days" +%s)',
        "stakeAmount":1000000,
        "delegationFeeRate":10,
        "username":"username",
        "password":"password"
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

#### Example Response

```json
{
    "jsonrpc": "2.0",
    "result": {
        "txID": "6pb3mthunogehapzqmubmx6n38ii3lzytvdrxumovwkqftzls",
        "changeAddr": "P-avax103y30cxeulkjfe3kwfnpt432ylmnxux8r73r8u"
    },
    "id": 1
}
```

### platform.addSubnetValidator

Add a validator to a Subnet other than the Primary Network.
The Validator must validate the Primary Network for the entire duration they validate this Subnet.

#### Signature

```go
platform.addSubnetValidator(
    {
        nodeID: string,
        subnetID: string,
        startTime: int,
        endTime: int,
        weight: int,
        changeAddr: string, (optional)
        username: string,
        password: string
    }
) ->
{
    txID: string,
    changeAddr: string,
}
```

* `nodeID` is the node ID of the validator.
* `subnetID` is the subnet they will validate.
* `startTime` is the unix time when the validator starts validating the subnet.
* `endTime` is the unix time when the validator stops validating the subnet.
* `weight` is the validator's weight used for sampling.
* `changeAddr` is the address any change will be sent to. If omitted, change is sent to one of the addresses controlled by the user.
* `username` is the user that pays the transaction fee.
* `password` is `username`'s password.
* `txID` is the transaction ID.
* `changeAddr` in the result is the address where any change was sent.

#### Example call

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.addSubnetvalidator",
    "params": {
        "nodeID":"NodeID-7xhw2mdxuds44j42tcb6u5579esbst3lg",
        "subnetID":"zbfoww1ffkpvrfywpj1cvqrfnyesepdfc61hmu2n9jnghduel",
        "startTime":1583524047,
        "endTime":1604102399,
        "weight":1,
        "changeAddr": "P-avax103y30cxeulkjfe3kwfnpt432ylmnxux8r73r8u",
        "username":"username",
        "password":"password"
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

#### Example response

```json
{
    "jsonrpc":"2.0",
    "id"     :1,
    "result" :{
        "txID": "2exafyvRNSE5ehwjhafBVt6CTntot7DFjsZNcZ54GSxBbVLcCm",
        "changeAddr": "P-avax103y30cxeulkjfe3kwfnpt432ylmnxux8r73r8u"
    }
}
```

### platform.createAddress

Create a new address controlled by the given user.

#### Signature

```go
platform.createAddress({
    username: string,
    password:string
}) -> {address: string}
```

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.createAddress",
    "params": {
        "username":"myUsername",
        "password":"myPassword"
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/P
```

#### Example Response

```json
{
    "jsonrpc": "2.0",
    "result": {
        "address": "P-avax12lqey27sfujqq6mc5a3jr5av56cjsu8hg2d3hx"
    },
    "id": 1
}
```

### platform.createBlockchain

Create a new blockchain.
Currently only supports creation of new instances of the AVM and the Timestamp VM.

#### Signature

```go
platform.createBlockchain(
    {
        subnetID: string,
        vmID: string,
        name: string,
        genesisData: string,
        changeAddr: string, (optional)
        username: string,
        password:string
    }
) -> 
{
    txID: string,
    changeAddr: string
}
```

* `subnetID` is the ID of the Subnet that validates the new blockchain.
  The Subnet must exist and can't be the Primary Network.
* `vmID` is the ID of the Virtual Machine the blockchain runs.
  Can also be an alias of the Virtual Machine.
* `name` is a human-readable name for the new blockchain. Not necessarily unique.
* `genesisData` is the base 58 (with checksum) representation of the genesis state of the new blockchain.
  Virtual Machines should have a static API method named `buildGenesis` that can be used to generate `genesisData`.
* `changeAddr` is the address any change will be sent to. If omitted, change is sent to one of the addresses controlled by the user.
* `username` is the user that pays the transaction fee. This user must have a sufficient number of the subnet's control keys.
* `password` is `username`'s password.
* `txID` is the transaction ID.
* `changeAddr` in the result is the address where any change was sent.

#### Example Call

In this example we're creating a new instance of the Timestamp Virtual Machine.
`genesisData` came from calling `timestamp.buildGenesis`.

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.createBlockchain",
    "params" : {
        "vmID":"timestamp",
        "SubnetID":"2bRCr6B4MiEfSjidDwxDpdCyviwnfUVqB2HGwhm947w9YYqb7r",
        "name":"My new timestamp",
        "genesisData": "45oj4CqFViNHUtBxJ55TZfqaVAXFwMRMj2XkHVqUYjJYoTaEM",
        "changeAddr": "P-avax103y30cxeulkjfe3kwfnpt432ylmnxux8r73r8u",
        "username":"username",
        "password":"password"
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

#### Example Response

```json
{
    "jsonrpc": "2.0",
    "result": {
        "txID": "2TBnyFmST7TirNm6Y6z4863zusRVpWi5Cj1sKS9bXTUmu8GfeU",
        "changeAddr": "P-avax103y30cxeulkjfe3kwfnpt432ylmnxux8r73r8u"
    },
    "id": 1
}
```

### platform.createSubnet

Create a new Subnet.

The Subnet's ID is the same as this transaction's ID.

#### Signature

```go
platform.createSubnet(
    {
        controlKeys: []string,
        threshold: int,
        changeAddr: string, (optional)
        username: string,
        password: string
    }
) -> 
{
    txID: string,
    changeAddr: string
}
```

* In order to create add a validator to this subnet, `threshold` signatures are required from the addresses in `controlKeys`.
* `changeAddr` is the address any change will be sent to. If omitted, change is sent to one of the addresses controlled by the user.
* `username` is the user that pays the transaction fee.
* `password` is `username`'s password.
* `txID` is this transaction's ID.
* `changeAddr` in the result is the address where any change was sent.

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.createSubnet",
    "params": {
        "controlKeys":[
            "P-avax13xqjvp8r2entvw5m29jxxjhmp3hh6lz8laep9m",
            "P-avax165mp4efnel8rkdeqe5ztggspmw4v40j7pfjlhu"
        ],
        "threshold":2,
        "changeAddr": "P-avax103y30cxeulkjfe3kwfnpt432ylmnxux8r73r8u",
        "username":"username",
        "password":"password"
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

#### Example Response

```json
{
    "jsonrpc": "2.0",
    "result": {
        "txID": "hJfC5xGhtjhCGBh1JWn3vZ51KJP696TZrsbadPHNbQG2Ve5yd"
    },
    "id": 1
}
```

### platform.exportAVAX

Send AVAX from an address on the P-Chain to an address on the X-Chain. 
After issuing this transaction, you must call the X-Chain's [`importAVAX`](./avm.md#avmimportavax) method to complete the transfer.

#### Signature

```go
platform.exportAVAX(
    {
        amount: int,
        to: string,
        changeAddr: string, (optional)
        username: string,
        password:string
    }
) -> 
{
    txID: string,
    changeAddr: string
}
```

* `amount` is the amount of nAVAX to send.
* `to` is the address on the X-Chain to send the AVAX to.
* `changeAddr` is the address any change will be sent to. If omitted, change is sent to one of the addresses controlled by the user.
* `username` is the user sending the AVAX and paying the transaction fee.
* `password` is `username`'s password.
* `txID` is the ID of this transaction.
* `changeAddr` in the result is the address where any change was sent.

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.exportAVAX",
    "params": {
        "to":"X-avax1yv8cwj9kq3527feemtmh5gkvezna5xys08mxet",
        "amount":1,
        "changeAddr": "P-avax103y30cxeulkjfe3kwfnpt432ylmnxux8r73r8u",
        "username":"username",
        "password":"password"
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

#### Example Response

```json
{
    "jsonrpc": "2.0",
    "result": {
        "txID": "2Kz69TNBSeABuaVjKa6ZJCTLobbe5xo9c5eU8QwdUSvPo2dBk3",
        "changeAddr": "P-avax103y30cxeulkjfe3kwfnpt432ylmnxux8r73r8u"
    },
    "id": 1
}
```

### platform.exportKey

Get the private key that controls a given address.  
The returned private key can be added to a user with `platform.importKey`.

#### Signature

```go
platform.exportKey({
    username: string,
    password:string,
    address:string
}) -> {privateKey: string}
```

* `username` is the user that controls `address`.
* `password` is `username`'s password.
* `privateKey` is the string representation of the private key that controls `address`.

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"platform.exportKey",
    "params" :{
        "username" :"username",
        "password":"password",
        "address": "P-avax1zwp96clwehpwm57r9ftzdm7rnuslrunj68ua3r"
    }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

#### Example Response

```json
{
    "jsonrpc":"2.0",
    "id"     :1,
    "result" :{
        "privateKey":"PrivateKey-Lf49kAJw3CbaL783vmbeAJvhscJqC7vi5yBYLxw2XfbzNS5RS"
    }
}
```

### platform.getBalance

Get the balance of AVAX controlled by a given address.

#### Signature

```go
platform.getBalance({
    address:string
}) -> {
    balance: int,
    utxoIDs: []{
        txID: string,
        outputIndex: int
        }
    }
}
```

* `address` is the address to get the balance of.
* `balance` is the balance, in nAVAX.
* `utxoIDs` are the IDs of the UTXOs that reference `address`.

#### Example Call

```json
curl -X POST --data '{
  "jsonrpc":"2.0",
  "id"     : 1,
  "method" :"platform.getBalance",
  "params" :{
      "address":"P-avax1m8wnvtqvthsxxlrrsu3f43kf9wgch5tyfx4nmf"
  }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/P
```

#### Example Response

```json
{
    "jsonrpc":"2.0",
    "id"     :1,
    "result" :{
        "balance":"20000000000000",
        "utxoIDs":[
            {
                "txID":"LUriB3W919F84LwPMMw4sm2fZ4Y76Wgb6msaauEY7i1tFNmtv",
                "outputIndex":0
            }
        ]
    }
}
```

### platform.getBlockchains

Get all the blockchains that exist (excluding the P-Chain).

#### Signature

```go
platform.getBlockchains() ->
{
    blockchains: []{
        id: string,
        name:string,
        subnetID: string,
        vmID: string
    }
}
```

* `blockchains` is all of the blockchains that exists on the Avalanche network.
* `name` is the human-readable name of this blockchain.
* `id` is the blockchain's ID.
* `subnetID` is the ID of the Subnet that validates this blockchain.
* `vmID` is the ID of the Virtual Machine the blockchain runs.

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.getBlockchains",
    "params": {},
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

#### Example Response

```json
{
    "jsonrpc": "2.0",
    "result": {
        "blockchains": [
            {
                "id": "mnihvmrJ4MiojP7qhnF3sKR43RJvJbHrbkM8yFoLdwc4nwEqV",
                "name": "AVM",
                "subnetID": "11111111111111111111111111111111LpoYY",
                "vmID": "jvYyfQTxGMJLuGWa55kdP2p2zSUYsQ5Raupu4TW34ZAUBAbtq"
            },
            {
                "id": "2rWWhAMu2NyNPEHrDNnTfhtdV9MZWKkp1L5D6ANWnhAkJAkosN",
                "name": "Athereum",
                "subnetID": "11111111111111111111111111111111LpoYY",
                "vmID": "mgj786NP7uDwBCcq6YwThhaN8FLyybkCa4zBWTQbNgmK6k9A6"
            },
            {
                "id": "CqhF97NNugqYLiGaQJ2xckfmkEr8uNeGG5TQbyGcgnZ5ahQwa",
                "name": "Simple DAG Payments",
                "subnetID": "11111111111111111111111111111111LpoYY",
                "vmID": "sqjdyTKUSrQs1YmKDTUbdUhdstSdtRTGRbUn8sqK8B6pkZkz1"
            },
            {
                "id": "VcqKNBJsYanhVFxGyQE5CyNVYxL3ZFD7cnKptKWeVikJKQkjv",
                "name": "Simple Chain Payments",
                "subnetID": "11111111111111111111111111111111LpoYY",
                "vmID": "sqjchUjzDqDfBPGjfQq2tXW1UCwZTyvzAWHsNzF2cb1eVHt6w"
            },
            {
                "id": "2SMYrx4Dj6QqCEA3WjnUTYEFSnpqVTwyV3GPNgQqQZbBbFgoJX",
                "name": "Simple Timestamp Server",
                "subnetID": "11111111111111111111111111111111LpoYY",
                "vmID": "tGas3T58KzdjLHhBDMnH2TvrddhqTji5iZAMZ3RXs2NLpSnhH"
            },
            {
                "id": "KDYHHKjM4yTJTT8H8qPs5KXzE6gQH5TZrmP1qVr1P6qECj3XN",
                "name": "My new timestamp",
                "subnetID": "2bRCr6B4MiEfSjidDwxDpdCyviwnfUVqB2HGwhm947w9YYqb7r",
                "vmID": "tGas3T58KzdjLHhBDMnH2TvrddhqTji5iZAMZ3RXs2NLpSnhH"
            },
            {
                "id": "2TtHFqEAAJ6b33dromYMqfgavGPF3iCpdG3hwNMiart2aB5QHi",
                "name": "My new AVM",
                "subnetID": "2bRCr6B4MiEfSjidDwxDpdCyviwnfUVqB2HGwhm947w9YYqb7r",
                "vmID": "jvYyfQTxGMJLuGWa55kdP2p2zSUYsQ5Raupu4TW34ZAUBAbtq"
            }
        ]
    },
    "id": 1
}
```

### platform.getBlockchainStatus

Get the status of a blockchain.

#### Signature

```go
platform.getBlockchainStatus(
    {
        blockchainID: string
    }
) -> {status: string}
```

`status` is one of:

* `Validating`: The blockchain is being validated by this node.
* `Created`:    The blockchain exists but isn't being validated by this node.
* `Preferred`:  The blockchain was proposed to be created and is likely to be created but the transaction isn't yet accepted.
* `Unknown`:    The blockchain either wasn't proposed or the proposal to create it isn't preferred. The proposal may be resubmitted.

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.getBlockchainStatus",
    "params":{
    	"blockchainID":"2NbS4dwGaf2p1MaXb65PrkZdXRwmSX4ZzGnUu7jm3aykgThuZE"
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

#### Example Response

```json
{
    "jsonrpc": "2.0",
    "result": {
        "status": "Created"
    },
    "id": 1
}
```

### platform.getCurrentValidators

List the current validators of the given Subnet.

#### Signature 

```go
platform.getCurrentValidators({subnetID: string}) ->
{
    validators: []{
        startTime: int,
        endTime: int,
        weight: int, (optional)
        stakeAmount: int, (optional)
        address: string
        nodeID: string
    }
}
```

* `subnetID` is the subnet whose current validators are returned. If omitted, returns the current validators of the Primary Network.
* `startTime` is the Unix time when the validator starts validating the Subnet.
* `endTime` is the Unix time when the validator stops validating the Subnet.
* `weight` is the validator's weight when sampling validators.
  Omitted if `subnetID` is the Primary Network.
* `stakeAmount` is the amount of nAVAX this validator staked.
  Omitted if `subnetID` is not the Primary Network.
* `nodeID` is the validator's node ID.

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.getCurrentValidators",
    "params": {},
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

#### Example Response

```json
{
    "jsonrpc": "2.0",
    "result": {
        "validators": [
            {
                "startTime": "1591878109",
                "endtime": "1594469809",
                "stakeAmount": "319902",
                "nodeID": "NodeID-NDmcZNsWoPrkN9KSt2A9js639hEQWUmUf"
            },
            {
                "startTime": "1591473391",
                "endtime": "1592855191",
                "stakeAmount": "10000",
                "nodeID": "NodeID-62T5AAwKdFMNi7Gm193A6zyJhVscRfuhP"
            },
            {
                "startTime": "1591387125",
                "endtime": "1622923025",
                "stakeAmount": "20000000000000",
                "nodeID": "NodeID-HGZ8ae74J3odT8ESreAdCtdnvWG1J4X5n"
            }
        ]
    },
    "id": 1
}
```

### platform.getHeight

Returns the height of the last accepted block.

#### Signature 

```go
platform.getHeight() ->
{
      height: int,
}
```

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.getHeight",
    "params": {},
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

#### Example Response

```json
{
    "jsonrpc": "2.0",
    "result": {
        "height": "56"
    },
    "id": 1
}
```

### platform.getMinStake

Get the minimum staking amount of the network.

#### Signature 

```go
platform.getMinStake() -> {minStake:uint64}
```

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"platform.getMinStake"
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

#### Example Response

```json
{
    "jsonrpc":"2.0",
    "id"     :1,
    "result" :{
        "minStake": "5000000"
    }
}
```

### platform.getPendingValidators

List the validators in the pending validator set of the specified Subnet.
Each validator is not currently validating the Subnet but will in the future.

#### Signature 

```go
platform.getPendingValidators({subnetID: string}) ->
{
    validators: []{
        startTime: int,
        endTime: int,
        weight: int, (optional)
        stakeAmount: int, (optional)
        nodeID: string
    }
}
```

* `subnetID` is the subnet whose current validators are returned. If omitted, returns the current validators of the Primary Network.
* `startTime` is the Unix time when the validator starts validating the Subnet.
* `endTime` is the Unix time when the validator stops validating the Subnet.
* `weight` is the validator's weight when sampling validators.
  Omitted if `subnetID` is the Primary Network.
* `stakeAmount` is the amount of nAVAX this validator staked.
  Omitted if `subnetID` is not the Primary Network.
* `nodeID` is the validator's node ID.

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.getPendingValidators",
    "params": {},
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

#### Example Response

```json
{
    "jsonrpc": "2.0",
    "result": {
        "validators": [
            {
                "startTime": "1592400591",
                "endtime": "1622923025",
                "stakeAmount": "10000",
                "nodeID": "NodeID-DpL8PTsrjtLzv5J8LL3D2A6YcnCTqrNH9"
            },
        ]
    },
    "id": 1
}
```

### platform.getSubnets

Get all the Subnets that exist.

#### Signature

```go
platform.getSubnets(
    {ids: []string}
) ->
{
    subnets: []{
            id: string,
            controlKeys: []string,
            threshold: string
    }
}
```
`ids` are the IDs of the subnets to get information about. If omitted, gets information about all subnets.
`id` is the Subnet's ID.  
`threshold` signatures from addresses in `controlKeys` are needed to add a validator to the subnet.  
See [here](../tutorials/adding-validators.md#add-a-validator-to-a-subnet) for information on adding a validator to a Subnet.

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.getSubnets",
    "params": {"ids":["hW8Ma7dLMA7o4xmJf3AXBbo17bXzE7xnThUd3ypM4VAWo1sNJ"]},
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

#### Example Response

```json
{
    "jsonrpc": "2.0",
    "result": {
        "subnets": [
            {
                "id": "hW8Ma7dLMA7o4xmJf3AXBbo17bXzE7xnThUd3ypM4VAWo1sNJ",
                "controlKeys": [
                    "KNjXsaA1sZsaKCD1cd85YXauDuxshTes2",
                    "Aiz4eEt5xv9t4NCnAWaQJFNz5ABqLtJkR"
                ],
                "threshold": "2"
            }
        ]
    },
    "id": 1
}'
```

### platform.getStake

Get the amount of nAVAX staked by a set of addresses.
The amount returned does not include staking rewards.

#### Signature

```go
platform.getStake({addresses: []string}) -> {stake: int}
```

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.getStake",
    "params": {
    	"addresses": [
            "P-everest1g3ea9z5kmkzwnxp8vr8rpjh6lqw4r0ufec460d",
            "P-everest12un03rm579fewele99c4v53qnmymwu46dv3s5v"
        ]
    },
    "id": 1
}
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

#### Example Response

```json
{
    "jsonrpc": "2.0",
    "result": {
        "staked": "5000000"
    },
    "id": 1
}
```

### platform.getTx

Gets a transaction by its ID.

#### Signature

```go
platform.getTx({txID: string} -> {tx: string})
```

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.getTx",
    "params": {
    	"txID":"TAG9Ns1sa723mZy1GSoGqWipK6Mvpaj7CAswVJGM6MkVJDF9Q"
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

#### Example Response

```json
{
    "jsonrpc": "2.0",
    "result": {
        "tx": "111117XV7Rm5EoKbwXFJp5WWWouAENJcF1zXGxPDPCfTbpiLfwkUXcoHKnfzdXz7sRgGYeaVtJkcD9MNgGuKGXsyWEWpTK2zAToEf64ezp7r7SyvyL7RqC5oqvNbRDShn5hm9pDV4JTCjZR5RzAxjBEJZ2V8eqtU6jvpsJMHxNBtCwL6Atc1t2Dt7s5nqf7wdbFUBvwKXppBb2Yps8wUvtTKQifssMUAPygc2Rv4rGd9LRANk4JTiT15qzUjXX7zSzz16pxdBXc4jp2Z2UJRWbdxZdaybL3mYCFj197bBnYieRYzRohaUEpEjGcohrmkSfHB8S2eD74o2r66sVGdpXYo95vkZeayQkrMRit6unwWBx8FJR7Sd7GysxS9A3CiMc8cL4oRmr7XyvcFCrnPbUZK7rnN1Gtq3MN8k4JVvX6DuiFAS7xe61jY3VKJAZM9Lg3BgU6TAU3gZ"
    },
    "id": 1
}
```

### platform.getTxStatus

Gets a transaction's status by its ID.

#### Signature

```go
platform.getTxStatus({txID: string} -> {status: string})
```

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.getTxStatus",
    "params": {
    	"txID":"TAG9Ns1sa723mZy1GSoGqWipK6Mvpaj7CAswVJGM6MkVJDF9Q"
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

#### Example Response

```json
{
    "jsonrpc": "2.0",
    "result": "Committed",
    "id": 1
}
```

### platform.getUTXOs

Gets the UTXOs that reference a given set address.

#### Signature

```go
platform.getUTXOs(
    {
        addresses: string,
        limit: int,
        startIndex: {
            address: string,
            utxo: string
        }
    },
) -> 
{
    numFetched: int
    utxos: []string,
    stopIndex: {
        address: string,
        utxo: string
    }
}
```

* `utxos` is a list of UTXOs such that each UTXO references at least one address in `addresses`.
* At most `limit` UTXOs are returned. If `limit` is omitted or greater than 1024, it is set to 1024.
* This method supports pagination. `stopIndex` denotes the last UTXO returned. To get the next set of UTXOs,
  use the value of `stopIndex` as `startIndex` in the next call.
* If `startIndex` is omitted, will fetch all UTXOs up to `limit`. 
* When using pagination (ie when `startIndex` is provided), UTXOs are not guaranteed to be unique across multiple calls. 
  That is, a UTXO may appear in the result of the first call, and then again in the second call.
* When using pagination, consistency is not guaranteed across multiple calls.
  That is, the UTXO set of the addresses may have changed between calls.

#### Example

Suppose we want all UTXOs that reference at least one of `P-avax1s994jad0rtwvlfpkpyg2yau9nxt60qqfv023qx` and `P-avax1fquvrjkj7ma5srtayfvx7kncu7um3ym73ztydr`.

```json
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"platform.getUTXOs",
    "params" :{
        "addresses":["P-avax1s994jad0rtwvlfpkpyg2yau9nxt60qqfv023qx", "P-avax1fquvrjkj7ma5srtayfvx7kncu7um3ym73ztydr"],
        "limit":5
    }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/P
```

This gives response:

```json
{
    "jsonrpc": "2.0",
    "result": {
        "numFetched": "5",
        "utxos": [
            "11PQ1sNw9tcXjVki7261souJnr1TPFrdVCu5JGZC7Shedq3a7xvnTXkBQ162qMYxoerMdwzCM2iM1wEQPwTxZbtkPASf2tWvddnsxPEYndVSxLv8PDFMwBGp6UoL35gd9MQW3UitpfmFsLnAUCSAZHWCgqft2iHKnKRQRz",
            "11RCDVNLzFT8KmriEJN7W1in6vB2cPteTZHnwaQF6kt8B2UANfUkcroi8b8ZSEXJE74LzX1mmBvtU34K6VZPNAVxzF6KfEA8RbYT7xhraioTsHqxVr2DJhZHpR3wGWdjUnRrqSSeeKGE76HTiQQ8WXoABesvs8GkhVpXMK",
            "11GxS4Kj2od4bocNWMQiQhcBEHsC3ZgBP6edTgYbGY7iiXgRVjPKQGkhX5zj4NC62ZdYR3sZAgp6nUc75RJKwcvBKm4MGjHvje7GvegYFCt4RmwRbFDDvbeMYusEnfVwvpYwQycXQdPFMe12z4SP4jXjnueernYbRtC4qL",
            "11S1AL9rxocRf2NVzQkZ6bfaWxgCYch7Bp2mgzBT6f5ru3XEMiVZM6F8DufeaVvJZnvnHWtZqocoSRZPHT5GM6qqCmdbXuuqb44oqdSMRvLphzhircmMnUbNz4TjBxcChtks3ZiVFhdkCb7kBNLbBEmtuHcDxM7MkgPjHw",
            "11Cn3i2T9SMArCmamYUBt5xhNEsrdRCYKQsANw3EqBkeThbQgAKxVJomfc2DE4ViYcPtz4tcEfja38nY7kQV7gGb3Fq5gxvbLdb4yZatwCZE7u4mrEXT3bNZy46ByU8A3JnT91uJmfrhHPV1M3NUHYbt6Q3mJ3bFM1KQjE"
        ],
        "endIndex": {
            "address": "P-avax1fquvrjkj7ma5srtayfvx7kncu7um3ym73ztydr",
            "utxo": "kbUThAUfmBXUmRgTpgD6r3nLj7rJUGho6xyht5nouNNypH45j"
        }
    },
    "id": 1
}
```

Since `numFetched` is the same as `limit`, we can tell that there may be more UTXOs that were not fetched.
We call the method again, this time with `startIndex`:

```json
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"platform.getUTXOs",
    "params" :{
        "addresses":["P-avax1fquvrjkj7ma5srtayfvx7kncu7um3ym73ztydr"],
        "limit":5,
        "startIndex": {
            "address": "P-avax1fquvrjkj7ma5srtayfvx7kncu7um3ym73ztydr",
            "utxo": "kbUThAUfmBXUmRgTpgD6r3nLj7rJUGho6xyht5nouNNypH45j"
        }
    }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/P
```

This gives response:

```json
{
    "jsonrpc": "2.0",
    "result": {
        "numFetched": "4",
        "utxos": [
            "115ZLnNqzCsyugMY5kbLnsyP2y4se4GJBbKHjyQnbPfRBitqLaxMizsaXbDMU61fHV2MDd7fGsDnkMzsTewULi94mcjk1bfvP7aHYUG2i3XELpV9guqsCtv7m3m3Kg4Ya1m6tAWqT7PhvAaW4D3fk8W1KnXu5JTWvYBqD2",
            "11QASUuhw9M1r52maTFUZ4fnuQby9inX77VYxePQoNavEyCPuHN5cCWPQnwf8fMrydFXVMPAcS4UJAcLjSFskNEmtVPDMY4UyHwh2MChBju6Y7V8yYf3JBmYt767NPsdS3EqgufYJMowpud8fNyH1to4pAdd6A9CYbD8KG",
            "11MHPUWT8CsdrtMWstYpFR3kobsvRrLB4W8tP9kDjhjgLkCJf9aaJQM832oPcvKBsRhCCxfKdWr2UWPztRCU9HEv4qXVwRhg9fknAXzY3a9rXXPk9HmArxMHLzGzRECkXpXb2dAeqaCsZ637MPMrJeWiovgeAG8c5dAw2q",
            "11K9kKhFg75JJQUFJEGiTmbdFm7r1Uw5zsyDLDY1uVc8zo42WNbgcpscNQhyNqNPKrgtavqtRppQNXSEHnBQxEEh5KbAEcb8SxVZjSCqhNxME8UTrconBkTETSA23SjUSk8AkbTRrLz5BAqB6jo9195xNmM3WLWt7mLJ24"
        ],
        "endIndex": {
            "address": "P-avax1fquvrjkj7ma5srtayfvx7kncu7um3ym73ztydr",
            "utxo": "21jG2RfqyHUUgkTLe2tUp6ETGLriSDTW3th8JXFbPRNiSZ11jK"
        }
    },
    "id": 1
}
```

Since `numFetched` is less than `limit`, we know that we are done fetching UTXOs and don't need to call this method again.

### platform.importAVAX

Complete a transfer of AVAX from the X-Chain to the P-Chain.

Before this method is called, you must call the X-Chain's [`exportAVAX`](./avm.md#avmexportavax) method to initiate the transfer.

#### Signature

```go
platform.importAVAX(
    {
        to: string,
        sourceChain: string,
        changeAddr: string, (optional)
        username: string,
        password: string
    }
) -> 
{
    txID: string,
    changeAddr: string
}
```

* `to` is the ID of the address the AVAX is imported to.
  This must be the same as the `to` argument in the corresponding call to the X-Chain's `exportAVAX`.
* `sourceChain` is the ID or alias of the chain the AVAX is being imported from.
  To import funds from the X-Chain, use `"X"`.
* `changeAddr` is the address any change will be sent to. If omitted, change is sent to one of the addresses controlled by the user.
* `username` is the user that controls the address specified in `to`.
* `password` is `username`'s password.
* `txID` is this transaction's ID.
* `changeAddr` in the result is the address where any change was sent.

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.importAVAX",
    "params": {
        "to":"P-avax1apzq2zt0uaaatum3wdz83u4z7dv4st7l5m5n2a",
        "sourceChain":"X",
        "changeAddr": "P-avax103y30cxeulkjfe3kwfnpt432ylmnxux8r73r8u",
        "username":"bob",
        "password":"loblaw"
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

#### Example Response

```json
{
    "jsonrpc": "2.0",
    "result": {
        "txID": "P63NjowXaQJXt5cmspqdoD3VcuQdXUPM5eoZE2Vcg63aVEx8R",
        "changeAddr": "P-avax103y30cxeulkjfe3kwfnpt432ylmnxux8r73r8u"
    },
    "id": 1
}
```

### platform.importKey

Give a user control over an address by providing the private key that controls the address.

#### Signature

```go
platform.importKey({
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
    "method" :"platform.importKey",
    "params" :{
        "username" :"bob",
        "password":"loblaw",
        "privateKey":"PrivateKey-2w4XiXxPfQK4TypYqnohRL8DRNTz9cGiGmwQ1zmgEqD9c9KWLq"
    }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

#### Example Response

```json
{
    "jsonrpc":"2.0",
    "id"     :1,
    "result" :{
        "address":"P-avax19hwpvkx2p5q99w87dlpfhqpt3czyh8ywasfaym"
    }
}
```

<!-- TODO: add issueTx to platform API
### platform.issueTx

Issue a transaction to the Platform Chain.

#### Signature

```go
platform.issueTx({tx: string}) -> {txID: string}
```

* `tx` is the base 58 (with checksum) representation of a transaction.
* `txID` is the transaction's ID.

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.issueTx",
    "params": {
        "tx":"111Bit5JNASbJyTLrd2kWkYRoc96swEWoWdmEhuGAFK3rCAyTnTzomuFwgx1SCUdUE71KbtXPnqj93KGr3CeftpPN37kVyqBaAQ5xaDjr7wVBTUYi9iV7kYJnHF61yovViJF74mJJy7WWQKeRMDRTiPuii5gsd11gtNahCCsKbm9seJtk2h1wAPZn9M1eL84CGVPnLUiLP"
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

#### Example Response

```json
{
    "jsonrpc": "2.0",
    "result": {
        "txID": "G3BuH6ytQ2averrLxJJugjWZHTRubzCrUZEXoheG5JMqL5ccY"
    },
    "id": 1
}
```
-->

### platform.listAddresses

List addresses controlled by the given user.

#### Signature

```go
platform.listAddresses({
    username: string,
    password: string
}) -> {addresses: []string}
```

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.listAddresses",
    "params": {
        "username":"myUsername",
        "password":"myPassword"
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/P

```

#### Example Response

```json
{
    "jsonrpc": "2.0",
    "result": {
        "addresses": ["P-avax1ffksh2m592yjzwfp2xmdxe3z4ushln9s09z5p0"]
    },
    "id": 1
}
```

### platform.sampleValidators

Sample validators from the specified Subnet.

#### Signature

```go
platform.sampleValidators(
    {
        size: int,
        subnetID: string
    }
) ->
{
    validators:[size]string
}
```

* `size` is the number of validators to sample.
* `subnetID` is the Subnet to sampled from.
  If omitted, defaults to the Primary Network.
* Each element of `validators` is the ID of a validator.

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"platform.sampleValidators",
    "params" :{
        "size":2
    }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

#### Example Response

```json
{
    "jsonrpc":"2.0",
    "id"     :1,
    "result" :{
        "validators":[
            "NodeID-MFrZFVCXPv5iCn6M9K6XduxGTYp891xXZ",
            "NodeID-NFBbbJ4qCmNaCzeW7sxErhvWqvEQMnYcN"
        ]
    }
}
```

### platform.validatedBy

Get the Subnet that validates a given blockchain.

#### Signature

```go
platform.validatedBy(
    {
        blockchainID: string
    }
) -> {subnetID: string}
```

* `blockchainID` is the blockchain's ID.
* `subnetID` is the ID of the Subnet that validates the blockchain.

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.validatedBy",
    "params": {
        "blockchainID": "KDYHHKjM4yTJTT8H8qPs5KXzE6gQH5TZrmP1qVr1P6qECj3XN"
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

#### Example Response

```json
{
    "jsonrpc": "2.0",
    "result": {
        "subnetID": "2bRCr6B4MiEfSjidDwxDpdCyviwnfUVqB2HGwhm947w9YYqb7r"
    },
    "id": 1
}
```

### platform.validates

Get the IDs of the blockchains a Subnet validates.

#### Signature

```go
platform.validates(
    {
        subnetID: string
    }
) -> {blockchainIDs: []string}
```

* `subnetID` is the Subnet's ID.
* Each element of `blockchainIDs` is the ID of a blockchain the Subnet validates.

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.validates",
    "params": {
        "subnetID":"2bRCr6B4MiEfSjidDwxDpdCyviwnfUVqB2HGwhm947w9YYqb7r"
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

#### Example Response

```json
{
    "jsonrpc": "2.0",
    "result": {
        "blockchainIDs": [
            "KDYHHKjM4yTJTT8H8qPs5KXzE6gQH5TZrmP1qVr1P6qECj3XN",
            "2TtHFqEAAJ6b33dromYMqfgavGPF3iCpdG3hwNMiart2aB5QHi"
        ]
    },
    "id": 1
}
```