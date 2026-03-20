import sys
from PySide6.QtWidgets import QApplication
from app.ui.main_window import MainWindow
from PySide6.QtGui import QIcon

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("app/assets/bat.ico"))

    with open("app/ui/styles.qss") as f:
        app.setStyleSheet(f.read())

    window = MainWindow()
    window.setWindowIcon(QIcon("app/assets/bat.ico"))
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()