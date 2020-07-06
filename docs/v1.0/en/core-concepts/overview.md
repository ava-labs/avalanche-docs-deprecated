# System Overview

## Introduction

This document describes the core concepts and architecture of the Avalanche network.

## What is a Blockchain?

A blockchain is a decentralized digital ledger. It's decentralized because there is no single
entity in charge of maintaining the ledger. Many parties, called **validators**, maintain their own
copy of the ledger. The validators use a **consensus protocol** to ensure they always agree on the
contents of the ledger.

A desirable property of blockchains is that validators agree on the contents of the ledger
even in the presence of byzantine (malicious) validators who do not follow the rules of
the consensus protocol.

## What is a Decentralized Application?

An application stores some information, or **state**. You can interact with the application by performing a **transaction**.
Transactions change the state of the application or, in other words, cause a **state transition**.
Applications also allows users to retrieve information about the state (query it) without modifying it.

A **decentralized application** (dApp) is one where there is no single authority that maintains the state and processes transactions.
This might all seem very abstract, so let's look at Bitcoin through the lens of decentralized applications.

Bitcoin is a decentralized application built atop a blockchain. The state of the application is a record of
who has how many Bitcoin. The state is stored on Bitcoin's blockchain. Remember, a blockchain is a ledger;
in this case, the entries in the ledger are something like "Alice sends Bob 1 Bitcoin" or "Jasmine pays Tosha 2 Bitcoin."
Each transaction causes a state transition by adding a new entry to the ledger.
Bitcoin is decentralized because many independent validators maintain the blockchain, which holds its state, and process transactions.

## A Brief History of Blockchains

In order to understand the value Avalanche provides, it's necessary to look at legacy blockchain technologies.

### Blockchain 1.0

Bitcoin demonstrated the value of blockchains and decentralization by creating a robust, decentralized payments system.
However, the Bitcoin network supports a small number of transactions per second, and Bitcoin's architecture makes 
it difficult to adapt its codebase for any use other than digital payments.
A number of other blockchain platforms duplicated the Bitcoin code base, with some small modifications, to issue their own coins.
Most of these copycat efforts provided zero additional value from both a technical and business perspective.
Bitcoin's main value proposition today is as a store of value and hedge against inflation.

### Blockchain 2.0

In 2014, Ethereum introduced the innovative idea of using a decentralized application (Ethereum) to launch and use 
new decentralized applications (smart contracts.) 
Before, it had been impossible to launch a blockchain-based decentralized application without creating
and launching one's own blockchain. 
Ethereum sparked a huge wave of new dApps, including DeFi (decentralized finance) applications.

### Blockchain 3.0 and Avalanche

Like Bitcoin and Ethereum, Avalanche introduces new paradigms to the blockchain world.

Unlike legacy blockchain networks, which have only one blockchain and one validator set, **Avalanche is a heterogeneous network of many blockchains and validator sets.**

Just as Ethereum allows one to launch a decentralized application defined by a smart contract, Avalanche allows one to launch a decentralized applications defined by a **Virtual Machine.**
Unlike Ethereum, each dApp runs on its own independent blockchain.
Each blockchain is validated by a **Subnet,** a dynamic, custom set of validators.
This allows for the creation of private blockchains.

Avalanche is not just a platform for creating custom dApps. It also has native support for creating and trading smart digital assets.
An asset can have a complex, custom ruleset that defines its behavior (eg "can't be traded until next year"), allowing users to get the functionality they want and to comply with regulations.

Avalanche is the first blockchain network to use **Avalanche**, a new family of consensus protocols
created by distributed systems researchers in 2018 that allow Avalanche to process thousands of transactions per second.
Avalanche permanently finalizes transactions in a few seconds, making Avalanche suitable for real-time payments.
Avalanche can be used to achieve consensus on not only linear blockchains but also on blockchains that are **Directed Acyclic Graphs (DAGs).**

Avalanche uses **Proof-of-Stake**, which allows tens of thousands of validators to have a first-hand say in the system while consuming minimal energy.

The following sections explain Avalanche's architecture, innovations and capabilities in greater detail.

## What are Virtual Machines

A **Virtual Machine** (VM) defines the application-level logic of a blockchain.
In technical terms, it defines a state machine.
It specifies the blockchain's state, state transition function, transactions and the API through which users can interact with the blockchain.

Every blockchain on the Avalanche network is an instance of a Virtual Machine.
(We sometimes say, equivalently, that a blockchain *runs* a Virtual Machine.)

