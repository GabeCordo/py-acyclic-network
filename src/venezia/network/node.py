###############################
#		python imports
###############################

import socket, asyncio
from time import sleep, time
from threading import Thread

###############################
#		global imports
###############################

from src.utils import errors, enums, logging, containers

###############################
#	   venezia imports
###############################

from src.venezia.crypto import rsa
from src.venezia.timing.stopwatch import StopWatch
from src.venezia.timing.timer import Timer
from src.venezia.types import dynamic

###############################
#		   main code
###############################

PARAM_EMPTY_PORT = ''
PARAM_PERMITTED_CHAR_LEN = 100 #the max number of chars allowed per bitstream (RSA maximum)
REQUEST_BYTE_SIZE = 1024
REQUEST_TIMEOUT = 5.0
QUEUE_MONITOR_SCANNER_DELAY = 60
QUEUE_MONITOR_MAX_GROWTH = 1000

class Node:
	def __init__(self, container_addresses, container_paths, container_customizations):
		'''
			(Node, Addresses, Paths, Customizations) -> None
			
			:the class constructor for the primitive node type. All children
			 class are specific variations of the node class for specific
			 socket input and output manipulation on the mock 'tor' network.
			
			!the node class uses containers to store huge amounts of variables
			 for better customizability, reusability and to make code cleaner
			
				L-> all wrapper classes found under utils/containers
			
			** defaulted to end-to-end encryption enabled **
		'''
		# Imported Containers
		self.container_addresses = container_addresses
		self.container_paths = container_paths
		self.container_customizations = container_customizations
		
		# Generic Variables
		socket_request_queue = dynamic.RequestQueue()
		socket_request_hash_table = dynamic.ResponseHashTable()
		
		# Initialize the receiving socket
		self.incoming = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		# Initialize the encryption handler
		self.handler_keys = rsa.Handler(container_paths.directory_key_private, container_paths.directory_key_public)
		
		# Settup logging file for connection speed data
		logging.Logger(container_paths.directory_file_logging, container_customizations.supports_console_cout)

		# this thread is the background event loop to run through coroutine functions
		self.background_event_loop = Thread(target=self.listen, args=())
	
	def getIp(self):
		'''
			(Node) -> (string)
			:the getter function for the ip bind to the Node Class
			
			@returns the ip of the server the socket is bind to.
		'''
		return self.container_addresses.ip
	
	def isListening(self):
		'''
			(Node) -> (boolean)
			:the getter function for whether accepting incoming traffic is
			 toggled
			
			@returns whether the socket is currently listening.
		'''
		return self.container_customizations.supports_listening
		
	def isEncrypted(self):
		'''
			(Node) -> (boolean)
			:the getter function for whether encryption is toggled
			
			@returns whether the node allows for end-to-end encryption
		'''
		return self.container_customizations.supports_encryption
	
	def isMonitoring(self):
		'''
			(Node) -> (boolean)
			:the getter function for whether the queue monitor is daemon
			
			@returns a boolean value representing whether the monitor is toggled
		'''
		return self.container_customizations.supports_monitoring
	
	def specialFunctionality(self, message: str, address: str) -> tuple(bool, str):
		'''
			(string, string) -> (boolean, string)
			:child classes can overide this function to offer special functionality
			 to the listening aspect of the server
			
			@returns a boolean value representing whether to enqueue message
		'''
		return (True, '0') #by default we want it to queue all the requests
	
	def specialFunctionalityError(self, status: str) -> enums.ReturnCode:
		'''
			(string, string) -> (string)
			:child classes can overide this function to offer special functionality
			 to processing and re-writting the errors processed by the node
			
			@returns a string representing a processed error code
		'''
		return (status)
	
	def listen(self) -> None:
		'''
			(Node, int) -> None
			:listens to all incoming traffic to the server node.
			
			@returns nothing.
			@exception will not queue any incoming messages that are over
					   1024 bites long to enforce maximum runtime of string
					   parsing.
					
			**despite not returning anything, all incoming messages
			 are checked and then enqueued on the node to be processed.**
		'''
		self.incoming.bind((self.container_addresses.ip, self.container_addresses.port))
		self.incoming.listen(10)
		
		while True:
			
			c, addr = self.incoming.accept()
			print(f'Console: Received connection from {addr}') #console logging
			
			optimizer = StopWatch(4) #we will use this to capture time between data captures to offer the best latency
			print("Set Optimizer" + str(optimizer))
			
			try:
				
				#send whether the node supports end-to-end encryption
				if (self.container_customizations.supports_encryption == True):
					pre_message = self.handler_keys.getPublicKey()
				else:
					pre_message = b'None'
				optimizer.lap()
				c.send(pre_message) ##send the encryption key or None indiciating it's disabled
				optimizer.lap()
				
				if (self.container_customizations.supports_encryption == True):
					#receive the connectors public RSA key
					publicRSA = c.recv(REQUEST_BYTE_SIZE)
				
				print(f'Console: Received publicRSA') #console logging
				print(publicRSA) #debuging
				
				#receive the cypher text from the connector
				time_warning = time() #keep track of the start (we want to avoid going over ~10 seconds)
				
				optimizer.lap() #start timing the transfer time according to latency
				cyphertexts = [c.recv(REQUEST_BYTE_SIZE)]
				optimizer.lap() #measure the latency time to compensate for when sending data
				print(f'Console: Time difference - {optimizer.getLog()}')
				i = 0
				
				delay = optimizer.getShortestLap()
				#start receiving data from the sending socket
				while (cyphertexts[i] != b'<<'): #loop until the terminating operator is reached
				
					sleep(delay)
					cyphertexts.append(c.recv(REQUEST_BYTE_SIZE))
					
					#ensure data collection has not exceeded 5 seconds
					if ((time() - time_warning) > REQUEST_TIMEOUT):
						raise TimeoutError('Data Transfer Exceeded 5 seconds')
					i+=1
				
				cyphertexts.pop() #remove the null terminating character
				
				print(f'Console: Received cyphertext') #console logging
				
				#we want to decrypt the message only if encryption is enabled otherwise it is
				#in plain-text and decrypting it will raise an error
				if (self.container_customizations.supports_encryption == True):
					#we need to individually decrypt each message and then join it
					for i in range(0, len(cyphertexts)):
						cyphertexts[i] = self.handler_keys.decrypt(cyphertexts[i]) #decrypt the cypher text and place it into a temp holder
				else:
					#we need to individually decode the utf-8 bitsream into plain text
					for i in range(0, len(cyphertexts)):
						cyphertexts[i] = cyphertexts[i].decode()
					
				message = ''.join(cyphertexts)
				
				#allow child classes to manipulate the message
				data_processed = self.specialFunctionality(message, addr[0])
				
				print(f'Console: proccessed data') #console logging
				print(data_processed) #debuging
				
				#send the response code that will alert the sender whether to listen for future
				#response data associated with the request sent to the "server"
				c.send(data_processed[1].encode())
				
				#return the data to the user
				if (data_processed[1] == '1'):
					
					data_processed_lst = []
					permitted_char_len = 100 #the max number of chars allowed per bitstream (RSA maximum)
					
					#prepare the message we are going to send to the 
					if(self.supports_encryption == True):
						
						#if encryption is enabled, cypher it with the received public rsa
						#we need to make sure the byte size of the string being encrypted does not grow > than 250
						remaining_chars = permitted_char_len
						
						while ((len(data_processed[1]) - len(data_processed_lst)*permitted_char_len) > permitted_char_len): #repeat untill the len is less than 150 chars
							#for visibility we will throw this into temp vars
							beggining = remaining_chars - permitted_char_len
							end = remaining_chars
							
							#encrypt and append to the list of message segments to send that are encrypted
							temp = self.handler_keys.encrypt(data_processed[1][beggining:end], publicRSA)
							data_processed_lst.append(temp)
							
							#append the number of chars that remain within the message
							remaining_chars+=permitted_char_len
						
						#append the final part of the message to the list
						beggining = remaining_chars - permitted_char_len
						temp = self.handler_keys.encrypt(data_processed[1][beggining:], publicRSA)
						data_processed_lst.append(temp)
							
					else:
						
						data_processed_lst.append(bytes(data_processed[1], 'utf-8'))
					
					data_processed_lst.append(b'<<') #add the message transfer terminator
					
					print(f'Console: finished preparing response') #console logging
					print(data_processed_lst) #debugging
					
					delay = optimizer.getLongestLap()
					#send the encrypted message to the listening node, we don't encode this into utf-8 as the cyphered text will
					#already be in this form, and won't be able to be sent
					for data_segment in data_processed_lst:
						sleep(delay)
						c.send(data_segment)
						
					print(f'Console: sent response') #console logging
					
				#append to the message queue if required for further functionality
				if (data_processed[0]):
					self.queue.append(message)
				
			except Exception as e:
				proccessed_error = self.specialFunctionalityError(e)
				print(f'Console: There was a problem during execution ({proccessed_error})')
			
			#close the connection with the connector
			c.close()

	def close(self) -> None:
		'''
			(Node) -> None
			:close the socket listening for incoming connections.
		'''
		#make sure the listening port is open in the first place before closing
		#the socket otherwise it will throw an error.
		if (self.container_customizations.supports_listening == False):
			#ensure the socket is closed
			self.incoming.close()
	
	async def send(self, ip_target: int, message=enums.ReturnCode.PING_SERVER, port=PARAM_EMPTY_PORT) -> (str):
			'''
				(Node, int, message) -> (string)
				:sends a bitsream to another Node.
				
				ip_target : the ip-address of the receiving node
				message : the bitsream to send to the node
				
				@returns a response code in the form of a strins from the server.
				@exception returns an empty string if there was a failure.
			'''
			try:
				outgoing = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				
				#if we aren't send a port to send the message to, assume its the same as
				#the one given upon class declaration (option: send to a diff network)
				if (port == PARAM_EMPTY_PORT):
					port = self.port
				
				optimizer = StopWatch(6) #we will use this to capture time between data captures to offer the best latency
				outgoing.connect((ip_target, port)) #all outgoing requests are sent on port 8075
				
				#if we leave the string empty we are asking for a simple ping of the listening
				#server so if we establish connection return '1' and end everything else
				if (message == enums.ReturnCode.PING_SERVER):
					return enums.ReturnCode.PING_SERVER
				
				optimizer.lap()
				received_rsa_public = outgoing.recv(REQUEST_BYTE_SIZE).decode()
				optimizer.lap()
				
				key_pub_ours = self.handler_keys.getPublicKey()
				if (received_rsa_public != 'None'):
					outgoing.send(key_pub_ours) #send public key for any responses
				
				message_lst = []
				print(f'Console: Time difference - {optimizer.getLog()}')
				
				#prepare the message we are going to send to the
				if(received_rsa_public != 'None'):
					#if encryption is enabled, cypher it with the received public rsa
					#we need to make sure the byte size of the string being encrypted does not grow > than 250
					remaining_chars = PARAM_PERMITTED_CHAR_LEN
					
					while ((len(message) - len(message_lst)*PARAM_PERMITTED_CHAR_LEN) > PARAM_PERMITTED_CHAR_LEN): #repeat until the len is less than 150 chars
						#for visibility we will throw this into temp vars
						beggining = remaining_chars - PARAM_PERMITTED_CHAR_LEN
						end = remaining_chars
						
						#encrypt and append to the list of message segments to send that are encrypted
						temp = self.handler_keys.encrypt(message[beggining:end], received_rsa_public)
						message_lst.append(temp)
						
						#append the number of chars that remain within the message
						remaining_chars+=PARAM_PERMITTED_CHAR_LEN
					
					#append the final part of the message to the list
					beggining = remaining_chars - PARAM_PERMITTED_CHAR_LEN
					temp = self.handler_keys.encrypt(message[beggining:], received_rsa_public)
					message_lst.append(temp)
						
				else:
					message_lst.append(bytes(message, 'utf-8'))
				
				message_lst.append(b'<<') #add the message transfer terminator
				
				print(f'Console: prepared message') #console logging
				
				delay = optimizer.getLongestLap()
				#send the encrypted message to the listening node, we don't encode this into utf-8 as the cyphered text will
				#already be in this form, and won't be able to be sent
				for message_segment in message_lst:
					sleep(delay)
					outgoing.send(message_segment)
					
				print(f'Console: Sent message') #console logging
				
				#we are going to receive a response code back from the user after this possibly indicating some status
				#code or will 'spit out' some sort of data associated with the request
				
				response_code = outgoing.recv(REQUEST_BYTE_SIZE)
				
				if (response_code == b'1'):
				
					#receive the cypher text from the connector
					time_warning = time() #keep track of the start (we want to avoid going over ~10 seconds)
					
					cyphertexts = [outgoing.recv(REQUEST_BYTE_SIZE)]
					i = 0

					delay = optimizer.getShortestLap()
					#start receiving data from the sending socket
					while (cyphertexts[i] != b'<<'): #loop until the terminating operator is reached
					
						sleep(delay)
						cyphertexts.append(outgoing.recv(REQUEST_BYTE_SIZE))
						
						#ensure data collection has not exceeded 5 seconds
						if ((time() - time_warning) > 5.0):
							raise TimeoutError('Data Transfer Exceeded 5 seconds')
						
						i+=1
						
					cyphertexts.pop() #remove the null terminating character
					
					print(f'Console: Received Cyphertext') #console logging
					
					#we want to decrypt the message only if encryption is enabled otherwise it is
					#in plain-text and decrypting it will raise an error
					if (received_rsa_public != 'None'):
						#we need to individually decrypt each message and then join it
						for i in range(0, len(cyphertexts)):
							cyphertexts[i] = self.handler_keys.decrypt(cyphertexts[i]) #decrypt the cypher text and place it into a temp holder
					else:
						#we need to individually decode the utf-8 bitsream into plain text
						for i in range(0, len(cyphertexts)):
							cyphertexts[i] = cyphertexts[i].decode()
						
					response = ''.join(cyphertexts) #join the decoded cyphertexts
					
					print(f'Console: Formated cypher to plain text') #console logging
					
					#if we receive a status code of '0' that means something went wrong
					if (response == '400' or response == None):
						#if there is default to returning an empty string
						outgoing.close()
						return 'Error 400: Bad Resquest'
					else:
						#the bitsream was successfully sent, we received usefully information from
						#the server we may need to process (it might be a response)
						outgoing.close()
						return response
			
				else:
					
					if (response_code == b'0'):
						print(f'Console: (Code 0) General Failure')
					elif (response_code == b'2'):
						print(f'Console: (Code 2) Transfer Failure')
						
				outgoing.close()
				return None
			
			except Exception as e:
				
				print(f'Console: Experienced Error {e}') #debugging
				
				#we need to check that the ip_target is not self.ip_backup to avoid going into a recursive infinite loop
				if (self.container_customizations.supports_backup_ip != None and ip_target != self.container_customizations.ip_backup):
					self.send(self.ip_backup, message)
				else:
					outgoing.close()
					return e
	
	async def monitor(self) -> None:
		'''
			(Node) -> None
			
			:the monitor function is an active listener on the enqueued messages
			 looking for potential spamming or overflows
			
			1) Check for garbage messages near the end of the queue
			
			**Queues only near the end of the queue will be effect to ensure it
			  does not interfere with the any systems working to manipulate/handle
			  elements at the front of the queue during runtime AVOIDING MEMORY RACES **
		'''
		length_queue_previous = 0
		#runs throughout the lifetime of the incoming socket
		while (self.container_customizations.supports_listening == True):
			sleep(QUEUE_MONITOR_SCANNER_DELAY)
			#account for the fact that during runtime, this might be closed midway
			try:
				#check to see if the queue size has increased by N in N(s) seconds
				#it should process quickly, this means its laggining/being flooded
				length_queue = len(self.queue)
				if ((length_queue - length_queue_previous) > QUEUE_MONITOR_MAX_GROWTH):
					#reset the queue to 60s before the current check
					self.queue = self.queue[:length_queue_previous+1]
				else:
					#account for the new queue additions
					length_queue_previous = length_queue
			except Exception:
				#stop monitoring the queue
				return
	
	def settup(self):
		'''
			(Node) -> None
			:creates two new threads for the socket node on the network
			
			1) Thread One : Receives and sorts all incoming bitsream traffic
			2) Thread Two : Monitors the enqueued bitsreams for overflow/flooding
			
			** settup end-to-end encryption keys for the socket node **
		'''
		if (self.container_customizations.supports_listening == True):
			##settup and start the incoming socket##
			self.thread_one.setDaemon(True) # Daemonize thread (run in background)
			self.thread_one.start()
		
		if (self.container_customizations.supports_monitoring == True):
			##settup and start the queue monitor##  
			self.thread_two.setDaemon(True) # Daemonize thread (run in background)
			self.thread_two.start()

		##settup the end-to-end encryption keys##
		#will generate a new key-set when the server is started
		self.handler_keys.generateKeySet()

		#this is the last option as (if enabled) it will launch a terminal client
		if (self.container_customizations.supports_dynamic_interaction == True):
			##settup and start the input console##
			pass
			
		
	def isThreadOneRuning(self):
		'''
			(Node) -> (boolean)
		'''
		return self.thread_one.is_alive()
	
	def closeThreadOne(self):
		'''
			(Node) -> None
		'''
		self.thread_one._Thread_stop()
			
	def isThreadTwoRunning(self):
		'''
			(Node) -> (boolean)
		'''
		return self.thread_two.is_alive()
		
	def closeThreadTwo(self):
		'''
			(Node) -> None
		'''
		self.thread_two._Thread_stop()
	
	def isThreadThreeRunning(self):
		'''
			(Node) -> (boolean)
		'''
		return self.thread_two.is_alive()
		
	def closeThreadThree(self):
		'''
			(Node) -> None
		'''
		self.thread_two._Thread_stop()

	def __repr__(self):
		return f'Node(ip:{self.container_addresses.ip}, port:{self.container_addresses.port}, queue-len:{len(self.queue)})'

	def __eq__(self, other):
		if (other == None):
			return
		if (type(other) != type(Node)):
			return
		return self.container_customizations == other.container_customizations

	def __del__(self):
		self.close()
		print('Console: the node has been closed.')