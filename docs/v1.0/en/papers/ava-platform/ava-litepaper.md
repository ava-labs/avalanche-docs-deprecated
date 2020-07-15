author:
- 'Daniel Laine, Stephen Buttolph, Kevin Sekniqi, and Emin Gün Sirer'
  Platform Release V1\

Introduction
============

System Spec
===========

The Core Protocol
-----------------

### Introduction

Distributed payments and -- more generally -- computation, require
agreement (consensus) between a set of machines. There are many variants
of consensus protocols that have been proposed in 40+ years of
distributed systems research. Most fall under two families: Nakamoto
consensus (or, more broadly, longest-chain-based protocols), and
traditional (classical, or all-to-all voting-based) consensus protocols.
Since May of 2018, there is now a third, and fundamentally different
family: the Snow family, of which the most predominant instantiation is
the Avalanche consensus protocol. Unlike classical voting-based
protocols which require all-to-all voting and which provide
deterministic guarantees, the Snow family operates through randomized
sub-sampled voting and is the first voting-based BFT protocol to provide
probabilistic guarantees. In return for these new sets of guarantees,
the Snow family enjoys best-in-class scalability and performance without
sacrificing practical security guarantees, robustness, or
decentralization.

### Snow consensus in a nutshell

First, a transaction is created by a user and sent to a validating node
(a node participating in the consensus procedure). It is then propagated
out to other nodes in the network via gossiping. In an ideal
environment, where no party misbehaves, all transactions would be valid
and thus consensus would simply be a matter of propagation of
information. But what happens if there is malicious behavior and users
issue conflicting transactions (e.g. a user trying to spend the same
amount of money to two different people)? The Snow family employs a very
simple, but powerful mechanism: every node randomly queries a small
subset of nodes and requests which transaction, amongst the conflicting
set, they think is the valid one. If the querying node receives a
supermajority response in favor of one transaction, then the node
changes its own response to that transaction. Every node in the network
repeats this simple procedure until the entire network comes to
consensus on one of the conflicting transactions.

### Decentralization, immutability, and security guarantees

A core feature of the Snow family is its ability to scale without
incurring fundamental tradeoffs. Snow protocols can scale to tens of
thousands or millions of nodes, without delegation to subsets of
validators. These protocols enjoy the best-in-class system
decentralization, allowing every node to fully validate. First-hand
continuous participation has deep implications for the security of the
system. In almost every proof-of-stake protocol that attempts to scale
to a large participant set, the typical mode of operation is to enable
scaling by delegating validation to a subcommittee. Naturally, this
implies that the security of the system is now precisely as high as the
corruption cost of the subcommittee. Subcommittees are furthermore
subject to cartel formation. In Snow-type protocols, such delegation is
not necessary, allowing every node operator to have a first-hand say in
the system, at all times. Another design, typically referred to as state
sharding, attempts to provide scalability by parallelizing transaction
serialization to independent networks of validators. Unfortunately, the
security of the system in such a design becomes only as high as the
easiest corruptible independent set (or shard). Therefore, neither
subcommittee election nor sharding are appropriate scaling solutions for
crypto platforms.

Unlike classical protocols, the Snow protocols also enjoy robustness.
The latest slew of blockchain projects which employ classical consensus
protocols require full membership knowledge. Knowing the entire set of
participants is sufficiently simple in closed, permissioned systems, but
becomes increasingly hard in open, decentralized networks. This
limitation imposes high security risks to existing incumbents employing
such protocols. Conversely, Snow protocols do not impose such strict
requirements. Validators of Snow protocols enjoy the ability to validate
without continuous full membership knowledge.

### Performance measurements

Blockchain's lack of performance remains one of the toughest hurdles to
its adoption. Most blockchains today are unable to support business
applications, such as trading or daily retail payments. It is simply
unworkable to wait minutes, or even hours, for confirmation of
transactions. New blockchain solutions that perform well trade off
decentralization and security and opt for more centralized and insecure
consensus mechanisms in order to achieve higher performance.

On the flip side, Avalanche's constant-sized subsampling means that the
platform can support high throughput (5000+ transactions per second) and
low latency (1-2 second confirmations). These numbers are taken directly
from a real, fully implemented Avalanche network running on 2000 nodes on AWS,
geo-distributed across the globe on low-end machines, without employing
any "numbers tricks" that often times are present in other similar
claims. Higher performance results (10,000+) can be achieved through
assuming higher bandwidth provisioning for each node and dedicated
hardware for signature verification. Finally, we note that the
aforementioned metrics are at the base-layer. Layer-2 scaling solutions,
such as sharding, immediately augment these results.

