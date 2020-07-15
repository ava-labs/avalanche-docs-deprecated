# Command Line Interface

When running a node, there are a variety of possible configurations that are supported.

## Arguments

`--api-admin-enabled` (bool):

If set to false, this node will not expose the Admin API. Defaults to `false`.

`--api-ipcs-enabled` (bool):

If set to true, this node will expose the IPCs API. Defaults to `false`.

`--api-keystore-enabled` (bool):

If set to false, this node will not expose the Keystore API. Defaults to `true`.

`--api-metrics-enabled` (bool):

If set to false, this node will not expose the Metrics API. Defaults to `true`.

`--assertions-enabled` (bool):

When set to true, assertions will execute at runtime throughout the codebase. This is intended for use in debugging, as we may get a more specific error message. Defaults to `true`.

`--bootstrap-ids` (string):

Bootstrap IDs is an array of validator IDs. These IDs will be used to authenticate bootstrapping peers. This only needs to be set when `--p2p-tls-enabled=true`. An example setting of this field would be `--bootstrap-ids="7Xhw2mDxuDS44j42TCB6U5579esbSt3Lg,MFrZFVCXPv5iCn6M9K6XduxGTYp891xXZ"`. The default value is the empty set.

`--bootstrap-ips` (string):

Bootstrap IPs is an array of IPv4:port pairs. These IP Addresses will be used to bootstrap the current Avalanche state. An example setting of this field would be `--bootstrap-ips="127.0.0.1:12345,1.2.3.4:5678"`. The default value is the empty set.

`--db-dir` (string, file path):

Specifies the directory to which the database is persisted. Defaults to `"$HOME/.gecko/db"`.

`--db-enabled` (bool):

If set to false, state updates are performed solely to an in-memory database, without making any changes on permanent storage.
When set to true, state updates are written to a local persistent database. Defaults to `true`.

`--http-host` (string):

The address that HTTP APIs listen on. The default value is `127.0.0.1`.
This means that by default, your node can only handle API calls made from the same machine.
To allow API calls from other machines, do `--http-host=[PUBLIC IP OF MACHINE RUNNING NODE]`.

`--http-port` (int):

Each node runs an HTTP server that provides the APIs for interacting with the node and the Avalanche network.
This argument specifies the port that the http server will listen on. The default value is `9650`.

`--http-tls-cert-file` (string, file path):

This argument specifies the location of the TLS certificate used by the node for the HTTPS server. This must be specified when `--http-tls-enabled=true`. There is no default value.

`--http-tls-enabled` (bool):

If set to true, this flag will attempt to upgrade the server to use HTTPS. Defaults to `false`.

`--http-tls-key-file` (string, file path):

This argument specifies the location of the TLS private key used by the node for the HTTPS server. This must be specified when `--http-tls-enabled=true`. There is no default value.

`--log-level` (string, `{Off, Fatal, Error, Warn, Info, Debug, Verbo}`):

The log level determines which events to log. There are 7 different levels, in order from highest priority to lowest.

* `Off`: No logs have this level of logging.
* `Fatal`: Fatal errors that are not recoverable.
* `Error`: Errors that the node encounters, these errors were able to be recovered.
* `Warn`: A Warning that might be indicative of a spurious byzantine node, or potential future error.
* `Info`: Useful descriptions of node status updates.
* `Debug`: Debug logging is useful when attempting to understand possible bugs in the code. More information that would be typically desired for normal usage will be displayed.
* `Verbo`: Tracks extensive amounts of information the node is processing. This includes message contents and binary dumps of data for extremely low level protocol analysis.

When specifying a log level note that all logs with the specified priority or higher will be tracked. Defaults to `Info`.

`--log-display-level` (string, `{Off, Fatal, Error, Warn, Info, Debug, Verbo}`):

The log level determines which events to display to the screen. If left blank, will default to the value provided to `--log-level`.

`--log-dir` (string, file path):

Specifies the directory in which system logs are kept. Defaults to `"$HOME/.gecko/logs"`.

`--network-id` (string):

The identity of the network the node should connect to. Can be one of:

* `--network-id=denali` -> Connect to the Denali test-network. This aliases `network-3`.
* `--network-id=testnet` -> Connect to the current test-network. (Right now, this is Denali.)
* `--network-id=local` -> Connect to a local test-network. This aliases `network-12345`.
* `--network-id=network-{id}` -> Connect to the `id` network. `id` must be in the range `[0, 2^32)`.

`--network-id` defaults to `denali`.

`--public-ip` (string):

Validators must know their public facing IP addresses so they can let other nodes know how to connect to them.
If this argument is not provided, the node will attempt to perform NAT traversal to get the node's public IP. Should be set to `127.0.0.1` to create a local network. The default value is `""`.

