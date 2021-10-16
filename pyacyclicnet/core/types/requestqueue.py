from pyacyclicnet.core.types.result import Result
from pyacyclicnet.core.types.errors import QueueEmpty


class RequestQueue:
	def __init__(self) -> None:
		self.__queue = []  # all unhandled requests will go here

	def size_of_queue(self) -> int:
		"""
			returns the size of the queued messages
		"""
		return len(self.__queue)

	def push(self, plaintext_request) -> None:
		"""
			pushes a new request onto the queue to be processed
		"""
		self.__queue.append(plaintext_request)

	def de_queue(self) -> Result(str, QueueEmpty):
		"""
			retrieves the enqueued messages that have been retrieved by the
			open port on the node.

			@returns a string of max bit-length 1024
			@exception returns an empty string if the queue is empty
		"""
		length_queue = len(self.__queue)
		if length_queue > 0:
			# return the first element in the queue according to the first-in-first-out
			# principle enforced by the queue algorithm
			return Result(self.__queue.pop(0), None)
		else:
			# the queue was empty, no bitstreams have been received or approved for enqueuing
			return Result(None, QueueEmpty)

	def manipulate(self, index_one: int = -1, index_two: int = -1) -> Result(bool, IndexError):
		"""
		the function's job is to slice the RequestQueue, providing some error
		handling for out-of-bounds bugs that can be cause by slicing out of bounds

		@param index_one: the first index of the slice
		@param index_two: the second index of the slice
		@return: True if it was successful, False if no slice was performed
		@exception: there is only support for Z+ indexing to avoid out of bounds bugs
		"""
		# we are out of bounds of positive indexing in Z+
		# account for the fact that -1 represents an empty slice so it IS valid as a default value
		if (index_one < -1) or (index_two > (len(self.__queue) - 1)):
			return Result(None, IndexError)
		# the left parameter of the slice is empty
		if (index_one == -1) and (index_two != -1):
			self.__queue = self.__queue[:index_two]
		# the right parameter of the slice is empty
		elif (index_two == -1) and (index_one != -1):
			self.__queue = self.__queue[index_one:]
		# bother parameters are empty, we cannot perform a slice
		elif (index_one == -1) and (index_two == -1):
			return Result(False, None)
		else:
			# there are valid index's on both sides of the slice
			self.__queue = self.__queue[index_one:index_two]
		return Result(True, None)
