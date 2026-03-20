from PySide6.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QLabel


class ProgressBar(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)

        self.label = QLabel("Progress: 0/0")
        self.bar = QProgressBar()

        self.bar.setValue(0)

        layout.addWidget(self.label)
        layout.addWidget(self.bar)

    def update_progress(self, current, total):
        if total == 0:
            return

        percent = int((current / total) * 100)
        self.bar.setValue(percent)
        self.label.setText(f"{current}/{total} files")