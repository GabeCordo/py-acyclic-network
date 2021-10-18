##########################################
# Fatal Errors
##########################################


class NetworkNotConfigured(Exception):
	def __init__(self):
		Exception.__init__(self, f'Fatal Error: There was attempt to use a tor-network that is improperly configured.')


class UnauthorizedNetwork(Exception):
	def __init__(self):
		Exception.__init__(self, f'Fatal Error: There was attempt to attach a node that is not authorized to be apart of a network.')

##########################################
# Generic Network Errors
##########################################


class IllegalRequest(Exception):
	def __init__(self, request):
		Exception.__init__(self, f'Generic Network Error: Illegal Request was provided to the node. This could be missing paramaters is a send request.')
		self.request = request


class CorruptedMessage(Exception):
	def __init__(self, message):
		Exception.__init__(self, f'Generic Network Error: The message can not be decoded by the userid public RSA.')
		self.message = message
  
class NoResponseNeeded(Exception):
	def __init__(self, message):
		Exception.__init__(self, f'Generic Network Error: No network response needed, kill the connection.')
		self.message = message

##########################################
# Security Network Errors
##########################################


class MissingRSAKey(Exception):
	def __init__(self):
		Exception.__init__(self, f'Security Network Error: There was an attempt to send a message to a target-id but the public RSA was missing and cannot be encoded.')


class UnknownFriendWarning(Exception):
	def __init__(self):
		Exception.__init__(self, f'Security Network Error: There was an attempt to send a message to a target-id that has not been friended.')


class UnusualTraffic(Exception):
	def __init__(self):
		Exception.__init__(self, f'Security Network Error: The local relay node received unusual traffic and was automatically shut-down.')


class AuthenticationFailure(Exception):
	def __init__(self):
		Exception.__init__(self, f'Security Network Error: There was a mis-match in authenticator codes, access denied.')

##########################################
# Connection Network Errors
##########################################


class TransferFailure(Exception):
	def __init__(self, ip):
		Exception.__init__(self, f'Connection Network Error: There was an attempt to send a bitstream to a non-responsive node.')
		self.transfer = ip


class NodeIncomingWarning(Exception):
	def __init__(self, transfer):
		Exception.__init__(self, f'Connection Network Warning: Incoming transfer(friend)-requests is toggled off.')
		self.transfer = transfer


class EndToEndOffWarning(Exception):
	def __init__(self):
		Exception.__init__(self, f'Connection Network Warning: End-toEnd encryption on this node is toggled off.')
		
##########################################
# Indexing Node Errors
##########################################


class CleanupFailure(Exception):
	def __init__(self, time):
		Exception.__init__(self, f'Indexing Node Error: There was an attempt to load the local index to the JSON file but an error occurred.')
		self.time = time


class MissingIndex(Exception):
	def __init__(self, request):
		Exception.__init__(self, f'Indexing Node Error: There was an attempt to pull from JSON but the indexing file was missing.')
		self.request = request
		
##########################################
# Balancer Node Errors
##########################################


class TrafficOverloadError(Exception):
	def __init__(self):
		Exception.__init__(self, f'Balancer Node Error: As a result of an unusual amount of requests the Node has closed.')
		
##########################################
# Parsing/Markup Errors
##########################################


class MismatchedSyntax(Exception):
	def __init__(self):
		Exception.__init__(self, f'Parsing Error: There was an attempt to pass incorrect syntax to the parser.')

class SanitizerCleaningFailed(Exception):
	def __init__(self):
		Exception.__init__(self, f'Sanitizer Error: There was a failure while attempting to remove reserved chars from your bitsream.')

class SanitizerRestoreFailed(Exception):
	def __init__(self):
		Exception.__init__(self, f'Sanitizer Error: There was a failure while attempting to restore reserved chars in your bitsream.')
		
##########################################
# Encryption Errors
##########################################


class MismatchedKeys(Exception):
	def __init__(self):
		Exception.__init__(self, f'Encryption Error: the key pair provided is incorrect or corrupted.')


class EncryptionFailed(Exception):
	def __init__(self):
		Exception.__init__(self, f'Encryption Error: there might be an issue with your keys.')
		
##########################################
# Routine Errors
##########################################


class CorruptedRoutine(Exception):
	def __init__(self):
		Exception.__init__(self, f'There was an unknown error encountered when processing the node routine!')


class IncompleteRoutineConfig(Exception):
	def __init__(self):
		Exception.__init__(self, f'The routines config is missing configuration data required by the socket.')


class ConflictingRoutineConfig(Exception):
	def __init__(self):
		Exception.__init__(self, f'The configurations found the in the venezia routine is conflicting, hence, invalid.')

class RoutineNotFound(Exception):
	def __init__(self):
		Exception.__init__(self, f'Could not find a valid routine associated with the provided name.')
  
class RoutineCouldNotShutdown(Exception):
    def __init__(self):
        Exception.__init__(self, f'While attempting to shutdown the routine, there was an error.')
  
##########################################
# Dynamic Errors
##########################################


class InvalidResultClassArguments(Exception):
	def __init__(self):
		Exception.__init__(self, 'Any.class has been given either a value and exception or none at all.')

##########################################
# Queue Errors
##########################################


class QueueEmpty(Exception):
	def __init__(self):
		super().__init__(self, 'Tried popping from an empty Queue.class')

##########################################
# Proc Errors
##########################################

class ProcessLabelInvalid(Exception):
	def __init__(self):
		super().__init__(self, 'The provided label for the new Supravisor child-process is invalid.')

class ProcessLabelNotFound(Exception):
	def __init__(self):
		super().__init__(self, 'Could not find the Process Label under the Supravisor.')