# Create a Local Test Network

In the quickstart tutorial we connect a node to the test network.
You might find it useful to create a local test network.

We'll show you how to launch a 5 node local test network with staking enabled and with staking disabled.
For both we'll show how to launch the network using [Avash](../tools/avash.md) and manually. 

The 5 nodes will have HTTP ports (where API calls should be sent) `9650`, `9652`, `9654`, `9656` and `9658`.

## Create a Local Test Network with Staking Disabled

Let's launch a network with staking disabled (every node validates every blockchain.)

### Manually

To start the network:

```sh
cd $GOPATH/src/github.com/ava-labs/gecko
./scripts/build.sh
./build/avalanche --public-ip=127.0.0.1 --http-port=9650 --staking-port=9651 --db-dir=db/node1 --staking-tls-enabled=false --snow-sample-size=2 --snow-quorum-size=2 --network-id=local --staking-tls-cert-file=$(pwd)/staking/local/staker1.crt --staking-tls-key-file=$(pwd)/staking/local/staker1.key

./build/avalanche --public-ip=127.0.0.1 --http-port=9652 --staking-port=9653 --db-dir=db/node2 --staking-tls-enabled=false --snow-sample-size=2 --snow-quorum-size=2 --network-id=local --bootstrap-ips=127.0.0.1:9651 --bootstrap-ids=7Xhw2mDxuDS44j42TCB6U5579esbSt3Lg --staking-tls-cert-file=$(pwd)/staking/local/staker2.crt --staking-tls-key-file=$(pwd)/staking/local/staker2.key

./build/avalanche --public-ip=127.0.0.1 --http-port=9654 --staking-port=9655 --db-dir=db/node3 --staking-tls-enabled=false --snow-sample-size=2 --snow-quorum-size=2 --network-id=local --bootstrap-ips=127.0.0.1:9651 --bootstrap-ids=7Xhw2mDxuDS44j42TCB6U5579esbSt3Lg --staking-tls-cert-file=$(pwd)/staking/local/staker3.crt --staking-tls-key-file=$(pwd)/staking/local/staker3.key

./build/avalanche --public-ip=127.0.0.1 --http-port=9656 --staking-port=9657 --db-dir=db/node4 --staking-tls-enabled=false --snow-sample-size=2 --snow-quorum-size=2 --network-id=local --bootstrap-ips=127.0.0.1:9651 --bootstrap-ids=7Xhw2mDxuDS44j42TCB6U5579esbSt3Lg --staking-tls-cert-file=$(pwd)/staking/local/staker4.crt --staking-tls-key-file=$(pwd)/staking/local/staker4.key

./build/avalanche --public-ip=127.0.0.1 --http-port=9658 --staking-port=9659 --db-dir=db/node5 --staking-tls-enabled=false --snow-sample-size=2 --snow-quorum-size=2 --network-id=local --bootstrap-ips=127.0.0.1:9651 --bootstrap-ids=7Xhw2mDxuDS44j42TCB6U5579esbSt3Lg --staking-tls-cert-file=$(pwd)/staking/local/staker5.crt --staking-tls-key-file=$(pwd)/staking/local/staker5.key

```

### With Avash

We assume you've installed [Avash](../tools/avash.md).

To open Avash:

```sh
cd $GOPATH/src/github.com/ava-labs/avash
go build
./avash
```

Now we're in Avash.
To start the nodes:

```sh
runscript scripts/five_node_network.lua
```

When you want to tear down the network, run `exit` to exit Avash.

## Create a Local Test Network with Staking Enabled

Let's launch a network with staking enabled.
Each of the 5 nodes we launch is a validator of the Default Subnet.

### Manually

To start the network:

