from PyQt6.QtCore import pyqtSignal, QObject, QThread

from algorithms.algorithm import Algorithm
from algorithms.algorithm_factory import create_algorithm
from config.types.scheduling import SchedulingConfig
from config.types.clock import ClockConfig
from processes.process import Process

from global_clock import GlobalClock
from typing import List

class SchedulerWorker(QObject):
    updateProcessesDisplay = pyqtSignal(object)
    updateRunningProcessDisplay = pyqtSignal(object)
    updateCompletedProcessesDisplay = pyqtSignal(object, int)
    updateCompletedOverTimeGraph = pyqtSignal(int)
    updateAvgGraph = pyqtSignal(object)
    
    processStarted = pyqtSignal(Process)
    processCompleted = pyqtSignal(Process)
    processPreempted = pyqtSignal(Process, str)
    
    def __init__(self, schedulingConfig: SchedulingConfig, clockConfig: ClockConfig):
        super().__init__()
        self.schedulingConfig = schedulingConfig
        self.clockConfig = clockConfig
        self.algorithm = create_algorithm(schedulingConfig)
        self.readyProcesses = []
        self.completedProcesses = []
        self.currentProcess = None
        self.current_time = 0
        self.updateUITime = 0
        self.processSwitchCount = 0
        
    def receiveNewProcess(self, newProcess: Process):
        # Add new process to our list and notify algorithm
        self.readyProcesses.append(newProcess)
        self.algorithm.process_arrival(newProcess)
        self.updateProcessesDisplay.emit(self.readyProcesses)
        
        # Check if we need to schedule something
        self._checkScheduling()
    
    def runSchedulingCycle(self):
        self.current_time += self.clockConfig.tick
        self.updateUITime += self.clockConfig.tick

        # If we have a current process, execute one time unit
        if self.currentProcess:

            # Execute one time unit
            self.currentProcess.remaining_time -= self.clockConfig.tick
            self.currentProcess.time_in_current_quantum += self.clockConfig.tick

            # Check if process is completed
            if self.currentProcess.remaining_time <= 0:
                completed_process = self.currentProcess
                completed_process.completionTime = self.current_time 
                completed_process.turnaroundTime = completed_process.completionTime - completed_process.arrivalTime
                completed_process.waitingTime = completed_process.turnaroundTime - completed_process.burstTime
                self.currentProcess = None
                self.algorithm.process_completion(completed_process)
                self.processCompleted.emit(completed_process)
                self.completedProcesses.append(completed_process)

                # when a new process is completed, send signal to update CompletedProcess over Time graph
                self.updateCompletedOverTimeGraph.emit(len(self.completedProcesses))
                if completed_process in self.readyProcesses:
                    self.readyProcesses.remove(completed_process)
                
                self._checkScheduling()
                
            # Check if the process current time quantuam is greater or equal to the desired time quantum 
            # if it is we need to stop running that process and run the next one in the queue
            elif self.currentProcess.time_in_current_quantum >= self.schedulingConfig.timeQuantum and self.schedulingConfig.scheduleAlgorithm.upper() == "ROUND ROBIN":
                preempted_process = self.currentProcess
                preempted_process.time_in_current_quantum = 0 
                self.currentProcess = None
                self.processPreempted.emit(preempted_process, "quantum")
                self.algorithm.process_preemption(preempted_process, "quantum")
                self.algorithm.ready_queue.append(preempted_process)
                self._checkScheduling()
                
            # Check if there is any process with higher priority than the currenty being processed 
            # if there is then we stop running that process and run the next the one in queue
            elif (self.currentProcess.priority > min(self.algorithm.ready_queue, key=lambda process: process.priority).priority) and (self.currentProcess.remaining_time > 0) and (len(self.algorithm.ready_queue) > 0) and (self.schedulingConfig.scheduleAlgorithm.upper() == "PRIORITY SCHEDULING (PREEMPTIVE)"):
                preempted_process = self.currentProcess
                self.currentProcess = None 
                self.algorithm.ready_queue.append(preempted_process)
                self.processPreempted.emit(preempted_process, "priority")
                self.algorithm.process_preemption(preempted_process, "priority")
                self._checkScheduling()
                
        else:
            self._checkScheduling()
        
        if self.updateUITime >= 0.1: 
            self.updateProcessesDisplay.emit(self.readyProcesses)
            self.updateRunningProcessDisplay.emit(self.currentProcess)
            self.updateCompletedProcessesDisplay.emit(self.completedProcesses, self.processSwitchCount)

            self.updateUITime = 0

        
    def hasRunningProcesses(self):
        return self.currentProcess is not None or len(self.readyProcesses) > 0
    
    def _checkScheduling(self):
        if not self.currentProcess:
            next_process = self.algorithm.schedule()
            if next_process:
                if not next_process.firstScheduling:
                    next_process.firstScheduling = GlobalClock.getTime()

                self.processSwitchCount += 1
                self.currentProcess = next_process
                self.processStarted.emit(next_process)
    
    def getAllProcesses(self):
        # Combine todas as listas de processos relevantes
        all_processes = []
        
        # Adicionar processos prontos
        if self.readyProcesses:
            all_processes.extend(self.readyProcesses)
        
        # Adicionar processo em execução se existir
        if self.currentProcess is not None:
            all_processes.append(self.currentProcess)
        
        # Adicionar processos completados
        if self.completedProcesses:
            all_processes.extend(self.completedProcesses)
        
        return all_processes

