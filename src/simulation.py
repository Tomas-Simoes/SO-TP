from config.config import Config

from clock import Clock
from scheduler import Scheduler
from processes.process_generation import ProcessGenerator

class Simulation:
    def __init__(self, configDir="./config.json"):
        # Initializes our simulation configuration
        config = Config(configDir)
        processGenConfig = config.processGenerationConfig
        clockConfig = config.clockConfig
        schedulingConfig = config.schedulingConfig

        # Responsible for generate processes using probabilistics distributions
        processGenerator = ProcessGenerator(processGenConfig)

        processList = (processGenerator.generate_random_processes()
                       if processGenConfig.useProcessGeneration
                       else processGenerator.get_static_processes())

        # Responsible to decide which process to execute
        self.scheduler = Scheduler(schedulingConfig)

        # Responsible for feading the Scheduler with a process when it arrives
        self.clock = Clock(clockConfig, self.scheduler, processList)
        self.clock.start()

