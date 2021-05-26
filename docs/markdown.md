# Venezia Markdown
Data is encapsulated in containers, containing metadata pre-and-post fixes around square brackets.

## Identifiers
Identifiers are metadata prefixed to the encapsulated data to identify the meaning or purpose of information. Identifiers can be reserved keywords that are used by the markdown interpreter to unwrap data patterns common between multiple nodes.

1. request
2. request
3. pathway
4. destination

## Data
Data is the associative information tied to the identifier. It can be further encapsulated containers or a list of data-components separated with the data_separator symbol. 

## Handlers
Handlers are metadata postfixed to the encapsulated data to identify how the data should be processed, or who the data should be sent to.


## Symbols
Symbols are used to separate data elements of the markdown, they cannot be used within the prefix, postfix, or data portions of the markdown

1. data_start [
2. data_end ]
3. data_separator ~
4. handler_start (
5. handler_end )

```
A: request[[ B ]](origin_identifier)
B: pathway[[ C ]](list~~of~~nodes)
C: message[[ data ]](destination_identifier)
```

### Example 1
For communications between two nodes with no pathway

```
request[[origin[[destination[[(data)]](value)]](value)]](value)
```

### Example 2
For communications between two nodes with a pathway

```
request[[pathway[[origin[[destination[[(data)]](value)]](value)]](d~~a~~t~~a)]](value)
```

