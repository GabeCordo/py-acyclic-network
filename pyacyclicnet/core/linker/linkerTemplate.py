###############################
# python imports
###############################

from time import sleep
from threading import Thread

###############################
# core imports
###############################

from src.core.types.result import Result

###############################
# main code
###############################


class Linker:
	def __init__(self, *args) -> None:
		"""
			the constructor function of the linkerJSON handler class
			takes in as many files as are required by the Node or element
			
			@exception throws a FileNotFound() error if one or more of
					the files are not valid
		"""
		self.files = args
		self.data = []
		# self.template_pull(None) #validate that the files provided to the class exist
		# TODO - fix this this is based on a legacy version
			
	def template_push(self, dump_function) -> Result(bool, FileNotFoundError):
		"""
			responsible for pushing the class dictionaries in data into
			the JSON files linearly
				
			@exception throws a FileNotFound() error if one or more of the
					files are not valid
		"""
		try:
			for i in range(0, len(self.files)):
				write_to_markup = open(self.files[i], 'w')
				dump_function(self.data[i], write_to_markup)
				write_to_markup.close()
			return Result(True, None)
		except FileNotFoundError as e:
			return Result(None, e)
	
	def template_pull(self, load_function) -> Result(bool, FileNotFoundError):
		"""
			responsible for pulling the data from the JSON files into the
			class dictionaries linearly
				
			@exception throws a FileNotFound() error if one or more of the
					files are not valid
		"""
		try:
			for i in range(0, len(self.files)):
				if self.files[i][0] is not None:
					file_current = open(self.files[i][0], 'r')
					self.data.append(load_function(file_current))
					file_current.close()
			return Result(True, None)
		except FileNotFoundError as e:
			return Result(None, e)
	
	def cleaner_functionality(self, element):
		"""
			adds special functionality to the Markup updater file
		"""
		raise NotImplementedError
	
	def template_cleaner(self, timer, dump_function):
		"""
			responsible for manipulating and pushing the dictionary data
			to the Markup files every 'timer' seconds
		"""
		while True:
			# complete this loop every 'timer' seconds
			sleep(timer)
			for file_json in range(0, len(self.files)):
				keys = self.data[file_json].keys()
				for key in range(0, keys):
					element = self.data[file_json][key]
					# pass the element into the additional_functionality function to manipulate the local data
					self.cleaner_functionality(element)
			# push all local changes to the JSON files
			self.template_push(dump_function)
			
	def template_start_cleaner(self, timer, dump_function):
		"""
			Starts the cleaner, we want to avoid using it (wastes cpu thread)
			if we don't need it
		"""
		# thread one and two are occupied by listening port and queue monitor respectively
		thread_three = Thread(target=self.template_cleaner(timer, dump_function), args=())
		thread_three.daemon = True
		thread_three.start()
