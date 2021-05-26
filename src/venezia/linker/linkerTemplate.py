###############################
#		python imports
###############################
from time import sleep
from threading import Thread

###############################
#	   venezia imports
###############################

from src.venezia.types import errors
from src.venezia.types.dynamic import Result

###############################
#		   main code
###############################
class Handler:
	def __init__(self, *args) -> None:
		'''
			(Handler, n strings) -> None
			:the constructor function of the linkerJSON handler class
			 takes in as many files as are required by the Node or element
			
			@exception throws a FileNotFound() error if one or more of
					   the files are not valid
		'''
		self.files = args
		self.data  = []
		#self.template_pull(None) #validate that the files provided to the class exist
		#TODO - fix this this is based on a legacy version
			
	def template_push(self, dump_function) -> Result(bool, FileNotFoundError):
		'''
			(Handler, Markup Dump Function) -> None
			:responsible for pushing the class dictionaries in data into
			 the JSON files linearly
				
			@exception throws a FileNotFound() error if one or more of the
					   files are not valid
		'''
		try:
			for i in range(0, len(self.files)):
				write_to_markup = open(self.files[i], 'w')
				dump_function(self.data[i], write_to_markup)
				write_to_markup.close()
			return Result(True, None)
		except Exception:
			return Result(None, FileNotFoundError)
	
	def template_pull(self, load_function) -> Result(bool, FileNotFoundError):
		'''
			(Handler, Markup Loader Function) -> None
			:responsible for pulling the data from the JSON files into the
			 class dictionaries linearly
				
			@exception throws a FileNotFound() error if one or more of the
					   files are not valid
		'''
		try:
			for i in range(0, len(self.files)):
				if (self.files[i][0] != None):
					file_current = open(self.files[i][0], 'r')
					self.data.append(load_function(file_current))
					file_current.close()
			return Result(True, None)
		except Exception as e:
			return Result(None, FileNotFoundError)
	
	def cleaner_functionality(self, element):
		'''(Handler) -> None
			:adds special functionality to the Markup updater file
		'''
		pass # this is a slot function
	
	def cleaner(self, timer):
		'''
			(Handler, int) -> None
			:responsible for manipulating and pushing the dictionary data
			 to the Markup files every 'timer' seconds
		'''
		while True:
			#complete this loop every 'timer' seconds
			sleep(timer)
			for file_json in range(0, len(self.files)):
				keys = self.data[file_json].keys()
				for key in range(0, keys):
					element = self.data[file_json][key]
					#pass the element into the additionalFunctionality function to manipulate the local data
					self.additionalFunctionality(element)
			#push all local changes to the JSON files
			self.push()
			
	def start_cleaner(self, timer):
		'''
			(Handler) -> None
			:Starts the cleaner, we want to avoid using it (wastes cpu thread)
			 if we don't need it
		'''
		#thread one and two are occupied by listening port and queue monitor respectively
		thread_three = Thread(target=self.cleaner(timer), args=())
		thread_three.daemon = True
		thread_three.start()