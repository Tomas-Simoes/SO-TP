from algorithms.algorithm import Algorithm
from algorithms.algorithm_factory import create_algorithm
from config.types.scheduling import SchedulingConfig

class Scheduler:
    def __init__(self, schedulingConfig: SchedulingConfig):
        self.schedulingConfig = schedulingConfig
        self.algorithm: Algorithm = create_algorithm(schedulingConfig)

        # test
        self.algorithm.schedule()
        
    def receiveNewProcess(self, newProcess):
        print("new process arrived: ", newProcess)
        return
    
    