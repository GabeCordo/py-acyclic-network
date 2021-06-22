from src.core.types.enums import RequestCode


class Request:
	def __init__(self, ip: str, cipher: str, rsa_pub: str, plaintext: str,
			authentication: str, nonce: str, request: RequestCode):
		"""
		"""
		self.ip = ip
		self.request_code = request
		self.rsa_pub = rsa_pub
		self.cipher = cipher
		self.plaintext = plaintext
		self.authentication = authentication
		self.nonce = nonce

	def serialize(self) -> dict:
		"""
		"""
		return {
			'ip': self.ip,
			'req': self.request_code,
			'metdata': {
				'rsa': self.rsa_pub,
				'auth': self.authentication,
				'nonce': self.nonce
			},
			'data': {
				'cipher': self.cipher,
				'plain': self.plaintext
			}
		}

	def un_serialize(self, json_dic) -> None:
		"""
		"""
		self.ip = json_dic['ip']
		self.request_code = json_dic['req']
		self.rsa_pub = json_dic['metdata']['rsa']
		self.cipher = json_dic['data']['cipher']
		self.plaintext = json_dic['data']['plain']
		self.authentication = json_dic['metdata']['auth']
		self.nonce = json_dic['metdata']['nonce']

	def __eq__(self, other) -> bool:
		"""
		"""
		if other is None:
			return False
		if isinstance(other, Request):
			return False
		if self.nonce == other.nonce:
			return True
		return False

	def __str__(self) -> str:
		"""
		"""
		return f'ip:{self.ip}\nrequest:{self.request}\nauth:{self.authentication}\n' \
			   + f'nonce:{self.nonce}\n{self.rsa_pub}\n{self.cipher}\n{self.plaintext}'

	def __repr__(self) -> str:
		"""
		"""
		return f'Request({self.ip}, {self.request}, {self.nonce})'