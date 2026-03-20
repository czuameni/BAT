from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel


class StatusBar(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)

        self.label = QLabel("Ready")

        layout.addWidget(self.label)

    def set_status(self, text):
        self.label.setText(text)