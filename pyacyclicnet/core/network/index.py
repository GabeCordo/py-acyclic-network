###############################
#		python imports
###############################
import random
from os import remove
from datetime import date
from threading import Thread

###############################
# core imports
###############################

from pyacyclicnet.core.crypto import rsa
from pyacyclicnet.core.bitstream import basic
from pyacyclicnet.core.network.node import Node
from pyacyclicnet.core.linker import linkerJSON
from pyacyclicnet.core.types import errors, enums, containers
from pyacyclicnet.core.types.decorators import overrides
from pyacyclicnet.core.types.result import Result

###############################
# main code
###############################
# This node is responsible for storing all SENSITIVE information, hence it is important
# that this node remain HIGHLY ANONYMOUS and can only receive connections from the entry
# node in such a way that it acts as a proxy to conceal the address or data of this node


class Index(Node, linkerJSON.Handler):
	def __init__(self, container_addresses, container_paths, 
				 directory_index, directory_log, directory_collected_keys, 
				 simplified_network = False):
		"""
			constructor method for the Index Class
			
			@parameters a valid pathway(directory) for all the user-id
						to ip-addr matches
			@exception the class constructor will throw an error if the
						pathway is NOT valid
		"""
		Node.__init__(self, container_addresses, container_paths, containers.PRESET_SETTINGS_INDEX)
		linkerJSON.Handler.__init__(self, directory_index, directory_log)
		
		# Setting up indexing, logging JSON files AND the RSA keys directory for storage
		self.directory_index = directory_index
		self.directory_log = directory_log
		self.directory_collected_keys = directory_collected_keys
		
		# Setup the indexing node to either run on simplified network mode or full mode
		self.simplified_network = simplified_network
		
		# Pull the extracted JSON sheets from the linkerJSON class variable 'self.data'
		self.index = self.data[0]
		self.log = self.data[1]
		
	def lookup_index(self, id_origin: str) -> Result(str, Exception):
		"""
			lookup an ip address associated with a certain id
			
			@parameters a valid userid on the index node is provided
			@returns the ip-address of a user-id in the index JSON file
			@exception if there is an error (id doesnt exist) an empty 
						string is returned
		"""
		try:
			return Result(self.index[id_origin]['ip'], None)
		except Exception as e:
			return Result(None, e)
	
	def lookup_ip(self, ip: str) -> Result(str, Exception):
		"""
			lookup the timestamp associate with the initialization of
			an ip with userid
			
			@parameters a valid ip-address on the index node is provided
			@returns the userid of a ip-address in the logger JSON file
			@exception if there is an error (ip doesn't exist) an empty 
					string is returned
		"""
		try:
			return Result(self.log[ip], None)
		except Exception as e:
			return Result(None, e)
	
	def add_rsa(self, id_origin: str, rsa_public: str) -> bool:
		"""
			this is a private function responsible for adding a new public
			encryption key file to the directory for all userid-keys
			
			@returns boolean true if the file was created successfully
			@exception returns boolean false if the file could not be made
			
				** files created with the formatted (userid).pem **
		"""
		try:
			f = open(self.index[id_origin]['rsa'], 'w')
			f.write(rsa_public)
			f.close()
		except FileNotFoundError:
			return False
		return True
	
	def lookup_rsa(self, id_origin=None, ip=None) -> Result(str, FileNotFoundError):
		"""
			lookup the public RSA key associated with the provided user-id
			from the directory of public RSA keys specified through the c-
			lasses initializer
			
			@parameters a valid userid on the index node is provided
			@returns the public RSA key string in the index JSON file
			@exception if there is an error (id doesn't exist) an empty string
					is returned
		"""
		try:
			if (id_origin is None) or (ip is not None):
				id_origin = self.lookupIP(ip)
			if id_origin is not None:
				self.lookupIndex(id_origin)
			test = self.index[id_origin]['rsa']
			f = open(self.index[id_origin]['rsa'], 'rb')
			key = f.read()
			f.close()
			return Result(key, None)
		except FileNotFoundError as e:
			return Result(None, e)
			
	def delete_rsa(self, id_origin: str) -> bool:
		"""
			deletes the public RSA key file associated with the provided
			userid
			
			@returns boolean true if the file was removed successfully
			@exception returns boolean false if the file doesn't exist
			
					** looks for a file named (userid.pem) **
		"""
		check = self.lookup_rsa(id_origin=id_origin)
		if check.exception() is not None:
			return False
		remove(self.index[id_origin]['rsa'])
		return True
	
	def add_index(self, id_origin, public_rsa, ip_connecting):
		"""
			insert a new user-id / ip link within the index JSON file and
			timestamp it in the JSON log file
			
			@parameters a valid ip-address on the index node is provided
			@returns boolean true if the userid and ip were successfully added
					 to the index and log JSON files
			@exception returns boolean false; it is likely that the userid or
					   ip has not been used before
		"""
		# check to see if the userid already exists
		if self.lookupIndex(id_origin) != '':
			return 'Already Indexed'
		# check to see if the ip address already has an id assigned
		if self.lookupIP(ip_connecting) != '':
			return 'Already Has IP'
		
		self.index[id_origin] = {
			'ip': ip_connecting,
			'rsa': self.directory_collected_keys + f'{id_origin}.pem'
		}
		self.log[ip_connecting] =  id_origin
		self.addRSA(id_origin, public_rsa)
		return 'Successfully Added'
	
	def delete_index(self, id_origin, ip_connecting):
		"""
			delete the userid and ip found within the index and log JSON files
			
			@parameters the userid exists within the index JSON file and the
						connecting ip is associated with the account
			@returns boolean true if the userid was successfully deleted
			@exception returns boolean false if any of the parameters are not met
		"""
		ip_is_logged = self.lookupIndex(id_origin)
		
		# check to see that if the userid exists (the ip will exist if the userid does)
		if ip_is_logged == '':
			return '0'
		# check to see that the ip-address matches the logged user-id
		if ip_is_logged != ip_connecting:
			return '0'
		
		self.deleteRSA(id_origin)
		self.index.pop(id_origin)
		self.log.pop(ip_connecting)
		
		return 'Successfully Deleted'
	
	def validate_relay(self, ip):
		"""
			pings the ip-address that needs to be validated and if a ping
			attempt fails (node closed), de-index the ip-id match
			
			@parameters the connectingIP address given is in the JSON log
						file
			@returns boolean true if the logged relay could be reached and
						was not de-indexed
			@exception returns boolean false if the logged relay could not
						be reached and was de-indexed
					
			** this is to fix issues when people hard-close their client
				nodes instead of running a proper de-indexing quit process. **
		"""
		# check to see if the id exists already (we don't want to add an ip unknowingly
		# and not have it link up with the index JSON file
		if self.lookupIP(ip) == '':
			return False
		
		try:
			self.send(ip, '')  # all empty strings are discarted (treated as a ping)
		except Exception:
			self.deleteIndex(self.log[ip], ip)
			
		return True
			
	def encrypt_pathway_and_exit(self):
		"""
			creates a randomized path through the server relay nodes
			
			@returns the first relay ip and a path of 4 node relays encrypted
		"""
		h = rsa.Handler()
		active_relays = self.log.keys()
		
		ip_first = ''
		ip_previous = ''
		for i in range(0, 4):
			random_index = random.randrange(0, len(active_relays))
			
			if i > 0:
				relay_ip = active_relays.pop(random_index)
				relay_encrypted = h.encrypt(relay_ip, self.lookup_rsa(ip = ip_previous))
			else:
				ip_first = active_relays.pop(random_index)
				continue  # skip to the begining of the loop
			
			pathway = pathway + ":" + relay_encrypted
			ip_previous = relay_ip
			
			if i == 3:
				active_exits = len(self.index['exit'])
				exit_node = random.randrange(0, active_exits)
				
				exit = self.index['exit'][exit_node]['ip']
		
		return (ip_first, f'^{pathway}^@{exit}@')
		
	def encrypt_data(self, id_origin: str, message: str) -> str:
		"""
			(Index, string, string) -> (string)
		"""
		rsa_temp = self.lookupRSA(id_origin)
		print(message)
		encrypted_message = self.handler_keys.encrypt(message, rsa_temp)
		# send the encrypted data with the RSA of the receiver
		return encrypted_message
	
	def format_message(self, id_target: str, message: str, id_origin: str) -> str:
		"""
			(Index, string, string, string) -> (string)
		"""
		message = self.encryptData(message)
		route = self.encryptPathwayAndExit()
		# send the next_ip and the bitstream readable only to the network
		return (route[0], f'#{message}#{route}<{id_origin}<>{id_target}>')
		
	def format_message_short(self, id_target: str, message: str, id_origin: str) -> str:
		"""
			(Index, string, string, string) -> (string)
		"""
		ip_target = self.lookupIndex(id_target)
		message = self.encryptData(id_origin, message)
		# send the next_ip (target-ip since it is simplified network msg)
		# and the message readable by the target
		return (ip_target, f'4:{message}~{id_origin}')
				
	@overrides(Node)
	def special_functionality(self, message, connecting_address):
		"""
			(Node, string, string) -> (boolean, string)
			:auto-handles the generic requests made to the indexing function
			
			@returns boolean False indicating that messages will NOT be enqueued
					 to a queue
		"""
		# parse the simple bitsream requests
		try:
			p = basic.Parser(message)
			
			request = p.getRequest()
			data_first = p.getPrimaryData()
			data_second = p.getSecondaryData()
		except Exception:
			return (False, '400')  # error code 400: invalid request type
		
		print(self.index)
		
		# check all the standard network requests
		if request == '0':
			address = self.lookup_index(data_first)  # the first data is the userid
			return (False, address)
		elif request == '1':
			userid = self.lookup_ip(data_first)  # the first data is the ip
			return (False, userid)
		elif request == '2':
			data_third = p.get_other_data()[0]
			check = self.add_index(data_first, data_second, data_third) #the first data is the userid, second is publicRSA, last is userip
			print(f'CHECK: {check}')
			return (False, check)
		elif request == '3':
			check = self.delete_index(data_first, data_second) #the first data is the userid, last is userip
			return (False, check)
		elif request == '4':
			data_third = p.get_other_data()[0]
			if self.simplified_network:
				message = self.format_message_short(data_first, data_second, data_third) #for simplified networks
			else:
				message = self.format_message(data_first, data_second, data_third) #for complex networks
			return (False, f'{message[0]}%{message[1]}')
		
		# the message has been handled by the generic implemented index requests
		return (False, '400')  # error code 400: invalid request type
