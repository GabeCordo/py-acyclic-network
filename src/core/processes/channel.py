###############################
#		python imports
###############################

###############################
# core imports
###############################

from typing import Generic, Tuple
from src.core.timing.timer import Timer

###############################
#		Container Class
###############################

class Channel:
	
	def __init__(self, class_g):
		'''
			(Container, Generic) -> None
			:the constructor for the Container class
			
			@paramters an object with a valid de-constructor function must be
					   provided to the wrapper class
			@paramters the generic should be a type of Node socket
		'''
		self.class_g = class_g #the class passed to be wrapped by the container
		self.alive = 0.0 #time the container has been alive
		
		self._timer = Timer() #records the time container was created
		self._metadata = []
	
	def time_running(self) -> float:
		'''
			(Container) -> (float)
			:return the time the the Container has been alive for since being
			 initialized
			
			@returns a float representing the time on the heap 
		'''
		return self._timer.timeAlive()

	def freeze(self):
		# TODO
		pass

	def restart(self):
		# TODO
		pass
		
	def kill(self) -> float:
		'''
			(Container) -> (float)
			:calls the destructor method of the class argument pushed to generic
			 and stops the timer, returning the total runtime of the object
			
			@returns a float representing the total runtime of the object 
		'''
		del(self.class_g)
		del(self._timer)
	
	def __eq__(self, other) -> bool:
		'''
			(Container, object) -> (boolean)
			:compares two wrapper containers based upon the time they have been
			 running (upon initialization)
			
			@paramaters object must be of type Container
			@returns boolean true if the two containers are equal
			@exception returns boolean false if the two times are not the same
		'''
		if (type(other) != type(self)):
			return False
			
		if (self.alive != other.alive):
			return False
			
		return True
		
	def __lt__(self, other) -> bool:
		'''
			(Container, object) -> (boolean)
			:compares two wrapper containers based upon whether the current object
			 is less than the other object
			
			@paramaters object must be of type Container
			@returns boolean true if this container is less than the other container
			@exception returns boolean false if this container is greater
		'''
		if (type(other) != type(self)):
			return False
			
		if (self.alive > other.alive):
			return False
		
		return True
		
	def __gt__(self, other) -> bool:
		'''
			(Container, object) -> (boolean)
			:compares two wrapper containers based upon whether the current object
			 is greater than the other object
			
			@paramaters object must be of type Container
			@returns boolean true if this container is greater than the other
			 		 container
			@exception returns boolean false if this container is less than the
					   other container
		'''
		if (type(other) != Channel):
			return False
			
		if (self.alive < other.alive):
			return False
		
		return True
		
	def __str__(self) -> str:
		'''
			(Container) -> (string)
			:this function overrides the string-representation of the Container
			 class by presenting a client-friendly output
			
			@returns a string representing the Container class with the name of
					 the Generic class and the life-time of the container
		'''
		return f'Container({self.class_g}, {self.alive})'
	
	def __repr__(self) -> Tuple():
		'''
			(Container) -> (Generic, list of Generics)
			:the Container class is represented as a tuple which contains the
			 class along with the meta-data that is required to be stored along-
			 side it
			
			@returns a tuple of the class and the metadata list
		'''
		return (self.class_g, self._metadata)