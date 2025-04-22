from typing import Dict, List
from PyQt6.QtWidgets import (
    QWidget, QGroupBox, QLabel, QVBoxLayout, QHBoxLayout, 
    QSizePolicy, QScrollArea, QGridLayout, QFrame
)
from PyQt6.QtCore import Qt, pyqtSlot
from ui.custom.process_block import ProcessBlock
from processes.process import Process

import math

class CompletedPanel(QGroupBox):
    completedProcessBlocks: Dict[int, ProcessBlock]
    prioritiesLabels: Dict[int, QLabel]
    statisticsLabels: List[QLabel]

    def __init__(self, config, parent=None):
        super().__init__("Complete Processes Panel", parent)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.config = config 
        self.readyProcessBlocks = {}
        self.prioritiesLabels = {}
        
        self.completedProcessSection()
        self.completedQueueSection()
        self.statisticsSection()

        self.mainLayout.addStretch(1)

    @pyqtSlot(object)
    def updateCompletedProcesses(self, processList: List[Process]):
        newPIDs = {process.pid for process in processList}
        oldPIDs = set(self.readyProcessBlocks.keys())

        removedPIDs = oldPIDs - newPIDs

        for pid in removedPIDs:
            removedBlock = self.readyProcessBlocks.pop(pid)
            self.completedLayout.removeWidget(removedBlock)
            removedBlock.setParent(None)
            removedBlock.deleteLater()            

        for process in processList:
            pid = process.pid
            if pid not in self.readyProcessBlocks:
                newProcessBlock = ProcessBlock(process)
                self.readyProcessBlocks[pid] = newProcessBlock
                self.completedLayout.addWidget(newProcessBlock)

        self.updatePrioritiesSection(processList)
        self.updateStatistics(processList)

    def updatePrioritiesSection(self, processList: List[Process]):
        priorityCounts = {i: 0 for i in range(10)}

        for process in processList:
            priorityCounts[process.priority] += 1
        
        for priority, count in priorityCounts.items():
            self.prioritiesLabels.get(priority).setText(
                f"Priority {priority} ({self.config['processGeneration']['priorities']['weights'][priority]:.2f}): {count} processes         ({(count / len(processList)) * 100:.2f}%)")

    def updateStatistics(self, processList: List[Process]):
        numProcesses = len(processList)
        
        if numProcesses == 0:
            return  

        totalBurstTimes = sum(process.burstTime for process in processList)
        self.statisticsLabels["totalExpectedTime"].setText(f"Total expected execution time: {totalBurstTimes:.2f}")
        
        # Average execution time        
        averageBurstTime = totalBurstTimes / numProcesses
        minBurstTime = min(process.burstTime for process in processList)
        maxBurstTime = max(process.burstTime for process in processList)
        self.statisticsLabels["averageExecutionTime"].setText(f"Average Execution Time: {averageBurstTime:.2f}   (min: {minBurstTime:.2f}, max: {maxBurstTime:.2f})")
        
        # Standard Deviation of burst time
        standardDeviation = math.sqrt(sum((process.burstTime - averageBurstTime) ** 2 for process in processList) / numProcesses)
        self.statisticsLabels["standardDeviation"].setText(f"Standard Deviation of Burst Time: {standardDeviation:.2f}")
        
        # Average inter-arrival time
        sortedArrivalTimes = sorted(process.arrivalTime for process in processList)
        averageInterArrivalTime = sum(sortedArrivalTimes[i+1] - sortedArrivalTimes[i] for i in range(len(sortedArrivalTimes) - 1)) / (numProcesses - 1) if numProcesses > 1 else 0
        self.statisticsLabels["averageInterArrivalTime"].setText(f"Average Inter-Arrival Time: {averageInterArrivalTime:.2f}")
        
        # Total number of processes
        self.statisticsLabels["totalNumber"].setText(f"Total number of processes: {numProcesses}")

    # Creates running process section in the following format:
    #       
    #  Current Running Process  | Statistics about that Processs
    def completedProcessSection(self):
        containerGroup = QGroupBox("Process Information (press one in Ready Queue)")
        containerGroup.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)

        # Horizontal layout to hold both sections
        containerLayout = QHBoxLayout()
        containerLayout.setSpacing(20)

        informationGroup = QGroupBox("Information")
        informationGroup.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)

        informationLayout = QGridLayout()
        informationLayout.setVerticalSpacing(2)
        informationLayout.setHorizontalSpacing(20)

        self.informationLabels = {
            "pid": QLabel("PID: No"),
            "arrivalTime": QLabel("Arrival Time: 0"),
            "burstTime": QLabel("Burst Time: 0   (min: 0, max: 0)"),
            "priority": QLabel("Priority: 0"),
            "isCompleted": QLabel("Is Completed: No"),
            "remainingTime": QLabel("Remaining Time: 0"),
            "waitingTime": QLabel("Waiting time: 0"),
            "turnaroundTime": QLabel("Turnaround time: 0"),
            "startTime": QLabel("Start time: 0"),
            "status": QLabel("Status: 0"),
        }

        # Add to grid layout in two columns
        for i, label in enumerate(self.informationLabels.values()):
            row = i // 2
            col = i % 2
            informationLayout.addWidget(label, row, col)

        informationGroup.setLayout(informationLayout)

        containerLayout.addWidget(informationGroup)
        containerGroup.setLayout(containerLayout)
        
        self.mainLayout.addWidget(containerGroup)
    
    # Creates ready queue section, which contains a list of ProcessBlocks
    def completedQueueSection(self):
        completedQueueGroup = QGroupBox("Completed Process Queue")
        completedQueueGroup.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        scrollWidget = QWidget()
        completedLayout = QHBoxLayout(scrollWidget)
        completedLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        completedLayout.setContentsMargins(0, 0, 0, 0)
        completedLayout.setSpacing(10)  
        
        scrollArea.setWidget(scrollWidget)
        
        completedQueueLayout = QVBoxLayout()
        completedQueueLayout.addWidget(scrollArea)
        completedQueueGroup.setLayout(completedQueueLayout)
        completedQueueGroup.setMaximumHeight(150)
        completedQueueLayout.setContentsMargins(0, 0, 0, 0)
        completedQueueLayout.setSpacing(0)

        self.mainLayout.addWidget(completedQueueGroup)

        self.completedLayout = completedLayout
        self.completedQueueGroup = completedQueueGroup
    
    def statisticsSection(self):
        # Statistics section
        statisticsGroup = QGroupBox("Statistics")
        statisticsGroup.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        
        statisticsLayout = QVBoxLayout()
        statisticsLayout.setSpacing(2)

        self.statisticsLabels = {
            "averageCompletitionTime": QLabel("Average Completition time: 0   (min: 0, max: 0)"),
            "averageTurnaroundTime": QLabel("Average Turnaround time: 0   (min: 0, max: 0)"),
            "averageWaitingTime": QLabel("Average Turnaround time: 0   (min: 0, max: 0)"),
            "turnaroundVariance": QLabel("Turnaround variance: 0"),
            "processSwitchCount": QLabel("Process switch count: 0")
        }
        
        for label in self.statisticsLabels.values():
            statisticsLayout.addWidget(label)
        
        statisticsGroup.setLayout(statisticsLayout)
        self.mainLayout.addWidget(statisticsGroup)
    
 
