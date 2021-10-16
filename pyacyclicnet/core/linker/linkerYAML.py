###############################
# python imports
###############################

from yaml import load, dump

###############################
# core imports
###############################

from src.core.linker.linkerTemplate import Linker
from src.core.types.decorators import implements

###############################
# YAML LINKER Wrapper
###############################

TIMER = 60


class LinkerYaml(Linker):
	
	def __init__(self, *args):
		"""
			Constructor function for the YAML handler. This function allows any number of JSON files to be entered under args*.
		"""
		super().__init__(args)

	@implements(Linker)
	def push(self):
		"""
			pushes to the changes in the class
			dictionary to all the YAML files
		"""
		self.template_push(dump)

	@implements(Linker)
	def pull(self):
		"""
			pulls all the data within the YAML
			files that have been pushed as class
			parameters
		"""
		self.template_pull(load)

	@implements(Linker)
	def cleaner(self):
		"""
		@return:
		"""
		self.template_cleaner(TIMER, dump)

	@implements(Linker)
	def start_cleaner(self):
		""""""
		self.template_start_cleaner(TIMER, dump)
