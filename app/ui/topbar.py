from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel


class TopBar(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        self.label = QLabel("No folder selected")

        layout.addWidget(self.label)

    def set_folder(self, path):
        self.label.setText(f"📁 {path}")