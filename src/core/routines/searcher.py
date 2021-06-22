from posixpath import dirname
from src import constants
from os import walk

class Searcher:
    def __init__(self) -> None:
        '''
        '''
        self.routines = []

    def _add_routine(self):
        pass

    def _find_routines(self):
        '''
        '''

        # collect the name of folders within the 'common/collection' directory
        _, routine_names, _ = next(walk(constants.PATH_COLLECTION_ROUTINES))

        # iterate over the folder names and try to add them as routines
        for i in len(routine_names):
            self._add_routine(routine_names[i])
