from PyQt6.QtWidgets import (
    QWidget, QGroupBox, QLabel, QVBoxLayout, QHBoxLayout,
    QSizePolicy, QScrollArea, QGridLayout
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, pyqtSlot

from ui.custom.process_block import ProcessBlock
from ui.graphs.completedOverTimeGraph import CompletionOverTimeGraph
class ClockPanel(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Time Panel", parent)
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)  
        self.main_layout.setSpacing(0)  
        self.setLayout(self.main_layout)
        
        clock_widget = QWidget()
        clock_layout = QHBoxLayout()  
        clock_layout.setSpacing(2)
        clock_layout.setContentsMargins(0, 0, 0, 0)
        clock_widget.setLayout(clock_layout)
        
        hours = QLabel("00")
        minutes = QLabel("00")
        seconds = QLabel("00")
        milliseconds = QLabel("000")
        separatorH = QLabel(":")
        separatorM = QLabel(":")
        
        hours.setFont(QFont("Courier", 40, QFont.Weight.Bold))
        minutes.setFont(QFont("Courier", 40, QFont.Weight.Bold))
        seconds.setFont(QFont("Courier", 40, QFont.Weight.Bold))
        milliseconds.setFont(QFont("Courier", 20, QFont.Weight.Normal))
        separatorH.setFont(QFont("Courier", 40, QFont.Weight.Bold)) 
        separatorM.setFont(QFont("Courier", 40, QFont.Weight.Bold)) 
        
        for label in [minutes, seconds, milliseconds, separatorH, separatorM]:
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        milliseconds.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter)
        
        clock_layout.addWidget(hours)
        clock_layout.addWidget(separatorH)
        clock_layout.addWidget(minutes)
        clock_layout.addWidget(separatorM)
        clock_layout.addWidget(seconds)
        clock_layout.addWidget(milliseconds)

        self.completionOverTimeGraph = CompletionOverTimeGraph()

        self.main_layout.addWidget(clock_widget, 0, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.main_layout.addWidget(self.completionOverTimeGraph)
        self.main_layout.addStretch(1) 

        self.hours = hours 
        self.minutes = minutes 
        self.seconds = seconds 
        self.milliseconds = milliseconds
    
    @pyqtSlot(int, int, int, int)
    def updateDisplay(self, hours, minutes, seconds, milliseconds):
        self.total_ms = (hours * 3600 * 1000) + (minutes * 60 * 1000) + (seconds * 1000) + milliseconds
        self.hours.setText(f"{hours:02d}")
        self.minutes.setText(f"{minutes:02d}")
        self.seconds.setText(f"{seconds:02d}")
        self.milliseconds.setText(f"{milliseconds:03d}")

    @pyqtSlot(int)
    def updateCompletionOverTimeGraph(self, completionCount):
        self.completionOverTimeGraph.addNewPoint(self.total_ms, completionCount)