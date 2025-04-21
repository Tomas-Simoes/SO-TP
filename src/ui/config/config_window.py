import sys, json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QFormLayout, QHBoxLayout,
    QCheckBox, QSpinBox, QDoubleSpinBox,
    QLineEdit, QComboBox, QPushButton, QLabel,
    QFileDialog, QMessageBox
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt  

from ui.config.elements.pg_panel import PGConfigPanel
from ui.config.elements.clock_panel import ClockConfigPanel
from ui.config.elements.scheduling_panel import SchedulingConfigPanel

from ui.simulation.simulation_window import SimulationWindow
from simulation import Simulation

class ConfigWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scheduling Simulation")
        self.resize(400, 600)
        
        self.configurationMenu()

    def configurationMenu(self, config=None):
        central = QWidget()
        self.main_layout = QVBoxLayout()
        central.setLayout(self.main_layout)
        self.setCentralWidget(central)

        # Configuration Panels
        self.pgPanel = PGConfigPanel(config["processGeneration"] if config else None)
        self.clockPanel = ClockConfigPanel(config["clock"] if config else None)
        self.schedulingPanel = SchedulingConfigPanel(config["scheduling"] if config else None)

        # Add Load Config File Button
        btn_load_file = QPushButton("Load config from file")
        btn_load_file.setToolTip("Click to load a config file.")
        btn_load_file.clicked.connect(self.loadConfigFile)  
        
        # Logo
        image = QLabel(self)
        pixmap = QPixmap("./image.png") 
        image.setPixmap(pixmap)
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image.setScaledContents(True) 
        image_layout = QHBoxLayout()
        image_layout.setContentsMargins(20,20,20,20)
        image_layout.addWidget(image)

        # Start Simulation Button
        btn_start = QPushButton("Start Simulation")
        btn_start.setToolTip("Click to start the simulation with the configured settings.")
        btn_start.clicked.connect(self.validateAndStartSimulation)

        # Add panels and button to the main layout
        self.main_layout.addWidget(self.pgPanel)
        self.main_layout.addWidget(self.clockPanel)
        self.main_layout.addWidget(self.schedulingPanel)
        self.main_layout.addWidget(btn_load_file)
        self.main_layout.addLayout(image_layout)
        self.main_layout.addStretch()
        self.main_layout.addWidget(btn_start)
    
    def validateAndStartSimulation(self):
        config = self.buildAndValidateConfig()
        
        if config:
            self.simulationWindow = SimulationWindow(config)
            self.simulationWindow.show()
            self.close()
                

    def buildAndValidateConfig(self):
        config = {
            "processGeneration": self.pgPanel.getProcessGenerationConfig(),
            "clock": self.clockPanel.getClockConfig(),
            "scheduling": self.schedulingPanel.getSchedulingConfig()
        }
        
        return config

    def loadConfigFile(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("JSON files (*.json)")
        
        if file_dialog.exec():
            file_paths = file_dialog.selectedFiles()
            if file_paths:
                file_path = file_paths[0]
                
                try:
                    with open(file_path, 'r') as f:
                        config_data = json.load(f)
                    
                    self.clearCurrentLayout()
                    self.configurationMenu(config_data)
                except Exception as e:
                    self.showError(f"Failed to load configuration file:\n{e}")

    def clearCurrentLayout(self):
        if hasattr(self, 'main_layout') and self.main_layout:
            while self.main_layout.count():
                item = self.main_layout.takeAt(0)
                widget = item.widget()
                
                if widget is not None:
                    widget.setParent(None)
                    widget.deleteLater()
                else:
                    del item