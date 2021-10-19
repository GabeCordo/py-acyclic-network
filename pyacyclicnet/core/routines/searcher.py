from pyacyclicnet import constants
from os import walk

from pyacyclicnet.constants import PATH_COLLECTION_ROUTINES, STANDARD_ROUTINE_ROOT_FILES, STANDARD_ROUTINE_ROOT_DIRS
from pyacyclicnet.core.types.errors import RoutineNotFound
from pyacyclicnet.core.types.routine import Routine
from pyacyclicnet.core.types.result import Result

class RoutineSearcher:
    def __init__(self) -> None:
        '''
        '''
        self.routines = {}  # [key:name_of_routine => value:routine_path]
    
    @staticmethod
    def is_valid(path:str) -> bool:
        '''
        '''
        _, dirs, files = walk(PATH_COLLECTION_ROUTINES, topdown=False)
        contains_req_dirs = set(STANDARD_ROUTINE_ROOT_DIRS) <= set(dirs)
        contains_req_files = set(STANDARD_ROUTINE_ROOT_FILES) <= set(files)
        if contains_req_dirs and contains_req_files:
            return True
        return False

    def find_routines(self) -> dict:
        '''
        '''
        for root, dirs, files in walk(PATH_COLLECTION_ROUTINES, topdown=False):
            contains_req_dirs = set(STANDARD_ROUTINE_ROOT_DIRS) <= set(dirs)
            contains_req_files = set(STANDARD_ROUTINE_ROOT_FILES) <= set(files)
            if contains_req_dirs and contains_req_files:
                routine_name = root.split("/")[-1]  # split a pwd by the root / character, the last index should be the name of the routine folder
                self.routines[routine_name] = root  # the root directory of the current index
        
        return self.routines
    
    def load_routine(self, name: str) -> Result(Routine, RoutineNotFound):
        if name not in self.routines:
            return Result(None, RoutineNotFound)
        # pass the directory of the routine we want into the Routine class and generate
        # a new object which contains all the associated metadata to the CustomNode object
        return Routine(self.routines[name])

if __name__ == '__main__':
    r = RoutineSearcher()
    r.find_routines()
    