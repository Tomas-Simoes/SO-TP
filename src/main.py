from config.config import Config

from clock import Clock
from scheduler import Scheduler
from processes.process_generation import ProcessGenerator


def bootstrap():
    # Responsible for extracting modules configurations from ./config.json
    config = Config("./config.json")
    processGeneratorConfig = config.processGenerationConfig
    clockConfig = config.clockConfig
    schedulingConfig = config.schedulingConfig

    # Responsible for generate processes using probabilistics distributions
    processGenerator = ProcessGenerator(processGeneratorConfig)

    processList = []
    if processGeneratorConfig.useProcessGeneration:
        processList = processGenerator.generate_random_processes() 
    else:
        processList = processGenerator.get_static_processes()

    # Responsible to decide which process to execute
    scheduler = Scheduler(schedulingConfig)

    # Responsible for feading the Scheduler with a process when it arrives
    clock = Clock(clockConfig, scheduler, processList)
    clockThread = clock.thread


if __name__ == "__main__":
    bootstrap()