When a developer writes a Virtual Machine they do not need to concern themself
with lower-level logic like networking, consensus and the structure of the blockchain.
Avalanche does all of that behind the scenes so that developers can focus on the thing they'd like to build.

Think of a Virtual Machine as a blueprint for a blockchain; one can use the same Virtual Machine to
create arbitrarily many blockchains, each of which follows the same ruleset but is logically independent from other blockchains.

### Why Virtual Machines

At first, blockchain networks had one Virtual Machine with a pre-defined, static set of functionality.
This rigid, monolithic design limited what blockchain-based applications one could run on such networks.

People who wanted custom decentralized applications had to create their own, entirely new blockchain network from scratch.
Doing so required a great deal of time and effort, offered limited security, and generally resulted in a bespoke, fragile blockchain that never got off the ground.

Ethereum made a step toward solving this problem with smart contracts.
Developers didn't need to worry about networking and consensus but creating decentralized applications was still hard.
The Ethereum Virtual Machine has low performance and imposes restrictions on smart contract developers.
Solidity and the other few languages for writing Ethereum smart contracts are unfamiliar to most programmers.

Avalanche Virtual Machines make it easy to define a blockchain-based decentralized application.
Rather than lightly-used, poorly-understood languages like Solidity, developers can write Virtual Machines in Go.
(Avalanche will support VM creation in other popular languages in the future.)

Virtual machines can contain almost any arbitrary logic and Avalanche imposes few restrictions on a VM's functionality.

### Creating Your Own Blockchain and Virtual Machine

Avalanche is a network of custom, independent blockchains, so naturally blockchain creation is a core feature of Avalanche.

Avalanche does not yet support creation of new Virtual Machines.
This means that presently, Avalanche only supports creation of new instances of the [AVM](../api/avm.md) or the [Timestamp VM.](../api/timestamp.md) That is, one can only create a new blockchain that runs the AVM or Timestamp VM. See [this tutorial](../tutorials/create-a-blockchain.md) to learn how to do so.

In the future Avalanche will allow users to define and launch custom blockchains, and we'll release SDKs to help developers do so. 

To get an idea of what a Virtual Machine implementation looks like, check out [this tutorial](../tutorials/creating-a-virtual-machine.md), which shows and explains all of the code in a simple Virtual Machine, the Timestamp VM.

## What are Subnets

A **Subnet**, or Subnetwork, is a dynamic set of validators working together to achieve consensus on the state of a set of blockchains.
Each blockchain is validated by exactly one Subnet.
A Subnet can validate arbitrarily many blockchains.
A node may be a member of arbitrarily many Subnets.

A Subnet manages its own membership and it may require that its constituent validators have certain properties.
This is very useful and we explore its ramifications in more depth below.

