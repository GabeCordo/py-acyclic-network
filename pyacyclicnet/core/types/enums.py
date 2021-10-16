##########################################
# python imports
##########################################

from enum import IntEnum

##########################################
# Node Enums
##########################################

# The type of relay nodes present within the tor network

class Nodes(IntEnum):
	NODE = 0
	ENTRY = 1
	RELAY = 2
	EXIT = 3
	INDEX = 4
	BALANCER = 5


# Whether the node has end-to-end encryption enabled

class Encrypted(IntEnum):
	DISABLED = 0
	ENABLED = 1
	
 
# whether the node is set to listen for incoming traffic by default

class Listening(IntEnum):
	DISABLED = 0
	ENABLED = 1


# this is left for (future) cryptographic implementations

class Encryption(IntEnum):
	RSA = 0
	ECDSA = 1


# DEPRECIATED - this is used as a switch variable for the processing function

class DataTransfer(IntEnum):
	BASIC = 0
	ADVANCED = 1


# Return error constants

class ReturnCode(IntEnum):
	PRE_TRANSFER_FAILURE = 0
	PRE_ENCRYPTION_MISMATCH = 1
	PRE_TRANSFER_TIMEOUT = 2
	POST_TRANSFER_FAILURE = 3
	POST_RESPONSE_TIMEOUT = 4
	POST_CIPHER_CORRUPT = 5
	SUCCESSFUL_TRANSFER = 6


# Default Server Request Codes

class RequestCode(IntEnum):
	PING_SERVER = 1
	SEND_DATA = 2
	SEND_DATA_NO_RESPONSE = 3
	RELAY_FOLLOWUP = 4
	DO_YOU_KNOW = 5


# this indicated whether the sever should enqueue the plaintext request

class EnqueueRequest(IntEnum):
	QUEUE = 0			# there is no response to the client, push it into a to-be-done queue
	PROCESSES = 1		# we need to calculate an encrypted response

 
 # this indicates what type of information we are looking for in a DO_YOU_KNOW request
 
class DoYouKnowOption(IntEnum):
    IP_INDEX = 0
    IP_BACKUP_INDEX = 1
	
##########################################
# Routine Enums
##########################################

class ProcessDataStatus(IntEnum):
    FAILED = 0
    SUCCESS = 1

class Serialize(IntEnum):
	JSON = 0
	YAML = 1

##########################################
# Processes Enums
##########################################


class ProcessType(IntEnum):
	SUPERVISOR = 0
	CHANNEL = 1


class ProcessSpecification(IntEnum):
	START = 0
	RESTART = 1
	SHUTDOWN = 2
	FREEZE = 3


class ProcessRestart(IntEnum):
	PERMANENT = 0
	TEMPORARY = 1  # child process is never restarted
	TRANSIENT = 2  # child process is only restarted if it terminates abnormally


class ProcessStrategies(IntEnum):
	ONE_FOR_ONE = 0  # if a child process is terminated, restart
	ONE_FOR_ALL = 1  # if a child process is terminated, restart all child processes
	REST_FOR_ONE = 2  # if a child process is terminated, restart all processes started after it

##########################################
# RequestHashTable Enums
##########################################


class RequestTableLifetime(IntEnum):
	NEVER = 0  # this is element will exist till the node is terminated
	RESPONDED = 1  # this will be deleted when a response is gathered
	TIME = 2  # the request has lasted longer than the maximum time permitted
	RESPONDED_TIME = 3  # a response is generated OR the time limit has been exceeded