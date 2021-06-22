from src.core.types import enums
from src.core.bitstream.basic import Parser
from datetime import datetime
from src.core.types.result import Result

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

	def insert_request(self, request: Parser, lifetime: enums.RequestTableLifetime) -> bool:
		"""
		"""
		if request is None:
			return False
		if self.__validate_nonce(request.nonce):
			self.__table[request.nonce] = [
				request.origin,
				request.destination,
				request.requestCode,
				request.returnValue,
				datetime.now(),
				lifetime
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
			return Result(self.__table[nonce][3], None)  # index 3 is the response value
		except Exception as e:
			return Result(str, e)

	def get_identifiers(self, nonce: str) -> Result(tuple(str, str), Exception):
		"""
			grab the origin and destination values of the nonce request

			@returns a tuple of the origin and destination str identifiers respectively
			@exception returns None if the nonce doesn't exist in the table
		"""
		try:
			temp_origin = self.__table[nonce][0]
			temp_destination = self.__table[nonce][1]
			return Result((temp_origin, temp_destination), None)  # index 3 is the response value
		except Exception as e:
			return Result(None, e)

	def get_request_code(self, nonce: str) -> Result(bool, Exception):
		"""
			grab the request code associated with the nonce request

			@returns returns an integer representing the request code of the nonce
			@exception returns an arbitrate integer 999 if no nonce request exists
		"""
		try:
			return Result(self.__table[nonce][2], None)  # index 2 is the request code
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
			return Result(self.__table[nonce][4],
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
				code = self.__table[nonce][5]
				flag = False  # flag representing if the nonce was deleted
				if code == enums.RequestTableLifetime.RESPONDED:
					if self.get_return_value(nonce) != "":
						flag = True
				elif code == enums.RequestTableLifetime.TIME:
					if TIME_DIFFERENCE(self.__table[nonce][4]):
						flag = True
				elif code == enums.RequestTableLifetime.RESPONDED_TIME:
					if TIME_DIFFERENCE(self.__table[nonce][4]) and self.get_return_value(nonce) != "":
						flag = True
				if flag:
					self.__table.pop(nonce)
				return flag
			except Exception:
				return False
		return False
