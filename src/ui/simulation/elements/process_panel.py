from typing import Dict, List
from PyQt6.QtWidgets import (
    QWidget, QGroupBox, QLabel, QVBoxLayout, QHBoxLayout, 
    QSizePolicy, QScrollArea, QGridLayout, QFrame
)
from PyQt6.QtCore import Qt, pyqtSlot
from ui.custom.process_block import ProcessBlock
from processes.process import Process

class ProcessesPanel(QGroupBox):
    readyProcessBlocks: Dict[int, ProcessBlock]
    prioritiesLabels: Dict[int, QLabel]

    def __init__(self, config, parent=None):
        super().__init__("Processes Panel", parent)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.config = config 
        self.readyProcessBlocks = {}
        self.prioritiesLabels = {}
        
        self.runningProcessSection()
        self.readyQueueSection()
        self.prioritiesSection()
        self.statisticsSection()

        self.mainLayout.addStretch(1)

    @pyqtSlot(object)
    def updateReadyProcesses(self, processList: List[Process]):
        newPIDs = {process.pid for process in processList}
        oldPIDs = set(self.readyProcessBlocks.keys())

        removedPIDs = oldPIDs - newPIDs

        for pid in removedPIDs:
            removedBlock = self.readyProcessBlocks.pop(pid)
            self.readyLayout.removeWidget(removedBlock)
            removedBlock.setParent(None)
            removedBlock.deleteLater()            

        for process in processList:
            pid = process.pid
            if pid not in self.readyProcessBlocks:
                newProcessBlock = ProcessBlock(pid)
                self.readyProcessBlocks[pid] = newProcessBlock
                self.readyLayout.addWidget(newProcessBlock)

        self.readyQueueGroup.setTitle(f"Ready Process Queue ({len(self.readyProcessBlocks)})")
        self.updatePrioritiesSection(processList)

    def updatePrioritiesSection(self, processList: List[Process]):
        priorityCounts = {i: 0 for i in range(10)}

        for process in processList:
            priorityCounts[process.priority] += 1
        
        for priority, count in priorityCounts.items():
            self.prioritiesLabels.get(priority).setText(f"Priority {priority} ({self.config['processGeneration']['priorities']['weights'][priority]}): {count}")

    # Creates running process section in the following format:
    #       
    #  Current Running Process  | Statistics about that Processs
    def runningProcessSection(self):
        sectionLayout = QHBoxLayout()
        
        placeholderRunningProcessBlock = ProcessBlock("None")

        runningProcessGroup = QGroupBox("Running Process")
        runningProcessGroup.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)

        runningProcessLayout = QVBoxLayout()
        runningProcessLayout.addWidget(placeholderRunningProcessBlock, 0, Qt.AlignmentFlag.AlignCenter)
        runningProcessGroup.setLayout(runningProcessLayout)
        
        statsGroup = QGroupBox("Running Process Stats")
        statsGroup.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        
        statsLayout = QGridLayout()
        statsLayout.setVerticalSpacing(5)
        statsLayout.setHorizontalSpacing(10)
        
        self.pidValue = QLabel("N/A")
        self.priorityValue = QLabel("N/A")
        self.timeRunValue = QLabel("0.0s")
        self.timeLeftValue = QLabel("0.0s")
        self.cpuUsageValue = QLabel("0%")
        
        statsLayout.addWidget(QLabel("PID:"), 0, 0)
        statsLayout.addWidget(self.pidValue, 0, 1)
        
        statsLayout.addWidget(QLabel("Priority:"), 1, 0)
        statsLayout.addWidget(self.priorityValue, 1, 1)
        
        statsLayout.addWidget(QLabel("Time Run:"), 2, 0)
        statsLayout.addWidget(self.timeRunValue, 2, 1)
        
        statsLayout.addWidget(QLabel("Time Left:"), 3, 0)
        statsLayout.addWidget(self.timeLeftValue, 3, 1)
        
        statsLayout.addWidget(QLabel("CPU Usage:"), 4, 0)
        statsLayout.addWidget(self.cpuUsageValue, 4, 1)
        
        statsGroup.setLayout(statsLayout)
        
        sectionLayout.addWidget(runningProcessGroup, 1)
        sectionLayout.addWidget(statsGroup, 1)
        
        self.mainLayout.addLayout(sectionLayout)
    
           
    # Creates ready queue section, which contains a list of ProcessBlocks
    def readyQueueSection(self):
        readyQueueGroup = QGroupBox("Ready Process Queue")
        readyQueueGroup.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        scrollWidget = QWidget()
        readyLayout = QHBoxLayout(scrollWidget)
        readyLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        readyLayout.setContentsMargins(0, 0, 0, 0)
        readyLayout.setSpacing(10)  
        
        scrollArea.setWidget(scrollWidget)
        
        readyQueueLayout = QVBoxLayout()
        readyQueueLayout.addWidget(scrollArea)
        readyQueueGroup.setLayout(readyQueueLayout)
        readyQueueGroup.setMaximumHeight(150)
        readyQueueLayout.setContentsMargins(0, 0, 0, 0)
        readyQueueLayout.setSpacing(0)

        self.mainLayout.addWidget(readyQueueGroup)

        self.readyLayout = readyLayout
        self.readyQueueGroup = readyQueueGroup
    
    def prioritiesSection(self):
        prioritiesGroup = QGroupBox("Priorities (Weight%)")
        prioritiesGroup.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        
        prioritiesLayout = QGridLayout()
        prioritiesLayout.setVerticalSpacing(2)
        prioritiesLayout.setHorizontalSpacing(10)
        
        for i in range(10):
            row = i % 5
            col = i // 5
            label = QLabel(f"Priority {i} ({self.config['processGeneration']['priorities']['weights'][i]}): None")
            prioritiesLayout.addWidget(label, row, col)

            self.prioritiesLabels[i] = label
        
        prioritiesGroup.setLayout(prioritiesLayout)
        self.mainLayout.addWidget(prioritiesGroup)
    
    def statisticsSection(self):
        # Statistics section
        statisticsGroup = QGroupBox("Statistics")
        statisticsGroup.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        
        statisticsLayout = QVBoxLayout()
        statisticsLayout.setSpacing(2)
        
        self.processes_not_arrived_label = QLabel("Processes not yet arrived: 0")
        self.total_expected_time_label = QLabel("Total expected execution time: 0")
        
        statisticsLayout.addWidget(self.processes_not_arrived_label)
        statisticsLayout.addWidget(self.total_expected_time_label)
        
        statisticsGroup.setLayout(statisticsLayout)
        self.mainLayout.addWidget(statisticsGroup)
    
 
