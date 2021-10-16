###############################
# python imports
###############################

import socket
from time import sleep, time
from threading import Thread
from typing import Tuple

import traceback
from pyacyclicnet.core.types.request import Request

###############################
# global imports
###############################

from pyacyclicnet.utils import logging

###############################
# core imports
###############################

from pyacyclicnet.core.crypto import rsa
from pyacyclicnet.core.timing.stopwatch import StopWatch
from pyacyclicnet.core.types.enums import RequestCode, RequestTableLifetime, ReturnCode, EnqueueRequest, DoYouKnowOption, ProcessDataStatus
from pyacyclicnet.core.types.containers import Addresses, Paths, Customizations
from pyacyclicnet.core.types.result import Result
from pyacyclicnet.core.types.requestqueue import RequestQueue
from pyacyclicnet.core.types.responsehashtable import ResponseHashTable
from pyacyclicnet.core.types.errors import CorruptedMessage, IllegalRequest, EncryptionFailed, NoResponseNeeded, MismatchedSyntax
from pyacyclicnet.core.bitstream.parser import ProtocolParser

###############################
# constants
###############################

PARAM_EMPTY_PORT = 23245
PARAM_PERMITTED_CHAR_LEN = 100  # the max number of chars allowed per bitstream (RSA maximum)
REQUEST_BYTE_SIZE = 1024
REQUEST_TIMEOUT = 5.0
QUEUE_MONITOR_SCANNER_DELAY = 60
QUEUE_MONITOR_MAX_GROWTH = 1000

###############################
# node
###############################


