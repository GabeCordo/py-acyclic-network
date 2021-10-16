###############################
# python imports
###############################

from json import dump, load

###############################
# core imports
###############################

from pyacyclicnet.core.linker.linkerTemplate import Linker
from pyacyclicnet.core.types.decorators import implements

###############################
# JSON LINKER Wrapper
###############################

TIMER = 60


class LinkerJson(Linker):
	
	def __init__(self, *args):
		"""
			Constructor function for the JSON handler. This function allows any number of JSON files to be entered under args*.
		"""
		super().__init__(args)
		self.pull()  # pull the loaded json files (if they exist) into memory
	
	@implements(Linker)
	def push(self):
		"""
			pushes to the changes in the class dictionary to all the JSON files.
		"""
		self.template_push(dump)
	
	@implements(Linker)
	def pull(self):
		"""
			pulls all the data within the JSON files that have been pushed as class
			parameters.
		"""
		self.template_pull(load)

	@implements(Linker)
	def cleaner(self):
		"""
		"""
		self.template_cleaner(TIMER, dump)

	@implements(Linker)
	def start_cleaner(self):
		"""
		This will start the cleaner, we need to assert the clean_functionality method has been defined
		"""
		self.template_start_cleaner(TIMER, dump)
