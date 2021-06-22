###############################
# core imports
###############################

from src.core.bitstream.basic import BasicParser
from src.core.network.node import Node
from src.core.linker.linkerJSON import LinkerJson
from src.core.types.enums import EnqueueRequest
from src.core.types import containers

from src.core.types.result import Result
from src.core.types.decorators import overrides

###############################
# main code
###############################


class NodeBalancer(Node):
	def __init__(self, container_addresses, container_paths, directory_entry_nodes):
		"""
			constructor for the Balancer class takes a list of ip-addresses
			representing the available entry Nodes.
		"""
		Node.__init__(self, container_addresses, container_paths, containers.PRESET_SETTINGS_BALANCER)
		
		json_handler = LinkerJson(directory_entry_nodes)
		self.nodes_entry = json_handler.data[0]
		self.trackers = [0] * len(self.nodes_entry)
	
	def track(self, ip):
		"""
			find the number of times traffic has been re-directed to a specific
			ip
			
			@returns an integer representing the number of re-directs
		"""
		index = self.nodes_entry.index(ip)
		return self.trackers[index]
		
	def redirect(self):
		"""
			find the entry node with the least re-directs and return it
			
			@returns a string of the ip-address with the least re-directs
		"""
		index = self.trackers.index(min(self.trackers))
		self.trackers[index] = self.trackers[index] + 1
		return self.nodes_entry[index]
		
	def syntax_validator(self, message: str) -> bool:
		"""
			validates whether the basic markup request is valid
			
			@returns nothing indicating it is valid
			@exception raises MismatchedSyntax() error if it is invalid
		"""
		BasicParser(message)  # will throw an error if this fails
		return True
	
	@overrides(Node)
	def special_functionality(self, message: str, connecting_address: str) \
		-> Result(tuple[EnqueueRequest, str], Exception):
		"""
		"""
		try:
			self.syntax_validator(message)  # will throw an error if invalid (hence, using try/catch)
			entry = self.redirect()
			# if the syntax is valid and we have a new entry node, send the message into the network
			message_modified = f'{message}~{connecting_address}'
			self.send(entry, message_modified)
		except Exception as e:
			# TODO - add log message
			return Result(None, e)
		
		# we always want this to return False, there is NO need to have any other functionality
		return Result(EnqueueRequest.PROCESSES, None)
