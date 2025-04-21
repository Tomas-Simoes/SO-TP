from PyQt6.QtWidgets import (
    QWidget, QMainWindow, QGridLayout, QGroupBox, QLabel, 
    QVBoxLayout, QHBoxLayout, QSizePolicy, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt

from ui.simulation.elements.process_panel import ProcessesPanel  # Import the new class
from ui.simulation.elements.config_panel import ConfigPanel

from simulation import Simulation

class SimulationWindow(QMainWindow):
    def __init__(self, simulationConfig):
        super().__init__()
        self.setWindowTitle("Simulation Window")
        self.resize(800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QGridLayout()
        central_widget.setLayout(main_layout)

        top_left_panel = ProcessesPanel(simulationConfig)
        bottom_left_panel = ConfigPanel(simulationConfig)
        top_right_panel = self.createBottomRightPanel()
        bottom_right_panel = self.createBottomRightPanel()

        # Add the panels to the grid layout
        main_layout.addWidget(top_left_panel, 0, 0)
        main_layout.addWidget(top_right_panel, 0, 1)
        main_layout.addWidget(bottom_left_panel, 1, 0)
        main_layout.addWidget(bottom_right_panel, 1, 1)

        # Set equal stretch factors for all columns and rows
        main_layout.setColumnStretch(0, 1)
        main_layout.setColumnStretch(1, 1)
        main_layout.setRowStretch(0, 1)
        main_layout.setRowStretch(1, 1)

        ## Class to do the actual simulation
        Simulation()


    def createTopRightPanel(self):
        top_right_panel = QGroupBox("Top Right Panel")
        top_right_panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Content for Top Right"))
        
        # Add a stretch to ensure consistent sizing
        layout.addStretch(1)
        
        top_right_panel.setLayout(layout)
        return top_right_panel

    def createBottomLeftPanel(self):
        bottom_left_panel = QGroupBox("Bottom Left Panel")
        bottom_left_panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Content for Bottom Left"))
        
        # Add a stretch to ensure consistent sizing
        layout.addStretch(1)
        
        bottom_left_panel.setLayout(layout)
        return bottom_left_panel
    
    def createBottomRightPanel(self):
        bottom_right_panel = QGroupBox("Bottom Right Panel")
        bottom_right_panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Content for Bottom Right"))
        
        # Add a stretch to ensure consistent sizing
        layout.addStretch(1)
        
        bottom_right_panel.setLayout(layout)
        return bottom_right_panel