from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget


class BackupView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.select_btn = QPushButton("Select Folder")
        self.backup_btn = QPushButton("Run Backup")
        self.list_widget = QListWidget()

        layout.addWidget(self.select_btn)
        layout.addWidget(self.backup_btn)
        layout.addWidget(self.list_widget)