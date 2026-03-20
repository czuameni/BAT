from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class StatCard(QWidget):
    def __init__(self, title):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        self.title = QLabel(title)
        self.title.setObjectName("cardTitle")

        self.value = QLabel()
        self.value.setObjectName("cardValue")

        # 🔥 KLUCZ
        self.value.setText("0")

        layout.addWidget(self.title)
        layout.addWidget(self.value)

        self.setObjectName("statCard")

    def set_value(self, text):
        self.value.setText(str(text))
        self.value.repaint()   # 🔥 FORCE UPDATE