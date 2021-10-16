from pyacyclicnet.network.node import Node
from pyacyclicnet.types import containers

addresses = containers.Addresses(
	ip='',
 	port='1053',
  	ip_index='', 
    ip_backup=''
)

paths = containers.Paths(
	directory_key_public='keys/public2.pem', 
 	directory_key_private='keys/private2.pem',
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
 	containers.NODE
)
n2.settup()

pk = n2.handler_keys.getPublicKey().decode()
message1 = f'2:bob~{pk}~127.0.0.1'
message2 = f'3:bob~127.0.0.1'


result = n2.send('127.0.0.1', message2, 1052)
print(result)