from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget


class HistoryView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        self.list_widget = QListWidget()

        layout.addWidget(self.list_widget)