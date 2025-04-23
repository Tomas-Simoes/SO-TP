from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QTabWidget, 
                            QDialog, QSizePolicy, QLabel)
from PyQt6.QtCore import Qt, QTimer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib
matplotlib.use('Qt5Agg')

class CompletionOverTimeGraph(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.completionTimeData = []

        self.layout = QVBoxLayout(self)
        
        self.figure = plt.figure(figsize=(8, 4), dpi=100)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        self.layout.addWidget(self.canvas)
        
        # Create the axes
        self.axes = self.figure.add_subplot(111)
        self.axes.set_title('Completed Processes Over Time')
        self.axes.set_xlabel('Time')
        self.axes.set_ylabel('Number of Completed Processes')
        self.axes.grid(True)
        
        # Initialize empty line
        self.line, = self.axes.plot([], [], marker='o', linestyle='-', color='blue')
    
    def updateGraph(self):
        if not self.completionTimeData:
            self.axes.set_xlim(0, 10)  # Show 0-10 time units
            self.axes.set_ylim(0, 5)   # Show 0-5 processes
            self.canvas.draw()
            return
                
        times, counts = zip(*self.completionTimeData)
        
        self.line.set_data(times, counts)
        
        self.axes.set_xlim(0, max(times) * 1.1)  
        self.axes.set_ylim(0, max(counts) * 1.1 if counts else 5)  
        
        self.canvas.draw()

    def addNewPoint(self, currentTime, completedCount):
        self.completionTimeData.append((currentTime, completedCount))
        self.updateGraph()