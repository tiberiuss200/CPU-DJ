import sys

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QIcon
import matplotlib
matplotlib.use('QtAgg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class graph(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=10, height=10, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(graph, self).__init__(fig)



class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowIcon(QIcon("logo.png"))           #Sets the window's icon in the top left of the window to our logo
        self.setWindowTitle("Graphs Testing")           #Sets the title of the entire window
        test = graph(self, width=5, height=10, dpi=100)

        test.axes.plot([0,1,2,3,4], [3,10,2,5,7])

        test.show()








app = QApplication(sys.argv)
window = Window()
window.show()

sys.exit(app.exec())