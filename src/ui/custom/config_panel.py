from PyQt6.QtWidgets import QGroupBox, QFormLayout

class ConfigPanel(QGroupBox):
    def __init__(self, title: str):
        super().__init__(title)
        form_layout = QFormLayout()
        self.setLayout(form_layout)
