#####################################
#		   Python Imports
#####################################

import cmd, os, sys

#####################################
#		PyAcyclicNet Imports
#####################################

from pyacyclicnet.constants import PATH_CONFIG, PATH_CACHE
from pyacyclicnet.core.linker.linkerJSON import LinkerJson
from pyacyclicnet.core.types.containers import NODE_SETTINGS_TRANSMITTER
from pyacyclicnet.core.routines.searcher import RoutineSearcher

#####################################
#			CLI Imports
#####################################

from pyacyclicnet.cli.requests import local
from pyacyclicnet.cli.graphics import terminal

#####################################
# 		  Global Variables
#####################################

config = LinkerJson(PATH_CONFIG).data[0]

path = ""

routines = RoutineSearcher()
routines.find_routines()  # load all routines into from the common folder

#####################################
#		 Terminal Interface
#####################################

class Interface(cmd.Cmd):
	
	def __init__(self):
		cmd.Cmd.__init__(self)
		self.prompt = terminal.underline("acn") + ' > ' #this will display the node that is currently being configured
		self.cmdloop(intro=terminal.banner())
	
	def do_banner(self, args):
		'''Refresh the manakin client terminal with a new banner.
		'''
		os.system('clear') #clear the terminal to have a fresh start
		self.cmdloop(intro=terminal.banner())
	def def_banner(self, args):
		'''
		'''
		print("syntax: banner")

	
	def do_pending(self, args):
		'''
		'''
		text = local.pull_pending(PATH_CACHE)
		terminal.file('pending', text)
	def def_pending(self, args):
		'''
		'''
		print("syntax: pending")

	
	def do_whitelist(self, args):
		'''
		'''
		if len(args) == 0:
			text = local.pull_whitelist(PATH_CACHE)
			terminal.file('whitelist', text)
		elif args[0] == "--add" or args[0] == '-a':
			result = local.add_whitelist(PATH_CACHE, args)
			terminal.alert('Whitelist', f'Added {args} to the file. ({result})')
		elif args[0] == "--remove" or args[0] == '-r':
			local.remove_whitelist(PATH_CACHE, args)
			terminal.alert('Whitelist', f'Removed {args} from the file.')
	def def_whitelist(self):
		'''
		'''
		print("syntax: whitelist")

	
	def do_blacklist(self, args):
		'''
		'''
		if len(args) == 0:
			text = local.pull_blacklist(PATH_CACHE)
			terminal.file('blacklist', text)
		elif args[0] == "--add" or args[0] == '-a':
			result = local.add_blacklist(PATH_CACHE, args)
			terminal.alert('Blacklist', f'Added {args} to the file. ({result})')
		elif args[0] == "--remove" or args[0] == '-r':
			result = local.remove_blacklist(PATH_CACHE, args)
			terminal.alert('Blacklist', f'Removed {args} to the file. ({result})')
	def def_blacklist(self):
		'''
		'''
		print("syntax: blacklist")
		result = local.remove_blacklist(PATH_CACHE, args)
		terminal.alert('Blacklist', f'Removed {args} to the file. ({result})')
	
 
	def do_routine(self, args):
		'''Toggle the caching of messages received on your client whitelist.
		'''
		pass
	def def_routine(self):
		'''
		'''
		print("syntax: routine")
  
	
	def do_storage(self, args):
		'''Toggle the caching of messages received on your client whitelist.
		'''
		pass
	def def_storage(self):
		'''
		'''
		print("syntax: routine")
	
	
	def do_quit(self, args):
		'''Remove your user-id on the tor indexing server, delete the cache, and close the terminal. 
		'''
		terminal.message(id_user="console", message="Shuting down acn",comment= "goodbye", timestamp=True)
		sys.exit(1)
	def def_quit(self):
		'''
		'''
		print("syntax: quit [userid]")

		
	def do_docs(self, args):
		'''https://github.com/GabeCordo/scms-framework/blob/master/docs/reference.md#Routines
		'''
		print("github.com/GabeCordo/py-acyclic-net/blob/master/docs/reference.md#Routines")
	def def_docs(self):
		'''
		'''
		print("syntax: quit [userid]")