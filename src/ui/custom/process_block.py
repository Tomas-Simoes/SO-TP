from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt

from processes.process import Process

class ProcessBlock(QWidget):
    def __init__(self, process: Process=None):
        super().__init__()
        self.setFixedSize(100, 50)
        self.setStyleSheet("""
            QWidget {
                border: 2px solid #4682B4;
                border-radius: 5px;
                background-color: #E0F7FA;
            }
            QLabel {
                font-size: 12px;
                color: #000000;
            }
        """)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        label_title = QLabel(f"Process\n  ID: {process.pid if process else 0}")
        layout.addWidget(label_title)
        self.setLayout(layout)
