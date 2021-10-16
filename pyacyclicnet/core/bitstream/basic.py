"""
	INTERFACE FOR PARSING RAW BASIC SERVER BITSTREAMS
		-          DO NOT MODIFY THIS FILE          -

	*** used for bitstream transfers with minimal (one-
		two elements of data on-top of the standard
		request, can be used by any node class: O(n) ***
"""

###############################
# core imports
###############################

from src.core.types.errors import MismatchedSyntax
from src.core.types.result import Result

###############################
# main code
###############################


class BasicParser:
	
	def __init__(self, message='') -> None:
		"""
			(Parser, string) -> None
			@description the constructor class for the simple parser
			
			@syntax (request):(primary_data)~(secondary_data)
						^			^				^
						0			1				2
			
			0: the action the server needs to preform on the data
			1: the most significant piece of data
			2: assisting data to the primary data
			
			@exception throws MismatchedSyntax() Error if given an
					invalid message
		"""
		self.message = message
		
		self.request = ''
		self.data_primary = ''
		self.data_secondary = ''
		self.data_other = []
		
		self.parse()
	
	def parse(self) -> Result(bool, MismatchedSyntax):
		"""
			using indexing, parses the pieces of data into the class
			variables
			
			@returns nothing to the main program but initializes the
					class variables
			@exception if an incorrect syntax is provided, throws
					MismatchedSyntax() Error
		"""
		try:
			request_separator = self.message.index(':')
			
			# the request is from index 0 to the request separator
			self.request = self.message[:request_separator]
			
			# split the data added on-top of the request
			self.data_other = self.message[request_separator+1:].split('~')
			return Result(True, None)
		except IndexError:
			return Result(None, MismatchedSyntax)
		
	def get_request(self) -> str:
		"""
			the getter function for the messages request field
			
			@returns the request parsed from the message during initialization
			@exception returns an empty string if invalid syntax was provided
		"""
		return self.request
		
	def get_primary_data(self) -> str:
		"""
			the getter function for the messages primary data field
			
			@returns the primary data parsed from the message during initialization
			@exception returns an empty string if invalid syntax was provided
		"""
		return self.data_primary
		
	def get_secondary_data(self) -> str:
		"""
			the getter function for the messages secondary data field
			
			@returns the secondary data parsed from the message during initialization
			@exception returns an empty string if invalid syntax was provided
		"""
		return self.data_secondary
		
	def get_other_data(self) -> list[str]:
		"""
			the getter function for the messages other data field(s)
			
			@returns any other data appended to the simple request as a list of strings
			@exception returns an empty string if invalid syntax was provided
		"""
		return self.data_other
		
	def __str__(self) -> str:
		"""
			@returns a string representation of the class variables in the proper
					simple bitstream syntax
		"""
		return f'{self.request}:{self.data_primary}/{self.data_secondary}'
		
	def __repr__(self) -> str:
		"""
			@returns a string representation of the class type
		"""
		return f'Parser({self.message})'
