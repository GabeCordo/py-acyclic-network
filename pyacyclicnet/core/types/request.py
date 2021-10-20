from dataclasses import dataclass
from pyacyclicnet.core.types.enums import RequestCode

@dataclass
class Request:
	ip:str
	request_code:RequestCode
	rsa_pub:str
	cipher:str
	plaintext:str
	authentication:str
	nonce:str

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
		return f'ip:{self.ip}\nrequest:{self.request_code}\nauth:{self.authentication}\n' \
			   + f'nonce:{self.nonce}\n{self.rsa_pub}\n{self.cipher}\n{self.plaintext}'