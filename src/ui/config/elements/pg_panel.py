from PyQt6.QtWidgets import QGroupBox, QFormLayout, QCheckBox, QSpinBox, QDoubleSpinBox

class PGConfigPanel(QGroupBox):
    def __init__(self, pgConfigurations):
        super().__init__("Process Generation Config")
        form_layout = QFormLayout()
        self.setLayout(form_layout)
        
        use_random_gen = QCheckBox("Use Random Generation")
        use_random_gen.setToolTip("Enable to generate processes with random attributes.")
        use_random_gen.setObjectName("use_random_gen")
        
        max_time = QSpinBox()
        max_time.setToolTip("Set the maximum duration for the simulation.")
        max_time.setRange(1, 9999)  
        max_time.setObjectName("max_time")
        
        arrival_lambda = QDoubleSpinBox()
        arrival_lambda.setToolTip("Lambda (λ) parameter for the arrival time distribution.")
        arrival_lambda.setRange(0.1, 1000.0) 
        arrival_lambda.setSingleStep(0.1)
        arrival_lambda.setObjectName("arrival_lambda")
        
        burst_lambda = QDoubleSpinBox()
        burst_lambda.setToolTip("Lambda (λ) parameter for the burst time distribution.")
        burst_lambda.setRange(0.1, 1000.0)  
        burst_lambda.setSingleStep(0.1)
        burst_lambda.setObjectName("burst_lambda")
        
        seed = QSpinBox()
        seed.setToolTip("Seed value for random number generation to ensure reproducibility.")
        seed.setRange(1, 9999)  
        seed.setObjectName("seed")
        
        use_random_gen.setChecked(True)
        max_time.setValue(30)
        arrival_lambda.setValue(4.0)
        burst_lambda.setValue(0.5)
        seed.setValue(57)
        
        if pgConfigurations:
            use_random_gen.setChecked(pgConfigurations.get("useProcessGeneration", True))
            max_time.setValue(pgConfigurations.get("maxTime", 30))
            arrival_lambda.setValue(pgConfigurations.get("arrival", {}).get("lambda", 4.0))
            burst_lambda.setValue(pgConfigurations.get("burst", {}).get("lambda", 0.5))
            seed.setValue(pgConfigurations.get("seed", 57))
        
        self.layout().addRow(use_random_gen)
        self.layout().addRow("Max Time:", max_time)
        self.layout().addRow("Arrival λ:", arrival_lambda)
        self.layout().addRow("Burst λ:", burst_lambda)
        self.layout().addRow("Seed:", seed)
        
        self.use_random_gen = use_random_gen
        self.max_time = max_time
        self.arrival_lambda = arrival_lambda
        self.burst_lambda = burst_lambda
        self.seed = seed
    
    def getProcessGenerationConfig(self):
        use_random_gen = self.use_random_gen.isChecked()
        max_time = self.max_time.value()
        arrival_lambda = self.arrival_lambda.value()
        burst_lambda = self.burst_lambda.value()
        seed = self.seed.value()
        
        if max_time <= 0:
            raise ValueError("Max Time must be greater than zero.")
        if arrival_lambda <= 0:
            raise ValueError("Arrival λ must be greater than zero.")
        if burst_lambda <= 0:
            raise ValueError("Burst λ must be greater than zero.")
        if seed <= 0:
            raise ValueError("Seed must be greater than zero.")
            
        return {
            "useProcessGeneration": use_random_gen,
            "maxTime": max_time,
            "arrival": {"lambda": arrival_lambda},
            "burst": {"lambda": burst_lambda},
            "priorities": {
                "values": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "weights": [0.25, 0.20, 0.15, 0.10, 0.08, 0.07, 0.05, 0.04, 0.03, 0.02, 0.01]
            },
            "seed": seed
        }