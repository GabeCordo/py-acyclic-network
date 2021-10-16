# Library Standards
These standards attempt to enforce consistency across the codebase to assist developers that wish to read or understand the source code.

## Naming Conventions
All identifiers must follow these conventions to better identify types derived from the package.

1. CamelCase for all Classes and Functions
    1. N prefix for extensions of modules that manipulate the default network code.
    2. R prefix for extensions of the Relay Node.
    3. B prefix for extensions of the Balancer Node.
    4. I prefix for extensions of the Indexer Node.
    5. EY prefix for extensions of the Entry Node.
    6. ET prefix for extensions of the Exit Node.
2. Snake_Case for all Variables
    1. _p object reference
    2. _e enumerators
    3. _s classes acting as structs
    4. _t for unique types defined
    5. _g for generic variables
3. Capitalization for Constants

## Commenting Conventions
Comments should follow a standard format, making it easy to understand the arguments, expected outcomes, and possible errors associated with a codebase.

1. File Comments
```
[File Name]
:this is a description of the python module
			
@author(s) **a list of individuals who worked on the file**
@created **the date the file was created**
@last-edit **the date the file was last edited**
@common **what all the functions / structs / types have in common within the file**
@use-case **the use case for the module, when it should be used, etc.**
```

2. Import Comments
Group common imports from the sys, src, cli, gui, or util libraries when there is lots of imports.

3. Class Comments
```
[Class Name]
:this is a description of the function
			
@purpose **why the class is important / how it helps the user**
@use-case **where the class should, and should not be used**
```

4. Function Comments
```
(parameters) -> (output)
:this is a description of the function
			
@parameters **textually identify specific parameter requirements**
@returns **textually identify what should be returned**
@except **textually identify what is expected when the function fails**
```

## Global Conventions
Python files or sub-directories that MAY be used by one or many codebase must be put in the root src directory.

1. Constants should be placed in src/constants.py
2. Functions useful between all sub-directories should be placed in src/utils/*.py