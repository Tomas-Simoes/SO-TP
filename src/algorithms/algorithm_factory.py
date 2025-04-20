from algorithms.fcfs import FCFS
from algorithms.shortest_job import ShortestJob
from algorithms.priority import PriorityNonPreemptive, PriorityPreemptive
from algorithms.round_robin import RoundRobin
from algorithms.rate_monotonic import RateMonotonic
from algorithms.earliest_deadline import EarliestDeadline

from config.types.scheduling import SchedulingConfig

def create_algorithm(config: SchedulingConfig):
    algorithmName = config.scheduleAlgorithm.upper()
    
    match algorithmName:
        case "FCFS":
            return FCFS()
        case "SJF" | "SJ" | "SHORTEST_JOB_FIRST":
            return ShortestJob()
        case "PRIORITY_NON_PREEMPTIVE":
            return PriorityNonPreemptive()
        case "PRIORITY_PREEMPTIVE":
            return PriorityPreemptive()
        case "RR" | "ROUND_ROBIN":
            if config and config.timeQuantum:
                return RoundRobin(time_quantum=config["time_quantum"])
            else:
                raise ValueError("Time quantum must be specified for Round Robin scheduling")
        case "RATE_MONOTONIC":
            return RateMonotonic()
        case "EDF" | "EARLIEST_DEADLINE_FIRST":
            return EarliestDeadline()
        case _:
            raise ValueError(f"Unknown scheduling algorithm: {algorithmName}")