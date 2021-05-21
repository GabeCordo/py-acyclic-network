## -------------------------------------------

class Any:
    def __init__(self, value_g) -> None:
        self._value_g = value_g

    def value(self):
        return self._value_g

## -------------------------------------------

class RequestQueue:
    def __init__(self) -> None:
        self.queue = [] #all unhandled requests will go here

    def sizeOfQueue(self) -> (int):
        '''
			(Node) -> (int)
			@returns the size of the queued messages
        '''
        return len(self.queue)
        
    def deQueue(self) -> (str):
        '''
			(Node) -> (string)
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

    def _validate_nonce(self, hash: str) -> bool:
        '''
            :checks to see if a nonce hash already exists in the table
            @returns true if the nonce does not exist, allowing the program to proceed
            @exception returns false if the nonce exists in the table already
        '''
        if hash in self._table:
            return False
        else:
            return True
    
    def insertRequest(self, request: Parser, lifetime: enums.RequestTableLifetime) -> bool:
        if (request == None):
            return False
        if (self._validate_nonce(request.nonce)):
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

    def getReturnValue(self, nonce: str) -> str:
        '''
            :checks to see if a nonce hash exists in the table and if there was ever a response

            @returns the str representation of the response to send to the origin
            @exception returns an empty string if there is no nonce or value
        '''
        try:
            return self._table[nonce][3] # index 3 is the response value
        except Exception as e:
            return ""

    def getIdentifiers(self, nonce: str) -> tuple(str, str):
        '''
            :grab the origin and destination values of the nonce request

            @returns a tuple of the origin and destination str identifiers respectively
            @exception returns None if the nonce doesn't exist in the table
        '''
        try:
            return (self._table[nonce][0], self._table[nonce][1]) # index 3 is the response value
        except Exception as e:
            return None

    def getRequestCode(self, nonce: str) -> int:
        '''
            :grab the request code associated with the nonce request

            @returns returns an integer representing the request code of the nonce
            @exception returns an arbitrate integer 999 if no nonce request exists
        '''
        try:
            return self._table[nonce][2] # index 2 is the request code
        except Exception as e:
            return 999

    def getTimestamp(self, nonce: str) -> datetime:
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

    def deleteNonce(self, nonce: str) -> bool:
        '''
            :grab the origin and destination values of the nonce request

            @returns returns True if the nonce existed and met the criteria to be deleted
            @exception returns False if the nonce doesn't exist or doesn't meet the citeria to be deleted
        '''
        if not self._validate_nonce(nonce):
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