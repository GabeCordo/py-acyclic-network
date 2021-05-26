###############################
#		python imports
###############################
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from base64 import b64encode, b64decode

from src.venezia.types.dynamic import Result
from src.venezia.types.errors import MismatchedKeys, MissingRSAKey

###############################
#		   main code
###############################
#an out-of the box and easy to use object-oriented RSA encryption handler for developers
#to implement end-to-end encryption within socket communication
class Handler:
	def __init__(self, directory_key_private=None, directory_key_public=None) -> Result(bool, FileNotFoundError):
		'''
			(Handler, string, string) -> None
			:constructor function of the end-to-end encryption handler
			
			@paramaters directories must point to a valid path
		'''
		##class variables##
		self.directory_key_private = directory_key_private
		self.directory_key_public = directory_key_public
		
		#check to see that the directories given for the encryption keys are valid
		try:
			if (directory_key_private != None):
				#check the private key pathway
				check_pathway = open(directory_key_private, 'r')
				check_pathway.close()
			if (directory_key_public != None):
				#check the public key pathway
				check_pathway = open(directory_key_public, 'r')
				check_pathway.close()
		except FileNotFoundError:
			return Result(None, FileNotFoundError('RSA Key Error: one or more key paths are invalid'))
			
		##instance variables
		self.__private_key = ''
		self.__public_key = ''
		
		self.restoreKeySet()
		return Result(True, None)
	
	def get_public_key(self) -> str:
		'''
			(Handler) -> (string)
			:getter function for the classes public encryption key
			
			@paramaters a public key must exist
			@returns the public key found within the placeholder variable
			@exception returns an empty string if no key was generated or
					   restored
		'''
		return self.__public_key
	
	def get_private_key(self) -> str:
		'''
			(Handler) -> (string)
			:getter function for the classes private encryption key
			
			@paramaters a private key must exist
			@returns the private key found within the placeholder variable
			@exception returns an empty string if no key was generated or
					   restored
		'''
		return self.__private_key
	
	def restore_key_set(self) -> Result(bool, MissingRSAKey):
		'''
			(Handler) -> (boolean)
			:loads all public and private keys from text-files to class variables
			
			@paramaters keys must be pre-initialized within the file directories,
						password must be valid
			@returns boolean true if the keys were transferred from file to instance
					 var
			@exception returns boolean false if there was an issue (password likeley
					   INVALID)
		'''
		if (self.directory_key_private != None):
			#Open the file containing the private key and store in the class instance variable
			try:
				key_private = open(self.directory_key_private, 'rb')
				self.__private_key = key_private.read()
			except Exception:
				return Result(None, MissingRSAKey)
		if (self.directory_key_public != None):
			#Open the file containing the public key and store in the class instance variable
			try:
				key_public = open(self.directory_key_public, 'rb')
				self.__public_key = key_public.read()
			except Exception:
				return Result(None, MissingRSAKey)
		return Result(True, None)
	
	def generate_key_set(self) -> Result(list(str), Exception):
		'''
			(Handler) -> (list of strings)
			:creates a random private key deleting the old private key
			
			@paramaters none
			@returns a list of keys: public at index [0], private at index [1]
		'''
		key = RSA.generate(2048)
		#generate a new private key, store it in the placeholder variable and place it into the directory
		try:
			key_private = key.export_key()
			write_to_file = open(self.directory_key_private, 'wb')
			write_to_file.write(key_private)
			write_to_file.close() #close the file handler
			self.__private_key = key_private
		except Exception as e:
			return Result(None, e)
		#generate a new public key, store it in the placeholder variable and place it into the directory
		try:
			key_public = key.publickey().export_key()
			write_to_file = open(self.directory_key_public, 'wb')
			write_to_file.write(key_public)
			write_to_file.close() #close the file handler
			self.__public_key = key_public
		except Exception as e:
			return Result(None, e)
		return Result((self.__public_key, self.__private_key), None)

	def format_for_encryption(self, message) -> Result():
		'''
			(Handler, string) -> (utf8)
			:turns a string into a utf8 encryptable form for RSA
			
			@returns a utf8 encoded form for encryption
		'''
		if ( isinstance(message, int) ):
			return message.binary_type(message)
		for str_type in six.string_types:
			if isinstance(message, str_type):
				return message.encode('utf8')
		if ( isinstance(message, six.binary_type) ):
			return message
	
	def encrypt(self, message: str, key_public: str) -> Result(str, MismatchedKeys):
		'''
			(Handler, string, string) -> (string)
			:transforms a plain text into a cypher text
			
			@paramaters no value for a password will leave it as an empty string
			@default keyPublic defaults to your public keys path for debugging
		'''
		#python doesn't like us using self declarations in the default tab so in case we are given an
		#empty keyPublic field we need to adhere to using our own public_key for default testing possibly
		if ( key_public == '' ):
			key_public = self.__public_key
		
		try:
			cypher_rsa = RSA.importKey(key_public)
			cypher_rsa = PKCS1_OAEP.new(cypher_rsa)
			#encrypt the given message using a given (or our own) public RSA key 
			message_base64 = b64encode(message.encode('ascii')) #text needs to be in base64 to be encrypted
			return Result(cypher_rsa.encrypt(message_base64), None)
		except Exception:
			return Result(None, MismatchedKeys)
	
	def decrypt(self, text_cyphered: str) -> Result(str, MismatchedKeys):
		'''
			(Handler, string) -> (string)
			:transforms a cypher text into a plain text
		'''
		if (self.directory_key_private != None):
			cypher_rsa = RSA.importKey(self.__private_key)
			cypher_rsa = PKCS1_OAEP.new(cypher_rsa)
			text_plain = cypher_rsa.decrypt(text_cyphered)
			return Result(b64decode( text_plain ).decode(), None)
		else:
			return Result(None, MismatchedKeys)
	
	def __eq__(self, other) -> bool:
		'''
			(Handler) -> (boolean)
			:compares two encryption handlers and compares them based on directories
			
			@returns boolean true if both directories are the same
			@exception returns boolean false if the directories are not the same
		'''
		if (not isinstance(other, Handler)):
			return False
		#check to see if the public key directories are the same
		if (self.directory_key_public != other.directory_key_public):
			return False
		#check to see if the private key directories are the same
		elif (self.directory_key_private != other.directory_key_private):
			return False
		#they are the same; all checks have passed
		return True