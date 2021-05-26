###############################
#	  	python imports
###############################

from json import dump, load

###############################
#	   venezia imports
###############################

from src.venezia.linker import linkerTemplate
from src.venezia.types.decorators import overrides

###############################
#	  JSON LINKER Wrapper
###############################

class Handler(linkerTemplate.Handler):
	
	def __init__(self, *args):
		'''
			(List of Strings) -> None
			:Constructor function for the JSON handler. This function allows any number of JSON files to be entered under args*.
		'''
		super().__init__(args)
	
	@overrides(linkerTemplate.Handler)
	def push(self):
		'''
			:pushes to the changes in the class
			 dictionary to all the JSON files.
		'''
		self.template_push(dump)
	
	@overrides(linkerTemplate.Handler)
	def pull(self):
		'''
			:pulls all the data within the JSON
			 files that have been pushed as class
			 parameters.
		'''
		self.template_pull(load)
		
###############################
#	 		 EOF
###############################