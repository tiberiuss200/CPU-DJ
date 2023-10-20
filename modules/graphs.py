import sys

from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QIcon

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("logo.png"))           #Sets the window's icon in the top left of the window to our logo
        self.setWindowTitle("Graphs Testing")           #Sets the title of the entire window




def graph():
    ...




app = QApplication(sys.argv)
window = Window()
window.show()

sys.exit(app.exec())