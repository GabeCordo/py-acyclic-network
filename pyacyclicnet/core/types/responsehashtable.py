from pyacyclicnet.core.types.enums import RequestTableLifetime
from pyacyclicnet.core.bitstream.parser import ProtocolParser
from datetime import date, datetime
from pyacyclicnet.core.types.result import Result

RESPONSE_TIME_THRESHOLD = 600
TIME_DIFFERENCE = lambda last_time: (datetime.now() - last_time).total_seconds() >= RESPONSE_TIME_THRESHOLD


class ResponseHashTable:
	def __init__(self) -> None:
		"""
			:initializes a new hash-table to store request structs
		"""
		self.__table = {}

	def __validate_nonce(self, hash: str) -> bool:
		"""
			checks to see if a nonce hash already exists in the table
			@returns true if the nonce does not exist, allowing the program to proceed
			@exception returns false if the nonce exists in the table already
		"""
		if hash in self.__table:
			return False
		else:
			return True

	def insert_request(self, packet: ProtocolParser, lifetime: RequestTableLifetime) -> bool:
		"""
		"""
		if packet is None:
			return False
		if self.__validate_nonce(packet.nonce):
			self.__table[packet.nonce] = [
				packet.next_ip,  # destination
				packet.request,  # the request code given to the node
				None,			 # this will be the response of the request 
				datetime.now(),  # the timestamp when the request was put into the table
				lifetime		 # the lifetime that this entry will sit in the table
			]
		else:
			return False
		return True

	def get_return_value(self, nonce: str) -> Result(str, Exception):
		"""
			checks to see if a nonce hash exists in the table and if there was ever a response

			@returns the str representation of the response to send to the origin
			@exception returns an empty string if there is no nonce or value
		"""
		try:
			return Result(self.__table[nonce][2], None)  # index 3 is the response value
		except Exception as e:
			return Result(str, e)

	def get_request_destination(self, nonce: str) -> Result(str, Exception):
		"""
			grab the origin and destination values of the nonce request

			@returns a tuple of the origin and destination str identifiers respectively
			@exception returns None if the nonce doesn't exist in the table
		"""
		try:
			return Result(self.__table[nonce][0], None)  # index 0 is the request destination
		except Exception as e:
			return Result(None, e)

	def get_request_code(self, nonce: str) -> Result(bool, Exception):
		"""
			grab the request code associated with the nonce request

			@returns returns an integer representing the request code of the nonce
			@exception returns an arbitrate integer 999 if no nonce request exists
		"""
		try:
			return Result(self.__table[nonce][1], None)  # index 2 is the request code
		except Exception as e:
			return Result(None, e)

	def get_timestamp(self, nonce: str) -> Result(datetime, Exception):
		"""
			grab the timestamp associated with when the request was added to the
			node's hash table.

			@returns returns the datetime value if the nonce exists in the table
			@exception returns None if the nonce request doesn't exists
		"""
		try:
			return Result(self.__table[nonce][3],
						  None)  # index 4 is the timestamp for when the request was added to the table
		except Exception as e:
			return Result(None, e)

	def delete_nonce(self, nonce: str) -> bool:
		"""
			:grab the origin and destination values of the nonce request

			@returns returns True if the nonce existed and met the criteria to be deleted
			@exception returns False if the nonce doesn't exist or doesn't meet the citeria to be deleted
		"""
		if not self.__validate_nonce(nonce):
			# if the nonce doesn't exist we don't want the program crashing
			try:
				code = self.__table[nonce][4]
				flag = False  # flag representing if the nonce was deleted
				if code == RequestTableLifetime.RESPONDED:
					if self.get_return_value(nonce) != "":
						flag = True
				elif code == RequestTableLifetime.TIME:
					if TIME_DIFFERENCE(self.__table[nonce][3]):
						flag = True
				elif code == RequestTableLifetime.RESPONDED_TIME:
					if TIME_DIFFERENCE(self.__table[nonce][3]) and self.get_return_value(nonce) != "":
						flag = True
				if flag:
					self.__table.pop(nonce)
				return flag
			except Exception:
				return False
		return False
