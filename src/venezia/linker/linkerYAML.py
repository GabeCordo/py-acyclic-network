###############################
#	  	python imports
###############################

from yaml import load, dump

###############################
#	   venezia imports
###############################

from src.venezia.linker import linkerTemplate
from src.venezia.types.decorators import overrides

###############################
#	  YAML LINKER Wrapper
###############################

class Handler(linkerTemplate.Handler):
	
	def __init__(self, *args):
		'''
			(List of Strings) -> None
			:Constructor function for the YAML handler. This function allows any number of JSON files to be entered under args*.  
		'''
		super().__init__(args)
	
	@overrides(linkerTemplate.Handler)
	def push(self):
		'''
			:pushes to the changes in the class
			 dictionary to all the YAML files
		'''
		self.template_push(dump)
		
	@overrides(linkerTemplate.Handler)
	def pull(self):
		'''
			:pulls all the data within the YAML
			 files that have been pushed as class
			 parameters
		'''
		self.template_pull(dump)
		
###############################
#	 		 EOF
###############################