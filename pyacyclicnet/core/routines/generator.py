###############################
#		python imports
###############################

from os import mkdir, path
from shutil import rmtree, copytree
from shutil import copyfile, copytree
from sys import path

from typing import TypeVar
T = TypeVar('T')

###############################
#	   core imports
###############################

from pyacyclicnet.constants import PATH_COLLECTION_ROUTINES, PATH_COLLECTION_TEMPLATE

from pyacyclicnet.core.linker import linkerYAML, linkerJSON
from pyacyclicnet.core.types.errors import CorruptedRoutine, IllegalRequest
from pyacyclicnet.core.types.enums import SerializeTo
from pyacyclicnet.core.types.containers import Customizations, Paths, Addresses, RoutineAuthor, RoutineSettings

###############################
#		generator code
###############################

class Routine:
	
	def __init__(self, container_routine_author: RoutineAuthor, container_routine_settings: RoutineSettings,
				 container_addresses: Addresses, container_paths: Paths, container_customizations: Customizations):
		'''
			(Routine, Addresses, Paths, Customizations) -> None
			:The constructor function for the Routine generator. Required to initialize
			 the various data-containers needed by the generator to create a proper r-
			 outline directory, furthermore creating holder-class variables for YAML and
			 directory handlers.
		'''
		# routine specific containers
		self.container_routine_author = container_routine_author
		self.container_routine_settings = container_routine_settings
	
		# node specific containers
		self.container_addresses = container_addresses
		self.container_paths = container_paths
		self.container_customizations = container_customizations
  
		# the linker functions for interacting with the JSON and YAML config files
		self.yaml_handler = None
  
		# the directory that will be created once calling the create_routine() function
		# will remain as None until called
		self.directory_root = None
	
	def _generate_template_routine(self) -> bool:
		'''
			(Routine, String) -> None
			:Copies the template for protocol routines found within the source code and
			 creates a deep-copy in the directory provided as an argument to the function
    
			@returns true if the function successfully created a new folder
		'''
		routine_path_new = PATH_COLLECTION_ROUTINES + self.container_routine_author.name
		# if the path in the "common/collections" folder doesn't exist, create a new folder
		if path.exists(routine_path_new):
			return False

		try:
			# we have a default template for routines, we copy that folder into the collection/
			# directory and rename it to what we want the new routine to be
			copytree(PATH_COLLECTION_TEMPLATE, routine_path_new)
			self.yaml_handler = linkerYAML.Handler(self.directory_root+'author.yaml', self.directory_root+'config.yaml')
		except Exception:
			# check to see if we reached the point where a new routine folder was created, though
			# since an exception was called something else failed and we need to remove this garbage
			if path.exists(routine_path_new):
				rmtree(routine_path_new)  # removes all the contents created under the failed routine folder
			return False

		return True
	
	def _dictionary_create_author(self):
		'''
			(Routine) -> (boolean)
			:creates a YAML file for the author/routine information that does not effect the
			 functionality of the 
				
			@returns boolean True if the YAML file was successfully created with the data in the
					 containers passed as class arguments
			@paramaters the _generate_template_routine must have been called creating the blank
						directories and markup files
		'''
		if self.directory_root is None:
			raise CorruptedRoutine

		# the author YAML file will be in the first index (the first file supplied)
		self.yaml_handler.data[0] = {
			"data" : {
				"author" : {
					"name": self.container_routine_author.author_name,
					"email": self.container_routine_author.author_email,
					"site": self.container_routine_author.author_site,
					"date": self.container_routine_author.date
				},
				"routine" : {
					"name": self.container_routine_author.name,
					"version": self.container_routine_author.version,
					"description": self.container_routine_author.description,
					"licence": self.container_routine_author.licence,
					"keywords": self.container_routine_author.keywords,
					"classifiers": self.container_routine_author.classifiers,
					"documentation": self.container_routine_author.documentation
				}
			}
		} 
		self.yaml_handler.push()
		
	def _dictionary_create_config(self):
		'''
			(Routine) -> (boolean)
			:creates a YAML file for the config information that effects the functionality of
			 the routine being implemented
				
			@returns boolean True if the YAML file was successfully created with the data in the
					 containers passed as class arguments
			@paramaters the _generate_template_routine must have been called creating the blank
						directories and markup files
		'''
		if self.directory_root is None:
			raise CorruptedRoutine

  		# the config YAML file will be in the 2nd index (the 2nd file supplied)
		self.yaml_handler.data[1] = {
			"config" : {
				"settings" : {
					"port": self.container_addresses.port,
					"return-codes": self.container_routine_settings.return_codes,
					"buffer-size": self.container_routine_settings.buffer_size,
					"latency-size": self.container_routine_settings.latency_size
				},
				"addresses" : {
					"ip": self.container_addresses.ip,
					"index": self.container_addresses.ip_index,
					"backup": self.container_addresses.ip_backup
				},
				"paths" : {
					"rsa": self.directory_root + '/paths/keys/',
					"logging": self.directory_root + './paths/logging/',
					"markup": self.directory_root + './paths/markup'
				},
				"customizations" : {
					"encryption": self.container_customizations.supports_encryption,
					"listening": self.container_customizations.supports_listening,
					"monitoring": self.container_customizations.supports_monitoring,
					"recovery": self.container_customizations.supports_recovery,
					"console": self.container_customizations.supports_console_cout,
					"data-capture": self.container_customizations.supports_data_capture,
					"dynamic-interaction": self.container_customizations.supports_dynamic_interaction,
					"dynamic-keyset": self.container_customizations.supports_dynamic_keyset
				},
				"custom" : {
					"using-custom": self.container_routine_settings.using_custom,
					"custom-settings": self.container_routine_settings.custom_settings,
					"custom-scripts": self.container_routine_settings.custom_scripts,
					"markup-sheets": self.container_routine_settings.markup_sheets
				}
			}
		}
		self.yaml_handler.push()
	
	def _use_custom_settings(self):
		'''
			:due to the verbose syntax, this is a form of syntactical sugar
			 to make the manipulation of this deep-data in the dictionary
			 easily changeable
		'''
		self.yaml_handler[1]['config']['custom']['using-custom'] = True
		self.yaml_handler.push()
  
	def _using_custom_settings(self) -> bool:
		'''
			:syntactic sugar for the custom settings yaml
		'''
		return self.yaml_handler[1]['config']['custom']['using-custom']
		
	def add_custom_setting(self, identifier:str, value: T):
		'''
			(String, Generic T) -> (None)
			:add an key-data pair to the custom-settings dictionary to the config
			 file for storing information custom to the created routine
			
			@paramaters the generic must be a primitive type supported by the YAML
						markup language
		'''
		# see if we have recorded that we are using custom settings in the config
		if not self._using_custom_settings:
			self._use_custom_settings() # if not, mark it as true now before we add it
		self.yaml_handler[1]['config']['custom']['custom-settings'][identifier] = T
	
	def add_script(self, script_name: str, directory_script: str):
		'''
			(Routine, String, String) -> (None)
			:add a custom python script to the folder in the routine, these are to be
			 called by the official python files
			
			!this custom directory will standardize the location for custom code that 
			 has been abstracted from the official scripts 
				L-> this directory will be imported by default in all official python 
					scripts

			! you need to have .py in the script_name paramater
		'''
		# see if we have recorded that we are using custom settings in the config
		if not self._using_custom_settings:
			self._use_custom_settings() # if not, mark it as true now before we add it
		self.yaml_handler_config['config']['custom']['custom-scripts'].append(script_name)
		# wherever the supplied script was, add it to the /script folder in the routine dir
		copyfile(directory_script, self.directory_root+'/scripts')
	
	def create_markup(self, markup_name:str, data:dict, markup_type:SerializeTo):
		'''
			(Routine, String, RoutineSettings, String) -> (None)
			:add a custom markup file to the folder in the routine, this is for detailed
			 data-sheets that ARE NOT CONFIG SETTINGS
				L-> Config settings are added to the official config yaml markup
			
			!markups must be one of the officially supported languages, check supported
			 markups in the protocol documentation for more information
    
			!the markup name should include the expected .json or .yaml prefix
		'''
		if (markup_name is None) or (data is None):
			raise CorruptedRoutine

		new_file_name = self.directory_root+'/data/'+markup_name
		tmp = open(new_file_name+markup_name, 'w')
		tmp.close()
  
		if markup_type is SerializeTo.JSON:
			l = linkerJSON.LinkerJson(new_file_name)
			l.data[0] = data
			l.push()
		elif markup_type is SerializeTo.YAML:
			l = linkerYAML.LinkerYaml(new_file_name)
			l.data[0] = data
			l.push()
   
		self.yaml_handler[1]['config']['custom']['markup-sheets'].append(markup_name)
		self.yaml_handler.push()
		
	def generate_new_routine(self, routine_name:str):
		'''
			(Routine, String) -> (None)
			:creates a bare-bone routine (based off of the template within the library) and
			 customizes the author and config sheets based on data passed to the class
			
			!scripts, markups and settings must be added individually
		'''
		if routine_name is None:
			raise IllegalRequest
		try:
			self._generate_template_routine()
			self._dictionary_create_author()
			self._dictionary_create_config()
		except Exception:
			raise CorruptedRoutine