### Comparative Charts

Table
[\[table:comparativechartconsensus\]](#table:comparativechartconsensus){reference-type="ref"
reference="table:comparativechartconsensus"} describes the differences
between the three known families of consensus protocols through a set of
8 critical axes.

                                                                           Nakamoto            Classical            Snow\*     
  ------------------------------------------------------------------ ------------------- --------------------- -----------------
  Robust (Suitable for Open Settings)                                        \+                   \-                  \+
  Highly Decentralized (Allows Many Validators)                              \+                   \-                  \+
  Low Latency and Quick Finality (Fast Transaction Confirmation)             \-                   \+                  \+
  High Throughput (Allows Many Clients)                                      \-                   \+                  \+
  Lightweight (Low System Requirements)                                      \-                   \+           
  Quiescent (Not Active When No Decisions Performed)                         \-                   \+                  \+
  Safety Parameterizable (Beyond 1/2 Adversarial Presence)                   \-                   \+                  \+
  Safety Guarantees                                                     Probabilistic        Deterministic       Probabilistic
  Sybil Protection                                                           PoW                  PoS                 PoS

  : Comparative chart between the three known families of consensus
  protocols. Avalanche, Snowman, and Frosty all belong to the Snow\*
  family.[]{label="table:comparativechartconsensus"}

The Platform
------------

The first version of the Avalanche platform, aims to be a platform for
enabling high performance, ultra-decentralized applications, as well as
the issuance and trading of any arbitrary digital asset.

### An interoperable and Flexible Platform-of-Platforms

Avalanche's biggest innovation at the platform level is the plugin
architecture, which allows developers to issue assets inside flexible
and interoperable feature-specific-subnetworks (FSSs). FSSs are
subnetworks that run a plugin. A plugin defines the behavior and
functionality of an FSS. Upon creating an FSS, one defines:

1.  The plugin the FSS uses: this defines the functionality supported by
    the FSS.

2.  The genesis data: this represents the initial state of the FSS. This
    might include, for example, who the original holders of an asset
    are.

This architecture allows developers to create highly specialized FSSs
that define and implement their own unique business logic. A plugin may
implement almost any functionality, from virtual machines to Intel SGX,
and from ring signatures to zero knowledge proofs.

For all those that require it, Avalanche will be the first platform to support
the development of a rich marketplace of plugins that can enjoy strict
compliance rulesets, privacy, and innovative new features. Such a
flexible repository of FSSs allows both hobbyist developers as well as
large enterprises to deploy fully compliant and interoperable business
and system logic. The AVAX token will provide the core infrastructure for
enabling the security of the system while simultaneously providing the
universal unit of exchange (i.e. interoperation) between any assets
deployed on AVAX.

The Avalanche platform will allow the tokenization of all types of assets.
This includes support for arbitrary scripting languages, multiple types
of virtual machines (EVM, WASM, etc), and simple-to-use libraries for
token creation. For example, developers can create an asset that has
features of both BTC and ZEC. This flexibility enables interoperability
amongst various platforms, enabling true backwards compatibility and
new, more expressive, transactions.

For public infrastructure developers, this means that dapps can be
ported from existing platforms to Avalanche with little modification. For
private enterprise developers, this means the ability to deploy dapps
that must comply with strict regulatory and privacy guarantees. We
believe that such flexibility, for the first time, allows a truly
interoperable network of nodes under all forms of compliance guarantees,
whether permissioned or permissionless, and whether public, or private.

### Case study \#1: Tokenization

Digital asset issuance is simply a matter of choosing an appropriate FSS
that enables some core set of functionalities, or -- if no such FSS
exists -- making our own. For example, suppose that a developer team
wants to issue a new token that represents crop insurance in Argentina
and build a new decentralized exchange for listing, buying, and selling
insurance contracts. This team can launch their system by simply
launching an instance of the EVM plugin and then writing a simple smart
contract that performs the order matching. They can also build on top of
the existing EVM plugin to implement KYC functionality in order to
ensure land ownership for a particular contract.

### Case study \#2: If-This-Then-That Cross-Chain Triggers

