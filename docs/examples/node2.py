import pathlib
ROOT_PATH = str(pathlib.Path(__file__).parent.resolve())

from pyacyclicnet.core.network.node import Node
from pyacyclicnet.core.types import containers

addresses = containers.Addresses(
	ip='',
 	port=23244,
  	ip_index='', 
    ip_backup=''
)

paths = containers.Paths(
	directory_key_public=ROOT_PATH+'/index/private/public2.pem', 
 	directory_key_private=ROOT_PATH+'/index/private/private2.pem',
  	directory_file_logging='index/json/log_node2.json'
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

n2 = Node(
	addresses,
 	paths,
 	containers.NODE_SETTINGS_DEFAULT
)
n2.setup()

pk = n2.handler_keys.get_public_key()
message1 = f'2:bob~{pk}~127.0.0.1'
message2 = f'3:bob~127.0.0.1'


result = n2.send(port=23245)  # the default send is a "ping" request to see if the server is alive
print(result)