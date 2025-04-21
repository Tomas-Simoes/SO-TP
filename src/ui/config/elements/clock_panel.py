from PyQt6.QtWidgets import QGroupBox, QFormLayout, QCheckBox, QDoubleSpinBox

class ClockConfigPanel(QGroupBox):
    def __init__(self, clockConfig):
        super().__init__("Clock Config")
        
        form_layout = QFormLayout()
        self.setLayout(form_layout)
        
        use_real_time = QCheckBox("Use real-time simulation")
        use_real_time.setToolTip("Enable to synchronize simulation time with real-world time.")
        use_real_time.setObjectName("use_real_time")

        tick_duration = QDoubleSpinBox()
        tick_duration.setToolTip("Duration of each simulation tick or time unit.")
        tick_duration.setRange(0.01, 10.0)  
        tick_duration.setSingleStep(0.1)
        tick_duration.setObjectName("tick_duration")
        
        use_real_time.setChecked(False)
        tick_duration.setValue(0.1)

        if clockConfig:
            use_real_time.setChecked(clockConfig.get("useRealTimeSimulation", False))
            tick_duration.setValue(clockConfig.get("tick", 0.1))

        self.layout().addRow(use_real_time)
        self.layout().addRow("Tick:", tick_duration)

        self.use_real_time = use_real_time
        self.tick_duration = tick_duration

    def getClockConfig(self):
        use_real_time = self.use_real_time.isChecked()
        tick_duration = self.tick_duration.value()
        
        if tick_duration <= 0:
            raise ValueError("Tick duration must be greater than zero.")
        
        return {
            "useRealTimeSimulation": use_real_time,
            "tick": tick_duration
        }