Avalanche's modular plugin architecture makes it simple to enable
"If-This-Then-That" functionality, wherein developers of an FSS (e.g.
Purple) can interact with another FSS (e.g. Orange) via an IFTTT plugin.
Per way of illustration, the IFTTT plugin could, for example, trigger an
automatic sell between Purple and Orange upon some conditional event
being met on the Orange subnet, as illustrated in the figure below.

### Case study \#3: Enabling borderless frictionless Asset Transfer and Ownership

In order for a non-US Resident to acquire US based securities they would
usually have to work with a US-based securities broker. Such a broker
would handle the compliance and custody of assets and would charge fees
to generate a profit. Asset swaps on the Avalanche platform will be truly
peer-to-peer. For example, an individual who passes compliance
requirements and previously without access to financial products in a
certain jurisdiction will be able to seamlessly purchase assets directly
from a market. The Avalanche Platform's native support for compliance features
will cut out the middle men and enable frictionless value transfer
between participating parties. The purchaser of assets would need only
to pass the KYC process, comply with location regulation and own a
wallet that supports assets on the Avalanche platform.

The AVAX Token
=============

### Payments

True decentralized peer-to-peer payments are largely an unrealized dream
for the industry due to the current lack of performance from incumbents.
We envision Avalanche to be as powerful and easy to use as payments with Visa,
allowing thousands of transactions globally every second, in a fully
trustless, decentralized manner. Furthermore, for merchants worldwide,
we aim to provide a direct value proposition over Visa, namely lower
fees.

### Securing the system: staking

On the Avalanche platform, sybil control will be achieved via staking. In
order to validate, a participant will have to lock up coins (a stake).
Validators (stakers) will be compensated for their validation services
based on staking amount and staking duration, amongst other properties.
The chosen compensation function should minimize variance, ensuring that
large stakers do not disproportionately receive more compensation.
Participants will also not be subject to any \"luck\" factors, as in PoW
mining. Such a reward scheme also discourages the formation of mining or
staking pools enabling truly decentralized, trustless participation in
the network.

### Atomic swaps

Besides providing the core security of the system, the AVAX token will
serve as the universal unit of exchange. From there, the Avalanche platform
will be able to support trustless atomic swaps natively on the platform
enabling native, truly decentralized exchanges of any type of asset
directly on Avalanche.

### Governance

Governance is critical to the development and adoption of the Avalanche
platform because -- as with all other types of systems -- Avalanche will also
face natural evolutions and updates. There is on-chain governance for
critical parameters of the network where participants will be able to
vote on changes to the network and settle network upgrade decisions
democratically. This will include factors such as the minimum staking
amount, minting rate, as well as other economic parameters. This enables
the platform to effectively perform dynamic parameter optimization
through a crowd oracle. However, unlike more generic governance
platforms out there, Avalanche does not allow governance of arbitrary aspects
of the system, ensuring a much higher degree of assurance and safety for
participants in Avalanche. Lastly, all governable parameters are subject to
limited change within specific time bounds, ensuring that sporadic,
black swan events to do not affect the system in negative ways.

### Monetary Policy

The objective of Avalanche's monetary policy is to balance the incentives
of users to stake the coin versus use it to interact with the variety of
services available on the Avalanche platform. Participants in the Avalanche network
collectively act as a decentralized reserve bank. We follow the example
of the federal reserve bank, which utilizes several tools to accomplish
their monetary policy objectives. The levers available on Avalanche are
staking rewards, fees, and airdrops, all of which are influenced by
governable parameters. Staking rewards are set by on-chain governance.
Staking can be induced by increasing fees or increasing staking rewards.
On the other hand, we can induce increased engagement with the Avalanche
platform services by lowering fees, decreasing the staking reward.

[^1]: Forward-looking statements generally relate to future events or
    our future performance. This includes, but is not limited to, Avalanche's
    projected performance; the expected development of its business and
    projects; execution of its vision and growth strategy; and
    completion of projects that are currently underway, in development
    or otherwise under consideration. Forward-looking statements
    represent our management's beliefs and assumptions only as of the
    date of this presentation. These statements are not guarantees of
    future performance and undue reliance should not be placed on them.
    Such forward-looking statements necessarily involve known and
    unknown risks, which may cause actual performance and results in
    future periods to differ materially from any projections expressed
    or implied herein. Ava Labs undertakes no obligation to update
    forward-looking statements. Although forward-looking statements are
    our best prediction at the time they are made, there can be no
    assurance that they will prove to be accurate, as actual results and
    future events could differ materially. The reader is cautioned not
    to place undue reliance on forward-looking statements.
