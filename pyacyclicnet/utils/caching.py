#####################################
#		   Python Imports
#####################################

from os import remove

#####################################
#	   fileHandler for Caching
#####################################

class Cache:
	
	def __init__(self, directory):
		self.directory = directory
	
	def generate_path(self, file_identifier):
		'''
			(fileHandler, string) -> (string)
			
			@paramaters a non-empty string is provided
			@returns a modified pathway where the user-id message data
					 should have been cached if created properly
			@exception if an empty-string is provided, the pathway will
					   not be created an an empty string will be returned
		'''
		# a valid cache identifier cannot be an empty-string because it will
		# throw an OS exception for '.txt' being an invalid name
		if (file_identifier == ''):
			return file_identifier
		
		path = (self.directory
				+ file_identifier
				+ '.txt')

		return path

	def write_cached_file(self, identifier, message=''):
		'''
			(fileHandler, string, string) -> (boolean)
			
			@paramaters provided a non-empty string as a user-id
			@returns boolean true if a new cached-file is created
			@exception returns boolean false if the file-exists or the
					   pathway is corrupt or invalid
		'''
		path = self.generate_path(identifier)
		
		try:
			file_manage = open(path, "w+")
			file_manage.write(message)
			file_manage.close()
		except Exception as e:
			print(f'Console: caching experienced {e}')
			return False
		
		# no exceptions were encountered, run successful
		return True
		
	def lookup_cached_file(self, identifier):
		'''
			(fileHandler, string) -> (list of strings)
		
			@paramaters a user-id that is cached is provided
			@returns a list of strings, each index representing a new line
			@exception returns an empty list if the file doesn't exist
		'''
		path = self.generate_path(identifier)
		
		try:
			file_manage = open(path, "r")
			data = file_manage.read().splitlines()  # splits each line based on the '\n' opp.
			file_manage.close()
		except Exception as e:
			print(f'Console: caching experienced {e}')
			return []  # will return an empty list
			
		return data
		
	def lookup_cached_file_string(self, identifier):
		'''
			(fileHandler, string) -> (string)
			
			@paramaters a user-id that is cached is provided
			@returns the cached file as a string
			@exception returns an empty string if the file doesn't exist
		'''
		return '\n'.join(self.lookup_cached_file(identifier))
	
	def lookup_cached_file_element(self, identifier):
		'''
			(fileHandler, string) -> (boolean)
			
			@paramaters none.
			@returns boolean true if the id_user is in the file
			@exception returns boolean false if it is not in the file
		'''
		try:
			temp_list = self.lookup_cached_file(identifier)
			temp_list.pop(identifier)  # will error if it does not exist
		except Exception as e:
			print(f'Console: caching experienced {e}')
			return False
		
		# if it did not error, the user-id must exist
		return True
			
	def append_cached_file(self, identifier, message):
		'''
			(fileHandler, string, string) -> (boolean)
			
			@paramaters a valid user-id was provided
			@returns boolean true if the message paramater was
					 appended to the cache file
			@exception returns boolean false if the data was not
					   written
		'''
		path = self.generate_path(identifier)
		
		try:
			file_manage = open(path, "a")
			file_manage.write(message + '\n')
			file_manage.close()
		except Exception as e:
			print(f'Console: caching experienced {e}')
			return False
		
		# no exceptions were encountered, run successful
		return True
	
	def delete_cached_file(self, identifier):
		'''
			(fileHandler) -> (boolean)
			
			@return boolean true if the cache file was deleted
			@exception returns boolean false if the file was not
					   deleted from the cache folder
		'''
		path = self.generate_path(identifier)
		
		try:
			remove(path)  # linked to os.remove
		except Exception as e:
			print(f'Console: caching experienced {e}')
			return False
			
		# no exceptions were encountered, run successful
		return True
	
	def delete_cached_element(self, identifier, element):
		'''
			(fileHandler) -> (boolean)
			
			@paramaters a valid user-id is provided
			@returns boolean true if the data embedded within the
					 cache file that matched the 'element' param
					 was exclusively removed from the file
			@exception returns boolean false if the paramaters
					   were not met
					
			** if the element d.n.e will return true still **
		'''
		# grab the data currently stored within the cache file
		data = self.lookup_cached_file(identifier)
		i = data.index(element)  # index the element we want to remove
		data.pop(i)
		
		path = self.generate_path(identifier)
		
		try:
			file_manage = open(path, 'w')
			for line in range(0, len(data)):
				file_manage.write(data[line])  # write the data back into the file
			file_manage.close()
		except Exception as e:
			print(f'Console: caching experienced {e}')
			return False
		
		# no exceptions were encountered, run successful
		return True
	
	def __del__(self):
		'''
			(fileHandler) -> None
		'''
		pass