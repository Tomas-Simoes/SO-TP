from PyQt6.QtCore import pyqtSignal, QObject, QThread, QDateTime

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
        baseTick_ms = 1000  # 1 second as base unit
        simulationSpeed = self.config.tick  # How fast simulation should run
        
        realTimeSleep_ms = int(baseTick_ms / simulationSpeed)
        simulationTick_ms = int(baseTick_ms)  
        
        hours = minutes = seconds = milliseconds = total_ms = 0
        
        while (len(self.processList) > 0 or self.scheduler.hasRunningProcesses()):
            GlobalClock.setSimulationTime(total_ms)

            total_ms += simulationTick_ms
            newProcess = self.checkNewArrivals(total_ms / 1000)
            if newProcess:
                self.processList.pop(0)
                self.scheduler.receiveNewProcess(newProcess)
                
            self.scheduler.runSchedulingCycle()
            
            QThread.msleep(realTimeSleep_ms)

    def checkNewArrivals(self, currentClock):
        if self.processList:
            currentProcess = self.processList[0]
        else:
            return None

        if currentProcess.arrivalTime <= currentClock:
            return currentProcess

        return None
    
class GlobalClock():
    currentTime_ms = 0
    simulationTime_ms = 0
    lastRealTime = 0

    def updateGlobalTime():
        nowRealTime = QDateTime.currentMSecsSinceEpoch()
        timeElapsed = nowRealTime - GlobalClock.lastRealTime

        GlobalClock.currentTime_ms = GlobalClock.simulationTime_ms + timeElapsed

        print("current clock: ", GlobalClock.currentTime_ms)
        print("timeElapsed: ", timeElapsed)

    def setSimulationTime(time):
        GlobalClock.lastRealTime = QDateTime.currentMSecsSinceEpoch()
        GlobalClock.simulationTime_ms = time 

    def getTime():
        return GlobalClock.currentTime_ms