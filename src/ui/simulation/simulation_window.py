from PyQt6.QtWidgets import (
    QWidget, QMainWindow, QGridLayout, QGroupBox, QLabel, 
    QVBoxLayout, QHBoxLayout, QSizePolicy, QScrollArea
)
from PyQt6.QtCore import Qt, QThread, pyqtSlot

from ui.simulation.elements.process_panel import ProcessesPanel 
from ui.simulation.elements.completed_panel import CompletedPanel 
from ui.simulation.elements.config_panel import ConfigPanel
from ui.simulation.elements.clock_panel import ClockPanel
from ui.graphs.ganttGraph import GanttChartWidget
from ui.graphs.metricsGraph import MetricsGraphWidget

from simulation import Simulation

class SimulationWindow(QMainWindow):
    def __init__(self, simulationConfig):
        super().__init__()
        self.setWindowTitle("Simulation Window")

        self.simulationConfig = simulationConfig
        ## Class to do the actual simulation
        self.simulation = Simulation(simulationConfig)

        self.buildSimulationWindow()
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
    #     self.simulation.schedulerWorker.updateProcessesDisplay.connect(
    #     lambda processes: self.ganttChart.updateGantt(self.simulation.schedulerWorker.readyProcesses)
    # )
    #     self.simulation.schedulerWorker.updateRunningProcessDisplay.connect(
    #     lambda _: self.ganttChart.updateGantt(self.simulation.schedulerWorker.readyProcesses)
    # )
    #     self.simulation.schedulerWorker.updateCompletedProcessesDisplay.connect(
    #     lambda processes, count: self.ganttChart.updateGantt(self.simulation.schedulerWorker.readyProcesses)
    # )
        self.simulation.clockWorker.updateClockDisplay.connect(self.onClockTick)
        self.simulation.schedulerWorker.updateMetricsChart.connect(self.metricsChart.updateMetrics)

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
        bottom_right_panel = QGroupBox("Metrics Over Time")
        bottom_right_panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout = QVBoxLayout()

        # self.ganttChart = GanttChartWidget([])
        # layout.addWidget(self.ganttChart)
        self.metricsChart = MetricsGraphWidget(parent=self)
        layout.addWidget(self.metricsChart)

        layout.addStretch(1)
        
        bottom_right_panel.setLayout(layout)
        return bottom_right_panel
    
    @pyqtSlot(int, int, int, int)
    def onClockTick(self, hours, minutes, seconds, milliseconds):
        # Convert to float seconds
        current_time = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000.0
<<<<<<< HEAD
        
        # Limitar atualizações do gráfico para não sobrecarregar a interface
        # Atualiza apenas a cada 0.1 segundos (ou outro valor que preferires)
        if not hasattr(self, '_last_metrics_update') or current_time - self._last_metrics_update >= 0.1:
            self._last_metrics_update = current_time
            
            # Compute average metrics at current time
            procs = self.simulation.schedulerWorker.completedProcesses  
            completed = [p for p in procs if p.completionTime is not None and p.completionTime <= current_time]
            if completed:
                avg_turn = sum(p.turnaroundTime for p in completed) / len(completed)
                avg_wait = sum(p.waitingTime for p in completed) / len(completed)
            else:
                avg_turn = avg_wait = 0.0
            
            # Update graph
            self.simulation.schedulerWorker.updateMetricsChart.emit(current_time, avg_turn, avg_wait)    
=======
    
    # Compute average metrics at current time
        procs = self.simulation.schedulerWorker.completedProcesses  
        completed = [p for p in procs if p.completionTime is not None and p.completionTime <= current_time]
        if completed:
            avg_turn = sum(p.turnaroundTime for p in completed) / len(completed)
            avg_wait = sum(p.waitingTime for p in completed) / len(completed)
        else:
            avg_turn = avg_wait = 0.0
    
        # Update graph
        self.simulation.schedulerWorker.updateMetricsChart.emit(current_time, avg_turn, avg_wait)    
        
>>>>>>> c905b507555d33064eb1f13372cad4a0ebef10d2
# def updateGanttChart(self):
#     # Obter todos os processos diretamente acessando as propriedades do schedulerWorker
#     all_processes = []
    
#     # Adicionar processos prontos
#     if hasattr(self.simulation.schedulerWorker, 'readyProcesses'):
#         all_processes.extend(self.simulation.schedulerWorker.readyProcesses)
    
#     # Adicionar processo em execução se existir
#     if hasattr(self.simulation.schedulerWorker, 'currentProcess') and self.simulation.schedulerWorker.currentProcess is not None:
#         all_processes.append(self.simulation.schedulerWorker.currentProcess)
    
#     # Adicionar processos completados
#     if hasattr(self.simulation.schedulerWorker, 'completedProcesses'):
#         all_processes.extend(self.simulation.schedulerWorker.completedProcesses)
    
#     # Atualizar o gráfico Gantt
#     self.ganttChart.updateGantt(all_processes)