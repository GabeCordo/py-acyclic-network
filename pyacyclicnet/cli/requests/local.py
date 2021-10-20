#####################################
#		Client-Side Requests
#####################################
from pyacyclicnet.utils import caching

##		Whitelist Functions		##

def pull_whitelist(directory):
	'''
		(string) -> (list of strings)
		
		@returns a list of strings where each index represents a user-id
				 that have been approved to send messages to the client
		@exceptions returns an empty list if the directory is invalid
	'''
	__caching = caching.Cache(directory)
	return __caching.lookup_cached_file('whitelist')

def add_whitelist(directory, id_user):
	'''
		(string, string) -> (boolean)
		
		@returns boolean true if the element was successfully added
		@exception returns boolean false if the element was not added
	'''
	__caching = caching.Cache(directory)
	return __caching.append_cached_file('whitelist', id_user)

def remove_whitelist(directory, id_user):
	'''
		(string, string) -> (boolean)
		
		@returns boolean true if the element was successfully removed
		@exception returns boolean false if the element was not removed
	'''
	__caching = caching.Cache(directory)
	return __caching.delete_cached_element('whitelist', id_user)

##		Blacklist Functions		##

def pull_blacklist(directory):
	'''
		(string) -> (list of strings)
		
		@returns a list of strings where each index represents a user-id
				 that have been blocked from sending messages to the client
		@exceptions returns an empty list if the directory is invalid
	'''
	__caching = caching.Cache(directory)
	return __caching.lookup_cached_file('blacklist')

def add_blacklist(directory, id_user):
	'''
		(string, string) -> (boolean)
		
		@returns boolean true if the element was successfully added
		@exception returns boolean false if the element was not added
	'''
	__caching = caching.Cache(directory)
	return __caching.append_cached_file('blacklist', id_user)

def remove_blacklist(directory, id_user):
	'''
		(string, string) -> (boolean)
		
		@returns boolean true if the element was successfully removed
		@exception returns boolean false if the element was not removed
	'''
	__caching = caching.Cache(directory)
	return __caching.delete_cached_element('blacklist', id_user)

##		Pending-File Functions		##

def pull_pending(directory):
	'''
		(string) -> (boolean)
		
		@returns a list of strings where each index represents a user-id
				 that is waiting to be added to the whitelist or blacklist
		@exceptions returns an empty list if the directory is invalid
	'''
	__caching = caching.Cache(directory)
	return __caching.lookup_cached_file('pending')

def add_pending(directory, id_user):
	'''
		(string, string) -> (boolean)
		
		@returns boolean true if the element was successfully added
		@exception returns boolean false if the element was not added
	'''
	__caching = caching.Cache(directory)
	return __caching.append_cached_file('pending', id_user)

def remove_pending(directory, id_user):
	'''
		(string, string) -> (boolean)
		
		@returns boolean true if the element was successfully removed
		@exception returns boolean false if the element was not removed
	'''
	__caching = caching.Cache(directory)
	return __caching.delete_cached_element('pending', id_user)

##		Chat History Functions		##

def pull_chat_history(directory, id_user):
	'''
		(string, string) -> (boolean)
		
		@returns a list of strings where each index represents a message
				 received from the specified user-id that has been cached
		@exceptions returns an empty list if the directory is invalid
	'''
	__caching = caching.Cache(directory)
	return __caching.lookup_cached_file(id_user)

def add_chat_history(directory, id_user, message):
	'''
		(string, string) -> (boolean)
		
		@returns boolean true if the element was successfully added
		@exception returns boolean false if the element was not added
	'''
	__caching = caching.Cache(directory)
	return __caching.append_cached_file(id_user, message)

def delete_chat_history(directory, id_user):
	'''
		(string, string) -> (boolean)
		
		@returns boolean true if the element was successfully removed
		@exception returns boolean false if the element was not removed
	'''
	__caching = caching.Cache(directory)
	return __caching.delete_cached_element(id_user)
	
def splitter(request):
	'''
		(string) -> (list of strings)
	'''
	return request.split(' ')