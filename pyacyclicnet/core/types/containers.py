from dataclasses import dataclass, field
from os import curdir

###############################
#	IP Address Indexing
###############################

@dataclass
class Addresses:
	ip:str = ''
	port:int = 23245
	ip_index:str = ''
	ip_backup:str = ''

	def key_pair(self) -> list():
		return {
			'ip': self.ip,
			'port': self.port,
   			'index': self.ip_index,
			'backup': self.ip_backup
		}


###############################
#	JSON/RSA Paths Container
###############################

@dataclass
class Paths:
	directory_key_public:str
	directory_key_private:str
	directory_file_logging:str
 
	def key_pair(self) -> list():
		return {
			'public key': self.directory_key_public,
			'private key': self.directory_key_private,
   			'logging': self.directory_file_logging
		}


###############################
#	Customization Container
###############################

@dataclass
class Customizations:
	supports_encryption:bool = True
	supports_listening:bool = True
	supports_monitoring:bool = True
	supports_backup_ip:bool = False
	supports_recovery:bool = True
	supports_console_cout:bool = False
	supports_data_capture:bool = False
	supports_dynamic_interaction:bool = True
	supports_dynamic_keyset:bool = True
 
	def key_pair(self) -> list():
		return {
			'encryption': self.supports_encryption,
			'listening': self.supports_listening,
   			'monitoring': self.supports_monitoring,
			'backup': self.supports_backup_ip,
			'recovery': self.supports_recovery,
			'console-out': self.supports_console_cout,
			'data-capture': self.supports_data_capture,
			'dynamic-interaction': self.supports_dynamic_interaction,
			'dynamic-keysets': self.supports_dynamic_keyset,
		}


## PRE-SET CUSTOMIZATIONS FOR ROUTING NODES

NODE_SETTINGS_DEFAULT = Customizations(
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

PRESET_SETTINGS_ENTRY = Customizations(
	supports_encryption=True,
	supports_listening=True,
	supports_monitoring=False,
	supports_recovery=True,
	supports_console_cout=False
)

PRESET_SETTINGS_BALANCER = Customizations(
	supports_encryption=True,
	supports_listening=True,
	supports_monitoring=False,
	supports_recovery=False,
	supports_console_cout=False
)

PRESET_SETTINGS_INDEX = PRESET_SETTINGS_BALANCER

PRESET_SETTINGS_RELAY = Customizations(
	supports_encryption=False,
	supports_listening=True,
	supports_monitoring=True,
	supports_recovery=True,
	supports_console_cout=False
)

PRESET_SETTINGS_EXIT = Customizations(
	supports_encryption=False,
	supports_listening=True,
	supports_monitoring=True,
	supports_recovery=False,
	supports_console_cout=False
)


###############################
#	 Routine Configuration
###############################

@dataclass
class RoutineAuthor:
	keywords:list = field(default_factory=list)
	classifiers:list = field(default_factory=list)
	documentation:list = field(default_factory=list)
	author_name:str = ''
	author_email:str = ''
	author_site:str = ''
	date:str = ''
	name:str = ''
	version:float = 1.0
	description:str = ''
	licence:str = ''


@dataclass
class RoutineSettings:
    custom_settings:list = field(default_factory=list)
    custom_scripts:list = field(default_factory=list)
    markup_sheets:list = field(default_factory=list)
    port:int = 5078
    return_codes:list = field(default_factory=list)
    buffer_size:int = 1024
    latency_size:int = 4
    using_custom:bool = False
