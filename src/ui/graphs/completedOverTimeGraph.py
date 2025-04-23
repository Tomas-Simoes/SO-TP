from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QTabWidget, 
                            QDialog, QSizePolicy, QLabel)
from PyQt6.QtCore import Qt, QTimer

class CompletionOverTimeGraph(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)