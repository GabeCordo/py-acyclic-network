# Acyclic Packet Protocol
The acyclic packet protocol is a basic format for routing-based TCP streams between multiple network nodes. This helps to standardize a parsing processes within each node and enforce certain parameters to be included in each transmission that guarantee: (1) route, (2) authenticator to validate no man-in-the-middle (MITM) attack has occurred, (3) identify a common PAT node to use along the routing-chain. If you haven't already, please read the [project manual](reference.md) to understand why it is important to contain these pieces of data within each data-transmission.

#### **Current Version** 0.0.1
#### **Release Date** 15-09-2021

---

## Syntax

| Section  | i0           | i1  | i2  | i3  | i4  |
| -------- |:-------------:| -----:| -----:| -----:| -----:|
| 1        | request | pat_id | pat_auth | next_node | idp_ip
| 2        | node_1      |   node_2 | ... | ... | node_n |
| 3        | data_start | ... | ... | ... | data_end

### Sections
+ Metadata (1)
+ Pathway (2)
+ Data (3)
### Reserved Keywords and Chars
+ <> Sections Separator

    Symbols are used to separate data elements of the markdown, they cannot be used within the prefix, postfix, or data portions of the markdown

+ :: Value Separator
+ \* Special Character Prefix
+ << End of File

---
## Examples

### Example 1
Packet without any special character prefixes.

```
request::pat_id::pat_auth::node0::idp_ip<>node1::node2::node3::node4<>Hello stranger.<<

Header -> request::pat_id::pat_auth::node0::idp_ip
          <>
Path   -> node1::node2::node3::node4
          <>
Data   -> Hello stranger.
          <<
```

### Example 2
Packet containing special character prefixes.

```
request::pat_id::pat_auth::node0::idp_ip<>node1::node2::node3::node4<>Hello*0 stran*1ger.<<

Header -> request::pat_id::pat_auth::node0::idp_ip
          <>
Path   -> node1::node2::node3::node4
          <>
Data   -> Hello*0 stran*1ger.
          <<
```

