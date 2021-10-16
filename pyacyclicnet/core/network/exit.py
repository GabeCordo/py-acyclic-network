###############################
# core imports
###############################

from pyacyclicnet.core.network.node import Node
from pyacyclicnet.core.bitstream import advanced
from pyacyclicnet.core.types import errors, enums, containers

from pyacyclicnet.core.types.decorators import overrides

###############################
# main code
###############################
#Responsible for sending the message request to the final destination in the userid

class NodeExit(Node):
	def __init__(self, container_addresses, container_paths):
		'''(NodeExit, string, string, string, string) -> None
			:the constructor is the same as the node server, small manipulation
			 of the original node server to specifically redirect data to the
			 final ip
		'''
		super().__init__(container_addresses, container_paths, containers.PRESET_SETTINGS_EXIT)
	
	def check_destination(self, id_origin):
		'''(Node) -> (string)
			:retrieves the ip-address of the userid inputted from the index server
				
			@returns the string representation of the ip-address associated with
					 the userid
			@exception if the connection is lost or the userid is invalid, returns
					   an empty string
		'''
		request = f'0:{id_origin}'
		return self.send(self.container_addresses.ip_index, request) #settup ip and port of indexing server
	
	def format_message(self, message, origin):
		'''(NodeExit, string) -> (string)
			:strip the advanced bitsream into a simpler form with less useless data
			 for the user and pass that to the specialFunctionality function
			
			@returns list with a simple bitsream 'request:message/origin_id' and
					 the destination id
		'''
		return f'4:{message}~{origin}'
	
	@overrides(Node)
	def special_functionality(self, message, connecting_address):
		'''(Node, string, string) -> (boolean)
			:handles all messages sent to the final recipient of the message/
			 request that has transversed through the relay network
			
			@returns boolean False indicating that messages will NOT be enqueued
					 to a queue
		'''
		modify = advanced.Parser(message)
		
		request = modify.get_request_type()
		#we need the origin in case a message needs to be sent back
		origin = modify.get_origin_id()
		destination = self.checkDestination(modify.get_target_id())
		
		#if we are sending a standard message
		if (request == '4'):
			message_formated = self.formatMessage(message, origin)
			#send to the target_id's ip on the index server on the default port for 8074
			self.send(destination, message_formated)
			
		#we shouldn't need any functionality other than sending data to a user's computer
		return (False, 'Successfully Handled')
	