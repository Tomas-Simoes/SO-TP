from PyQt6.QtWidgets import (
    QWidget, QMainWindow, QGridLayout, QGroupBox, QLabel, 
    QVBoxLayout, QHBoxLayout, QSizePolicy, QScrollArea
)
from PyQt6.QtCore import Qt, QThread

from ui.simulation.elements.process_panel import ProcessesPanel 
from ui.simulation.elements.completed_panel import CompletedPanel 
from ui.simulation.elements.config_panel import ConfigPanel
from ui.simulation.elements.clock_panel import ClockPanel

from simulation import Simulation

class SimulationWindow(QMainWindow):
    def __init__(self, simulationConfig):
        super().__init__()
        self.setWindowTitle("Simulation Window")

        self.simulationConfig = simulationConfig
        self.buildSimulationWindow()

        ## Class to do the actual simulation
        self.simulation = Simulation(simulationConfig)
        self.initializeThreads()
        self.subscribeEvents()

        self.clockThread.start()

    # Initializes our needed threads in order to not block main thread
    #
    #   - runTickBased() (from ClockWorker) runs on clockThread
    def initializeThreads(self):
        self.clockThread = QThread(self)
        self.simulation.clockWorker.moveToThread(self.clockThread)
        
        self.clockThread.started.connect(self.simulation.clockWorker.runTickBased)        
    
    # Subscribe event's in other to update our GUI when some event occurs
    def subscribeEvents(self):
        self.simulation.clockWorker.updateClockDisplay.connect(self.clockPanel.updateDisplay)
        self.simulation.schedulerWorker.updateProcessesDisplay.connect(self.processesPanel.updateReadyProcesses)
        self.simulation.schedulerWorker.updateRunningProcessDisplay.connect(self.processesPanel.updateRunningProcess)
        self.simulation.schedulerWorker.updateCompletedProcessesDisplay.connect(self.completedPanel.updateCompletedProcesses)
        self.simulation.schedulerWorker.updateCompletedOverTimeGraph.connect(self.clockPanel.updateCompletionOverTimeGraph)

    """
        Builds the simulation window in the following format:
        -------------------------------------
        |   Processes Panel     |  Panel 2  |
        | Config | Clock Panel  |  Panel 4  |
        -------------------------------------
    """
    def buildSimulationWindow(self):
        content = QWidget()
        contentLayout = QGridLayout(content)

        # Creates the four panels, ready to implement on the Simulation Window
        # where bottomLeftPanel is a combination of Config and Clock panels
        self.processesPanel = self.createTopLeftPanel()
        self.completedPanel = self.createTopRightPanel()
        bottomLeftPanel = self.createBottomLeftPanel()
        bottomRightPanel = self.createBottomRightPanel()


        # Add the panels to the grid layout
        contentLayout.addWidget(self.processesPanel, 0, 0)
        contentLayout.addWidget(self.completedPanel, 0, 1)
        contentLayout.addWidget(bottomLeftPanel, 1, 0)
        contentLayout.addWidget(bottomRightPanel, 1, 1)

        contentLayout.setColumnStretch(0, 1)
        contentLayout.setColumnStretch(1, 1)
        contentLayout.setRowStretch(0, 1)
        contentLayout.setRowStretch(1, 1)

        # Enable scrolling for lower resolutions
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(content)

        content.setMinimumSize(0, 0)
        content.setSizePolicy(
            QWidget().sizePolicy().Policy.Ignored,
            QWidget().sizePolicy().Policy.Ignored
        )

        self.setCentralWidget(scroll)

    def createTopLeftPanel(self):
        return ProcessesPanel(self.simulationConfig)

    # TODO
    def createTopRightPanel(self):
        return CompletedPanel(self.simulationConfig)

    # Creates two panels, Config and Clock, and attachs it to one bottomLeftPanel
    def createBottomLeftPanel(self):
        bottomLeftPanel = QWidget()
        bottomLeftLayout = QHBoxLayout(bottomLeftPanel)

        self.configPanel = ConfigPanel(self.simulationConfig)
        self.clockPanel = ClockPanel()

        bottomLeftLayout.addWidget(self.configPanel, stretch=1)
        bottomLeftLayout.addWidget(self.clockPanel, stretch=1)

        return bottomLeftPanel
    
    # TODO
    def createBottomRightPanel(self):
        bottom_right_panel = QGroupBox("Bottom Right Panel")
        bottom_right_panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Content for Bottom Right"))
        
        layout.addStretch(1)
        
        bottom_right_panel.setLayout(layout)
        return bottom_right_panel