## -------------------------------------------

from typing import Generic
from src.venezia.types import errors

class Result:
    def __init__(self, value_g, exception_g) -> None:
        '''
            (Result, Generic, Exception) -> None
            :Constructor for the Any Class

            @returns nothing
            @exception returns InvalidResultClassArguments exception
        '''
        #either value_g or exception_g needs to have a non None value
        if ((value_g != None) ^ (exception_g != None)):
            self.__value_g = value_g
            self.__exception_g = exception_g
        else:
            raise errors.InvalidResultClassArguments()

    def is_valid(self) -> bool:
        '''
            (Result) -> Boolean
            :A Valid Result.class represents a state where a real value has 
             been placed within the wrapper block

            @returns a boolean representing whether a non-exception value has been placed in the wrapper
        '''
        if (self.__value_g == None):
            return True
        return False

    def value(self):
        '''
            (Result) -> Generic
            :Getter function for the non-exception value placed in the Result.class wrapper
        '''
        return self.__value_g

    def exception(self) -> Exception:
        '''
            (Result) -> Exception
            :Getter function for the exception value placed in the Result.class wrapper
        '''
        return self.__exception_g

    def __eq__(self, other) -> bool:
        '''
            (Result, Result) -> boolean
            :Compares two Result.class wrappers and evalutes the equality of either there
             generic data values OR the exceptions placed in the wrapper
        '''
        # check that other.class is of type Result.class
        if (type(other) != Result):
            # other represents and Exception type we are trying to compare
            if (type(other) == Exception):
                # check if the two exception types are the same
                return (self.__exception_g == other)
            elif (type(self.__value_g) == type(other)):
                # check if the two values we are given are the same
                return (self.__value_g == other)
            else:
                # if they are not both exception and the values are not the same type return false
                return False
        else:
            # do both contain non-exception data values
            if (self.is_valid() and other.is_valid()):
                # are there values of the same type and do they equal eachother
                return ((type(self.__value_g) == type(other.__value_g)) and (self.__value_g == other.value()))
            else:
                # check if the two exception values are the same type
                return (self.__exception_g == other.exception())

## -------------------------------------------

class RequestQueue:
    def __init__(self) -> None:
        self.queue = [] #all unhandled requests will go here

    def size_of_queue(self) -> (int):
        '''
			(RequestQueue) -> (int)
			@returns the size of the queued messages
        '''
        return len(self.queue)
        
    def de_queue(self) -> (str):
        '''
			(RequestQueue) -> (string)
			:retrieves the enqueued messages that have been retrieved by the
			 open port on the node.
			
			@returns a string of max bit-length 1024
			@exception returns an empty string if the queue is empty
		'''
        length_queue = len(self.queue)
        if (length_queue > 0):
			#return the first element in the queue according to the first-in-first-out
			#principle enforced by the queue algorithm
            return self.queue.pop(0)
        else:
			#the queue was empty, no bitsreams have been received or approved for enqueuing
            return ''

## -------------------------------------------

from src.venezia.types import enums
from src.venezia.bitstream.basic import Parser
from datetime import datetime

RESPONSE_TIME_THRESHOLD = 600
TIME_DIFFERENCE = lambda last_time: (datetime.now() - last_time).total_seconds() >= RESPONSE_TIME_THRESHOLD

class ResponseHashTable:
    def __init__(self) -> None:
        self._table = {}

    def __validate_nonce(self, hash: str) -> bool:
        '''
            :checks to see if a nonce hash already exists in the table
            @returns true if the nonce does not exist, allowing the program to proceed
            @exception returns false if the nonce exists in the table already
        '''
        if hash in self._table:
            return False
        else:
            return True
    
    def insert_request(self, request: Parser, lifetime: enums.RequestTableLifetime) -> bool:
        if (request == None):
            return False
        if (self.__validate_nonce(request.nonce)):
            self._table[request.nonce] = [
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

    def get_return_value(self, nonce: str) -> str:
        '''
            :checks to see if a nonce hash exists in the table and if there was ever a response

            @returns the str representation of the response to send to the origin
            @exception returns an empty string if there is no nonce or value
        '''
        try:
            return self._table[nonce][3] # index 3 is the response value
        except Exception as e:
            return ""

    def get_identifiers(self, nonce: str) -> tuple(str, str):
        '''
            :grab the origin and destination values of the nonce request

            @returns a tuple of the origin and destination str identifiers respectively
            @exception returns None if the nonce doesn't exist in the table
        '''
        try:
            return (self._table[nonce][0], self._table[nonce][1]) # index 3 is the response value
        except Exception as e:
            return None

    def get_request_code(self, nonce: str) -> int:
        '''
            :grab the request code associated with the nonce request

            @returns returns an integer representing the request code of the nonce
            @exception returns an arbitrate integer 999 if no nonce request exists
        '''
        try:
            return self._table[nonce][2] # index 2 is the request code
        except Exception as e:
            return 999

    def get_timestamp(self, nonce: str) -> datetime:
        '''
            :grab the timestamp associated with when the request was added to the
             node's hash table.

            @returns returns the datetime value if the nonce exists in the table
            @exception returns None if the nonce request doesn't exists
        '''
        try:
            return self._table[nonce][4] # index 4 is the timestamp for when the request was added to the table
        except Exception as e:
            return None

    def delete_nonce(self, nonce: str) -> bool:
        '''
            :grab the origin and destination values of the nonce request

            @returns returns True if the nonce existed and met the criteria to be deleted
            @exception returns False if the nonce doesn't exist or doesn't meet the citeria to be deleted
        '''
        if not self.__validate_nonce(nonce):
            #if the nonce doesn't exist we don't want the program crashing
            try:
                code = self._table[nonce][5]
                flag = False # flag representing if the nonce was deleted
                if (code == enums.RequestTableLifetime.RESPONDED):
                    if (self.getReturnValue(nonce) != ""): 
                        flag = True
                elif (code == enums.RequestTableLifetime.TIME):
                    if (TIME_DIFFERENCE(self._table[nonce][4])):
                        flag = True
                elif (code == enums.RequestTableLifetime.RESPONDED_TIME):
                    if (TIME_DIFFERENCE(self._table[nonce][4]) and self.getReturnValue(nonce) != ""):
                        flag = True
                if (flag):
                    self._table.pop(nonce)
                return flag
            except Exception as e:
                return False
        return False