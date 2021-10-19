###############################
#		python imports
###############################

from sys import path
from threading import Thread
from importlib import import_module

###############################
# core imports
###############################

from pyacyclicnet.core.linker.linkerYAML import LinkerYaml
from pyacyclicnet.core.types.containers import Addresses, Paths, Customizations, RoutineAuthor, RoutineSettings

###############################
#		 routine code
###############################

class Routine():
	
	def __init__(self, directory_to_routine):
		'''
			(String) -> None
			:the constructor class for the routine handler function responsible
			 for initializing
		'''
		self.directory_to_routine = directory_to_routine
  
		self._node_customizations = None
		self._node_paths = None
		self._node_addresses = None
  
		self._routine_author = None
		self._routine_settings = None
  
		self._convert_markdown_to_containers()
		
		# these vars will remain as None until the user calls the startup() function
		# we also want this to be private to avoid tampering
		self._node_object = None
  
	def _convert_markdown_to_containers(self):
		'''Grab the contents of the YAML markdowns and place it into the proper container objects.'''
		linker = LinkerYaml(self.directory_to_routine+'author.yaml', self.directory_to_routine+'config.yaml')

  		# these containers will be used to print/retrieve meta-data about the routine
		author_data = linker.data[0]['data']  # author YAML markdown
		self._routine_author = RoutineAuthor(
			author_name = author_data['author']['name'],
			author_email = author_data['author']['email'],
			author_site = author_data['author']['site'],
			date = author_data['author']['date'],
			name = author_data['routine']['name'],
			version = author_data['routine']['version'],
			description = author_data['routine']['description'],
			licence = author_data['routine']['licence'],
			keywords = author_data['routine']['keywords'],
			classifiers = author_data['routine']['classifiers'],
			documentation = author_data['routine']['documentation']
		)
		self._routine_settings = RoutineSettings(
			port = author_data['settings']['port'],
			return_codes = author_data['settings']['return-codes'],
			buffer_size = author_data['settings']['buffer-size'],
			latency_size = author_data['settings']['latency-size'],
			using_custom = author_data['custom']['using-custom'],
			custom_settings = author_data['custom']['custom-settings'],
			custom_scripts = author_data['custom']['custom-scripts'],
			markup_sheets = author_data['custom']['markup-sheets'],
		)

		# these containers will be used to plug-into and run a Node object
		config_data = linker.data[1]['config']  # config YAML markdown
		self._node_addresses = Addresses(
			ip = config_data['addresses']['ip'],
			port = config_data['settings']['port'],
			ip_index = config_data['addresses']['index'],
			ip_backup = config_data['addresses']['backup']
		)
		self._node_paths = Paths(
			directory_key_public = config_data['paths']['rsa']+"public.pem",
        	directory_key_private = config_data['paths']['rsa']+"private.pem",
        	directory_file_logging = config_data['paths']['rsa']+"log.json",
		)
		self._node_customizations = Customizations(
			supports_encryption = config_data['customizations']['encryption'],
			supports_listening = config_data['customizations']['listening'],
			supports_monitoring = config_data['customizations']['monitoring'],
			supports_backup_ip = config_data['customizations']['uses-backup'],
			supports_recovery = config_data['customizations']['recovery'],
			supports_console_cout = config_data['customizations']['console'],
			supports_data_capture = config_data['customizations']['data-capture'],
			supports_dynamic_interaction = config_data['customizations']['dynamic-interaction'],
			supports_dynamic_keyset = config_data['customizations']['dynamic-keyset']
		)

	def has_routine_been_started(self) -> bool:
		'''Checks whether the Node object is a non-None value.'''
		if self._node_object is None:
			return False
		return True
	
	def startup(self):
		'''
			(None) -> (None)
			:the entrypoint into the routine function, this allows the framework to start a
			 custom routine script on a separate thread.
    
			@returns the object of the thread.
  		'''
		# the routine standard requires that the "routine.py" file be placed within the route directory as
		# the entrypoint into the custom piece of code -- here there also needs to be the standard run() func
		custom_module = import_module(self.directory_to_routine + "routine.py")
		self._node_object = custom_module.CustomNode()
		self._node_object.setup()  # the node will spawn 2 new threads (minimum for [1]listening and [2]monitoring)

	def restart(self) -> bool:
		'''Perform a shutdown and startup of the Node object.'''
		if self.shutdown():
			# the return was true meaning the Node object was shutdown successfully
			self.startup()
			return True
		# the Node never shutdown, the function failed and return false
		return False
  
	def shutdown(self) -> bool:
		'''Delete the Node object and remove the reference within the Routine class.'''
		if (self._node_object is None):
			return False

		del(self._node_object)
		self._node_object = None
		return True
      
	def __repr__(self) -> str:
		return f'Routine({self.directory_to_routine})'
    
	def __str__(self):
		print(self._routine_author)
   
	def __del__(self):
		'''Destroy the Node object and the Routine object.'''
		self.shutdown()
		



		
		