```sh
cd $GOPATH/src/github.com/ava-labs/gecko
./scripts/build.sh
./build/avalanche --public-ip=127.0.0.1 --snow-sample-size=2 --snow-quorum-size=2 --http-port=9650 --staking-port=9651 --db-dir=db/node1 --staking-tls-enabled=true --network-id=local --bootstrap-ips= --staking-tls-cert-file=$(pwd)/staking/local/staker1.crt --staking-tls-key-file=$(pwd)/staking/local/staker1.key
./build/avalanche --public-ip=127.0.0.1 --snow-sample-size=2 --snow-quorum-size=2 --http-port=9652 --staking-port=9653 --db-dir=db/node2 --staking-tls-enabled=true --network-id=local --bootstrap-ips=127.0.0.1:9651 --bootstrap-ids=7Xhw2mDxuDS44j42TCB6U5579esbSt3Lg --staking-tls-cert-file=$(pwd)/staking/local/staker2.crt --staking-tls-key-file=$(pwd)/staking/local/staker2.key
./build/avalanche --public-ip=127.0.0.1 --snow-sample-size=2 --snow-quorum-size=2 --http-port=9654 --staking-port=9655 --db-dir=db/node3 --staking-tls-enabled=true --network-id=local --bootstrap-ips=127.0.0.1:9651 --bootstrap-ids=7Xhw2mDxuDS44j42TCB6U5579esbSt3Lg --staking-tls-cert-file=$(pwd)/staking/local/staker3.crt --staking-tls-key-file=$(pwd)/staking/local/staker3.key
./build/avalanche --public-ip=127.0.0.1 --snow-sample-size=2 --snow-quorum-size=2 --http-port=9656 --staking-port=9657 --db-dir=db/node4 --staking-tls-enabled=true --network-id=local --bootstrap-ips=127.0.0.1:9651 --bootstrap-ids=7Xhw2mDxuDS44j42TCB6U5579esbSt3Lg --staking-tls-cert-file=$(pwd)/staking/local/staker4.crt --staking-tls-key-file=$(pwd)/staking/local/staker4.key
./build/avalanche --public-ip=127.0.0.1 --snow-sample-size=2 --snow-quorum-size=2 --http-port=9658 --staking-port=9659 --db-dir=db/node5 --staking-tls-enabled=true --network-id=local --bootstrap-ips=127.0.0.1:9651 --bootstrap-ids=7Xhw2mDxuDS44j42TCB6U5579esbSt3Lg --staking-tls-cert-file=$(pwd)/staking/local/staker5.crt --staking-tls-key-file=$(pwd)/staking/local/staker5.key
```

### With Avash

We assume you've installed [Avash](../tools/avash.md).

To open Avash:

```sh
cd $GOPATH/src/github.com/ava-labs/avash
go build
./avash
```

Now we're in Avash.
To start the network:

```sh
runscript scripts/five_node_staking.lua
```

When you want to tear down the network, run `exit` to exit Avash.

## Verifying Nodes are Connected

We can look at one of the node's peers to ensure that the nodes are connected.
To do so, call [`info.peers`.](../api/info.md#info-peers)

```json
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"info.peers"
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/info
```

`peers` should have 4 entries:

```json
{
   "jsonrpc":"2.0",
   "result":{
      "peers":[
         {
            "ip":"127.0.0.1:9158",
            "publicIP":"127.0.0.1:9158",
            "id":"NwEmCRVweJs9vTin7LpnweWSKVP4AB9Qi",
            "version":"avalanche/0.5.0",
            "lastSent":"2020-06-01T19:41:08Z",
            "lastReceived":"2020-06-01T19:41:08Z"
         },
         {
            "ip":"127.0.0.1:9156",
            "publicIP":"127.0.0.1:9156",
            "id":"6f3yBqjAJYV3tpBHLJKYruY3dPHAzKFEE",
            "version":"avalanche/0.5.0",
            "lastSent":"2020-06-01T19:41:08Z",
            "lastReceived":"2020-06-01T19:41:08Z"
         },
         {
            "ip":"127.0.0.1:9155",
            "publicIP":"127.0.0.1:9155",
            "id":"KxLwPp9MYV26CoP8ixTXggWvEgVaa9iPN",
            "version":"avalanche/0.5.0",
            "lastSent":"2020-06-01T19:41:08Z",
            "lastReceived":"2020-06-01T19:41:08Z"
         },
         {
            "ip":"127.0.0.1:9157",
            "publicIP":"127.0.0.1:9157",
            "id":"CkcATAFTDK4HHNWycEWfCz5wEMCsssZSt",
            "version":"avalanche/0.5.0",
            "lastSent":"2020-06-01T19:41:08Z",
            "lastReceived":"2020-06-01T19:41:08Z"
         }
      ]
   },
   "id":1
}
```

## Next steps

That's it! Your local Avalanche network is up and running.
It has the default blockchains: the X-Chain, C-Chain and P-Chain.
The only Subnet that exists is the Default Subnet.

You can add more nodes to the network.
Just remember to give unique values for `db-dir`, `http-port` and `staking-port`.