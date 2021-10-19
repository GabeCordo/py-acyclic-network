#####################################
#		   Python Imports
#####################################

from pyfiglet import Figlet
from clint.textui import colored
from random import randint
from datetime import datetime

#####################################
#		   ASCII GRAPHICS
#####################################

def watermark():
	'''
		None -> (string)
		
		@returns the programmer and repository details
	'''
	title = 'Venezia v0.1, Coded by: @GabeCordo (GitHub)'
	text = '\n[' + colored.yellow('+') + '] github.com/GabeCordo/manakin-messenger\n'
	return (title + text)

def bird():
	'''
		None -> (string)
		
		@returns a graphic image of a manakin bird
	'''
	banner = ('                        %&@@@\n'
			  + '                      &&@&&@@%#\\\n'
			  + '                   */////#&@%\n'
			  + '                 //((((((%&&@\n'
			  + '               #%%##%%&@@@@&\n'
			  + '              &@@@@@@@@@@@@#\n'
			  + '             @@@@@@@@@@@@@\n'
			  + '	         #@@@@@@#&\n'
			  + '           (%   * &   %\n'
			  + '        /@      %\\     %\\\n'
			  + '      /           ^      ^\n\n'
	)
	return colored.yellow(banner)
	
def logo():
	'''
		None -> (String)
		
		@returns a graphic representation of 'manakin'
	'''
	f = Figlet(font='slant')
	banner = ('\n' + str(colored.yellow(f.renderText(' Manakin'))))
	return banner
	
def banner():
	'''
		None -> (String)
		
		@returns a randomized graphic and the watermark
	'''
	i = randint(0, 2)
	#randomize the graphic
	if i == 0:
		banner = logo() + watermark()
	else:
		banner = bird() + watermark()
	return banner

#####################################
#		   Sheet Graphics
#####################################

MAX_PRINT_BOX_SIZE = 30
ASCII_BORDER = "-"*(MAX_PRINT_BOX_SIZE+1)

ascii_column = lambda largest_string, used_space: " " * (largest_string - used_space) + "| "
ascii_space_ending = lambda data, used_space : " " * (MAX_PRINT_BOX_SIZE - (len(str(data)) + used_space)) + "|"

def print_table(key_pairs: dict):
    '''
		(list(tuple(str, generic))) -> None
		:prints key-pair data into an ascii table.
  
		@param data must be formated in [ (key, pair) , ... ]
    '''
    # calculate the largest key in the dictionary
    largest_key = 0
    for key, _ in key_pairs.items():
        cur_len = len(key)
        if cur_len > largest_key:
            largest_key = cur_len
            
	# print the table to the screen
    print(ASCII_BORDER)
    for key, value in key_pairs.items():
        print("| " + key + ascii_column(largest_key, len(key)) + str(value) + ascii_space_ending(value, largest_key+4))
    print(ASCII_BORDER)
	
#####################################
#		   Data Graphics
#####################################

def file(header, data):
	'''
		(string, list of strings) -> (string)
		
		@returns a pretty version of the file text
	'''
	header = colored.green(header)
	header = f'\n[ {header} ]\n'
	
	line = ''
	for i in range(0, len(data)):
		line = line + f'{i+1}. {data[i]}\n'
	
	footer = colored.green('end of text')
	footer = f'[ {footer} ]\n'
	
	print(header + line + footer)
	
def message(id_user, message, comment, timestamp):
	'''
		(string, string, string, boolean) -> (string)
		
		@returns a pretty version of the received message
	'''
	header = colored.white(id_user)
	header = f'[ {header} ] '
	time = datetime.now()
	
	print(f'{header}{message} // {comment}\t( {time} )') 
	
def alert(header, message):
	'''
		(string, string) -> (string)
		
		@returns an alert titled with the header with the
				 description of the alert being the message
	'''
	header = colored.red(header)
	header = f'[ {header} ] '
	
	print(header + message)
	
def warning(header, message):
	header = colored.magenta(header)
	header = f'[ {header} ]'
	
	print(header + message)

#####################################
#		   		EOF
#####################################
	