from typing import Tuple
import multiprocessing

from src.core.processes.channel import Channel
from src.core.types.enums import ProcessType, ProcessStrategies, ProcessRestart, ProcessSpecification
from src.core.types.errors import ProcessLabelNotFound, ProcessLabelInvalid
from src.core.types.result import Result

class Supervisor:
    def __init__(self, proc_strategies: ProcessStrategies) -> None:
        ''''''
        self.cores = multiprocessing.cpu_count()
        self.child_processes = {}

    def __process_lifetime_loop(self, process:multiprocessing.Process, proc_restart_option:ProcessRestart):
        process.start()
        process.join()  # wait until the process terminates to restart or close process
        # a non-zero error code implies a non-standard exit causing termination
        if (proc_restart_option is ProcessRestart.TRANSIENT) and process.exitcode != 0:
            pass
        elif (proc_restart_option is ProcessRestart.PERMANENT):
            pass
        # recursively call itself once it's complete
        pass

    def process_new(self, label:str, channel:Channel, proc_restart_option:ProcessRestart, args:Tuple) -> Result(None, ):
        ''''''
        if (label is None) or label == '':
            return Result(None, ProcessLabelInvalid)
        if proc_restart_option is None:
            proc_restart_option = ProcessRestart.TEMPORARY
        if args is None:
            args = ()
        __tmp_new_process = multiprocessing.Process(target=channel,args=args)
        self.child_processes[label] = __tmp_new_process
        self.__process_lifetime_loop(__tmp_new_process, proc_restart_option)

    def process_update(self, label:str, option:ProcessSpecification) -> Result(None, ProcessLabelNotFound):
        ''''''
        # check to see if a child with that label exists
        if (label is None) or (self.child_processes[label] == None):
            return Result(None, ProcessLabelNotFound)
        # label is valid, find out what to do
        if option is ProcessSpecification.START:
            pass
        elif option is ProcessSpecification.RESTART:
            pass
        elif option is ProcessSpecification.FREEZE:
            pass
        else:
            # shutdown the child-process
            pass

    def freeze():
        # TODO
        pass

    def restart():
        # TODO
        pass

    def kill():
        # TODO
        pass
        