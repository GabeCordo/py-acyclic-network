###############################
#		python imports
###############################

from sys import path

###############################
# core imports
###############################

from src.core.linker import linkerYAML, linkerJSON

###############################
#		 routine code
###############################

class Handler(linkerYAML.Handler):
	
	def __init__(self, directory_to_routine):
		'''
			(String) -> None
			:the constructor class for the routine handler function responsible
			 for initializing
		'''
		super().__init__(directory_to_routine + 'author.yaml', directory_to_routine + 'config.yaml')
		
		self.sheet_author = self.data[0]
		self.sheet_config = self.data[1]
		
		self.directory_to_routine = directory_to_routine
		
		self.loadConfigurations() #check all the configurations in the file
		
		self.list_of_scripts = self.loadScripts()
		self.list_of_markdowns = self.loadMarkdowns()
	
	def change_ip(self, ip):
		'''
			(int) -> None
			:changes the ip-address that is located on the config sheet, this may be required
			 if the port-forwarded ip address has changed for some reason or the script has
			 been moved to a new machine
		'''
		self.sheet_config['config']['addresses']['ip'] = ip
		self.push() #dump the changes of the YAML configuration file to the stored location
	
	def uses_custom_settings(self):
		'''
			(None) -> (boolean)
			:returns whether the routine implements custom scripts, markup-sheets or settings
			 for the protocol listed under a specific section of the configuration sheet
		'''
		return self.sheet_config['config']['custom']['using-custom']
	
	def load_configurations(self):
		'''
			(None) -> (boolean)
			:create a reference to the location of the custom-config's dictionary
			 starting key to avoid redundant and convoluted dictionary syntax
		'''
		if self.usesCustomSettings():
			self.sheet_custom = self.sheet_config['config']['custom']
			return True
			
		#the custom-setting flag is set to false on the config sheet, so we will not
		#initialize any data that may, or may not exist past this point
		return False
		
	def load_markdowns(self):
		'''
			(None) -> (boolean)
		'''
		##there are 3 officially supported markups: JSON, YAML, GORM. All are stored in
		#arrays within the custom-markup key and can access each file by indexing
		self.list_of_markdowns.append(linkerJSON.Handler(self.sheet_config['config']['custom']['custom-markup'][0]))
		self.list_of_markdowns.append(linkerYAML.Handler(self.sheet_config['config']['custom']['custom-markup'][1]))
		
		#there has yet to be a linker written for GORM, as GORM is under development
	
	def load_scripts(self):
		'''
			(None) -> (boolean)
		'''
		path.append(self.directory_to_routine + '/scripts/official/')
		import dtpf, icf, qmf, rcf
		
		