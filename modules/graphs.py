import sys

from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QWidget


class Window(QWidget):
    def __init__(self):
        super().__init__()

app = QApplication(sys.argv)
window = Window()
window.show()

sys.exit(app.exec())