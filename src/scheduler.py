from PyQt6.QtCore import pyqtSignal, QObject, QThread

from algorithms.algorithm import Algorithm
from algorithms.algorithm_factory import create_algorithm
from config.types.scheduling import SchedulingConfig
from processes.process import Process

from typing import List

class SchedulerWorker(QObject):
    updateProcessesDisplay = pyqtSignal(object)
    processStarted = pyqtSignal(Process)
    processCompleted = pyqtSignal(Process)
    
    def __init__(self, schedulingConfig: SchedulingConfig):
        super().__init__()
        self.schedulingConfig = schedulingConfig
        self.algorithm = create_algorithm(schedulingConfig)
        self.readyProcesses = []
        self.currentProcess = None
        self.current_time = 0
        
    def receiveNewProcess(self, newProcess: Process):
        # Add new process to our list and notify algorithm
        self.readyProcesses.append(newProcess)
        self.algorithm.process_arrival(newProcess)
        self.updateProcessesDisplay.emit(self.readyProcesses)
        
        # Check if we need to schedule something
        self._checkScheduling()
    
    def runSchedulingCycle(self):
        self.current_time += 1
        
        # If we have a current process, execute one time unit
        if self.currentProcess:
            # Execute one time unit
            self.currentProcess.remaining_time -= 1
            
            # Check if process is completed
            if self.currentProcess.remaining_time <= 0:
                completed_process = self.currentProcess
                self.currentProcess = None
                self.algorithm.process_completion(completed_process)
                self.processCompleted.emit(completed_process)
                self.readyProcesses.remove(completed_process)
                
                self._checkScheduling()
        else:
            self._checkScheduling()
        
        # Update the UI
        self.updateProcessesDisplay.emit(self.readyProcesses)
        
        
    def hasRunningProcesses(self):
        return self.currentProcess is not None or len(self.readyProcesses) > 0
    
    def _checkScheduling(self):
        if not self.currentProcess:
            next_process = self.algorithm.schedule()
            if next_process:
                self.currentProcess = next_process
                self.processStarted.emit(next_process)
    