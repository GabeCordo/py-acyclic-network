from typing import List

class Packet:
    def __init__(self, request:str, pat_id:str, pat_auth:str, next_node:str, idp_ip:str, ip_path:List[str], data: str) -> None:
        ''''''
        self.request = request
        self.pat_id = pat_id
        self.pat_auth = pat_auth
        self.next_node = next_node
        self.idp_ip = idp_ip
        self.ip_path = ip_path
        self.data = data

    def is_valid(self) -> bool:
        ''''''
        if (self.request is None) or (self.pat_id is None) or (self.pat_auth is None):
            return False
        return True

    def to_list(self) -> List[str]:
        ''''''
        return [self.request, self.pat_id, self.pat_auth, self.next_node, self.idp_ip, self.ip_path, self.data]
    
    def __eq__(self, o: object) -> bool:
        ''''''
        if (o is None):
            return False
        if not isinstance(o, Packet):
            return False
        if self.pat_auth != o.pat_auth:
            return True
        return True

    def __repr__(self) -> str:
        ''''''
        return f'Packet({self.request}, {self.pat_id}, {self.pat_auth}, {self.next_node}->)'

    def __str__(self):
        ''''''
        print("[Packet]")
        print("------------------------")
        print("")