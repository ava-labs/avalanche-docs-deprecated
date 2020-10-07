# Staking

This document explains staking on the Avalanche network.
See the [quickstart guide](quickstart.md) for a step-by-step guide to staking.

## Validators

The security of the Avalanche Network is secured by a group of computers called **validators**.
Validators create new blocks/vertices and process transactions.
As part of Avalanche consensus, validators repeatedly sample each other.

The probability that a given validator is sampled is proportional to its **stake**.
A stake is a bond, in AVAX tokens, put forward by a node to become a validator.

When you add a node to the validator set you specify:

* Your node's ID
* When you want to start and stop validating
* How many AVAX you are staking
* The address to send any rewards to
* Your delegation fee rate (see below)

Note that once you issue the transaction to add a node as a validator, there is no way to change the parameters.
**You can't unstake early or change the stake amount, node ID or reward address.**
Please make sure you're using the correct values in the API calls below.
If you're not sure, ask for help on [Discord.](https://chat.avalabs.org)

## Running a validator

If you're running a validator, it's important that you follow some best practices to ensure that you receive a reward and keep your funds safe.

### Networking

Your node must be able to receive and send traffic from all addresses on the P2P port (`9651` by default.)

AvalancheGo attempts NAT traversal on startup to ensure that it can send and receive traffic on the P2P port. 
If your node is behind a router (e.g. in your home) your node can receive and send traffic properly without any action on your part thanks to NAT traversal.
However, you may want to also set up port forwarding on your router to ensure your node is well-connected if NAT traversal fails.
If your node is on a cloud service, make sure you've configured the security settings to allow incoming and outgoing traffic on the P2P port.

If your node is a validator, start your node with command line argument `--public-ip=[YOUR NODE'S PUBLIC IP HERE]` to ensure it is well connected.

If you want to make API calls to your node from remote machines, also allow traffic on the API port (`9650` by default.) 
If you do so, allow access to the smallest set of IP addresses possible.

### Secret Management

The only secret that you need on your validating node is its Staking Key, the TLS key that determines your node's ID.
The first time you start a node, the Staking Key is created and put in `$HOME/.avalanchego/staking/staker.key`.
You should back up this file (and `staker.crt`) somewhere secure.
Losing your Staking Key could jeopardize your validation reward, as your node will have a new ID.

You do not need to have AVAX funds on your validating node.
In fact, its best practice to **not** have a lot of funds on your node.
Almost all of your funds should be in "cold" addresses, whose private key is not on any computer.

### Monitoring

See [this tutorial](tutorials/node-monitoring.md) on setting up node monitoring.

## Validator rewards

Validators receive a reward, in AVAX, to incentivize them to secure the network.
A validator only receives a reward if they are sufficiently correct and responsive while it was validating. 
The size of the reward depends on how long they validate, how much they stake, and how many AVAX tokens exist.

## Timeline of fund movement for validators

When you issue the transaction to add a validator, the staked tokens and transaction fee are deducted from the addresses you control.
When you are done validating, the staked funds are returned to the addresses they came from.
If you earned a reward, it is sent to the address you specified when you added yourself as a validator.

## Delegators

You can stake your tokens to increase the sampling weight of another validator.
This is called delegation.

When you delegate stake to a validator you specify:

* The ID of the node you're delegating to
* When you want to start/stop delegating stake (must be while the validator is validating)
* How many AVAX you are staking
* The address to send any rewards to

## Delegator rewards

If the validator that you delegate stake to is sufficiently correct and responsive while you delegate stake to them, you receive a reward when you are done delegating to them.
Delegators are rewarded according to the same function as validators.
However, the validator that you delegate to keeps a portion of your reward.
The percentage of your reward that they keep is specified by the validator's delegation fee rate,
If it's set to 10%, then they keep 10% of any rewards from stake delegated to them.

## Timeline of fund movement for delegators

When you issue the transaction to delegate stake, the staked tokens and transaction fee are deducted from the addresses you control.
When you are done delegating stake, the staked funds are returned to the addresses they came from.
If you earned a reward, it is sent to the address you specified when you delegated stake.

## Staking parameters

* The minimum amount that a validator must stake is 2,000 AVAX
* The minimum amount that a delegator must stake is 25 AVAX
* The minimum amount of time one can stake funds for validation is 2 weeks
* The maximum amount of time one can stake funds for validation is 1 year
* The minimum amount of time one can stake funds for delegation is 2 weeks
* The maximum amount of time one can stake funds for delegation is 1 year
* The minimum delegation fee rate is 2%
* The maximum weight of a validator (their own stake + stake delegated to them) is the minimum of 3 x 10<sup>6</sup> AVAX and 5 times the amount the validator staked.
  For example, if you staked 2,000 AVAX to become a validator, only 8000 AVAX can be delegated to your node total (not per delegator)
* The minimum percentage of the time a validator must be correct and online to receive a reward is 60%
