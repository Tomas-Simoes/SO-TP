import threading 
import time 

from typing import List

from config.types.clock import ClockConfig
from scheduler import Scheduler
from processes.process import Process

class Clock:
    def __init__(self, config: ClockConfig, scheduler: Scheduler, processList: List[Process]):
        self.processList = processList
        self.config = config
        self.scheduler = scheduler

        if self.config.useRealTimeSimulation:
            self.thread = threading.Thread(target=self.eventBasedClock)
        else:
            self.thread = threading.Thread(target=self.tickBasedClock)
    
    def start(self):
        self.thread.start()
    
    def eventBasedClock(self):
        return
    
    def tickBasedClock(self):
        tick = self.config.tick
        clock = 0

        while len(self.processList) != 0:
            newProcess = self.checkNewArrivals(clock)
            
            if newProcess:
                self.processList.pop(0)
                self.scheduler.receiveNewProcess(newProcess)
            
            time.sleep(tick)
            clock += tick

    def checkNewArrivals(self, currentClock):
        currentProcess = self.processList[0]

        if currentProcess.arrivalTime <= currentClock:
            return currentProcess

        return None
    
    