`--signature-verification-enabled` (bool):

Enables signature verification to be disabled for testing. When set to false, signatures won't be checked in VMs that allow signatures to be disabled. Defaults to `true`.

`--staking-port` (string):

The port through which the staking server will connect to the Avalanche network. Defaults to `9651`.

`--p2p-tls-enabled` (boolean):

Avalanche uses two-way authenticated TLS connections to securely identify the `stakingID` of connected peers. However, This can be disabled for testing. When TLS is disabled, the `stakingID` will be derived from the IP Address the node claims it owns. This will also disable encryption of inter-node communication. This should only be specified for testing. Defaults to `true`. This must be true when `--staking-tls-enabled=true`.

`--staking-tls-enabled` (boolean):

Avalanche uses Proof of Stake (PoS) as Sybil resistance to make it prohibitively expensive to attack the network. When this is true, `--p2p-tls-enabled` must be set to true in order to secure P2P communications.

`--staking-tls-cert-file` (string, file path):

Avalanche uses two-way authenticated TLS connections to securely identify the `stakingID` of connected peers when `--p2p-tls-enabled=true`. This argument specifies the location of the TLS certificate used by the node. This must be specified when `--p2p-tls-enabled=true`. The default value is `""`.

`--staking-tls-key-file` (string, file path):

Avalanche uses two-way authenticated TLS connections to securely identify the `stakingID` of connected peers when `--p2p-tls-enabled=true`. This argument specifies the location of the TLS private key used by the node. This must be specified when `--p2p-tls-enabled=true`. The default value is `""`.

***

## Advanced Options

The following options affect the correctness of the platform. They may need to be changed network-wide, and as a result, an ordinary user should rarely change from the defaults.

`--avax-tx-fee` (int):

The required amount of nAVAX to be burned for a transaction to be valid. This parameter requires network agreement in its current form. Changing this value from the default should only be done on private networks. Defaults to `0` nAVAX per transaction.

`--snow-avalanche-batch-size` (int):

DAG implementations of Snow consensus define `b` as the number of transactions a vertex should include. Increasing `b` will, theoretically, increase throughput while increasing latency. The node will wait for at most 1 second to collect a batch, and will then issue the entire batch at once. The value must be at least `1`. The default value is `30`.

`--snow-avalanche-num-parents` (int):

DAG implementations of Snow consensus define `p` as the number of parents a vertex should include. Increasing `p` will improve the amortization of network queries. However, by increasing the connectivity of the graph, the complexity of the graph traversals is increased. The value must be at least `2`. The default value is `5`.

`--snow-concurrent-repolls` (int):

Snow consensus requires repolling transactions that are issued during low time of network usage. This parameter lets one define how aggressive the client will be in finalizing these pending transactions. This should only be changed after careful consideration of the tradeoffs of Snow consensus. The value must be at least `1` and at most `--snow-rogue-commit-threshold`. The default value is `1`.

`--snow-sample-size` (int):

Snow consensus defines `k` as the number of validators that are sampled during each network poll. This parameter lets one define the `k` value used for consensus. This should only be changed after careful consideration of the tradeoffs of Snow consensus. The value must be at least `1`. The default value is `20`.

`--snow-quorum-size` (int):

Snow consensus defines `alpha` as the number of validators that must prefer a transaction during each network poll to increase the confidence in the transaction. This parameter lets us define the `alpha` value used for consensus. This should only be changed after careful consideration of the tradeoffs of Snow consensus. The value must be at greater than `k/2`. The default value is `18`.

`--snow-virtuous-commit-threshold` (int):

Snow consensus defines `beta1` as the number of consecutive polls that a virtuous transaction must increase its confidence for it to be accepted. This parameter lets us define the `beta1` value used for consensus. This should only be changed after careful consideration of the tradeoffs of Snow consensus. The value must be at least `1`. The default value is `20`.

`--snow-rogue-commit-threshold` (int):

Snow consensus defines `beta2` as the number of consecutive polls that a rogue transaction must increase its confidence for it to be accepted. This parameter lets us define the `beta2` value used for consensus. This should only be changed after careful consideration of the tradeoffs of Snow consensus. The value must be at least `beta1`. The default value is `30`.

`--xput-server-enabled` [Deprecated] (boolean):

An optional server helps run throughput tests by injecting load into the network on command.
If enabled, this server is started up and listens for commands from a test coordinator.
The default value is `false`.

`--xput-server-port` [Deprecated] (string):

This option lets one specify on which port the throughput server, if enabled, will listen. The default value is `9652`.
