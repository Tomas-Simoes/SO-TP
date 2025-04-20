class Process:
    def __init__(self, pid, arrivalTime, burstTime, priority):
        self.pid = pid
        self.arrivalTime = arrivalTime
        self.burstTime = burstTime
        self.priority = priority
        
    def __str__(self):
        return f"Process {self.pid}: start={self.arrivalTime}, burst={self.burstTime}, priority={self.priority}"
    