###############################
# core imports
###############################

from pyacyclicnet.core.network.node import Node
from pyacyclicnet.core.bitstream import advanced
from pyacyclicnet.core.types import errors, enums, containers
from pyacyclicnet.core.types.result import Result
from pyacyclicnet.core.types.decorators import overrides

###############################
#		   main code
###############################
#Responsible for routing the packet to the next relay or exit node

class NodeRelay(Node):
	def __init__(self, container_addresses, container_paths) -> None:
		'''(NodeRelay, string, string, string, string) -> None
			:constructor for the NodeRelay class, sets up the relay node
			 server
		'''
		super().__init__(container_addresses, container_paths, containers.PRESET_SETTINGS_RELAY)
		
	def discover_next_node(self, bitsream) -> Result(list(str), Exception):
		'''(NodeRelay, string) -> (list of strings)
			:discover the next relay node for communication and modify the
			 path
			
			@paramaters a valid bitsream syntax is provided
			@returns a list of strings [the next relay node id, the modified
					 pathway, exitpath]
			@exception returns an empty list if the paramaters are not followed
		'''
		modify = advanced.Parser(bitsream)
		
		#retrieve the path ids and the ip-address of the exit node
		pathway = modify.get_relay_path()
		node_exit = modify.get_exit_node()
		
		#see whether to modify the relay path or exit node path
		try:
			relay_all = pathway.split(':')
			relay_encrypted = relay_all.pop(0)
			relay_next = self.handler_keys.decrypt(relay_encrypted)
		except Exception:
			node_exit = self.handler_keys.decrypt(node_exit)
		
		#[ only the last node, every relay but the last node, exitNode IP ]
		return [ relay_next, ':'.join(relay_all), node_exit ]
		
	@overrides(Node)
	def special_functionality(self, message, connecting_address):
		'''(Node, string, string) -> (boolean)
			:handles all relay requests made to the server
			
			@returns boolean False indicating that messages will NOT be enqueued
					 to a queue
		'''
		#extract the bitsream mapped route from the former entry or relay node
		resend_data = self.discoverNextNode(message)
		
		#if the next relay node is blank, this means that it needs to be sent to the exit node
		#as it is done meshing/anonamizing through the network
		if (resend_data[0] == ''):
			self.send(resend_data[2], message)
		#the bitsream still needs to be send through the network
		else:
			message_modified = modify.replace_paths(resend_data[1], resend_data[2])
			self.send(next_relay_ip, message_modified)
		
		#the relay node should only redirect data, it should never do anything else
		#(we want to avoid users capturing any traffic on the network)
		return (False, 'Successfully Handled')