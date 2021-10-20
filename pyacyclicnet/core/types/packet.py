from dataclasses import dataclass, field
from pyacyclicnet.core.types import request

@dataclass
class Packet:
    request:int
    pat_id:str
    pat_auth:str
    next_node:str
    idp_ip:str
    nonce:int
    data:str
    ip_pathlist:list = field(default_factory=list)

    def is_valid(self) -> bool:
        ''''''
        if (self.pat_id is None) or (self.pat_auth is None):
            return False
        return True

    def to_list(self) -> list():
        ''''''
        return [self.request, self.pat_id, self.pat_auth, self.next_node, self.idp_ip, self.nonce, self.ip_path, self.data]
    
    def __eq__(self, o: object) -> bool:
        ''''''
        if (o is None):
            return False
        if not isinstance(o, Packet):
            return False
        if self.pat_auth != o.pat_auth:
            return True
        return True

    def __str__(self):
        ''''''
        header_str = self.request+"::"+self.pat_id+"::"+self.pat_auth+"::"+self.next_node +"::"+self.idp_ip+"::"+self.nonce
        if self.ip_path is not None:
            path_str = "::".join(self.ip_path)
        else:
            path_str = ""
        
        return header_str+"<>"+path_str+"<>"+self.data