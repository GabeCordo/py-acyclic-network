###############################
# core imports
###############################

from src.core.bitstream import basic
from src.core.network.node import Node
from src.core.types import errors, enums, containers

###############################
#		   main code
###############################
#Responisble for handling incoming connections that are to be fed through the tor network
# [we will want to keep the template (even if it can increase runtime by 0.01s, we NEED to
# [ensure a failproof transfer of data to more sensitive areas of the network

class NodeEntry(Node):
	def __init__(self, container_addresses, container_paths):
		'''
			(NodeEntry, string, string, string, string, boolean) -> None
			
			:constructor for the node entry class; provides all the connective
			 functionality to begin routing messages or act as a middle-man for
			 indexing/removing/lookingup userids on the index node
		'''
		super().__init__(container_addresses, container_paths, containers.PRESET_SETTINGS_ENTRY)
		
	def checkDestination(self, bitstream, id_origin):
		'''
			(NodeEntry, string, string) -> (string)
			:retrieves the ip-address of the userid inputed from the index server
			
			@returns the string representation of the ip-address associated with
					 the userid
			@exception if the connection is lost or the userid is invalid, returns
					 an empty string
		'''
		return self.send(self.container_addresses.ip_index, bitstream) #settup ip and port of indexing server
	
	def indexUserID(self, bitstream, id_origin, ip_connecting):
		'''
			(NodeEntry, string, string, string) -> (boolean)
			:add a new userid and ip-address match on the indexing node for
			 transmission
			
			@paramaters the userid must be unique and the ip must not have an id
						already indexed
			@returns a boolean true if the userid was added to the indexing node
			@exception returns boolean false if the userid or ip is already used
		'''
		return self.send(self.container_addresses.ip_index, bitstream)

	def deindexUserID(self, bitstream, id_origin, ip_connecting):
		'''
			(NodeEntry, string, string, string) -> (boolean)
			:remove a userid and ip-address match on the indexing node
			
			@paramaters the userid must be valid and the ip must be associated
						with the indexed id
			@returns a boolean true if the userid was removed from the indexing
					 node
			@exception returns boolean false if the paramaters were invalid
		'''
		return self.send(self.container_addresses.ip_index, bitstream)
		
	def useridOfAddress(self, bitstream, ip):
		'''
			(NodeEntry, string, string) -> (string)
			:finds the associated id with the connecting ip address
			
			** this is a private function, it is important only the
			   entry node has this functionality					 **
		'''
		return self.send(self.container_addresses.ip_index, bitstream)
		
	def formatMessage(self, bitstream, id_target, message):
		'''
			(NodeEntry, string, string, string, string) -> None
			:formats the data into an advanced parsable bitsream request for
			 transmitting messages
		'''
		#process the relay-web ready string
		message = self.send(self.container_addresses.ip_index, bitstream)
		data = message.split('%')
		print(data) #debugging
		#send the message to the target or into the network and get a status code
		check = self.send(data[0], data[1])
		return check
	
	def specialFunctionality(self, message, connectingAddress):
		'''
			(Node, string, string) -> (boolean)
			:handles all socket requests that pertain to the requests under
			 'entry node' in the docs
			
			@returns boolean False indicating that messages will NOT be
					 enqueued to a queue
		'''
		#validate syntax in-case the message hasn't been run through a balancer which verifies syntax
		try:
			b = basic.Parser(message)
			request = b.getRequest()
			
			data_first = b.getPrimaryData()
			data_second = b.getSecondaryData()
			
			#check to see if the message has been run through a balancer which appends the origin-ip to a third
			#spot, ELSE, append it (this might be the case when using a simplified network
			if (len(b.getOtherData()) == 0):
				message = message + f'~{connectingAddress}'
		except:
			return (False, '')
		
		#request to lookup index (most likely)
		if (request == '0'):
			check = self.checkDestination(message, data_first)
			return (False, check)
		#request to send a message
		elif (request == '4'):
			message = self.formatMessage(message, data_first, data_second) #data_first: target_id | data_second: data
			return (False, check)
		#request to add index
		elif (request == '2'):
			check = self.indexUserID(message, data_first, data_second) #data_first: userid | data_second: userip
			return (False, check)
		#request to delete index (least likely)
		elif (request == '3'):
			check = self.deindexUserID(message, data_first, data_second) #data_first: userid | data_second: userip
			return (False, check)
		
		#the message has been handled automaticly, there is no need to enqueue
		return (False, '400')
	