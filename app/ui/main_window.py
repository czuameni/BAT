from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QFileDialog, QStackedWidget, QMessageBox
)
from pathlib import Path

# UI components
from app.ui.sidebar import Sidebar
from app.ui.topbar import TopBar
from app.ui.statusbar import StatusBar
from app.ui.progressbar import ProgressBar

# Views
from app.ui.views.backup_view import BackupView
from app.ui.views.history_view import HistoryView
from app.ui.views.settings_view import SettingsView
from app.ui.views.dashboard_view import DashboardView

# Core
from app.core.scanner import scan_directory
from app.core.backup_engine import BackupEngine
from app.db.database import Database
from app.core.restore import restore_file
from app.core.worker import BackupWorker
from app.core.stats import Stats


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BAT")
        self.setMinimumSize(900, 600)

        # ===== CORE =====
        self.folder = None
        self.engine = BackupEngine()
        self.db = Database()

        # ===== UI COMPONENTS =====
        self.sidebar = Sidebar()
        self.topbar = TopBar()
        self.statusbar = StatusBar()
        self.progress = ProgressBar()

        # ===== VIEWS =====
        self.stack = QStackedWidget()

        self.backup_view = BackupView()
        self.history_view = HistoryView()
        self.settings_view = SettingsView()
        self.dashboard_view = DashboardView()

        self.stack.addWidget(self.backup_view)   # index 0
        self.stack.addWidget(self.history_view)  # index 1
        self.stack.addWidget(self.settings_view) # index 2
        self.stack.addWidget(self.dashboard_view)  # index 3

        self.stats = Stats()

        # ===== LAYOUT =====
        main_layout = QHBoxLayout(self)

        content_layout = QVBoxLayout()
        content_layout.setSpacing(15)
        content_layout.setContentsMargins(15, 15, 15, 15)

        content_layout.addWidget(self.topbar)
        content_layout.addWidget(self.stack)
        content_layout.addWidget(self.progress)
        content_layout.addWidget(self.statusbar)

        main_layout.addWidget(self.sidebar)
        main_layout.addLayout(content_layout)

        # ===== CONNECT SIDEBAR (ROUTING) =====
        self.sidebar.backup_btn.clicked.connect(self.show_backup)
        self.sidebar.history_btn.clicked.connect(self.show_history)
        self.sidebar.settings_btn.clicked.connect(self.show_dashboard)

        # ===== CONNECT BACKUP VIEW =====
        self.backup_view.select_btn.clicked.connect(self.select_folder)
        self.backup_view.backup_btn.clicked.connect(self.run_backup)

        # ===== HISTORY CLICK =====
        self.history_view.list_widget.itemDoubleClicked.connect(self.restore_selected)

        # ===== INIT =====
        self.load_history()

        stats = self.stats.get_stats()
        self.dashboard_view.update_stats(stats)

        self.sidebar.set_active(self.sidebar.backup_btn)

    # =========================
    # 📁 SELECT FOLDER
    # =========================
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder = Path(folder)
            self.topbar.set_folder(folder)
            self.statusbar.set_status("Folder selected")

    # =========================
    # 🚀 BACKUP
    # =========================
    def run_backup(self):
        if not self.folder:
            self.statusbar.set_status("No folder selected")
            return

        self.backup_view.backup_btn.setEnabled(False)

        self.worker = BackupWorker(self.folder)

        self.worker.progress.connect(self.progress.update_progress)
        self.worker.status.connect(self.statusbar.set_status)
        self.worker.finished.connect(self.on_backup_finished)

        self.worker.start()

    def show_backup(self):
        self.stack.setCurrentIndex(0)
        self.sidebar.set_active(self.sidebar.backup_btn)


    def show_history(self):
        self.stack.setCurrentIndex(1)
        self.sidebar.set_active(self.sidebar.history_btn)


    def show_dashboard(self):
        self.stack.setCurrentIndex(3)
        self.sidebar.set_active(self.sidebar.settings_btn)

        stats = self.stats.get_stats()
        self.dashboard_view.update_stats(stats)

    def on_backup_finished(self, success, errors):
        self.backup_view.backup_btn.setEnabled(True)
        self.load_history()

        stats = self.stats.get_stats()
        self.dashboard_view.update_stats(stats)

        # ✅ UX LOGIC
        if success == 0 and errors == 0:
            QMessageBox.information(
                self,
                "No Changes",
                "All files are already up to date."
            )
        elif errors == 0:
            QMessageBox.information(
                self,
                "Backup Completed",
                f"Files backed up: {success}"
            )
        else:
            QMessageBox.warning(
                self,
                "Backup Completed with Errors",
                f"Files backed up: {success}\nErrors: {errors}"
            )

    # =========================
    # 📜 LOAD HISTORY
    # =========================
    def load_history(self):
        self.history_view.list_widget.clear()

        for row in self.db.get_history():
            # row = (original_path, backup_path, timestamp)
            self.history_view.list_widget.addItem(
                f"{row[0]} -> {row[2]}"
            )

    # =========================
    # 🔄 RESTORE
    # =========================
    def restore_selected(self, item):
        text = item.text()
        original, _, timestamp = text.partition(" -> ")

        for row in self.db.get_history():
            if row[0] == original and row[2] == timestamp:
                restore_file(row[1], original)
                self.statusbar.set_status("File restored")
                return