from algorithms.algorithm import Algorithm
from processes.process import Process
from typing import List, Optional


class RoundRobin(Algorithm):
    def __init__(self, time_quantum: float):
        super().__init__()
        self.ready_queue = []
        self.time_quantum = time_quantum
        self.index = -1
    
    def schedule(self) -> Optional[Process]:
        if not self.ready_queue:
            return None
        # Get the shortestJob from the queue
        self.index = (self.index + 1) % len(self.ready_queue)
        return self.ready_queue[self.index]
    
    def process_arrival(self, process: Process) -> None:
        print("Process arrived ", process)
        self.ready_queue.append(process)
    
    def process_completion(self, process: Process) -> None:
        print("Process completed ", process)
        if self.index > 0:
            self.index -= 1
            
        if process in self.ready_queue:
            self.ready_queue.remove(process)