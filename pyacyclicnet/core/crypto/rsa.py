###############################
# python imports
###############################

from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from base64 import b64encode, b64decode
from six import binary_type, string_types

###############################
# core imports
###############################

from pyacyclicnet.core.types.result import Result
from pyacyclicnet.core.types.errors import MismatchedKeys, MissingRSAKey, EncryptionFailed

###############################
# main code
###############################
# an out-of the box and easy to use object-oriented RSA encryption handler for developers
# to implement end-to-end encryption within socket communication


class Handler:
	def __init__(self, directory_key_private=None, directory_key_public=None):
		"""
			constructor function of the end-to-end encryption handler
			
			@parameters directories must point to a valid path
		"""
		# class variables
		self.directory_key_private = directory_key_private
		self.directory_key_public = directory_key_public
		
		# check to see that the directories given for the encryption keys are valid
		try:
			if directory_key_private is not None:
				# check the private key pathway
				check_pathway = open(directory_key_private, 'r')
				check_pathway.close()
			if directory_key_public is not None:
				# check the public key pathway
				check_pathway = open(directory_key_public, 'r')
				check_pathway.close()
		except FileNotFoundError:
			pass  # TODO - implement a log error
			
		# instance variables
		self.__private_key = ''
		self.__public_key = ''
		
		self.restore_key_set()
	
	def get_public_key(self) -> str:
		"""
			getter function for the classes public encryption key
			
			@parameters a public key must exist
			@returns the public key found within the placeholder variable
			@exception returns an empty string if no key was generated or
					restored
		"""
		return self.__public_key
	
	def get_private_key(self) -> str:
		"""
			getter function for the classes private encryption key
			
			@parameters a private key must exist
			@returns the private key found within the placeholder variable
			@exception returns an empty string if no key was generated or
					restored
		"""
		return self.__private_key
	
	def restore_key_set(self) -> Result(bool, MissingRSAKey):
		"""
			loads all public and private keys from text-files to class variables
			
			@parameters keys must be pre-initialized within the file directories,
						password must be valid
			@returns boolean true if the keys were transferred from file to instance
					var
			@exception returns boolean false if there was an issue (password likely
					INVALID)
		"""
		if self.directory_key_private is not None:
			# Open the file containing the private key and store in the class instance variable
			try:
				key_private = open(self.directory_key_private, 'rb')
				self.__private_key = key_private.read()
			except FileNotFoundError:
				return Result(None, MissingRSAKey)
		if self.directory_key_public is not None:
			# Open the file containing the public key and store in the class instance variable
			try:
				key_public = open(self.directory_key_public, 'rb')
				self.__public_key = key_public.read()
			except FileNotFoundError:
				return Result(None, MissingRSAKey)
		return Result(True, None)
	
	def generate_key_set(self) -> Result(list[str], Exception):
		"""
			(Handler) -> (list of strings)
			:creates a random private key deleting the old private key
			
			@parameters none
			@returns a list of keys: public at index [0], private at index [1]
		"""
		key = RSA.generate(2048)
		# generate a new private key, store it in the placeholder variable and place it into the directory
		try:
			key_private = key.export_key()
			write_to_file = open(self.directory_key_private, 'wb')
			write_to_file.write(key_private)
			write_to_file.close()  # close the file handler
			self.__private_key = key_private
		except Exception as e:
			return Result(None, e)
		# generate a new public key, store it in the placeholder variable and place it into the directory
		try:
			key_public = key.publickey().export_key()
			write_to_file = open(self.directory_key_public, 'wb')
			write_to_file.write(key_public)
			write_to_file.close()  # close the file handler
			self.__public_key = key_public
		except Exception as e:
			return Result(None, e)
		return Result((self.__public_key, self.__private_key), None)

	def format_for_encryption(self, message: str) -> Result(str, EncryptionFailed):
		"""
			turns a string into a utf8 encrypted form for RSA
			
			@returns a utf8 encoded form for encryption
		"""
		if isinstance(message, int):
			return Result(message.binary_type(message), None)
		for str_type in string_types:
			if isinstance(message, str_type):
				return Result(message.encode('utf8'), None)
		if isinstance(message, binary_type):
			return Result(message, None)
		return Result(None, EncryptionFailed)
	
	def encrypt(self, message: bytes, key_public: bytes) -> Result(str, EncryptionFailed):
		"""
			transforms a plain text into a cypher text
			
			@parameters no value for a password will leave it as an empty string
			@default keyPublic defaults to your public keys path for debugging
		"""
		# python doesn't like us using self declarations in the default tab so in case we are given an
		# empty keyPublic field we need to adhere to using our own public_key for default testing possibly
		if key_public == '':
			key_public = self.__public_key
		
		try:
			cypher_rsa = RSA.importKey(key_public)
			cypher_rsa = PKCS1_OAEP.new(cypher_rsa)
			# encrypt the given message using a given (or our own) public RSA key
			message_base64 = b64encode(message.encode('ascii'))  # text needs to be in base64 to be encrypted
			return Result(cypher_rsa.encrypt(message_base64), None)
		except Exception:
			return Result(None, EncryptionFailed)
	
	def decrypt(self, text_cyphered: str) -> Result(str, MismatchedKeys):
		"""
			transforms a cypher text into a plain text
		"""
		if self.directory_key_private is not None:
			cypher_rsa = RSA.importKey(self.__private_key)
			cypher_rsa = PKCS1_OAEP.new(cypher_rsa)
			text_plain = cypher_rsa.decrypt(text_cyphered)
			return Result(b64decode(text_plain).decode(), None)
		else:
			return Result(None, MismatchedKeys)
	
	def __eq__(self, other) -> bool:
		"""
			compares two encryption handlers and compares them based on directories
			
			@returns boolean true if both directories are the same
			@exception returns boolean false if the directories are not the same
		"""
		if not isinstance(other, Handler):
			return False
		# check to see if the public key directories are the same
		if self.directory_key_public != other.directory_key_public:
			return False
		# check to see if the private key directories are the same
		elif self.directory_key_private != other.directory_key_private:
			return False
		# they are the same; all checks have passed
		return True
