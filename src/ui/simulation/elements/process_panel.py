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

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.config = config 
        self.readyProcessBlocks = {}
        self.prioritiesLabels = {}
        
        self.runningProcessSection()
        self.readyQueueSection()
        self.prioritiesSection()
        self.statisticsSection()

        self.main_layout.addStretch(1)

    @pyqtSlot(object)
    def updateReadyProcesses(self, processList: List[Process]):
        newPIDs = {process.pid for process in processList}
        oldPIDs = set(self.readyProcessBlocks.keys())

        removedPIDs = oldPIDs - newPIDs

        for pid in removedPIDs:
            removedBlock = self.readyProcessBlocks.pop(pid)
            self.ready_layout.removeWidget(removedBlock)
            removedBlock.setParent(None)
            removedBlock.deleteLater()            

        for process in processList:
            pid = process.pid
            if pid not in self.readyProcessBlocks:
                newProcessBlock = ProcessBlock(pid)
                self.readyProcessBlocks[pid] = newProcessBlock
                self.ready_layout.addWidget(newProcessBlock)

        self.ready_queue_group.setTitle(f"Ready Process Queue ({len(self.readyProcessBlocks)})")
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
        runningProcessLayout = QHBoxLayout()
        
        placeholderRunningProcessBlock = ProcessBlock("None")

        runningProcessGroup = QGroupBox("Running Process")
        runningProcessGroup.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)

        runningprocessLayout = QVBoxLayout()
        runningprocessLayout.addWidget(placeholderRunningProcessBlock, 0, Qt.AlignmentFlag.AlignCenter)
        runningProcessGroup.setLayout(runningprocessLayout)
        
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
        
        runningProcessLayout.addWidget(runningProcessGroup, 1)
        runningProcessLayout.addWidget(statsGroup, 1)
        
        self.main_layout.addLayout(runningProcessLayout)
    
           
    # Creates running process section in the following format:
    #
    #  Current Running Process  | Statistics about that Processs
    def readyQueueSection(self):
        ready_queue_group = QGroupBox("Ready Process Queue")
        ready_queue_group.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        scroll_content = QWidget()
        ready_layout = QHBoxLayout(scroll_content)
        ready_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        ready_layout.setContentsMargins(0, 0, 0, 0)
        ready_layout.setSpacing(10)  # Adjust spacing to control shrinking
        
        scroll_area.setWidget(scroll_content)
        
        ready_queue_layout = QVBoxLayout()
        ready_queue_layout.addWidget(scroll_area)
        ready_queue_group.setLayout(ready_queue_layout)
        ready_queue_group.setMaximumHeight(150)
        ready_queue_layout.setContentsMargins(0, 0, 0, 0)
        ready_queue_layout.setSpacing(0)

        self.main_layout.addWidget(ready_queue_group)

        self.ready_layout = ready_layout
        self.ready_queue_group = ready_queue_group
    
    def prioritiesSection(self):
        # Priorities section
        priorities_group = QGroupBox("Priorities (Weight%)")
        priorities_group.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        
        priorities_layout = QGridLayout()
        priorities_layout.setVerticalSpacing(2)
        priorities_layout.setHorizontalSpacing(10)
        
        for i in range(10):
            row = i % 5
            col = i // 5
            label = QLabel(f"Priority {i} ({self.config['processGeneration']['priorities']['weights'][i]}): None")
            priorities_layout.addWidget(label, row, col)

            self.prioritiesLabels[i] = label
        
        priorities_group.setLayout(priorities_layout)
        self.main_layout.addWidget(priorities_group)
    
    def statisticsSection(self):
        # Statistics section
        statistics_group = QGroupBox("Statistics")
        statistics_group.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        
        statistics_layout = QVBoxLayout()
        statistics_layout.setSpacing(2)
        
        self.processes_not_arrived_label = QLabel("Processes not yet arrived: 0")
        self.total_expected_time_label = QLabel("Total expected execution time: 0")
        
        statistics_layout.addWidget(self.processes_not_arrived_label)
        statistics_layout.addWidget(self.total_expected_time_label)
        
        statistics_group.setLayout(statistics_layout)
        self.main_layout.addWidget(statistics_group)
    
 
