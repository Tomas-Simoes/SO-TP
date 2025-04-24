from PyQt6.QtWidgets import (
    QWidget, QMainWindow, QGridLayout, QGroupBox, QLabel, 
    QVBoxLayout, QHBoxLayout, QSizePolicy, QScrollArea
)
from PyQt6.QtCore import Qt, QThread, pyqtSlot, QTimer

from ui.simulation.elements.process_panel import ProcessesPanel 
from ui.simulation.elements.completed_panel import CompletedPanel 
from ui.simulation.elements.config_panel import ConfigPanel
from ui.simulation.elements.clock_panel import ClockPanel
from ui.graphs.avgMetricsGraph import AvgMetricsGraph

from simulation import Simulation
from clock import GlobalClock

class SimulationWindow(QMainWindow):
    def __init__(self, simulationConfig):
        super().__init__()
        self.setWindowTitle("Simulation Window")

        self.simulationConfig = simulationConfig
        self.simulation = Simulation(simulationConfig)

        self.buildSimulationWindow()
        self.initializeThreads()
        self.initializeUpdateTimer()
        self.subscribeUpdateEvents()

        self.clockThread.start()

    # Initialize our clock threads in order to not block main thread
    # which runs at simulation speed
    #   - runTickBased() (from ClockWorker) runs on clockThread
    def initializeThreads(self):
        self.clockThread = QThread(self)
        self.simulation.clockWorker.moveToThread(self.clockThread)
        self.clockThread.started.connect(self.simulation.clockWorker.runTickBased)        
    
    # Initializes a clock which updates the time-related UI
    #   - updateGlobalTim and updateTimeRelatedUI run on mainThread
    #   - runs at 60fps
    def initializeUpdateTimer(self):
        self.updateUITimer = QTimer(self)
        self.updateUITimer.timeout.connect(GlobalClock.updateGlobalTime)
        self.updateUITimer.timeout.connect(self.updateTimeRelatedUI)
        self.updateUITimer.start(16)

    # Subscribe event's in other to update our GUI when some event occurs
    def subscribeUpdateEvents(self):
        self.simulation.schedulerWorker.updateProcessesDisplay.connect(self.processesPanel.updateReadyProcesses)
        self.simulation.schedulerWorker.updateRunningProcessDisplay.connect(self.processesPanel.updateRunningProcess)
        self.simulation.schedulerWorker.updateCompletedProcessesDisplay.connect(self.completedPanel.updateCompletedProcesses)

    # At 60fps updates our time-related GUI 
    def updateTimeRelatedUI(self):
        self.clockPanel.updateCompletionOverTimeGraph(len(self.simulation.schedulerWorker.completedProcesses))
        self.avgMetricsGraph.updateAvgMetricsGraph(self.simulation.schedulerWorker.completedProcesses)
        self.clockPanel.updateDisplay()

    """
        Builds the simulation window in the following format:
        -----------------------------------------------------
        |   Processes Panel     |  Completed Process Panel  |
        | Config | Clock Panel  |         Graphs            |
        -----------------------------------------------------
    """
    def buildSimulationWindow(self):
        content = QWidget()
        contentLayout = QHBoxLayout(content)
        contentLayout.setSpacing(0)
        contentLayout.setContentsMargins(0, 0, 0, 0)
        
        # Creates the four panels, ready to implement on the Simulation Window
        # where bottomLeftPanel is a combination of Config and Clock panels
        self.processesPanel = self.createTopLeftPanel()
        self.completedPanel = self.createTopRightPanel()
        self.bottomLeftPanel = self.createBottomLeftPanel()
        self.bottomRightPanel = self.createBottomRightPanel()
        
        # Left column
        leftColumn = QVBoxLayout()
        leftColumn.setSpacing(0)
        leftColumn.addWidget(self.processesPanel)
        leftColumn.addWidget(self.bottomLeftPanel)
        
        # Right column
        rightColumn = QVBoxLayout()
        rightColumn.setSpacing(0)
        rightColumn.addWidget(self.completedPanel)
        rightColumn.addWidget(self.bottomRightPanel)

        contentLayout.addLayout(leftColumn)
        contentLayout.addLayout(rightColumn)

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
        bottom_right_panel = QGroupBox("Metrics Over Time")
        bottom_right_panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout = QVBoxLayout()

        self.avgMetricsGraph = AvgMetricsGraph(parent=self)
        self.avg2 = AvgMetricsGraph(parent=self)
        layout.addWidget(self.avgMetricsGraph)
        layout.addWidget(self.avg2)

        layout.addStretch(1)
        
        bottom_right_panel.setLayout(layout)
        return bottom_right_panel