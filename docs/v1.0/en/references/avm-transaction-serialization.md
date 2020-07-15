# AVM Transaction Serialization

This file is meant to be the single source of truth for how we serialize transactions in the `AVM`, the Avalanche Virtual Machine. This document uses the [primitive serialization](./serialization-primitives.md) format for packing and [secp256k1](./cryptographic-primitives.md#cryptography-in-the-avalanche-virtual-machine) for cryptographic user identification.

***

## Outputs

Outputs have two possible types: `SECP256K1TransferOutput`, and `NFTTransferOutput`.

***

### SECP256K1 Transfer Output

A [secp256k1](./cryptographic-primitives.md#cryptography-in-the-avalanche-virtual-machine) transfer output allows for sending a quantity of an asset to a collection of addresses after a specified unix time.

#### SECP256K1 Transfer Output Identifier

The `OutputID` for a secp256k1 transfer output type is `0x00000007`.

#### What SECP256K1 Transfer Output Contains

A secp256k1 transfer output contains an `OutputID`, `Amount`, `Locktime`, `Threshold`, and `Addresses`.

- **`OutputID`** is an int that defines which type this is. For a secp256k1 transfer output the `OutputID` is `0x00000007`.
- **`Amount`** is a long that specifies the quantity of the asset that this output owns. Must be positive.
- **`Locktime`** is a long that contains the unix timestamp that this output can be spent after. The unix timestamp is specific to the second.
- **`Threshold`** is an int that names the number of unique signatures required to spend the output. Must be less than or equal to the length of **`Addresses`**. If **`Addresses`** is empty, must be 0.
- **`Addresses`** is a list of unique addresses that correspond to the private keys that can be used to spend this output. Addresses must be sorted lexicographically.

#### Gantt SECP256K1 Transfer Output Specification

```boo
+-----------+------------+--------------------------------+
| output_id : int        |                        4 bytes |
+-----------+------------+--------------------------------+
| amount    : long       |                        8 bytes |
+-----------+------------+--------------------------------+
| locktime  : long       |                        8 bytes |
+-----------+------------+--------------------------------+
| threshold : int        |                        4 bytes |
+-----------+------------+--------------------------------+
| addresses : [][20]byte |  4 + 20 * len(addresses) bytes |
+-----------+------------+--------------------------------+
                         | 28 + 20 * len(addresses) bytes |
                         +--------------------------------+
```

#### Proto SECP256K1 Transfer Output Specification

```protobuf
message SECP256K1TransferOutput {
    uint32 output_id = 1;         // 04 bytes
    uint64 amount = 2;            // 08 bytes
    uint64 locktime = 3;          // 08 bytes
    uint32 threshold = 4;         // 04 bytes
    repeated bytes addresses = 5; // 04 bytes + 20 bytes * len(addresses)
}
```

#### SECP256K1 Transfer Output Example

Let's make a secp256k1 transfer output with:

- **`Amount`**: 12345
- **`Locktime`**: 54321
- **`Threshold`**: 1
- **`Addresses`**:
  - 0xc3344128e060128ede3523a24a461c8943ab0859
  - 0x51025c61fbcfc078f69334f834be6dd26d55a955

```splus
[
    OutputID  <- 0x00000007
    Amount    <- 12345 = 0x0000000000003039
    Locktime  <- 54321 = 0x000000000000d431
    Threshold <- 1     = 0x00000001
    Addresses <- [
        0xc3344128e060128ede3523a24a461c8943ab0859,
        0x51025c61fbcfc078f69334f834be6dd26d55a955,
    ]
]
=
[
    // output type:
    0x00, 0x00, 0x00, 0x07,
    // amount:
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x30, 0x39,
    // locktime:
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xd4, 0x31,
    // threshold:
    0x00, 0x00, 0x00, 0x01,
    // number of addresses:
    0x00, 0x00, 0x00, 0x02,
    // addrs[0]:
    0x51, 0x02, 0x5c, 0x61, 0xfb, 0xcf, 0xc0, 0x78,
    0xf6, 0x93, 0x34, 0xf8, 0x34, 0xbe, 0x6d, 0xd2,
    0x6d, 0x55, 0xa9, 0x55,
    // addrs[1]:
    0xc3, 0x34, 0x41, 0x28, 0xe0, 0x60, 0x12, 0x8e,
    0xde, 0x35, 0x23, 0xa2, 0x4a, 0x46, 0x1c, 0x89,
    0x43, 0xab, 0x08, 0x59,
]
```

***

### NFT Transfer Output

An NFT transfer output is an NFT that is owned by a collection of addresses.

#### NFT Transfer Output Identifier

The `OutputID` for an NFT transfer output type is `0x0000000b`.

#### What NFT Transfer Output Contains

An NFT transfer output contains an `OutputID`, `GroupID`, `Payload`, `Threshold`, and `Addresses`.

- **`OutputID`** is an int that defines which type this is. For an NFT transfer output the `OutputID` is `0x0000000b`.
- **`GroupID`** is an int that specifies the group this NFT was issued with.
- **`Payload`** is an arbitrary string of bytes long longer than 1024 bytes.
- **`Threshold`** is an int that names the number of unique signatures required to spend the output. Must be less than or equal to the length of **`Addresses`**. If **`Addresses`** is empty, must be 0.
- **`Addresses`** is a list of unique addresses that correspond to the private keys that can be used to spend this output. Addresses must be sorted lexicographically.

#### Gantt NFT Transfer Output Specification

```boo
+-----------+------------+-------------------------------+
| output_id : int        |                       4 bytes |
+-----------+------------+-------------------------------+
| group_id  : int        |                       4 bytes |
+-----------+------------+-------------------------------+
| payload   : []byte     |        4 + len(payload) bytes |
+-----------+------------+-------------------------------+
| threshold : int        |                       4 bytes |
+-----------+------------+-------------------------------+
| addresses : [][20]byte | 4 + 20 * len(addresses) bytes |
+-----------+------------+-------------------------------+
                         | 20 + len(payload)             |
                         |  + 20 * len(addresses) bytes  |
                         +-------------------------------+
```

#### Proto NFT Transfer Output Specification

```protobuf
message NFTTransferOutput {
    uint32 output_id = 1;         // 04 bytes
    uint32 group_id = 2;          // 04 bytes
    bytes payload = 3;            // 04 bytes + len(payload)
    uint32 threshold = 4;         // 04 bytes
    repeated bytes addresses = 5; // 04 bytes + 20 bytes * len(addresses)
}
```

#### NFT Transfer Output Example

Let's make an NFT transfer output with:

- **`GroupID`**: 12345
- **`Payload`**: 0x431100
- **`Threshold`**: 1
- **`Addresses`**:
  - 0xc3344128e060128ede3523a24a461c8943ab0859
  - 0x51025c61fbcfc078f69334f834be6dd26d55a955

```splus
[
    OutputID  <- 0x0000000b
    GroupID   <- 12345 = 0x00003039
    Payload   <- 0x431100
    Threshold <- 1     = 0x00000001
    Addresses <- [
        0xc3344128e060128ede3523a24a461c8943ab0859,
        0x51025c61fbcfc078f69334f834be6dd26d55a955,
    ]
]
=
[
    // output type:
    0x00, 0x00, 0x00, 0x0b,
    // groupID:
    0x00, 0x00, 0x30, 0x39,
    // length of payload:
    0x00, 0x00, 0x00, 0x03,
    // payload:
    0x43, 0x11, 0x00,
    // threshold:
    0x00, 0x00, 0x00, 0x01,
    // number of addresses:
    0x00, 0x00, 0x00, 0x02,
    // addrs[0]:
    0x51, 0x02, 0x5c, 0x61, 0xfb, 0xcf, 0xc0, 0x78,
    0xf6, 0x93, 0x34, 0xf8, 0x34, 0xbe, 0x6d, 0xd2,
    0x6d, 0x55, 0xa9, 0x55,
    // addrs[1]:
    0xc3, 0x34, 0x41, 0x28, 0xe0, 0x60, 0x12, 0x8e,
    0xde, 0x35, 0x23, 0xa2, 0x4a, 0x46, 0x1c, 0x89,
    0x43, 0xab, 0x08, 0x59,
]
```

***

## Transferable Output

Transferable outputs wrap a transfer output with an asset ID.

### What Transferable Output Contains

A transferable output contains an `AssetID` and an `Output`.

- **`AssetID`** is a 32-byte array that defines which asset this output references.
- **`Output`** is a transferable output object.

### Gantt Transferable Output Specification

```boo
+----------+----------+-------------------------+
| asset_id : [32]byte |                32 bytes |
+----------+----------+-------------------------+
| output   : Output   |      size(output) bytes |
+----------+----------+-------------------------+
                      | 32 + size(output) bytes |
                      +-------------------------+
```

### Proto Transferable Output Specification

```protobuf
message TransferableOutput {
    bytes asset_id = 1; // 32 bytes
    Output output = 2;  // size(output)
}
```

### Transferable Output Example

Let's make a transferable output:

- `AssetID: 0x000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f`
- `Output: "Example SECP256K1 Transfer Output from above"`

```splus
[
    AssetID <- 0x000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f
    Output  <- 0x000000070000000000003039000000000000d431000000010000000251025c61fbcfc078f69334f834be6dd26d55a955c3344128e060128ede3523a24a461c8943ab0859,
]
=
[
    // assetID:
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
    0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
    0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
    0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f,
    // output:
    0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x30, 0x39, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0xd4, 0x31, 0x00, 0x00, 0x00, 0x01,
    0x00, 0x00, 0x00, 0x02, 0x51, 0x02, 0x5c, 0x61,
    0xfb, 0xcf, 0xc0, 0x78, 0xf6, 0x93, 0x34, 0xf8,
    0x34, 0xbe, 0x6d, 0xd2, 0x6d, 0x55, 0xa9, 0x55,
    0xc3, 0x34, 0x41, 0x28, 0xe0, 0x60, 0x12, 0x8e,
    0xde, 0x35, 0x23, 0xa2, 0x4a, 0x46, 0x1c, 0x89,
    0x43, 0xab, 0x08, 0x59,
]
```

***

## Initial State

Initial state wraps a variable length array of outputs with a feature extension ID.

### What Initial State Contains

Initial state contains a `FxID` and `InitialState`.

- **`FxID`** is an int that defines which feature extension this state is part of. Currently, the only valid ID here is `0x00000000`.
- **`InitialState`** is a variable length array of transferable output objects.

### Gantt Initial State Specification

```boo
+---------------+----------+-------------------------------+
| fx_id         : int      |                       4 bytes |
+---------------+----------+-------------------------------+
| initial_state : []Output | 4 + size(initial_state) bytes |
+---------------+----------+-------------------------------+
                           | 8 + size(initial_state) bytes |
                           +-------------------------------+
```

### Proto Initial State Specification

```protobuf
message InitialState {
    uint32 fx_id = 1;                  // 4 bytes
    repeated Output initial_state = 2; // 4 + size(initial_state) bytes
}
```

### Initial State Example

Let's make an initial state:

- `FxID: 0x00000000`
- `InitialState: ["Example SECP256K1 Transfer Output from above"]`

```splus
[
    FxID <- 0x00000000
    InitialState  <- [
        0x000000070000000000003039000000000000d431000000010000000251025c61fbcfc078f69334f834be6dd26d55a955c3344128e060128ede3523a24a461c8943ab0859,
    ]
]
=
[
    // fxID:
    0x00, 0x00, 0x00, 0x00,
    // num outputs:
    0x00, 0x00, 0x00, 0x01,
    // output:
    0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x30, 0x39, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0xd4, 0x31, 0x00, 0x00, 0x00, 0x01,
    0x00, 0x00, 0x00, 0x02, 0x51, 0x02, 0x5c, 0x61,
    0xfb, 0xcf, 0xc0, 0x78, 0xf6, 0x93, 0x34, 0xf8,
    0x34, 0xbe, 0x6d, 0xd2, 0x6d, 0x55, 0xa9, 0x55,
    0xc3, 0x34, 0x41, 0x28, 0xe0, 0x60, 0x12, 0x8e,
    0xde, 0x35, 0x23, 0xa2, 0x4a, 0x46, 0x1c, 0x89,
    0x43, 0xab, 0x08, 0x59,
]
```

***

## Inputs

Inputs have one possible type: `SECP256K1TransferInput`.

***

### SECP256K1 Transfer Input

A [secp256k1](../cryptographic-primitives/#cryptography-in-the-avalanche-virtual-machine) transfer input allows for spending an unspent secp256k1 transfer output.

#### SECP256K1 Transfer Input Identifier

The `InputID` for a payment input is `0x00000005`.

#### What SECP256K1 Transfer Input Contains

A secp256k1 transfer input contains an `InputID`, `Amount` and `AddressIndices`.

- **`InputID`** is an int that defines which type this is. For a secp256k1 transfer input the `InputID` is `0x00000005`.
- **`Amount`** is a long that specifies the quantity that this input should be consuming from the UTXO. Must be positive. Must be equal to the amount specified in the UTXO.
- **`AddressIndices`** is a list of unique ints that define the private keys are being used to spend the UTXO. Each UTXO has an array of addresses that can spend the UTXO. Each int represents the index in this address array that will sign this transaction. The array must be sorted low to high.

#### Gantt SECP256K1 Transfer Input Specification

```boo
+-----------------+-------+-------------------------------------+
| input_id        : int   |                             4 bytes |
+-----------------+-------+-------------------------------------+
| amount          : long  |                             8 bytes |
+-----------------+-------+-------------------------------------+
| address_indices : []int |  4 + 4 * len(address_indices) bytes |
+-----------------+-------+-------------------------------------+
                          | 16 + 4 * len(address_indices) bytes |
                          +-------------------------------------+
```

#### Proto SECP256K1 Transfer Input Specification

```protobuf
message SECP256K1TransferInput {
    uint32 input_id = 1;                 // 04 bytes
    uint64 amount = 2;                   // 08 bytes
    repeated uint32 address_indices = 3; // 04 bytes + 4 bytes * len(address_indices)
}
```

#### SECP256K1 Transfer Input Example

Let's make a payment input with:

- **`Amount`**: 123456789
- **`AddressIndices`**:
  - 7
  - 3

```splus
[
    Amount         <- 123456789 = 0x00000000075bcd15,
    AddressIndices <- [0x00000007, 0x00000003]
]
=
[
    // input type:
    0x00, 0x00, 0x00, 0x05,
    // amount:
    0x00, 0x00, 0x00, 0x00, 0x07, 0x5b, 0xcd, 0x15,
    // length:
    0x00, 0x00, 0x00, 0x02,
    // sig[0]
    0x00, 0x00, 0x00, 0x03,
    // sig[1]
    0x00, 0x00, 0x00, 0x07,
]
```

***

## Transferable Input

Transferable inputs describe a specific UTXO with a provided transfer input.

### What Transferable Input Contains

A transferable input contains a `TxID`, `UTXOIndex` `AssetID` and an `Input`.

- **`TxID`** is a 32-byte array that defines which transaction this input is consuming an output from.
- **`UTXOIndex`** is an int that defines which utxo this input is consuming the specified transaction.
- **`AssetID`** is a 32-byte array that defines which asset this input references.
- **`Input`** is a transferable input object.

### Gantt Transferable Input Specification

```boo
+------------+----------+------------------------+
| tx_id      : [32]byte |               32 bytes |
+------------+----------+------------------------+
| utxo_index : int      |               04 bytes |
+------------+----------+------------------------+
| asset_id   : [32]byte |               32 bytes |
+------------+----------+------------------------+
| input      : Input    |      size(input) bytes |
+------------+----------+------------------------+
                        | 68 + size(input) bytes |
                        +------------------------+
```

### Proto Transferable Input Specification

```protobuf
message TransferableInput {
    bytes tx_id = 1;       // 32 bytes
    uint32 utxo_index = 1; // 04 bytes
    bytes asset_id = 3;    // 32 bytes
    Input input = 4;       // size(input)
}
```

### Transferable Input Example

Let's make a transferable input:

- `TxID: 0xf1e1d1c1b1a191817161514131211101f0e0d0c0b0a090807060504030201000`
- `UTXOIndex: 5`
- `AssetID: 0x000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f`
- `Input: "Example SECP256K1 Transfer Input from above"`

```splus
[
    TxID      <- 0xf1e1d1c1b1a191817161514131211101f0e0d0c0b0a090807060504030201000
    UTXOIndex <- 5 = 0x00000005
    AssetID   <- 0x000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f
    Input     <- 0x0000000500000000075bcd15000000020000000300000007
]
=
[
    // txID:
    0xf1, 0xe1, 0xd1, 0xc1, 0xb1, 0xa1, 0x91, 0x81,
    0x71, 0x61, 0x51, 0x41, 0x31, 0x21, 0x11, 0x01,
    0xf0, 0xe0, 0xd0, 0xc0, 0xb0, 0xa0, 0x90, 0x80,
    0x70, 0x60, 0x50, 0x40, 0x30, 0x20, 0x10, 0x00,
    // utxoIndex:
    0x00, 0x00, 0x00, 0x05,
    // assetID:
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
    0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
    0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
    0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f,
    // input:
    0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x00,
    0x07, 0x5b, 0xcd, 0x15, 0x00, 0x00, 0x00, 0x02,
    0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x07,
]
```

***

## Operations

Operations have one possible type: `NFTTransferOp`.

***

### NFT Transfer Op

An NFT transfer operation sending an unspent NFT transfer output to a new set of owners.

#### NFT Transfer Op Identifier

The `OpID` for an NFT transfer operation is `0x0000000d`.

#### What NFT Transfer Op Contains

An NFT transfer operation contains an `OpID`, `AddressIndices`, and an untyped `NFTTransferOutput`.

- **`OpID`** is an int that defines which type this is. For an NFT transfer operation the `OpID` is `0x0000000d`.
- **`AddressIndices`** is a list of unique ints that define the private keys are being used to spend the UTXO. Each UTXO has an array of addresses that can spend the UTXO. Each int represents the index in this address array that will sign this transaction. The array must be sorted low to high.
- **`NFTTransferOutput`** is the output of this operation and must be an NFT Transfer Output. This output doesn't have the **`OutputID`**, because the type is known by the context of being in this operation.

#### Gantt NFT Transfer Op Specification

```boo
+-----------------+------------+------------------------------------+
| op_id           : int        |                            4 bytes |
+-----------------+------------+------------------------------------+
| address_indices : []int      | 4 + 4 * len(address_indices) bytes |
+-----------------+------------+------------------------------------+
| group_id        : int        |                            4 bytes |
+-----------------+------------+------------------------------------+
| payload         : []byte     |             4 + len(payload) bytes |
+-----------------+------------+------------------------------------+
| threshold       : int        |                            4 bytes |
+-----------------+------------+------------------------------------+
| addresses       : [][20]byte |      4 + 20 * len(addresses) bytes |
+-----------------+------------+------------------------------------+
                               |       24 + len(payload)            |
                               |        + 4 * len(address_indices)  |
                               |        + 20 * len(addresses) bytes |
                               +------------------------------------+
```

#### Proto NFT Transfer Op Specification

```protobuf
message NFTTransferOp {
    uint32 op_id = 1;                    // 04 bytes
    repeated uint32 address_indices = 2; // 04 bytes + 4 bytes * len(address_indices)
    uint32 group_id = 3;                 // 04 bytes
    bytes payload = 4;                   // 04 bytes + len(payload)
    uint32 threshold = 5;                // 04 bytes
    repeated bytes addresses = 6;        // 04 bytes + 20 bytes * len(addresses)
}
```

#### NFT Transfer Op Example

Let's make an NFT transfer operation with:

- **`AddressIndices`**:
  - 0x00000007
  - 0x00000003
- **`GroupID`**: 12345
- **`Payload`**: 0x431100
- **`Threshold`**: 1
- **`Addresses`**:
  - 0xc3344128e060128ede3523a24a461c8943ab0859
  - 0x51025c61fbcfc078f69334f834be6dd26d55a955

```splus
[
    OpID       <- 0x0000000d
    AddressIndices <- [
        0x00000007,
        0x00000003,
    ]
    GroupID        <- 12345 = 0x00003039
    Payload        <- 0x431100
    Threshold      <- 1     = 0x00000001
    Addresses      <- [
        0xc3344128e060128ede3523a24a461c8943ab0859,
        0x51025c61fbcfc078f69334f834be6dd26d55a955,
    ]
]
=
[
    // op type:
    0x00, 0x00, 0x00, 0x0d,
    // number of address indices:
    0x00, 0x00, 0x00, 0x02,
    // address index 0:
    0x00, 0x00, 0x00, 0x03,
    // address index 1:
    0x00, 0x00, 0x00, 0x07,
    // groupID:
    0x00, 0x00, 0x30, 0x39,
    // length of payload:
    0x00, 0x00, 0x00, 0x03,
    // payload:
    0x43, 0x11, 0x00,
    // threshold:
    0x00, 0x00, 0x00, 0x01,
    // number of addresses:
    0x00, 0x00, 0x00, 0x02,
    // addrs[0]:
    0x51, 0x02, 0x5c, 0x61, 0xfb, 0xcf, 0xc0, 0x78,
    0xf6, 0x93, 0x34, 0xf8, 0x34, 0xbe, 0x6d, 0xd2,
    0x6d, 0x55, 0xa9, 0x55,
    // addrs[1]:
    0xc3, 0x34, 0x41, 0x28, 0xe0, 0x60, 0x12, 0x8e,
    0xde, 0x35, 0x23, 0xa2, 0x4a, 0x46, 0x1c, 0x89,
    0x43, 0xab, 0x08, 0x59,
]
```

***

## Transferable Op

Transferable operations describe a set of UTXOs with a provided transfer operation. Only one Asset ID is able to be referenced per operation.

### What Transferable Op Contains

A transferable input contains an `AssetID`, `UTXOIDs`, and `TransferOp`.

- **`AssetID`** is a 32-byte array that defines which asset this operation changes.
- **`UTXOIDs`** is an array of TxID-OutputIndex tuples. This array must be sorted in lexicographical order.
- **`TransferOp`** is a transferable operation object.

### Gantt Transferable Op Specification

```boo
+-------------+------------+------------------------------+
| asset_id    : [32]byte   |                     32 bytes |
+-------------+------------+------------------------------+
| utxo_ids    : []UTXOID   | 4 + 36 * len(utxo_ids) bytes |
+-------------+------------+------------------------------+
| transfer_op : TransferOp |      size(transfer_op) bytes |
+------------+-------------+------------------------------+
                           |   36 + 36 * len(utxo_ids)    |
                           |    + size(transfer_op) bytes |
                           +------------------------------+
```

### Proto Transferable Op Specification

```protobuf
message UTXOID {
    bytes tx_id = 1;       // 32 bytes
    uint32 utxo_index = 1; // 04 bytes
}
message TransferableOp {
    bytes asset_id = 1;           // 32 bytes
    repeated UTXOID utxo_ids = 2; // 4 + 36 * len(utxo_ids) bytes
    TransferOp transfer_op = 3;   // size(transfer_op)
}
```

### Transferable Op Example

Let's make a transferable input:

- `AssetID: 0x000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f`
- `UTXOIDs:`
  - `UTXOID:`
    - `TxID: 0xf1e1d1c1b1a191817161514131211101f0e0d0c0b0a090807060504030201000`
    - `UTXOIndex: 5`
- `Op: "Example NFT Transfer Op from above"`

```splus
[
    AssetID   <- 0x000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f
    UTXOIDs   <- [
        {
            TxID:0xf1e1d1c1b1a191817161514131211101f0e0d0c0b0a090807060504030201000
            UTXOIndex:5
        }
    ]
    Op     <- 0x0000000d0000000200000003000000070000303900000003431100000000010000000251025c61fbcfc078f69334f834be6dd26d55a955c3344128e060128ede3523a24a461c8943ab0859
]
=
[
    // assetID:
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
    0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
    0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
    0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f,
    // number of utxoIDs:
    0x00, 0x00, 0x00, 0x01,
    // txID:
    0xf1, 0xe1, 0xd1, 0xc1, 0xb1, 0xa1, 0x91, 0x81,
    0x71, 0x61, 0x51, 0x41, 0x31, 0x21, 0x11, 0x01,
    0xf0, 0xe0, 0xd0, 0xc0, 0xb0, 0xa0, 0x90, 0x80,
    0x70, 0x60, 0x50, 0x40, 0x30, 0x20, 0x10, 0x00,
    // utxoIndex:
    0x00, 0x00, 0x00, 0x05,
    // op:
    0x00, 0x00, 0x00, 0x0d, 0x00, 0x00, 0x00, 0x02,
    0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x07,
    0x00, 0x00, 0x30, 0x39, 0x00, 0x00, 0x00, 0x03,
    0x43, 0x11, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00,
    0x00, 0x00, 0x02, 0x51, 0x02, 0x5c, 0x61, 0xfb,
    0xcf, 0xc0, 0x78, 0xf6, 0x93, 0x34, 0xf8, 0x34,
    0xbe, 0x6d, 0xd2, 0x6d, 0x55, 0xa9, 0x55, 0xc3,
    0x34, 0x41, 0x28, 0xe0, 0x60, 0x12, 0x8e, 0xde,
    0x35, 0x23, 0xa2, 0x4a, 0x46, 0x1c, 0x89, 0x43,
    0xab, 0x08, 0x59,
]
```

***

## Credentials

Credentials have two possible types: `SECP256K1Credential`, and `NFTCredential`. Each credential is paired with an Input or Operation. The order of the credentials match the order of the inputs or operations.

***

### SECP256K1 Credential

A [secp256k1](../cryptographic-primitives/#cryptography-in-the-avalanche-virtual-machine) credential contains a list of 65-byte recoverable signatures.

#### SECP256K1 Credential Identifier

The `CredentialID` for a SECP256K1 credential is `0x00000009`.

#### What SECP256K1 Credential Contains

- **`Signatures`** is an array of 65-byte recoverable signatures. The order of the signatures must match the input's signature indices.

#### Gantt SECP256K1 Credential Specification

```boo
+-----------------+------------+---------------------------------+
| credential_type : int        |                         4 bytes |
+-----------------+------------+---------------------------------+
| signatures      : [][65]byte |  4 + 65 * len(signatures) bytes |
+-----------------+------------+---------------------------------+
                               |  8 + 65 * len(signatures) bytes |
                               +---------------------------------+
```

#### Proto SECP256K1 Credential Specification

```protobuf
message SECP256K1Credential {
    uint32 credential_type = 1;    // 4 bytes
    repeated bytes signatures = 2; // 4 bytes + 65 bytes * len(signatures)
}
```

#### SECP256K1 Credential Example

Let's make a payment input with:

- **`signatures`**:
  - `0x000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1e1d1f202122232425262728292a2b2c2e2d2f303132333435363738393a3b3c3d3e3f00`
  - `0x404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5e5d5f606162636465666768696a6b6c6e6d6f707172737475767778797a7b7c7d7e7f00`

```splus
[
    Signatures <- [
        0x000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1e1d1f202122232425262728292a2b2c2e2d2f303132333435363738393a3b3c3d3e3f00,
        0x404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5e5d5f606162636465666768696a6b6c6e6d6f707172737475767778797a7b7c7d7e7f00,
    ]
]
=
[
    // credential type:
    0x00, 0x00, 0x00, 0x09,
    // length:
    0x00, 0x00, 0x00, 0x02,
    // sig[0]
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
    0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
    0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
    0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1e, 0x1d, 0x1f,
    0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27,
    0x28, 0x29, 0x2a, 0x2b, 0x2c, 0x2e, 0x2d, 0x2f,
    0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37,
    0x38, 0x39, 0x3a, 0x3b, 0x3c, 0x3d, 0x3e, 0x3f,
    0x00,
    // sig[1]
    0x40, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47,
    0x48, 0x49, 0x4a, 0x4b, 0x4c, 0x4d, 0x4e, 0x4f,
    0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57,
    0x58, 0x59, 0x5a, 0x5b, 0x5c, 0x5e, 0x5d, 0x5f,
    0x60, 0x61, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67,
    0x68, 0x69, 0x6a, 0x6b, 0x6c, 0x6e, 0x6d, 0x6f,
    0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77,
    0x78, 0x79, 0x7a, 0x7b, 0x7c, 0x7d, 0x7e, 0x7f,
    0x00,
]
```

***

### NFT Credential

An NFT credential is the same as an secp256k1 credential with a different credential identifier.

#### NFT Credential Identifier

The `CredentialID` for an NFT credential is `0x0000000e`.

***

## Unsigned Transaction

Unsigned transactions contain the full content of a transaction with only the signatures missing. Unsigned transactions have three possible types: `BaseTx`, `CreateAssetTx`, and `OperationTx`.

### Unsigned Base Tx Identifier

The transaction identifier for a base tx is `0x00000000`.

### What Unsigned Base Tx Contains

An unsigned base tx contains an `ID`, `NetworkID`, `BlockchainID`, `Outputs`, and `Inputs`.

- **`ID`** is an int that defines which transaction type this is. Is `0x00000000`.
- **`NetworkID`** is an int that defines which network this transaction is meant to be issued to. This value is meant to support transaction routing and is not designed for replay attack prevention.
- **`BlockchainID`** is a 32-byte array that defines which blockchain this transaction was issued to. This is used for replay attack prevention for transactions that could potentially be valid across network or blockchain.
- **`Outputs`** is an array of transferable output objects. Outputs must be sorted lexicographically by their serialized representation. The total quantity of the assets created in these outputs must be less than or equal to the total quantity of each asset consumed in the inputs minus the transaction fee.
- **`Inputs`** is an array of transferable input objects. Inputs must be sorted and unique. Inputs are sorted first lexicographically by their **`TxID`** and then by the **`UTXOIndex`** from low to high. If there are inputs that have the same **`TxID`** and **`UTXOIndex`**, then the transaction is invalid as this would result in a double spend.

### Gantt Unsigned Base Tx Specification

```boo
+---------------+----------------------+-----------------------------------------+
| id            : int                  |                                 4 bytes |
+---------------+----------------------+-----------------------------------------+
| network_id    : int                  |                                 4 bytes |
+---------------+----------------------+-----------------------------------------+
| blockchain_id : [32]byte             |                                32 bytes |
+---------------+----------------------+-----------------------------------------+
| outputs       : []TransferableOutput |                 4 + size(outputs) bytes |
+---------------+----------------------+-----------------------------------------+
| inputs        : []TransferableInput  |                  4 + size(inputs) bytes |
+---------------+----------------------+-----------------------------------------+
                                       | 48 + size(outputs) + size(inputs) bytes |
                                       +-----------------------------------------+
```

### Proto Unsigned Base Tx Specification

```protobuf
message BaseTx {
    uint32 id = 1;               // 04 bytes
    uint32 network_id = 2;       // 04 bytes
    bytes blockchain_id = 3;     // 32 bytes
    repeated Output outputs = 4; // 04 bytes + size(outs)
    repeated Input inputs = 5;   // 04 bytes + size(ins)
}
```

### Unsigned Base Tx Example

Let's make an unsigned base tx that uses the inputs and outputs from the previous examples:

- `ID`: `0`
- `NetworkID`: `3`
- `BlockchainID`: `0xffffffffeeeeeeeeddddddddcccccccbbbbbbbbaaaaaaaa9999999988888888`
- **`Outputs`**:
  - `"Example Transferable Output as defined above"`
- **`Inputs`**:
  - `"Example Transferable Input as defined above"`

```splus
[
    ID           <- 0 = 0x00000000
    NetworkID    <- 3 = 0x00000003
    BlockchainID <- 0xffffffffeeeeeeeeddddddddcccccccbbbbbbbbaaaaaaaa9999999988888888
    Outputs      <- [
        0x000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f000000070000000000003039000000000000d431000000010000000251025c61fbcfc078f69334f834be6dd26d55a955c3344128e060128ede3523a24a461c8943ab0859
    ]
    Inputs       <- [
        0xf1e1d1c1b1a191817161514131211101f0e0d0c0b0a09080706050403020100000000005000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f0000000500000000075bcd15000000020000000300000007
    ]
]
=
[
    // id:
    0x00, 0x00, 0x00, 0x00,
    // networkID:
    0x00, 0x00, 0x00, 0x03,
    // blockchainID:
    0xff, 0xff, 0xff, 0xff, 0xee, 0xee, 0xee, 0xee,
    0xdd, 0xdd, 0xdd, 0xdd, 0xcc, 0xcc, 0xcc, 0xcc,
    0xbb, 0xbb, 0xbb, 0xbb, 0xaa, 0xaa, 0xaa, 0xaa,
    0x99, 0x99, 0x99, 0x99, 0x88, 0x88, 0x88, 0x88,
    // number of outputs:
    0x00, 0x00, 0x00, 0x01,
    // transferable output:
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
    0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
    0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
    0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f,
    0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x30, 0x39, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0xd4, 0x31, 0x00, 0x00, 0x00, 0x01,
    0x00, 0x00, 0x00, 0x02, 0x51, 0x02, 0x5c, 0x61,
    0xfb, 0xcf, 0xc0, 0x78, 0xf6, 0x93, 0x34, 0xf8,
    0x34, 0xbe, 0x6d, 0xd2, 0x6d, 0x55, 0xa9, 0x55,
    0xc3, 0x34, 0x41, 0x28, 0xe0, 0x60, 0x12, 0x8e,
    0xde, 0x35, 0x23, 0xa2, 0x4a, 0x46, 0x1c, 0x89,
    0x43, 0xab, 0x08, 0x59,
    // number of inputs:
    0x00, 0x00, 0x00, 0x01,
    // transferable input:
    0xf1, 0xe1, 0xd1, 0xc1, 0xb1, 0xa1, 0x91, 0x81,
    0x71, 0x61, 0x51, 0x41, 0x31, 0x21, 0x11, 0x01,
    0xf0, 0xe0, 0xd0, 0xc0, 0xb0, 0xa0, 0x90, 0x80,
    0x70, 0x60, 0x50, 0x40, 0x30, 0x20, 0x10, 0x00,
    0x00, 0x00, 0x00, 0x05, 0x00, 0x01, 0x02, 0x03,
    0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b,
    0x0c, 0x0d, 0x0e, 0x0f, 0x10, 0x11, 0x12, 0x13,
    0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b,
    0x1c, 0x1d, 0x1e, 0x1f, 0x00, 0x00, 0x00, 0x05,
    0x00, 0x00, 0x00, 0x00, 0x07, 0x5b, 0xcd, 0x15,
    0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x03,
    0x00, 0x00, 0x00, 0x07,
]
```

***

### Unsigned Create Asset Tx Identifier

The transaction identifier for a create asset tx is `0x00000001`.

### What Unsigned Create Asset Tx Contains

An unsigned create asset tx contains a `BaseTx`, `Name`, `Symbol`, `Denomination`, and `InitialStates`.

- **`ID`** is defined in `BaseTx`. For a create asset tx, the ID is `0x00000001`.
- **`Name`** is a human readable string that defines the name of the asset this transaction will create. The name is not guaranteed to be unique. The name must consist of only printable ASCII characters and must be no longer than 128 characters.
- **`Symbol`** is a human readable string that defines the symbol of the asset this transaction will create. The symbol is not guaranteed to be unique. The symbol must consist of only printable ASCII characters and must be no longer than 4 characters.
- **`Denomination`** is a byte that defines the divisibility of the asset this transaction will create. For example, the AVAX token is divisible into billionths. Therefore, the denomination of the AVAX token is 9. The denomination must be no more than 32.
- **`InitialStates`** is a variable length array that defines the feature extensions this asset supports, and the initial state of those feature extensions.

### Gantt Unsigned Create Asset Tx Specification

```boo
+----------------+----------------+--------------------------------------+
| base_tx        : BaseTx         |                  size(base_tx) bytes |
+----------------+----------------+--------------------------------------+
| name           : string         |                  2 + len(name) bytes |
+----------------+----------------+--------------------------------------+
| symbol         : string         |                2 + len(symbol) bytes |
+----------------+----------------+--------------------------------------+
| denomination   : byte           |                              1 bytes |
+----------------+----------------+--------------------------------------+
| initial_states : []InitialState |       4 + size(initial_states) bytes |
+----------------+----------------+--------------------------------------+
                                  | size(base_tx) + size(initial_states) |
                                  |  + 9 + len(name) + len(symbol) bytes |
                                  +--------------------------------------+
```

### Proto Unsigned Create Asset Tx Specification

```protobuf
message CreateAssetTx {
    BaseTx base_tx = 1;                       // size(base_tx)
    string name = 2;                          // 2 bytes + len(name)
    name symbol = 3;                          // 2 bytes + len(symbol)
    uint8 denomination = 4;                   // 1 bytes
    repeated InitialState initial_states = 5; // 4 bytes + size(initial_states)
}
```

### Unsigned Create Asset Tx Example

Let's make an unsigned base tx that uses the inputs and outputs from the previous examples:

- `BaseTx`: `"Example BaseTx as defined above with ID set to 1"`
- `Name`: `Volatility Index`
- `Symbol`: `VIX`
- `Denomination`: `2`
- **`InitialStates`**:
  - `"Example Initial State as defined above"`

```splus
[
    BaseTx        <- 0x0000000100000003ffffffffeeeeeeeeddddddddccccccccbbbbbbbbaaaaaaaa999999998888888800000001000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f000000070000000000003039000000000000d431000000010000000251025c61fbcfc078f69334f834be6dd26d55a955c3344128e060128ede3523a24a461c8943ab085900000001f1e1d1c1b1a191817161514131211101f0e0d0c0b0a09080706050403020100000000005000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f0000000500000000075bcd15000000020000000300000007
    Name          <- "Volatility Index" = 0x0010566f6c6174696c69747920496e646578
    Symbol        <- "VIX" = 0x0003564958
    Denomination  <- 2 = 0x02
    InitialStates <- [
        0x0000000000000001000000070000000000003039000000000000d431000000010000000251025c61fbcfc078f69334f834be6dd26d55a955c3344128e060128ede3523a24a461c8943ab0859,
    ]
]
=
[
    // base tx:
    0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x03,
    0xff, 0xff, 0xff, 0xff, 0xee, 0xee, 0xee, 0xee,
    0xdd, 0xdd, 0xdd, 0xdd, 0xcc, 0xcc, 0xcc, 0xcc,
    0xbb, 0xbb, 0xbb, 0xbb, 0xaa, 0xaa, 0xaa, 0xaa,
    0x99, 0x99, 0x99, 0x99, 0x88, 0x88, 0x88, 0x88,
    0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x02, 0x03,
    0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b,
    0x0c, 0x0d, 0x0e, 0x0f, 0x10, 0x11, 0x12, 0x13,
    0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b,
    0x1c, 0x1d, 0x1e, 0x1f, 0x00, 0x00, 0x00, 0x07,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x30, 0x39,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xd4, 0x31,
    0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x02,
    0x51, 0x02, 0x5c, 0x61, 0xfb, 0xcf, 0xc0, 0x78,
    0xf6, 0x93, 0x34, 0xf8, 0x34, 0xbe, 0x6d, 0xd2,
    0x6d, 0x55, 0xa9, 0x55, 0xc3, 0x34, 0x41, 0x28,
    0xe0, 0x60, 0x12, 0x8e, 0xde, 0x35, 0x23, 0xa2,
    0x4a, 0x46, 0x1c, 0x89, 0x43, 0xab, 0x08, 0x59,
    0x00, 0x00, 0x00, 0x01, 0xf1, 0xe1, 0xd1, 0xc1,
    0xb1, 0xa1, 0x91, 0x81, 0x71, 0x61, 0x51, 0x41,
    0x31, 0x21, 0x11, 0x01, 0xf0, 0xe0, 0xd0, 0xc0,
    0xb0, 0xa0, 0x90, 0x80, 0x70, 0x60, 0x50, 0x40,
    0x30, 0x20, 0x10, 0x00, 0x00, 0x00, 0x00, 0x05,
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
    0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
    0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
    0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f,
    0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x00,
    0x07, 0x5b, 0xcd, 0x15, 0x00, 0x00, 0x00, 0x02,
    0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x07,
    // name:
    0x00, 0x10, 0x56, 0x6f, 0x6c, 0x61, 0x74, 0x69,
    0x6c, 0x69, 0x74, 0x79, 0x20, 0x49, 0x6e, 0x64,
    0x65, 0x78,
    // symbol:
    0x00, 0x03, 0x56, 0x49, 0x58,
    // denomination:
    0x02,
    // number of InitialStates:
    0x00, 0x00, 0x00, 0x01,
    // InitialStates[0]:
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01,
    0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x30, 0x39, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0xd4, 0x31, 0x00, 0x00, 0x00, 0x01,
    0x00, 0x00, 0x00, 0x02, 0x51, 0x02, 0x5c, 0x61,
    0xfb, 0xcf, 0xc0, 0x78, 0xf6, 0x93, 0x34, 0xf8,
    0x34, 0xbe, 0x6d, 0xd2, 0x6d, 0x55, 0xa9, 0x55,
    0xc3, 0x34, 0x41, 0x28, 0xe0, 0x60, 0x12, 0x8e,
    0xde, 0x35, 0x23, 0xa2, 0x4a, 0x46, 0x1c, 0x89,
    0x43, 0xab, 0x08, 0x59,
]
```

***

### Unsigned Operation Tx Identifier

The transaction identifier for an operation tx is `0x00000002`.

### What Unsigned Operation Tx Contains

An unsigned operation tx contains a `BaseTx`, and `Ops`.

- **`ID`** is defined in `BaseTx`. For an operation tx, the ID is `0x00000002`.
- **`Ops`** is a variable length array of Transferable Ops.

### Gantt Unsigned Operation Tx Specification

```boo
+---------+--------------+-------------------------------------+
| base_tx : BaseTx       |                 size(base_tx) bytes |
+---------+--------------+-------------------------------------+
| ops     : []TransferOp |                 4 + size(ops) bytes |
+---------+--------------+-------------------------------------+
                         | 4 + size(ops) + size(base_tx) bytes |
                         +-------------------------------------+
```

### Proto Unsigned Operation Tx Specification

```protobuf
message OperationTx {
    BaseTx base_tx = 1;          // size(base_tx)
    repeated TransferOp ops = 2; // 4 bytes + size(ops)
}
```

### Unsigned Operation Tx Example

Let's make an unsigned operation tx that uses the inputs and outputs from the previous examples:

- `BaseTx`: `"Example BaseTx as defined above with ID set to 2"`
- **`Ops`**:
  - `"Example NFT Transfer Op as defined above"`

```splus
[
    BaseTx        <- 0x0000000200000003ffffffffeeeeeeeeddddddddccccccccbbbbbbbbaaaaaaaa999999998888888800000001000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f000000070000000000003039000000000000d431000000010000000251025c61fbcfc078f69334f834be6dd26d55a955c3344128e060128ede3523a24a461c8943ab085900000001f1e1d1c1b1a191817161514131211101f0e0d0c0b0a09080706050403020100000000005000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f0000000500000000075bcd15000000020000000300000007
    Ops <- [
        0x000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f00000001f1e1d1c1b1a191817161514131211101f0e0d0c0b0a090807060504030201000000000050000000d0000000200000003000000070000303900000003431100000000010000000251025c61fbcfc078f69334f834be6dd26d55a955c3344128e060128ede3523a24a461c8943ab0859,
    ]
]
=
[
    // base tx:
    0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x03,
    0xff, 0xff, 0xff, 0xff, 0xee, 0xee, 0xee, 0xee,
    0xdd, 0xdd, 0xdd, 0xdd, 0xcc, 0xcc, 0xcc, 0xcc,
    0xbb, 0xbb, 0xbb, 0xbb, 0xaa, 0xaa, 0xaa, 0xaa,
    0x99, 0x99, 0x99, 0x99, 0x88, 0x88, 0x88, 0x88,
    0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x02, 0x03,
    0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b,
    0x0c, 0x0d, 0x0e, 0x0f, 0x10, 0x11, 0x12, 0x13,
    0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b,
    0x1c, 0x1d, 0x1e, 0x1f, 0x00, 0x00, 0x00, 0x07,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x30, 0x39,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xd4, 0x31,
    0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x02,
    0x51, 0x02, 0x5c, 0x61, 0xfb, 0xcf, 0xc0, 0x78,
    0xf6, 0x93, 0x34, 0xf8, 0x34, 0xbe, 0x6d, 0xd2,
    0x6d, 0x55, 0xa9, 0x55, 0xc3, 0x34, 0x41, 0x28,
    0xe0, 0x60, 0x12, 0x8e, 0xde, 0x35, 0x23, 0xa2,
    0x4a, 0x46, 0x1c, 0x89, 0x43, 0xab, 0x08, 0x59,
    0x00, 0x00, 0x00, 0x01, 0xf1, 0xe1, 0xd1, 0xc1,
    0xb1, 0xa1, 0x91, 0x81, 0x71, 0x61, 0x51, 0x41,
    0x31, 0x21, 0x11, 0x01, 0xf0, 0xe0, 0xd0, 0xc0,
    0xb0, 0xa0, 0x90, 0x80, 0x70, 0x60, 0x50, 0x40,
    0x30, 0x20, 0x10, 0x00, 0x00, 0x00, 0x00, 0x05,
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
    0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
    0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
    0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f,
    0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x00,
    0x07, 0x5b, 0xcd, 0x15, 0x00, 0x00, 0x00, 0x02,
    0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x07,
    // number of operations:
    0x00, 0x00, 0x00, 0x01,
    // transfer operation:
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
    0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
    0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
    0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f,
    0x00, 0x00, 0x00, 0x01, 0xf1, 0xe1, 0xd1, 0xc1,
    0xb1, 0xa1, 0x91, 0x81, 0x71, 0x61, 0x51, 0x41,
    0x31, 0x21, 0x11, 0x01, 0xf0, 0xe0, 0xd0, 0xc0,
    0xb0, 0xa0, 0x90, 0x80, 0x70, 0x60, 0x50, 0x40,
    0x30, 0x20, 0x10, 0x00, 0x00, 0x00, 0x00, 0x05,
    0x00, 0x00, 0x00, 0x0d, 0x00, 0x00, 0x00, 0x02,
    0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x07,
    0x00, 0x00, 0x30, 0x39, 0x00, 0x00, 0x00, 0x03,
    0x43, 0x11, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00,
    0x00, 0x00, 0x02, 0x51, 0x02, 0x5c, 0x61, 0xfb,
    0xcf, 0xc0, 0x78, 0xf6, 0x93, 0x34, 0xf8, 0x34,
    0xbe, 0x6d, 0xd2, 0x6d, 0x55, 0xa9, 0x55, 0xc3,
    0x34, 0x41, 0x28, 0xe0, 0x60, 0x12, 0x8e, 0xde,
    0x35, 0x23, 0xa2, 0x4a, 0x46, 0x1c, 0x89, 0x43,
    0xab, 0x08, 0x59,
]
```

***

## Signed Transaction

A signed transaction is an unsigned transaction with the addition of an array of credentials.

### What Signed Transaction Contains

A signed transaction contains an `UnsignedTx`, `Credentials`.

- **`UnsignedTx`** is an unsigned transaction, as described above.
- **`Credentials`** is an array of credentials. Each credential will be paired with the input in the same index at this credential.

### Gantt Signed Transaction Specification

```boo
+-------------+--------------+------------------------------------------------+
| unsigned_tx : UnsignedTx   |                        size(unsigned_tx) bytes |
+-------------+--------------+------------------------------------------------+
| credentials : []Credential |                    4 + size(credentials) bytes |
+-------------+--------------+------------------------------------------------+
                             | 4 + size(unsigned_tx) + len(credentials) bytes |
                             +------------------------------------------------+
```

### Proto Signed Transaction Specification

```protobuf
message Tx {
    UnsignedTx unsigned_tx = 1;          // size(unsigned_tx)
    repeated Credential credentials = 2; // 4 bytes + size(credentials)
}
```

### Signed Transaction Example

Let's make a signed transaction that uses the unsigned transaction and credential from the previous examples.

- **`UnsignedTx`**: `0x0000000000000003ffffffffeeeeeeeeddddddddccccccccbbbbbbbbaaaaaaaa999999998888888800000001000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f000000070000000000003039000000000000d431000000010000000251025c61fbcfc078f69334f834be6dd26d55a955c3344128e060128ede3523a24a461c8943ab085900000001f1e1d1c1b1a191817161514131211101f0e0d0c0b0a09080706050403020100000000005000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f0000000500000000075bcd15000000020000000300000007`
- **`Credentials`**
  - `0x0000000900000002000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1e1d1f202122232425262728292a2b2c2e2d2f303132333435363738393a3b3c3d3e3f00404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5e5d5f606162636465666768696a6b6c6e6d6f707172737475767778797a7b7c7d7e7f00`

```splus
[
    UnsignedTx  <- 0x0000000000000003ffffffffeeeeeeeeddddddddccccccccbbbbbbbbaaaaaaaa999999998888888800000001000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f000000070000000000003039000000000000d431000000010000000251025c61fbcfc078f69334f834be6dd26d55a955c3344128e060128ede3523a24a461c8943ab085900000001f1e1d1c1b1a191817161514131211101f0e0d0c0b0a09080706050403020100000000005000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f0000000500000000075bcd15000000020000000300000007
    Credentials <- [
        0x0000000900000002000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1e1d1f202122232425262728292a2b2c2e2d2f303132333435363738393a3b3c3d3e3f00404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5e5d5f606162636465666768696a6b6c6e6d6f707172737475767778797a7b7c7d7e7f00,
    ]
]
=
[
    // unsigned transaction:
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03,
    0xff, 0xff, 0xff, 0xff, 0xee, 0xee, 0xee, 0xee,
    0xdd, 0xdd, 0xdd, 0xdd, 0xcc, 0xcc, 0xcc, 0xcc,
    0xbb, 0xbb, 0xbb, 0xbb, 0xaa, 0xaa, 0xaa, 0xaa,
    0x99, 0x99, 0x99, 0x99, 0x88, 0x88, 0x88, 0x88,
    0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x02, 0x03,
    0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b,
    0x0c, 0x0d, 0x0e, 0x0f, 0x10, 0x11, 0x12, 0x13,
    0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b,
    0x1c, 0x1d, 0x1e, 0x1f, 0x00, 0x00, 0x00, 0x07,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x30, 0x39,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xd4, 0x31,
    0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x02,
    0x51, 0x02, 0x5c, 0x61, 0xfb, 0xcf, 0xc0, 0x78,
    0xf6, 0x93, 0x34, 0xf8, 0x34, 0xbe, 0x6d, 0xd2,
    0x6d, 0x55, 0xa9, 0x55, 0xc3, 0x34, 0x41, 0x28,
    0xe0, 0x60, 0x12, 0x8e, 0xde, 0x35, 0x23, 0xa2,
    0x4a, 0x46, 0x1c, 0x89, 0x43, 0xab, 0x08, 0x59,
    0x00, 0x00, 0x00, 0x01, 0xf1, 0xe1, 0xd1, 0xc1,
    0xb1, 0xa1, 0x91, 0x81, 0x71, 0x61, 0x51, 0x41,
    0x31, 0x21, 0x11, 0x01, 0xf0, 0xe0, 0xd0, 0xc0,
    0xb0, 0xa0, 0x90, 0x80, 0x70, 0x60, 0x50, 0x40,
    0x30, 0x20, 0x10, 0x00, 0x00, 0x00, 0x00, 0x05,
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
    0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
    0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
    0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f,
    0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x00,
    0x07, 0x5b, 0xcd, 0x15, 0x00, 0x00, 0x00, 0x02,
    0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x07,
    // number of credentials:
    0x00, 0x00, 0x00, 0x01,
    // credential[0]:
    0x00, 0x00, 0x00, 0x09, 0x00, 0x00, 0x00, 0x02,
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
    0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
    0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
    0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1e, 0x1d, 0x1f,
    0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27,
    0x28, 0x29, 0x2a, 0x2b, 0x2c, 0x2e, 0x2d, 0x2f,
    0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37,
    0x38, 0x39, 0x3a, 0x3b, 0x3c, 0x3d, 0x3e, 0x3f,
    0x00, 0x40, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46,
    0x47, 0x48, 0x49, 0x4a, 0x4b, 0x4c, 0x4d, 0x4e,
    0x4f, 0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56,
    0x57, 0x58, 0x59, 0x5a, 0x5b, 0x5c, 0x5e, 0x5d,
    0x5f, 0x60, 0x61, 0x62, 0x63, 0x64, 0x65, 0x66,
    0x67, 0x68, 0x69, 0x6a, 0x6b, 0x6c, 0x6e, 0x6d,
    0x6f, 0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76,
    0x77, 0x78, 0x79, 0x7a, 0x7b, 0x7c, 0x7d, 0x7e,
    0x7f, 0x00,
```

***

## UTXO

A utxo is a standalone representation of a transaction output.

### What UTXO Contains

A UTXO contains signed transaction contains a `TxID`, `UTXOIndex`, and `Output`.

- **`TxID`** is a 32-byte transaction ID. Transaction IDs are calculated by taking sha256 of the bytes of the signed transaction.
- **`UTXOIndex`** is an int that specifies which output in the transaction specified by **`TxID`** that this utxo was created by.
- **`AssetID`** is a 32-byte array that defines which asset this utxo references.
- **`Output`** is the output object that created this utxo. The serialization of Outputs was defined above.

### Gantt UTXO Specification

```boo
+--------------+----------+-------------------------+
| tx_id        : [32]byte |                32 bytes |
+--------------+----------+-------------------------+
| output_index : int      |                 4 bytes |
+--------------+----------+-------------------------+
| asset_id     : [32]byte |                32 bytes |
+--------------+----------+-------------------------+
| output       : Output   |      size(output) bytes |
+--------------+----------+-------------------------+
                          | 68 + size(output) bytes |
                          +-------------------------+
```

### Proto UTXO Specification

```protobuf
message Utxo {
    bytes tx_id = 1;         // 32 bytes
    uint32 output_index = 2; // 04 bytes
    bytes asset_id = 3;      // 32 bytes
    Output output = 4;       // size(output)
}
```

### UTXO Example

Let's make a UTXO from the signed transaction created above:

- **`TxID`**: `0xf966750f438867c3c9828ddcdbe660e21ccdbb36a9276958f011ba472f75d4e7`
- **`UTXOIndex`**: 0 = 0x00000000
- **`AssetID`**: `0x000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f`
- **`Output`**: `"Example SECP256K1 Transferable Output as defined above"`

```splus
[
    TxID      <- 0xf966750f438867c3c9828ddcdbe660e21ccdbb36a9276958f011ba472f75d4e7
    UTXOIndex <- 0x00000000
    AssetID   <- 0x000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f
    Output    <-     0x000000070000000000003039000000000000d431000000010000000251025c61fbcfc078f69334f834be6dd26d55a955c3344128e060128ede3523a24a461c8943ab0859
]
=
[
    // txID:
    0xf9, 0x66, 0x75, 0x0f, 0x43, 0x88, 0x67, 0xc3,
    0xc9, 0x82, 0x8d, 0xdc, 0xdb, 0xe6, 0x60, 0xe2,
    0x1c, 0xcd, 0xbb, 0x36, 0xa9, 0x27, 0x69, 0x58,
    0xf0, 0x11, 0xba, 0x47, 0x2f, 0x75, 0xd4, 0xe7,
    // utxo index:
    0x00, 0x00, 0x00, 0x00,
    // assetID:
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
    0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
    0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
    0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f,
    // output:
    0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x30, 0x39, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0xd4, 0x31, 0x00, 0x00, 0x00, 0x01,
    0x00, 0x00, 0x00, 0x02, 0x00, 0x01, 0x02, 0x03,
    0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b,
    0x0c, 0x0d, 0x0e, 0x0f, 0x10, 0x11, 0x12, 0x13,
    0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b,
    0x1c, 0x1d, 0x1e, 0x1f, 0x20, 0x21, 0x22, 0x23,
    0x24, 0x25, 0x26, 0x27,
]
```
