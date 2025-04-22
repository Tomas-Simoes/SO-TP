from PyQt6.QtCore import pyqtSignal, QObject, QThread

from algorithms.algorithm import Algorithm
from algorithms.algorithm_factory import create_algorithm
from config.types.scheduling import SchedulingConfig
from processes.process import Process

from typing import List

class SchedulerWorker(QObject):
    updateProcessesDisplay = pyqtSignal(object)

    def __init__(self, schedulingConfig: SchedulingConfig):
        super().__init__()

        self.schedulingConfig = schedulingConfig
        self.algorithm: Algorithm = create_algorithm(schedulingConfig)

        self.readyProcesses = []
        
    def receiveNewProcess(self, newProcess: Process):
        print("new process arrived: ", newProcess)
        self.readyProcesses.append(newProcess)

        self.updateProcessesDisplay.emit(self.readyProcesses)

    
    