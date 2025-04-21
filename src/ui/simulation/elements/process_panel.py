# First, create a new file called processes_panel.py

from PyQt6.QtWidgets import (
    QWidget, QGroupBox, QLabel, QVBoxLayout, QHBoxLayout, 
    QSizePolicy, QScrollArea, QGridLayout, QFrame
)
from PyQt6.QtCore import Qt
from ui.custom.process_block import ProcessBlock

class ProcessesPanel(QGroupBox):
    def __init__(self, config, parent=None):
        self.config = config 
        
        super().__init__("Processes Panel", parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        
        self.runningProcessSection()
        self.readyQueueSection()
        self.prioritiesSection()
        self.statisticsSection()
        
        self.main_layout.addStretch(1)
        
    def runningProcessSection(self):
        running_process_container = QHBoxLayout()
        
        running_process_group = QGroupBox("Running Process")
        running_process_group.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        
        process_layout = QVBoxLayout()
        running_process_block = ProcessBlock("None")
        process_layout.addWidget(running_process_block, 0, Qt.AlignmentFlag.AlignCenter)
        running_process_group.setLayout(process_layout)
        
        stats_group = QGroupBox("Running Process Stats")
        stats_group.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        
        stats_layout = QGridLayout()
        stats_layout.setVerticalSpacing(5)
        stats_layout.setHorizontalSpacing(10)
        
        self.pid_value = QLabel("N/A")
        self.priority_value = QLabel("N/A")
        self.time_run_value = QLabel("0.0s")
        self.time_left_value = QLabel("0.0s")
        self.cpu_usage_value = QLabel("0%")
        
        stats_layout.addWidget(QLabel("PID:"), 0, 0)
        stats_layout.addWidget(self.pid_value, 0, 1)
        
        stats_layout.addWidget(QLabel("Priority:"), 1, 0)
        stats_layout.addWidget(self.priority_value, 1, 1)
        
        stats_layout.addWidget(QLabel("Time Run:"), 2, 0)
        stats_layout.addWidget(self.time_run_value, 2, 1)
        
        stats_layout.addWidget(QLabel("Time Left:"), 3, 0)
        stats_layout.addWidget(self.time_left_value, 3, 1)
        
        stats_layout.addWidget(QLabel("CPU Usage:"), 4, 0)
        stats_layout.addWidget(self.cpu_usage_value, 4, 1)
        
        stats_group.setLayout(stats_layout)
        
        running_process_container.addWidget(running_process_group, 1)
        running_process_container.addWidget(stats_group, 1)
        
        self.main_layout.addLayout(running_process_container)
    
    def readyQueueSection(self):
        # Ready Process Queue
        ready_queue_group = QGroupBox("Ready Process Queue")
        ready_queue_group.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        scroll_content = QWidget()
        ready_layout = QHBoxLayout(scroll_content)
        ready_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        ready_layout.setContentsMargins(5, 5, 5, 5)
        ready_layout.setSpacing(2)
        
        # Example: Adding placeholder process blocks
        for i in range(10):
            process_block = ProcessBlock(i)
            process_block.setMaximumSize(70, 35)
            ready_layout.addWidget(process_block)
        
        scroll_area.setWidget(scroll_content)
        
        ready_queue_layout = QVBoxLayout()
        ready_queue_layout.addWidget(scroll_area)
        ready_queue_group.setLayout(ready_queue_layout)
        ready_queue_group.setMinimumHeight(120)
        ready_queue_group.setMaximumHeight(150)
        
        self.main_layout.addWidget(ready_queue_group)
    
    def prioritiesSection(self):
        # Priorities section
        priorities_group = QGroupBox("Priorities (Weight%)")
        priorities_group.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        
        priorities_layout = QGridLayout()
        priorities_layout.setVerticalSpacing(2)
        priorities_layout.setHorizontalSpacing(10)
        
        # Create a grid layout with 6 rows and 2 columns for priorities
        for i in range(10):
            row = i % 5
            col = i // 5
            label = QLabel(f"Priority {i} ({self.config["processGeneration"]["priorities"]["weights"][i]}): None")
            priorities_layout.addWidget(label, row, col)
        
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
    
    def updateRunningProcess(self, process_id, priority, time_run, time_left, cpu_usage):
        # Update the running process display
        self.pid_value.setText(str(process_id))
        self.priority_value.setText(str(priority))
        self.time_run_value.setText(f"{time_run:.1f}s")
        self.time_left_value.setText(f"{time_left:.1f}s")
        self.cpu_usage_value.setText(f"{cpu_usage}%")
        
    def updateProcessesNotArrived(self, count):
        self.processes_not_arrived_label.setText(f"Processes not yet arrived: {count}")
        
    def updateTotalExpectedTime(self, time):
        self.total_expected_time_label.setText(f"Total expected execution time: {time}")