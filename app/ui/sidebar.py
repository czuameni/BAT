from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton


class Sidebar(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedWidth(150)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(10, 15, 10, 15)

        self.backup_btn = QPushButton("Backup")
        self.history_btn = QPushButton("History")
        self.settings_btn = QPushButton("Dashboard")

        layout.addWidget(self.backup_btn)
        layout.addWidget(self.history_btn)
        layout.addWidget(self.settings_btn)
        layout.addStretch()

        self.buttons = [
            self.backup_btn,
            self.history_btn,
            self.settings_btn
        ]

    def set_active(self, active_button):
        for btn in self.buttons:
            btn.setProperty("active", False)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        active_button.setProperty("active", True)
        active_button.style().unpolish(active_button)
        active_button.style().polish(active_button)