class Node:
	def __init__(self, container_addresses: Addresses, container_paths: Paths, container_customizations: Customizations):
		"""
			the class constructor for the primitive node type. All children
			class are specific variations of the node class for specific
			socket input and output manipulation on the mock 'tor' network.
			
			!the node class uses containers to store huge amounts of variables
			for better customizable, usability and to make code cleaner
			
				L-> all wrapper classes found under utils/containers
			
			** defaulted to end-to-end encryption enabled **
		"""
		# Imported Containers
		self.container_addresses = container_addresses
		self.container_paths = container_paths
		self.container_customizations = container_customizations
		
		# Generic Variables
		self.socket_request_queue = RequestQueue()
		self.socket_request_hash_table = ResponseHashTable()
		
		# Initialize the receiving socket
		self.incoming = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		# Initialize the encryption handler
		self.handler_keys = rsa.Handler(container_paths.directory_key_private, container_paths.directory_key_public)
  
		# Initialize the parser handler
		self.bitstream_parser = ProtocolParser()
		
		# Setup logging file for connection speed data
		logging.Logger(container_paths.directory_file_logging, container_customizations.supports_console_cout)

		#these threads will need to be visible to a grouping of functions in the
		#class so we are throwing it in the constructor
		self.thread_one = Thread(target=self.listen, args=())
		self.thread_two = Thread(target=self.monitor, args=())
	
	def get_ip(self) -> str:
		"""
			the getter function for the ip bind to the Node Class
			
			@returns the ip of the server the socket is bind to.
		"""
		return self.container_addresses.ip
	
	def is_listening(self) -> bool:
		"""
			the getter function for whether accepting incoming traffic is
			toggled
			
			@returns whether the socket is currently listening.
		"""
		return self.container_customizations.supports_listening
		
	def is_encrypted(self) -> bool:
		"""
			the getter function for whether encryption is toggled
			
			@returns whether the node allows for end-to-end encryption
		"""
		return self.container_customizations.supports_encryption
	
	def is_monitoring(self) -> bool:
		"""
			the getter function for whether the queue monitor is daemon
			
			@returns a boolean value representing whether the monitor is toggled
		"""
		return self.container_customizations.supports_monitoring
	
	def special_functionality(self, message: str, address: str) -> Result(tuple(), Exception):
		"""
			child classes can override this function to offer special functionality
			to the listening aspect of the server
			
			@returns Result((Enqueue Request, Raw Data), Exception)
		"""
		raise NotImplementedError
	
	def special_functionality_error(self, status: Exception) -> ReturnCode:
		"""
			child classes can override this function to offer special functionality
			to processing and re-writing the errors processed by the node
			
			@returns a string representing a processed error code
		"""
		raise NotImplementedError
	
	def listen(self) -> None:
		"""
			listens to all incoming traffic to the server node.
			
			@returns nothing.
			@exception will not queue any incoming messages that are over
					1024 bites long to enforce maximum runtime of string
					parsing.

			**despite not returning anything, all incoming messages
			are checked and then enqueued on the node to be processed.**
		"""
		self.incoming.bind((self.container_addresses.ip, self.container_addresses.port))
		self.incoming.listen(10)
		
		while True:
			
			c, addr = self.incoming.accept()
			print(f'Console: Received connection from {addr}')  # console logging
			
			optimizer = StopWatch(4)  # we will use this to capture time between data captures to offer the best latency
			print("Set Optimizer" + str(optimizer))
			
			try:
				
				# send whether the node supports end-to-end encryption
				if self.container_customizations.supports_encryption:
					pre_message = self.handler_keys.get_public_key()
				else:
					pre_message = b'None'
				optimizer.lap()
				print(pre_message)
				c.send(pre_message)  # send the encryption key or None indicating it's disabled
				optimizer.lap()
				
				if self.container_customizations.supports_encryption:
					# receive the connectors public RSA key
					public_rsa = c.recv(REQUEST_BYTE_SIZE)
				
				print(f'Console: Received publicRSA \n{public_rsa}')  # console logging
				
				# receive the cypher text from the connector
				time_warning = time()  # keep track of the start (we want to avoid going over ~10 seconds)
				
				optimizer.lap()  # start timing the transfer time according to latency
				ciphertexts = [c.recv(REQUEST_BYTE_SIZE)]
				optimizer.lap()  # measure the latency time to compensate for when sending data
				print(f'Console: Time difference - {optimizer.get_log()}')
				i = 0
				
				delay = optimizer.get_shortest_lap()
				# start receiving data from the sending socket
				while ciphertexts[i] != b'<<':  # loop until the terminating operator is reached
				
					sleep(delay)
					ciphertexts.append(c.recv(REQUEST_BYTE_SIZE))
					
					# ensure data collection has not exceeded 5 seconds
					if (time() - time_warning) > REQUEST_TIMEOUT:
						print('Console: Closed Connection as Data Transfer Exceeded 5 seconds')
						break
					i += 1
				
				ciphertexts.pop()  # remove the null terminating character
				
				print(f'Console: Received ciphertext')  # console logging
				
				# we want to decrypt the message only if encryption is enabled otherwise it is
				# in plain-text and decrypting it will raise an error
				if self.container_customizations.supports_encryption:
					# we need to individually decrypt each message and then join it
					for i in range(0, len(ciphertexts)):
						# the deciphered value will be placed into a Result() object -- see if the function failed
						temp = self.handler_keys.decrypt(ciphertexts[i])
						if temp.is_valid():
							ciphertexts[i] = temp.value()
						else:
							c.close()
							raise EncryptionFailed
				else:
					# we need to individually decode the utf-8 bitstream into plain text
					for i in range(0, len(ciphertexts)):
						ciphertexts[i] = ciphertexts[i].decode()
				
				# the encrypted text is sitting within a list after being decrypted, we need
				# to do a quick join in order to read the full protocol message and send it
				# into the parser
				plaintext_request = ''.join(ciphertexts)
				print(plaintext_request)  # debug
				
				# parse the raw plaintext into a request object so we can easily manipulate it
				# and pull data with pre-defined functions
				tmp_packet = self.bitstream_parser.parse(plaintext_request)
				if tmp_packet.is_valid():
					protocol_packet = tmp_packet.value()
				else:
					c.close()
					raise MismatchedSyntax

				raw_data_processed = None
				# apply a 'switch' case over the request in comparision to the known request ints
				if protocol_packet.request == RequestCode.PING_SERVER:
					raw_data_processed = Result((EnqueueRequest.PROCESSES, "Okay"), None)
				elif protocol_packet.request == RequestCode.SEND_DATA:
					raw_data_processed = self.special_functionality(plaintext_request, addr[0])
				elif protocol_packet.request == RequestCode.SEND_DATA_NO_RESPONSE:
					self.special_functionality(plaintext_request, addr[0])
					c.close()
					raise NoResponseNeeded
				elif protocol_packet.request == RequestCode.RELAY_FOLLOWUP:
					# the nonce should be passed into the data segment of the request, use
					# the nonce to grab the return value of the request
					nonce = protocol_packet.nonce
					if self.socket_request_hash_table.get_request_code(nonce) is RequestTableLifetime.RESPONDED:
						raw_data_processed = self.socket_request_hash_table.get_return_value(nonce)
					else:
						raw_data_processed = ""
				elif protocol_packet.request == RequestCode.DO_YOU_KNOW:
					if protocol_packet.data == DoYouKnowOption.IP_BACKUP_INDEX:
						raw_data_processed = self.container_addresses.ip_backup
					else:
						raw_data_processed = self.container_addresses.ip_index	
				else:
					# we leave the implementation up to the developer
					raw_data_processed = self.special_functionality(plaintext_request, addr[0])
    
				data_processed = None
				# check to see if we are returned valid data or an error
				if raw_data_processed.is_valid():
					data_processed = raw_data_processed.value()
				else:
					raise IllegalRequest
				
				print(f'Console: processed data')  # console logging
				print(data_processed)  # debugging
				
				# inform the sending node if we want to continue sending data (likely encrypted)
				# or we will be shutting down the node, the status code is behind a EnumInt in a tuple index 0
				c.send(str(int(data_processed[0])).encode())
				
				# return the data to the user
				if data_processed[0] is EnqueueRequest.PROCESSES:
					
					data_processed_lst = []
					permitted_char_len = 100  # the max number of chars allowed per bitstream (RSA maximum)
					
					# prepare the message we are going to send to the
					if self.container_customizations.supports_encryption:
						
						# if encryption is enabled, cypher it with the received public rsa
						# we need to make sure the byte size of the string being encrypted does not grow > than 250
						remaining_chars = permitted_char_len

						# repeat until the len is less than 150 chars
						while (len(data_processed[1]) - len(data_processed_lst)*permitted_char_len) > permitted_char_len:
							# for visibility we will throw this into temp vars
							beginning = remaining_chars - permitted_char_len
							end = remaining_chars
							
							# encrypt and append to the list of message segments to send that are encrypted
							temp = self.handler_keys.encrypt(data_processed[1][beginning:end], public_rsa)
							# check the result class, if we are returned an Error it means the encryption is broken and close
							# the socket before we send an erroneous message to the server and confuse it.
							if temp.is_valid():
								data_processed_lst.append(temp.value())
							else:
								c.close()
								raise EncryptionFailed
							
							# append the number of chars that remain within the message
							remaining_chars += permitted_char_len
						
						# append the final part of the message to the list
						beginning = remaining_chars - permitted_char_len
						temp = self.handler_keys.encrypt(data_processed[1][beginning:], public_rsa)
						if temp.is_valid():
							data_processed_lst.append(temp.value())
						else:
							c.close()
							raise EncryptionFailed
							
					else:
						
						data_processed_lst.append(bytes(data_processed[1], encoding='utf8'))
					
					data_processed_lst.append(b'<<')  # add the message transfer terminator
					
					print(f'Console: finished preparing response')  # console logging
					print(data_processed_lst)  # debugging
					
					delay = optimizer.get_longest_lap()
					# send the encrypted message to the listening node, we don't encode this into utf-8 as the cyphered text will
					# already be in this form, and won't be able to be sent
					for data_segment in data_processed_lst:
						sleep(delay)
						c.send(data_segment)
						
					print(f'Console: sent response')  # console logging
					
				# append to the message queue if required for further functionality
				elif data_processed.value()[0] == EnqueueRequest.QUEUE:
					self.socket_request_queue.push(plaintext_request)
				
			except Exception as e:
				print(traceback.format_exc())  # debugging
				processed_error = ""  #  TODO: self.special_functionality_error(e)
				print(f'Console: There was a problem during execution ({processed_error})')
			
			# close the connection with the connector
			c.close()

	def close(self) -> None:
		"""
			close the socket listening for incoming connections.
		"""
		# make sure the listening port is open in the first place before closing
		# the socket otherwise it will throw an error.
		if not self.container_customizations.supports_listening:
			# ensure the socket is closed
			self.incoming.close()
	
	def send(self, ip_target="127.0.0.1", request=RequestCode.PING_SERVER, message=None, port=PARAM_EMPTY_PORT) \
		-> Result(str, Exception):
		"""
			sends a bitstream to another Node.

			ip_target : the ip-address of the receiving node
			message : the bitstream to send to the node
				
			@returns a response code in the form of a strings from the server.
			@exception returns an empty string if there was a failure.
		"""
		try:
			outgoing = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

			# if we aren't send a port to send the message to, assume its the same as
			# the one given upon class declaration (option: send to a diff network)
			if port == PARAM_EMPTY_PORT:
				port = self.container_addresses.port

			# if we are sending an explicit message to a server node, we need to have the
			# the message param as a non-None value (every other enum type needs data except
   			#  for the PING_SERVER value)
			if request is not RequestCode.PING_SERVER and message is None:
				return Result(None, IllegalRequest)
			if request is RequestCode.PING_SERVER:
				message = "1::0::0::0::0::1<><>"
			
			optimizer = StopWatch(6)  # we will use this to capture time between data captures to offer the best latency
			outgoing.connect((ip_target, port))  # all outgoing requests are sent on port 8075

			optimizer.lap()  # finish measuring the time it takes to connect to the client
			received_rsa_public = outgoing.recv(REQUEST_BYTE_SIZE).decode()
			optimizer.lap()  # finish measuring the time it takes to receive the encryption hello
				
			key_pub_ours = self.handler_keys.get_public_key()
			if received_rsa_public != 'None':
				outgoing.send(bytes(key_pub_ours))  # send public key for any responses
			
			message_lst = []
			print(f'Console: Time difference - {optimizer.get_log()}')
				
			# prepare the message we are going to send to the
			if received_rsa_public != 'None':
				# if encryption is enabled, cypher it with the received public rsa
				# we need to make sure the byte size of the string being encrypted does not grow > than 250
				remaining_chars = PARAM_PERMITTED_CHAR_LEN

				# repeat until the len is less than 150 chars
				while (len(message) - len(message_lst)*PARAM_PERMITTED_CHAR_LEN) > PARAM_PERMITTED_CHAR_LEN:
					# for visibility we will throw this into temp vars
					beginning = remaining_chars - PARAM_PERMITTED_CHAR_LEN
					end = remaining_chars
						
					# encrypt and append to the list of message segments to send that are encrypted
					temp = self.handler_keys.encrypt(message[beginning:end], bytes(received_rsa_public, encoding='utf8'))
					# check the result class, if we are returned an Error it means the encryption is broken and close
					# the socket before we send an erroneous message to the server and confuse it.
					if temp.is_valid():
						message_lst.append(temp.value())
					else:
						outgoing.close()
						return Result(None, EncryptionFailed)
						
					# append the number of chars that remain within the message
					remaining_chars += PARAM_PERMITTED_CHAR_LEN
					
				# append the final part of the message to the list
				beginning = remaining_chars - PARAM_PERMITTED_CHAR_LEN
				temp = self.handler_keys.encrypt(message[beginning:], bytes(received_rsa_public, encoding='utf8'))
				if temp.is_valid():
					message_lst.append(temp)
				else:
					outgoing.close()
					return Result(None, EncryptionFailed)
						
			else:
				message_lst.append(bytes(message, encoding='utf8'))
				
			message_lst.append(b'<<')  # add the message transfer terminator
				
			print(f'Console: prepared message')  # console logging
				
			delay = optimizer.get_longest_lap()
			# send the encrypted message to the listening node, we don't encode this into utf-8 as the cyphered text will
			# already be in this form, and won't be able to be sent
			for message_segment in message_lst:
				sleep(delay)
				# check to see whether the message is a raw byte stream or wrapped in a Result object
				# that might have been created from an encrypt() call
				if isinstance(message_segment, Result):
					if message_segment.is_valid():
						outgoing.send(message_segment.value())
					else:
						# if it is in a Result() wrapper and an error, encryption failed or the message is corrupted - KILL
						outgoing.close()
						return Result(None, CorruptedMessage)
				else:
					# we have gotten to the end of the encrypted stream, meaning all that's left is the b'<<'
					# segment that is not wrapped into the Result() class
					outgoing.send(message_segment)	
					
			print(f'Console: Sent message')  # console logging
   
			# we may not care about the response of the server - or we do not plan to wait for any response
			# that may hold up this sender node
			
			if (request is not RequestCode.SEND_DATA_NO_RESPONSE):
				
				# we are going to receive a response code back from the user after this possibly indicating some status
				# code or will 'spit out' some sort of data associated with the request
				
				response_code = outgoing.recv(REQUEST_BYTE_SIZE)
				if response_code == b'1':
					
					# receive the cypher text from the connector
					time_warning = time()  # keep track of the start (we want to avoid going over ~10 seconds)
						
					ciphertexts = [outgoing.recv(REQUEST_BYTE_SIZE)]
					i = 0

					delay = optimizer.get_shortest_lap()
					# start receiving data from the sending socket
					while ciphertexts[i] != b'<<':  # loop until the terminating operator is reached
						
						sleep(delay)
						ciphertexts.append(outgoing.recv(REQUEST_BYTE_SIZE))
							
						# ensure data collection has not exceeded 5 seconds
						if (time() - time_warning) > 5.0:
							print('Console: Closed Connection as Data Transfer Exceeded 5 seconds')
							break
							
						i += 1
							
					ciphertexts.pop()  # remove the null terminating character
						
					print(f'Console: Received Ciphertext')  # console logging
						
					# we want to decrypt the message only if encryption is enabled otherwise it is
					# in plain-text and decrypting it will raise an error
					if received_rsa_public != 'None':
						# we need to individually decrypt each message and then join it
						for i in range(0, len(ciphertexts)):
							# decrypt the cypher text and place it into a temp holder
							tmp_plaintext = self.handler_keys.decrypt(ciphertexts[i])
							if tmp_plaintext.is_valid():
								ciphertexts[i] = tmp_plaintext.value()
							else:
								return (None, CorruptedMessage)
					else:
						# we need to individually decode the utf-8 bitstream into plain text
						for i in range(0, len(ciphertexts)):
							ciphertexts[i] = ciphertexts[i].decode()
							
					response = ''.join(ciphertexts)  # join the decoded ciphertexts
						
					print(f'Console: Formatted cypher to plain text')  # console logging
						
					# if we receive a status code of '0' that means something went wrong
					if response == '400':
						# if there is default to returning an empty string
						outgoing.close()
						return 'Error 400: Bad Request'
					else:
						# the bitstream was successfully sent, we received usefully information from
						# the server we may need to process (it might be a response)
						outgoing.close()
						return response
				
				else:

					outgoing.close()
					return response_code.decode()

			# We do not want to wait for a response so we will close the socket to open the socket
			# for the next message the node might want to send out
			else:
				outgoing.close()
    
		except Exception as e:
			print(f'Console: Experienced Error {e}')  # debugging
			print(traceback.format_exc())  # debugging
			# we need to check that the ip_target is not self.ip_backup to avoid going into a recursive infinite loop
			if (self.container_customizations.supports_backup_ip is not None) \
				and (ip_target != self.container_addresses.ip_backup):
				self.send(self.container_addresses.ip_backup, message)
			else:
				outgoing.close()
				return e
	
	def monitor(self) -> Result(bool, Exception):
		"""
			the monitor function is an active listener on the enqueued messages
			looking for potential spamming or overflows
			
			1) Check for garbage messages near the end of the queue
			
			**Queues only near the end of the queue will be effect to ensure it
			does not interfere with the any systems working to manipulate/handle
			elements at the front of the queue during runtime AVOIDING MEMORY RACES **
		"""
		length_queue_previous = 0
		# runs throughout the lifetime of the incoming socket
		while self.container_customizations.supports_listening:
			sleep(QUEUE_MONITOR_SCANNER_DELAY)
			# account for the fact that during runtime, this might be closed midway
			try:
				# check to see if the queue size has increased by N in N(s) seconds
				# it should process quickly, this means its lagging/being flooded
				length_queue = self.socket_request_queue.size_of_queue()
				if (length_queue - length_queue_previous) > QUEUE_MONITOR_MAX_GROWTH:
					# reset the queue to 60s before the current check
					self.socket_request_queue.manipulate(index_two=length_queue_previous+1)
				else:
					# account for the new queue additions
					length_queue_previous = length_queue
			except Exception as e:
				# stop monitoring the queue
				return Result(None, e)
		return Result(True, None)
	
	def setup(self) -> None:
		"""
			creates two new threads for the socket node on the network
			
			1) Thread One : Receives and sorts all incoming bitstream traffic
			2) Thread Two : Monitors the enqueued bitstreams for overflow/flooding
			
			** setup end-to-end encryption keys for the socket node **
		"""
		if self.container_customizations.supports_listening:
			# setup and start the incoming socket
			self.thread_one.setDaemon(True)  # Daemonize thread (run in background)
			self.thread_one.start()
		
		if self.container_customizations.supports_monitoring:
			# setup and start the queue monitor
			self.thread_two.setDaemon(True)  # Daemonize thread (run in background)
			self.thread_two.start()

		# setup the end-to-end encryption keys
		# will generate a new key-set when the server is started
		self.handler_keys.generate_key_set()

		# this is the last option as (if enabled) it will launch a terminal client
		if self.container_customizations.supports_dynamic_interaction:
			# setup and start the input console
			pass
		
	def is_background_event_thread_running(self) -> bool:
		"""
			The background event progress monitors the RequestQueue, ResponseHashTable
			and event monitoring required to keep the Node memory clean
		"""
		return self.background_event_loop.is_alive()

	def __repr__(self) -> str:
		"""
			The node is represented by it's designated ip, port and queue size
		"""
		return f'Node(ip:{self.container_addresses.ip}, ' \
			f'port:{self.container_addresses.port}, ' \
			f'queue-len:{self.socket_request_queue.size_of_queue()})'

	def __eq__(self, other):
		"""
		compares two Node objects based on their configuration parameters
		rather than ip, port, or hardware configurations

		@param other: a object of type Node that is properly configured
		@return: True if the two containers are CUSTOMIZED the same
		"""
		if not isinstance(other, Node):
			return False
		if not isinstance(other, Node):
			return False
		return self.container_customizations == other.container_customizations

	def __del__(self) -> None:
		self.close()
		print('Console: the node has been closed.')
