from src.core.types.packet import Packet
from src.core.types.result import Result 
from src.core.types.errors import MismatchedSyntax, SanitizerCleaningFailed, SanitizerRestoreFailed

class ProtocolParser:

    def __init__(self) -> None:
        ''''''

    def parse(self, bitsream: str) -> Result(Packet, MismatchedSyntax):
        ''''''
        raw_metadata, raw_path, data = bitsream.split('<>')
        # we may run into the case that we were not supplied enough argument within the packet header
        # meaning that we are missing some key-pieces of data
        if len(raw_metadata) < 5:
            return Result(None, MismatchedSyntax)
        metadata = raw_metadata.split("::")
        path = raw_path.split("::")
        # return the data in a packet object so that the calling section can call dependant functions
        return Result(
            Packet(
            request=metadata[0],
            pat_id=metadata[1],
            pat_auth=metadata[2],
            next_node=metadata[3],
            idp_ip=metadata[4],
            ip_path=path,
            data=data
            ),
            None
        )

    def sanitize(self, data:str) -> Result(str, SanitizerCleaningFailed):
        ''''''
        if (data is None):
            return(None, SanitizerCleaningFailed)
        __tmp_data_lst = list(data)
        for count, value in enumerate(__tmp_data_lst):
            if value == '<':
                __tmp_data_lst[count] = '*0'
            elif value == '>':
                __tmp_data_lst[count] = '*1'
            elif value == ':':
                __tmp_data_lst[count] = '*2'
            elif value == '*':
                __tmp_data_lst[count] = '*3'
        return Result(str(__tmp_data_lst), None)

    def remove_sanitization(self, data:str) -> Result(str, SanitizerRestoreFailed):
        ''''''
        if (data is None):
            return Result(None, SanitizerRestoreFailed)
        __tmp_data_lst = list(data)
        for count, value in enumerate(__tmp_data_lst):
            if value == '*' and count != len(__tmp_data_lst):
                if __tmp_data_lst[count+1] == '0':
                    __tmp_data_lst[count] = '<'
                elif __tmp_data_lst[count+1] == '1':
                    __tmp_data_lst[count] = '>'
                elif __tmp_data_lst[count+1] == '2':
                    __tmp_data_lst[count] = ':'
                elif __tmp_data_lst[count+1] == '3':
                    __tmp_data_lst[count] = '*'
                __tmp_data_lst.remove(count+1)
        return Result(str(__tmp_data_lst), None)
        
        
