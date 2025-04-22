from PyQt6.QtWidgets import QGroupBox, QFormLayout, QCheckBox, QDoubleSpinBox

"""
    Initializes the Clock configuration panel:
    - adds all necessary configs
    - set constraints for configs 
    - set default values if no configuration is set (if user didn't load config file)

    Also has a method to extract current configurations from the panel
"""
class ClockConfigPanel(QGroupBox):
    def __init__(self, clockConfig):
        super().__init__("Clock Config")
        
        formLayout = QFormLayout()
        self.setLayout(formLayout)
        
        useRealTime = QCheckBox("Use real-time simulation")
        useRealTime.setToolTip("Enable to synchronize simulation time with real-world time.")
        useRealTime.setObjectName("useRealTime")

        tickDuration = QDoubleSpinBox()
        tickDuration.setToolTip("Duration of each simulation tick or time unit.")
        tickDuration.setRange(0.001, 10.0)  
        tickDuration.setSingleStep(0.1)
        tickDuration.setDecimals(3)
        tickDuration.setObjectName("tickDuration")
        
        useRealTime.setChecked(False)
        tickDuration.setValue(1)

        if clockConfig:
            useRealTime.setChecked(clockConfig.get("useRealTimeSimulation", False))
            tickDuration.setValue(clockConfig.get("tick", 0.1))

        self.layout().addRow(useRealTime)
        self.layout().addRow("Tick:", tickDuration)

        self.useRealTime = useRealTime
        self.tickDuration = tickDuration

    def getClockConfig(self):
        useRealTime = self.useRealTime.isChecked()
        tickDuration = self.tickDuration.value()
        
        if tickDuration <= 0:
            raise ValueError("Tick duration must be greater than zero.")
        
        return {
            "useRealTimeSimulation": useRealTime,
            "tick": tickDuration
        }