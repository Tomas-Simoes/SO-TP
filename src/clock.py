from PyQt6.QtCore import pyqtSignal, QObject, QThread

from typing import List

from config.types.clock import ClockConfig
from scheduler import SchedulerWorker
from processes.process import Process

class ClockWorker(QObject):
    updateClockDisplay = pyqtSignal(int, int, int, int)

    def __init__(self, config: ClockConfig, scheduler: SchedulerWorker, processList: List[Process]):
        super().__init__()
        self.processList = processList
        self.config = config
        self.scheduler = scheduler

    def runTickBased(self):
        tick_ms = int(self.config.tick * 1000)
        hours = minutes = seconds = milliseconds = total_ms = 0

        while (len(self.processList) > 0 or self.scheduler.hasRunningProcesses()):
            milliseconds += tick_ms

            if milliseconds >= 1000:
                seconds += milliseconds // 1000
                milliseconds %= 1000

                if seconds >= 60:
                    minutes += seconds // 60
                    seconds %= 60

                    if minutes >= 60:
                        hours += minutes // 60
                        minutes %= 60  

            self.updateClockDisplay.emit(int(hours), int(minutes), int(seconds), int(milliseconds))

            total_ms += tick_ms
            newProcess = self.checkNewArrivals(total_ms / 1000)
            
            if newProcess:
                self.processList.pop(0)
                self.scheduler.receiveNewProcess(newProcess)
                
            self.scheduler.runSchedulingCycle()
            
            QThread.msleep(tick_ms)

    def checkNewArrivals(self, currentClock):
        if self.processList:
            currentProcess = self.processList[0]
        else:
            return None

        if currentProcess.arrivalTime <= currentClock:
            return currentProcess

        return None
    
    
