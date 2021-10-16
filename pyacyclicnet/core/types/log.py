from time import ctime
from src.core.types.enums import RequestCode


class Log:
	def __init__(self, message: str, description: str,
				request_code: RequestCode, latency: int):
		"""
		"""
		self.message = message
		self.description = description
		self.request_code = request_code
		self.time = ctime()
		self.latency = latency

	def serialize(self) -> dict:
		"""
		"""
		return {
			'msg': self.message,
			'des': self.description,
			'data': {
				'req': self.request_code,
				'time': self.time,
				'lat': self.latency
			}
		}

	def un_serialize(self, json_dic) -> None:
		"""
		"""
		self.message = json_dic['msg']
		self.description = json_dic['des']
		self.request_code = json_dic['data']['req']
		self.time = json_dic['data']['time']
		self.latency = json_dic['data']['lat']

	def __eq__(self, other) -> bool:
		"""
		"""
		if other is None:
			return False
		if not isinstance(other, Log):
			return False
		if self.request_code == other.request_code:
			return True
		return False

	def __str__(self) -> str:
		"""
		"""
		return f'({self.time}:{self.request_code}) {self.message}\n{self.description}\n{str(self.request_code)}'

	def __repr__(self) -> str:
		"""
		"""
		return f'Log({self.time}, {self.request_code})'
