from PySide6.QtWidgets import QWidget, QGridLayout

from app.ui.components.stat_card import StatCard


class DashboardView(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout(self)
        self.layout.setSpacing(25)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # cards
        self.files_card = StatCard("Files")
        self.backups_card = StatCard("Backups")
        self.size_card = StatCard("Total Size")
        self.last_card = StatCard("Last Backup")

        # grid (2x2)
        self.layout.addWidget(self.files_card, 0, 0)
        self.layout.addWidget(self.backups_card, 0, 1)
        self.layout.addWidget(self.size_card, 1, 0)
        self.layout.addWidget(self.last_card, 1, 1)

    def update_stats(self, stats):
        self.files_card.set_value(str(stats["unique_files"]))
        self.backups_card.set_value(str(stats["total_backups"]))

        size_mb = round(stats["total_size"] / (1024 * 1024), 2)
        self.size_card.set_value(f"{size_mb} MB")

        self.last_card.set_value(str(stats["last_backup"]))