import pathlib
ROOT_PATH = str(pathlib.Path(__file__).parent.resolve())

from pyacyclicnet.core.network.node import Node
from pyacyclicnet.core.types import containers

from time import sleep

addresses = containers.Addresses(
	ip='',
 	port=23245,
  	ip_index='', 
    ip_backup=''
)

paths = containers.Paths(
	directory_key_public=ROOT_PATH+'/index/private/public1.pem', 
 	directory_key_private=ROOT_PATH+'/index/private/private1.pem',
  	directory_file_logging='index/json/log_node1.json'
)

options = containers.Customizations(
	supports_encryption = True,	
    supports_listening = True,
    supports_monitoring = True,
    supports_backup_ip = False,
    supports_recovery = False,
    supports_console_cout = True,
    supports_data_capture = True,
    supports_dynamic_interaction = False,
    supports_dynamic_keyset = True,
)

n1 = Node(
	container_addresses = addresses,
	container_paths = paths,
	container_customizations = options
)

while True:

		sleep(0.01) #stop the cpu from constantly running at 100% cpu
		
		if (n1.socket_request_queue.size_of_queue() > 0):
			
			bitsream_received = n1.deQueue()
			
			print(bitsream_received)