There is a special Subnet called the **Default Subnet,** which validates Avalanche's [built-in blockchains.](#built-in-blockchains) 
All members of all Subnets must also be a member of the **Default Subnet.**
In order to become a member of the Default Subnet, one must [stake](#what-is-staking) some [AVAX tokens.](#the-x-chain)
The upshot of the preceding two points is that all validators of all blockchains must also validate Avalanche's built-in blockchains and must have staked AVAX tokens.

There are tutorials on [creating a subnet](../tutorials/create-a-subnet.md) and [adding validators to a subnet.](../tutorials/adding-validators.md)

### Compliance

Avalanche's Subnet architecture makes regulatory compliance manageable.
As mentioned above, a Subnet may require validators to meet an arbitrary set of requirements. 
This may include compliance requirements, such as:

* Validators must be located in a given country
* Validators must pass a KYC check 
* Validators must hold a certain license

### Support for Private Blockchains

One can create a Subnet where only certain pre-defined validators may join. 
In this way, one could create a private Subnet where the contents of blockchains would be visible only to those validators.

### Separation of Concerns

In a heterogeneous network of blockchains, some validators will not want to validate certain blockchains because they simply have no 
interest in those blockchains. The Subnet model allows validators to only concern themselves with blockchains that they care about, 
rather than forcing validators to concern themselves about the state of every blockchain. This reduces the burden on validators.

### Application-Specific Requirements

Different blockchain-based applications may require validators to have certain properties. For example, suppose there is an application that requires large amounts of RAM or CPU power. A Subnet could require that validators meet certain hardware requirements so that the application doesn't suffer from low performance due to slow validators.

## Built-in blockchains

As mentioned before, Avalanche is a network of blockchains.
There are 3 blockchains that are inherent to the Avalanche network.
They are validated by the [Default Subnet.](#what-are-subnets)

### The X-Chain

The **X-Chain** acts as a decentralized platform for creating and trading **smart digital assets.**
(Think X for eXchanging assets.)
A smart digital asset is a representation of a real-world thing, such as an equity or bond,
with a set of rules that govern its behavior, like "can't be traded until tomorrow" or "can only be sent to US citizens."

One of the assets traded on the X-Chain is **AVAX**. AVAX is the Avalanche network's native token.
When one issues a transaction to a blockchain on the Avalanche network they pay a fee denominated in AVAX.
Right now there are no transaction fees but there will be in the future.

The X-Chain is an instance of the Avalanche Virtual Machine (AVM).
(Recall that all blockchains are an instance of a Virtual Machine.)

See [here](../tutorials/fixed-cap-asset.md) for tutorials on creating and trading new assets on the X-Chain.

### The P-Chain

Another chain inherent to the Avalanche network is the **P-Chain**, which manages metadata about the Avalanche network.
(P stands for platform.)

The [P-Chain's API](../api/platform.md) allows clients to create subnets, add validators to subnets and create blockchains.

### The C-Chain

The final built-in chain is the **C-Chain**.
(C stands for contract.)

The C-Chain is an instance of the Ethereum Virtual Machine powered by [Avalanche](#what-is-avalanche).
One can create smart contracts on the C-Chain and do anything else they would do on Ethereum by using the [C-Chain's API](../api/evm.md).

## What is Avalanche

Many online applications require agreement (consensus) between a set of computers.
Asset trading is one such application; every participant needs to agree on who holds what assets.

In 2018 distributed systems researchers created Avalanche, a novel consensus protocol that is secure, performant and energy-efficient.

### Classical and Nakamoto Consensus Protocols

In order to illustrate what differentiates Avalance, it's worth reviewing legacy consensus protocols.

Classical protocols, including PBFT, Libra's HotStuff, Hedera Hashgraph, HyperLedger and Tendermint/Cosmos, are based on all-to-all voting.
They typically have a designated leader who initiates the decision process and a series of rounds of all-to-all communication. This process is inherently expensive; all-to-all communication
requires $O(N^2)$ messages, where N is the number of participants. Therefore, classical protocols can't handle many participants. Libra, for instance, is limited to less than 100 participants.

The Nakamoto family of protocols relies on a process known as proof-of-work mining. While this does away with
the requirement for all-to-all communication, it requires useless calculations that use vast amounts of energy; an analysis by the International Energy Agency estimates that cryptocurrency mining uses at least as much energy as the entire nation of Ireland. As a result, Nakamoto-based systems constantly leak value out of their ecosystems to power companies. To maintain the security of proof-of-work systems, the miners can never be switched off, thus ensuring that this eye-watering energy consumption never ends. Mining a block is difficult by design, so Nakamoto protocols finalize transactions very slowly -- it takes an hour for a Bitcoin transaction to become final, and this low latency will not improve even as technology does. 

### How Does Avalanche Work

Protocols in the Avalanche family operate through repeated sub-sampled voting.

When a validator is trying to determine whether a transaction should be accepted or rejected, it asks a small, random subset of validators whether they think the transaction should be accepted or rejected.
If the queried validator thinks the transaction is invalid, has already rejected the transaction or prefers a conflicting transaction, it replies that it thinks the transaction should be rejected. Otherwise, it replies that it thinks the transaction should be accepted.

If a sufficiently large portion (*alpha*) of the validators sampled reply that they think the transaction should be accepted, the validator prefers to accept the transaction.
That is, when it is queried about the transaction in the future, it will reply that it thinks the transaction should be accepted. Similarly, the validator will prefer to reject the transaction if a sufficiently large portion of the validators reply that they think the transaction should be rejected.

The validator repeats this sampling process until *alpha* of the validators queried reply the same way (accept/reject) for *beta* consecutive rounds. 

In the common case when a transaction has no conflicts, finalization happens very quickly.
When conflicts exist, honest validators quickly cluster around preferring one of the conflicting transactions, entering a positive feedback loop until all correct validators prefer that transaction, leading to its acceptance and the rejection of conflicting transactions. Avalanche gets its name from this cascading property.

It is guaranteed (with arbitrarily high probability based on system parameters) that if any honest validator accepts (rejects) a transaction, all honest validators will accept (reject) that transaction.

### Properties of Avalanche

Protocols in the Avalanche family are very fast.
They can achieve irreversible finality in 1-2 seconds, quicker than a typical credit card transaction.
They support many thousands of transactions per second, in excess of Visa's typical throughput.

In a given round a validator queries only a small sub-sample of validators, allowing Avalanche to scale to up to millions of participants.
No other proof-of-stake protocol can support nearly as many validators without compromising the security of the network.

Avalanche protocols are lightweight and sustainable.
Unlike Nakamoto protocols, they use very little energy, and when there is no work to do, the system quiesces (waits in a low-energy-consumption state.)

Finally, Avalanche protocols are highly secure.
Because they operate without a leader, they are immune to a large class of attacks that
other consensus protocol families face.
The large number of validators ensures immutability and censorship resistance that proof-of-work protocols, backed by small numbers of mining pools, cannot achieve.
Most projects that use proof-of-stake attempt to scale by delegating validation to a subcommittee.
The cost of violating safety in such a system is only as low as the cost of corrupting any subcommittee, which may be very low. 
In Avalanche protocols, such delegation is not necessary because the protocol allows every validator to have a first-hand say in consensus. 

Those interested in a more technical, in-depth discussion of Avalanche should read the [Avalanche whitepaper.](https://arxiv.org/pdf/1906.08936.pdf)

### Comparison of Consensus Protocol Families

The table below provides a comparison of the Avalanche, Nakamoto and Classical consensus protocol families.

|                                                                | Nakamoto | Classical | Avalanche |
|----------------------------------------------------------------|----------|-----------|-----------|
| Scalable                                                       |     +    |     -     |      +    |
| Robust                                                         |     +    |     -     |      +    |
| Highly Decentralized                                           |     +    |     -     |      +    |
| Low Latency                                                    |     -    |     +     |      +    |
| High Throughput                                                |     -    |     +     |      +    |
| Lightweight                                                    |     -    |     +     |      +    |
| Green, Sustainable                                             |     -    |     +     |      +    |
| Resilient to 51% Attacks                                       |     -    |     -     |      +    |


## What is Staking

### Sybil Attacks 

In a decentralized network like Bitcoin, Ethereum or Avalanche, each validator influences which transactions are accepted and which are rejected.

A [**sybil attack**](https://en.wikipedia.org/wiki/Sybil_attack) is an attack where the attacker controls many validators and therefore gains an unsafe amount of influence over the network.
This is analogous to vote-stuffing in an election.

Proof-of-Stake is the method by which the Avalanche network prevents Sybil attacks.

### How Does Proof-of-Stake Work

To resist sybil attacks, a decentralized network must require that influence over the network is paid for with a scarce resource so that it is infeasibly expensive for an attacker to gain enough influence over the network to compromise its security. In proof-of-work systems, the scarce resource is computing power. On the Avalanche network, the scarce resource is the native token, AVAX.

If a node wishes to validate for any blockchain it must *stake* AVAX.
To stake is to lock up some AVAX tokens, making them temporarily unspendable. 

### How Can I Validate the Default Subnet (Stake AVAX)

See [this tutorial.](../tutorials/adding-validators.md#add-a-validator-to-the-default-subnet)

### Validation Rewards

When a validator is done validating the Default Subnet it receives back the AVAX tokens it staked. 
Additionally, it may receive a reward for helping to secure the network by validating.

Right now, a reward is always paid out to validators.
In the future, a validator will only receive the validation reward if it is sufficiently responsive and correct during the time it validates.

See the [Avalanche token paper](https://files.avalabs.org/papers/ava-token.pdf) to learn more about AVAX and the mechanics of staking.

## Summary

### High performance

Blockchains built on Avalanche use the innovative Avalanche consensus protocol to 
handle thousands of transactions per second and permanently finalize transactions in seconds.

### Safety

Avalanche allows tens-of-thousands of validators to have a first-hand say in the system,
making Avalanche robust and resistant to attacks.

### Sustainability

Avalanche uses energy-efficient Proof-of-Stake rather than Proof-of-Work.

### Flexibility

Virtual Machines model allows developers to easily create custom blockchains and dApps that can contain almost any arbitrary logic.

### Private Blockchains

Users can create Subnets, allowing for private blockchains.

## Next steps

- [Get started with the quickstart tutorial](../quickstart/ava-getting-started.md)
- [Follow the Quickstart guide](../tutorials/fixed-cap-asset.md)
- [Explore Avalanche's APIs](../api/intro-apis.md)
- [Explore reference materials](../references/cryptographic-primitives.md)
- [Read the whitepaper and other papers](../../papers/)
