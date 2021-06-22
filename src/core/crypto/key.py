from src.core.crypto import rsa
from src.core.types import enums
from src.core.types.result import Result


class Keys:
	def __init__(self, type_encryption, directory_key_private, directory_key_public):
		"""
			constructor function of the RSA Key Pair Class

			@parameters directories must point to a valid path
		"""
		# class variables
		self.type_encryption = type_encryption
		self.directory_key_private = directory_key_private
		self.directory_key_public = directory_key_public

		# check keys
		self._publicKey = ''
		self._privateKey = ''
		self.verify_path()  # verify the are not corrupted

	def verify_path(self) -> Result(bool, Exception):
		"""
			checks whether the pathways provided are a valid key pair

			@returns nothing reveals the key pairs are not corrupted
			@exception throws MismatchedKeys() error
		"""
		try:
			if self.type_encryption == enums.Encryption.RSA:

				# use the directory of the public key to encrypt a test message
				h = rsa.Handler(self.directory_key_private, self.directory_key_public)
				message = 'test keys'
				encrypted = h.encrypt(message, h.get_public_key())

				# check if the original message and the decryption match
				if message == h.decrypt(encrypted):
					# if so, we can push them to the class variables and stop the function
					self._publicKey = h.get_public_key()
					self._privateKey = h.get_private_key()

				return Result(True, None)
		except Exception as e:
			return Result(None, e)

	def get_public_key(self) -> str:
		"""
			the getter function for the public encryption key

			@returns the public encryption key
		"""
		return self._publicKey

	def get_private_key(self) -> str:
		"""
			the getter function for the private encryption key

			@returns the private encryption key
		"""
		return self._privateKey

	def serialize(self) -> dict:
		pass

	def un_serialize(self, json_dic) -> None:
		pass
