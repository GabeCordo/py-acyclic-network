![](/docs/diagrams/terminal.png)

# py-acyclic-network
This project has been active since September 2019.

## Description

Venezia is a pythonic framework for developing decentralized networks, providing encrypted routing, and fault-tolerance through seen in Erlang and Elixir within Python.

* TCP Socket Networking 
* Default asymmetric encryption (RSA keysets) and salting that can be toggled
* Out of the box packet-routing (tor-like) capabilities for message-origin concealment
	1. Relays
	2. Entry/Exit Nodes
	3. Indexing Server (Creating IP-ID Account related pairs)
* Customizable Traffic Receivers/Transfer Routines

### Dependencies
Development and testing done with Python >= 3.7.9, other packages required to run the CLI and web-portal include:

* pycryptodomex==3.10.1
* clint==0.5.1
* pyyaml==5.4.1
* cffi==1.15.0
* pyfiglet==0.8.post1

### Installation
As of right now, the only way to install the program is to create a local pip installation.

* Navigate to the root folder.

	```python install -r requirements.txt```

	```pip3 install .```

* Validate the installation

	```pip3 show pyacyclicnet```
	
	###### If the installation is valid, pip will return information about the installed package.



### Further Reading
This README.md is limited to avoid overloading you with information. If you want to understand some of the decisions behind the design or how to contribute, these resources can help to get you started.

* [Documentation](https://github.com/GabeCordo/py-acyclic-network/tree/master/docs/reference.md) - design explanations and how to set up your network.
* [Framework](https://github.com/GabeCordo/py-acyclic-network/tree/master/docs/functions.md) - available functions, paramaters, use-cases. 
* [Standards](https://github.com/GabeCordo/py-acyclic-network/tree/master/docs/standards.md) - read this before contributing to the project.

## Credits

> Gabriel Cordovado

[![DigitalOcean Referral Badge](https://web-platforms.sfo2.digitaloceanspaces.com/WWW/Badge%203.svg)](https://www.digitalocean.com/?refcode=8e25aa8fe5cb&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge)