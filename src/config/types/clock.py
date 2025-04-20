
class ClockConfig:
    def __init__(self, config_dict):
        self.useRealTimeSimulation = config_dict["useRealTimeSimulation"]
        self.tick = config_dict["tick"]