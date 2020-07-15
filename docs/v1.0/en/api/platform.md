# Platform API

This API allows clients to interact with the P-Chain (Platform Chain), which maintains Avalanche's validator set and handles blockchain creation.

## Endpoint

```http
/ext/P
```

## Format

This API uses the `json 2.0` RPC format.  

## Methods

### platform.addDefaultSubnetDelegator

Add a delegator to the Default Subnet.

A delegator stakes AVAX and specifies a validator (the delegatee) to validate on their behalf.
The delegatee has an increased probability of being sampled by other validators (weight) in proportion to the stake delegated to them.

The delegatee charges a fee to the delegator; the former receives a percentage of the delegator's validation reward (if any.)

The delegation period must be a subset of the perdiod that the delegatee validates the Default Subnet.

#### Signature

```go
platform.addDefaultSubnetDelegator(
    {
        id: string,
        startTime: int,
        endTime: int,
        stakeAmount: int,
        payerNonce: int,
        destination: string
    }
) -> {unsignedTx: string}
```

* `id` is the node ID of the delegatee.
* `startTime` is the Unix time when the delegator starts delegating.
* `endTime` is the Unix time when the delegator stops delegating (and staked AVAX is returned).
* `stakeAmount` is the amount of nAVAX the delegator is staking.
* `payerNonce` is the next unused nonce of the account that will provide the staked AVAX and pay the transaction fee.
* `destination` is the address of the account the staked AVAX and validation reward (if applicable) are sent to at `endTime`.
* `unsignedTx` is the unsigned transaction.
  It must be signed (using `sign`) by the key of the account providing the staked AVAX and paying the transaction fee before it can be issued.

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.addDefaultSubnetDelegator",
    "params": {
        "id":"MFrZFVCXPv5iCn6M9K6XduxGTYp891xXZ",
        "payerNonce":1,
        "destination":"Q4MzFZZDPHRPAHFeDs3NiyyaZDvxHKivf",
        "startTime":1594102400,
        "endTime":1604102400,
        "stakeAmount":100000
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

#### Example Response

```json
{
    "jsonrpc":"2.0",
    "id"     :1,
    "result" :{
        "unsignedTx": "111Bit5JNASbJyTLrd2kWkYRoc96swEWoWdmEhuGAFK3rCAyTnTzomuFwgx1SCUdUE71KbtXPnqj93KGr3CeftpPN37kVyqBaAQ5xaDjr7wU8riGS89NDJ8AwVgZgnFkgF3uMfwCiCuPvvubGyQxNHE4TM9iDgj6h3URdGQ4JntP44wokCEP3ADn7sMM8kUTbmcNo84U87"
    }
}
```

### platform.addDefaultSubnetValidator

Add a validator to the Default Subnet.

#### Signature

```go
platform.addDefaultSubnetValidator(
    {
        id: string,
        startTime: int,
        endTime: int,
        stakeAmount: int,
        payerNonce: int,
        destination: string,
        delegationFeeRate: int
    }
) -> {unsignedTx: string}
```

* `id` is the node ID of the validator.
* `startTime` is the Unix time when the validator starts validating the Default Subnet.
* `endTime` is the Unix time when the validator stops validating the Default Subnet (and staked AVAX is returned).
* `stakeAmount` is the amount of nAVAX the validator is staking.
* `payerNonce` is the next unused nonce of the account that is providing the staked AVAX and paying the transaction fee.
* `destination` is the address of the account that the staked AVAX will be returned to, as well as a validation reward if the validator is sufficiently responsive and correct while it validated.
* `delegationFeeRate` is the percent fee this validator charges when others delegate stake to them, multiplied by 10,000.
  For example, suppose a validator has `delegationFeeRate` 300,000 and someone delegates to that validator.
  When the delegation period is over, if the delegator is entitled to a reward, 30% of the reward (300,000 / 10,000) goes to the validator and 70% goes to the delegator.
* `unsignedTx` is the the unsigned transaction.
  It must be signed (using `sign`) by the key of the account providing the staked AVAX/paying the transaction fee before it can be issued.

#### Example Call

In this example we use shell command `date` to compute Unix times 10 minutes and 30 days in the future.
(Note: If you're on a Mac, replace  `$(date` with `$(gdate`. If you don't have `gdate` installed, do `brew install coreutils`.)

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.addDefaultSubnetValidator",
    "params": {
        "id":"ARCLrphAHZ28xZEBfUL7SVAmzkTZNe1LK",
        "payerNonce":1,
        "destination":"Q4MzFZZDPHRPAHFeDs3NiyyaZDvxHKivf",
        "startTime":'$(date --date="10 minutes" +%s)',
        "endTime":'$(date --date="2 days" +%s)',
        "stakeAmount":1000000,
        "delegationFeeRate":100000
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

#### Example Response

```json
{
    "jsonrpc":"2.0",
    "id"     :1,
    "result" :{
        "unsignedTx": "1115K3jV5Yxr145wi6kEYpN1nPz3GEBkzG8mpF2s2959VsR54YGenLJrgdg3UEE7vFPNDE5n3Cq9Vs71HEjUUoVSyrt9Z3X7M5sKLCX5WScTcQocxjnXfFowZxFe4uH8iJU7jnCZgeKK5bWsfnWy2b9PbCQMN2uNLvwyKRp4ZxcgRptkuXRMCKHfhbHVKBYmr5e2VbBBht19be57uFUP5yVdMxKnxecs"
    }
}
```

### platform.addNonDefaultSubnetValidator

Add a validator to a Subnet other than the Default Subnet.
The validator must validate the Default Subnet for the entire duration they validate this Subnet.

#### Signature

```go
platform.addNonDefaultSubnetValidator(
    {
        id: string,
        subnetID: string,
        startTime: int,
        endTime: int,
        weight: int,
        payerNonce: int
    }
) -> {unsignedTx: string}
```

* `id` is the node ID of the validator.
* `subnetID` is the Subnet they will validate.
* `startTime` is the Unix time when the validator starts validating the Subnet.
* `endTime` is the Unix time when the validator stops validating the Subnet.
* `weight` is the validator's weight used for sampling.
* `payerNonce` is the next unused nonce of the account that will pay the transaction fee for this transaction.
* `unsignedTx` is the unsigned transaction.
  It must be signed (using `sign`) by the proper number of the Subnet's control keys and by the key of the account paying the transaction fee before it can be issued.

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.addNonDefaultSubnetValidator",
    "params": {
        "id":"7Xhw2mDxuDS44j42TCB6U5579esbSt3Lg",
        "subnetID":"zBfoWW1FfkPVRfywpJ1CVQRfnYesEpdFC61hmU2n9JNGhDUEL",
        "startTime":1583524047,
        "endTime":1604102399,
        "weight":1,
        "payerNonce":2
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

#### Example Response

```json
{
    "jsonrpc":"2.0",
    "id"     :1,
    "result" :{
        "unsignedTx": "1115K3jV5Yxr145wi6kEYpN1nPz3GEBkzG8mpF2s2959VsR54YGenLJrgdg3UEE7vFPNDE5n3Cq9Vs71HEjUUoVSyrt9Z3X7M5sKLCX5WScTcQocxjnXfFowZxFe4uH8iJU7jnCZgeKK5bWsfnWy2b9PbCQMN2uNLvwyKRp4ZxcgRptkuXRMCKHfhbHVKBYmr5e2VbBBht19be57uFUP5yVdMxKnxecs"
    }
}
```


### platform.createAccount

The P-Chain uses an account model.
This method creates an account.

#### Signature

```go
platform.createAccount(
    {
        username: string,
        password: string,
        privateKey: string (optional)
    }
) -> {address: string}
```

* `username` is the user that controls the new account.
* `password` is user's password.
* `privateKey` is the private key that controls the account.
  If omitted, a new private key is generated.
* `address` is the address of the newly created account

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.createAccount",
    "params": {
        "username":"bob",
        "password":"loblaw",
        "privateKey":"24jUJ9vZexUM6expyMcT48LBx27k1m7xpraoV62oSQAHdziao5"
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

#### Example Response

```json
{
    "jsonrpc": "2.0",
    "result": {
        "address": "Q4MzFZZDPHRPAHFeDs3NiyyaZDvxHKivf"
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
        payerNonce: int,
        genesisData: string
    }
) -> {unsignedTx: string}
```

* `subnetID` is the ID of the Subnet that validates the new blockchain.
  The Subnet must exist and can't be the Default Subnet.
* `vmID` is the ID of the Virtual Machine the blockchain runs.
  Can also be an alias of the Virtual Machine.
* `name` is a human-readable name for the new blockchain. Not necessarily unique.
* `payerNonce` is the next unused nonce of the account paying the transaction fee.
* `genesisData` is the base 58 (with checksum) representation of the genesis state of the new blockchain.
  Virtual Machines should have a static API method named `buildGenesis` that can be used to generate `genesisData`.
* `unsignedTx` is the unsigned transaction to create this blockchain.
  Must be signed by a sufficient number of the Subnet's control keys and by the account paying
  the transaction fee.

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
        "payerNonce" : 6
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

#### Example Response

```json
{
    "jsonrpc": "2.0",
    "result": {
        "unsignedTx": "111498J8u7uGkNzTKn2r7QUDPC1gq3Hb9XvAVNYHBK8AG2NXVMqo54SyiVAGFm1Ax5vGZgmxbuAMRS1TfsemkVDwK5N2Y5NzgU3pkT2WG9vJgg1N4m6gmDQp3WrKTa94eFWF4kwnjgAa8dLPBvFViCRY5FBtVAj3bXxMVPxYCn1THakh4dVmnHycQsdB3Hds3GHxQmYSXW712qHEvt2p4pd2Rk2grqAgvXLSgha1X3iovaeRM93KQiasYx8VTynPNwMmEo4NPs4x6GgEiSbGdxg9wRTcByG"
    },
    "id": 1
}
```

### platform.createSubnet

Create an unsigned transaction to create a new Subnet.

The unsigned transaction must be signed with the key of the account
paying the transaction fee.

The Subnet's ID is the ID of the transaction that creates it
(ie the response from `issueTx` when issuing the signed transaction.)

#### Signature

```go
platform.createSubnet(
    {
        controlKeys: []string,
        threshold: int,
        payerNonce: int
    }
) -> {unsignedTx: string}
```

* To add a validator to this Subnet, a transaction must have `threshold` signatures,
  where each signature is from a key whose address is an element of `controlKeys`.
* `payerNonce` is the next unused nonce of the account providing the transaction fee.

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.createSubnet",
    "params": {
        "controlKeys":[
            "98vMGrh2nWNr8oDNKVK9jdxN1bwkeg4Jd",
            "6UGRmWANxejv1uM5T8BiRR2VPFSk1aFWA"
        ],
        "threshold":2,
        "payerNonce":1
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

#### Example Response

```json
{
    "jsonrpc": "2.0",
    "result": {
        "unsignedTx": "1112LA7e8GvkGHDkxZa9Q7kszqvWHooumX5PhqA9NJG7erwXYcwQUPRQyukYX1ncu1DmWvvPNMuivUqvGp1t9M3wys5joqXrXtV2jescQ5AWaUKHiSBUWBRHseMLhGxWNT4Bv6LNVvaaA1ZW33avQBAzz7V84KpKGW7fD3Fz1okxknLgoG"
    },
    "id": 1
}
```

### platform.getAccount

The P-Chain uses an account model. An account is identified by an address.
This method returns the account with the given address.

#### Signature

```go
platform.getAccount({address: string}) ->
{
    address: string,
    nonce: int,
    balance: int
}
```

* `address` is the account's address.
* `nonce` is the account's most recently used nonce.
* `balance` is the account's balance in nAVAX.

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"platform.getAccount",
    "params" :{
        "address": "NcbCRXGMpHxukVmT8sirZcDnCLh1ykWp4"
    }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

#### Example Response

```json
{
    "jsonrpc": "2.0",
    "result": {
        "address": "NcbCRXGMpHxukVmT8sirZcDnCLh1ykWp4",
        "nonce": "0",
        "balance": "0"
    },
    "id": 1
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
        subnetID: string,
        vmID: string
    }
}
```

* `blockchains` is all of the blockchains that exists on the Avalanche network.
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
        id: string
    }
}
```

* `subnetID` is the subnet whose current validators are returned. If omitted, returns the current validators of the Default Subnet.
* `startTime` is the Unix time when the validator starts validating the Subnet.
* `endTime` is the Unix time when the validator stops validating the Subnet.
* `weight` is the validator's weight when sampling validators.
  Omitted if `subnetID` is the default subnet.
* `stakeAmount` is the amount of nAVAX this validator staked.
  Omitted if `subnetID` is not the default subnet.
* `address` is the P Chain address which was passed in as `destination` when adding the validator.
* `id` is the validator's ID.

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
                "address": "3dAxnVDDZpTZTAUbCboMKsGdi2X1oXbuJ",
                "id": "NDmcZNsWoPrkN9KSt2A9js639hEQWUmUf"
            },
            {
                "startTime": "1591473391",
                "endtime": "1592855191",
                "stakeAmount": "10000",
                "address": "EDCFiDfrqPnGk5PKR7BFdE132CwDmAHRX",
                "id": "62T5AAwKdFMNi7Gm193A6zyJhVscRfuhP"
            },
            {
                "startTime": "1591387125",
                "endtime": "1622923025",
                "stakeAmount": "20000000000000",
                "address": "95YUFjhDG892VePMzpwKF9JzewGKvGRi3",
                "id": "HGZ8ae74J3odT8ESreAdCtdnvWG1J4X5n"
            }
        ]
    },
    "id": 1
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
        address: string
        id: string
    }
}
```

* `subnetID` is the subnet whose current validators are returned. If omitted, returns the current validators of the Default Subnet.
* `startTime` is the Unix time when the validator starts validating the Subnet.
* `endTime` is the Unix time when the validator stops validating the Subnet.
* `weight` is the validator's weight when sampling validators.
  Omitted if `subnetID` is the default subnet.
* `stakeAmount` is the amount of nAVAX this validator staked.
  Omitted if `subnetID` is not the default subnet.
* `address` is the P Chain address which was passed in as `destination` when adding the validator.
* `id` is the validator's ID.

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
                "address": "6cesTteH62Y5mLoDBUASaBvCXuL2AthL",
                "id": "DpL8PTsrjtLzv5J8LL3D2A6YcnCTqrNH9"
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
platform.getSubnets({}) ->
{
    subnets: []{
            id: string,
            controlKeys: []string,
            threshold: string
    }
}
```

`id` is the Subnet's ID.  
`threshold` signatures from addresses in `controlKeys` are needed to add a validator to the subnet.  
See [here](../tutorials/adding-validators.md#add-a-validator-to-a-non-default-subnet) for information on adding a validator to a Subnet.

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.getSubnets",
    "params": {},
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
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

### platform.exportAVAX

Send AVAX from an account on the P-Chain to an address on the X-Chain.  
This transaction must be signed with the key of the account that
the AVAX is sent from and which pays the transaction fee.  
After issuing this transaction, you must call the X-Chain's [`importAVAX`](./avm.md#avmimportavax) method to complete the transfer.

#### Signature

```go
platform.exportAVAX(
    {
        amount: int,
        to: string,
        payerNonce: int,
    }
) -> {unsigndTx: string}
```

* `amount` is the amount of nAVAX to send.
* `to` is the address on the X-Chain to send the AVAX to. Do not include `X-` in the address.
* `payerNonce` is the next unused nonce of the account paying the tx fee and providing the sent AVAX.

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.exportAVAX",
    "params": {
        "to":"G5ZGXEfoWYNFZH5JF9C4QPKAbPTKwRbyB",
        "amount":1,
        "payerNonce":2
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

#### Example Response

```json
{
    "jsonrpc": "2.0",
    "result": {
        "unsignedTx": "1112Y8Y5ibRqMDtby9NSdpK9u3n1yGywybAAVYnhCkFYcRzEYbR7J5Ci6SX98PmgS2LpRf5pcu6YAgLYGiTuQpiSucRcX4dv7HbVnEsrQnjcieGbgkf9PFS126hC8xce4pEZUzr9jReVdfXe3g9BSUsXLj2XcWrnD6iTgHpiC18jjyjg1wjm1Vs4TcXhG472MRvGspucJ8LuUE91WV7353Kxdc2e7Trw2Sd6iV"
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

* `username` must control `address`.
* `privateKey` is the string representation of the private key that controls `address`.

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"platform.exportKey",
    "params" :{
        "username" :"bob",
        "password":"loblaw",
        "address": "7u5FQArVaMSgGZzeTE9ckheWtDhU5T3KS"
    }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
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

### platform.importAVAX

(Note: This method will change to `importAVAX` in the next release.)

Complete a transfer of AVAX from the X-Chain to the P-Chain.

Before this method is called, you must call the X-Chain's [`exportAVAX`](./avm.md#avmexportavax) method to initiate the transfer.

#### Signature

```go
platform.importAVAX(
    {
        to: string,
        payerNonce: int,
        username: string,
        password: string
    }
) -> {tx: string}
```

* `to` is the ID of the account the AVAX is sent to.
  This must be the same as the `to` argument in the corresponding call to the X-Chain's `exportAVAX`.
* `payerNonce` is the next unused nonce of the account specified in `to`.
* `username` is the user that controls the account specified in `to`.
* `tx` is the transaction, which should be sent to the network by calling `issueTx`.

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.importAVAX",
    "params": {
        "username":"bob",
        "password":"loblaw",
        "to":"Bg6e45gxCUTLXcfUuoy3go2U6V3bRZ5jH",
        "payerNonce":1
    },
    "id": 1
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

#### Example Response

```json
{
    "jsonrpc": "2.0",
    "result": {
        "tx": "1117xBwcr5fo1Ch4umyzjYgnuoFhSwBHdMCam2wRe8SxcJJvQRKSmufXM8aSqKaDmX4TjvzPaUbSn33TAQsbZDhzcHEGviuthncY5VQfUJogyMoFGXUtu3M8NbwNhrYtmSRkFdmN4w933janKvJYKNnsDMvMkmasxrFj8fQxE6Ej8eyU2Jqj2gnTxU2WD3NusFNKmPfgJs8DRCWgYyJVodnGvT43hovggVaWHHD8yYi9WJ64pLCvtCcEYkQeEeA5NE8eTxPtWJrwSMTciHHVdHMpxdVAY6Ptr2rMcYSacr8TZzw59XJfbQT4R6DCsHYQAPJAUfDNeX2JuiBk9xonfKmGcJcGXwdJZ3QrvHHHfHCeuxqS13AfU"
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
        "privateKey":"2w4XiXxPfQK4TypYqnohRL8DRNTz9cGiGmwQ1zmgEqD9c9KWLq"
    }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

#### Example Response

```json
{
    "jsonrpc":"2.0",
    "id"     :1,
    "result" :{
        "address":"7u5FQArVaMSgGZzeTE9ckheWtDhU5T3KS"
    }
}
```

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

### platform.listAccounts

List the accounts controlled by the specified user.

#### Signature

```go
platform.listAccounts(
    {
        username: string,
        password: string
    }
) ->
{
    accounts: []{
        address: string,
        nonce: int,
        balance: int
    }
}
```

* `address` is the account's address.
* `nonce` is the account's most recently used nonce.
* `balance` is the account's balance in nAVAX.

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"platform.listAccounts",
    "params" :{
        "username": "bob",
        "password": "loblaw"
    }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/P
```

#### Example Response

```json
{
    "jsonrpc": "2.0",
    "result": {
        "accounts": [
            {
                "address": "Q4MzFZZDPHRPAHFeDs3NiyyaZDvxHKivf",
                "nonce": "0",
                "balance": "0"
            },
            {
                "address": "NcbCRXGMpHxukVmT8sirZcDnCLh1ykWp4",
                "nonce": "0",
                "balance": "0"
            }
        ]
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
  If omitted, defaults to the Default Subnet.
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
            "MFrZFVCXPv5iCn6M9K6XduxGTYp891xXZ",
            "NFBbbJ4qCmNaCzeW7sxErhvWqvEQMnYcN"
        ]
    }
}
```


### platform.sign

Sign an unsigned or partially signed transaction.

Transactions to add non-default Subnets require signatures from control keys and from the account paying the transaction fee. If `signer` is a control key and the transaction needs more signatures from control keys, `sign` will provide a control signature. Otherwise, `signer` will sign to pay the transaction fee.

#### Signature

```go
platform.sign(
    {
        tx: string,
        signer: string,
        username: string,
        password: string
    }
) -> {tx: string}
```

* Argument `tx` is the unsigned/partially signed transaction.
* `signer` is the address of the key signing `tx`.
* `username` is the user that controls the key signing `tx`.
* `password` is `username`'s password.
* Response `tx` is the transaction after being signed.

#### Example Call

```json
curl -X POST --data '{
    "jsonrpc": "2.0",
    "method": "platform.sign",
    "params": {
        "tx":"111Bit5JNASbJyTLrd2kWkYRoc96swEWoWdmEhuGAFK3rCAyTnTzomuFwgx1SCUdUE71KbtXPnqj93KGr3CeftpPN37kVyqBaAQ5xaDjr7wU8riGS89NDJ8AwVgZgnFkgF3uMfwCiCuPvvubGyQxNHE4TM9iDgj6h3URdGQ4JntP44wokCEP3ADn7sMM8kUTbmcNo84U87",
        "signer":"6Y3kysjF9jnHnYkdS9yGAuoHyae2eNmeV",
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
        "Tx": "111Bit5JNASbJyTLrd2kWkYRoc96swEWoWdmEhuGAFK3rCAyTnTzomuFwgx1SCUdUE71KbtXPnqj93KGr3CeftpPN37kVyqBaAQ5xaDjr7wVBTUYi9iV7kYJnHF61yovViJF74mJJy7WWQKeRMDRTiPuii5gsd11gtNahCCsKbm9seJtk2h1wAPZn9M1eL84CGVPnLUiLP"
    },
    "id": 1
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
