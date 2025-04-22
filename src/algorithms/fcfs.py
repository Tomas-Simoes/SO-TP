from algorithms.algorithm import Algorithm
from processes.process import Process
from typing import List, Optional

class FCFS(Algorithm):
    def __init__(self, time_quantum: float):
        super().__init__()
        self.ready_queue = []
    
    def schedule(self) -> Optional[Process]:
        if not self.ready_queue:
            return None
        return self.ready_queue[0]  
    
    def process_arrival(self, process: Process) -> None:
        print("Process arrived ", process)
        self.ready_queue.append(process)
    
    def process_completion(self, process: Process) -> None:
        print("Process completed ", process)
        if process in self.ready_queue:
            self.ready_queue.remove(process)