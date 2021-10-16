#####################################
#		   Python Imports
#####################################

from pyacyclicnet.core.linker import linkerJSON

#####################################
#		   MANAKIN CONFIGs
#####################################

class Config:
	
	def __init__(self, path):
		'''
			(Config, string) -> None
		'''
		self.l = linkerJSON.Handler(path)
		self.l.pull()
		self.config = self.l.data[0]
	
	##		Config Settings		##
	
	def get_port(self):
		'''
			(Config) -> (int)
		'''
		return self.config['settings']['port']
	
	def set_port(self, port):
		'''
			(Config, int) -> None
		'''
		self.config['settings']['port'] = port
		self.l.push()
	
	def is_indexed(self):
		'''
			(Config) -> (boolean)
		'''
		return self.config['settings']['indexed']
	def set_indexed(self, index):
		'''
			(Config, boolean) -> None
		'''
		self.config['settings']['indexed'] = index
		self.l.push()
	
	def is_incoming(self):
		'''
			(Config) -> (boolean)
		'''
		return self.config['settings']['incoming']		
	def set_incoming(self, incoming):
		'''
			(Config, boolean) -> None
		'''
		self.config['settings']['incoming'] = incoming
		self.l.push()
	
	##		Caching Settings		##
	
	def is_caching(self):
		'''
			(Config) -> (boolean)
		'''
		return self.config['caching']['enabled']
	def set_caching(self, cache):
		'''
			(Config, boolean) -> None
		'''
		self.config['caching']['enabled'] = cache
		self.l.push()
		
	def directory_caching(self):
		'''
			(Config) -> (string)
		'''
		return self.config['caching']['directory']
	def set_directory_caching(self, directory):
		'''
			(Config, string) -> None
		'''
		self.config['caching']['directory'] = directory
		self.l.push()
	
	##		Entry-Server		##
	
	def get_entry_server(self):
		'''
			(Config) -> (string)
		'''
		return self.config['entry-server']['ip-address']
	def set_entry_server(self, server):
		'''
			(Config, string) -> None
		'''
		self.config['entry-server']['ip-address'] = server
		self.l.push()
	
	##		Encryption Keys		##
	
	def get_directory_public_key(self):
		'''
			(Config) -> (string)
		'''
		return self.config['encryption-keys']['public']
	def set_directory_public_key(self, directory):
		'''
			(Config, string) -> None
		'''
		self.config['encryption-keys']['public'] = directory
		self.l.push()
	
	def get_directory_private_key(self):
		'''
			(Config, string) -> None
		'''
		return self.config['encryption-keys']['private']
	def set_directory_private_key(self, directory):
		'''
			(Config, string) -> None
		'''
		self.config['encryption-keys']['private'] = directory
		self.l.push()
	