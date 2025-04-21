from PyQt6.QtWidgets import QGroupBox, QFormLayout, QDoubleSpinBox, QComboBox

class SchedulingConfigPanel(QGroupBox):
    def __init__(self, schedulingConfig):
        super().__init__("Scheduling Config")
        
        form_layout = QFormLayout()
        self.setLayout(form_layout)
        
        algorithm_combo = QComboBox()
        algorithm_combo.setObjectName("algorithm_combo")
        self.algorithms = [
            "First-Come, First-Served",
            "Shortest Job First",
            "Round Robin",
            "Priority Scheduling (Non-Preemptive)",
            "Priority Scheduling (Preemptive)",
            "Multilevel Queue Scheduling",
            "Earliest Deadline First",
            "Rate Monotonic",
            "Lottery Scheduling"
        ]
        algorithm_combo.addItems(self.algorithms)
        algorithm_combo.setToolTip("Select the scheduling algorithm for the simulation.")

        time_quantum = QDoubleSpinBox()
        time_quantum.setToolTip("Time quantum for algorithms like Round Robin.")
        time_quantum.setRange(0.1, 100.0)  
        time_quantum.setSingleStep(0.1)
        time_quantum.setObjectName("time_quantum")
        
        algorithm_combo.setCurrentText("First-Come, First-Served")
        time_quantum.setValue(2.0)

        if schedulingConfig:
            algorithm = schedulingConfig.get("schedulingAlgorithm", "First-Come, First-Served")
            algorithm_combo.setCurrentText(algorithm)
            
            time_quantum.setValue(schedulingConfig.get("timeQuantum", 2.0))

        self.layout().addRow("Algorithm:", algorithm_combo)
        self.layout().addRow("Time Quantum:", time_quantum)

        self.algorithm_combo = algorithm_combo
        self.time_quantum = time_quantum

    def getSchedulingConfig(self):
        algorithm = self.algorithm_combo.currentText()
        time_quantum = self.time_quantum.value()
        
        # Validate values
        if time_quantum <= 0:
            raise ValueError("Time Quantum must be greater than zero.")
        
        # Build the config object with the correct format
        return {
            "schedulingAlgorithm": algorithm,
            "timeQuantum": time_quantum
        }
