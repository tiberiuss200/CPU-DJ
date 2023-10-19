import sys

from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QIcon

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("logo.png"))
        self.setWindowTitle("Graphs Testing")



app = QApplication(sys.argv)
window = Window()
window.show()

sys.exit(app.exec())