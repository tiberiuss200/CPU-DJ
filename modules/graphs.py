import sys
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtGui import QIcon
import matplotlib

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure





class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        test = FigureCanvasQTAgg(fig)
        layout.addWidget(test)

        self.setWindowIcon(QIcon("logo.png"))           #Sets the window's icon in the top left of the window to our logo
        self.setWindowTitle("Graphs Testing")           #Sets the title of the entire window
        #test = graph(self, width=5, height=10, dpi=100)
        #layout = QVBoxLayout()
        #test.axes.plot([0,1,2,3,4], [3,10,2,5,7])
        #layout.addWidget(test)


fig = Figure()
ax = fig.add_subplot()

x = [0,1,2,3,4]
y = [3,10,2,5,7]
ax.plot(x,y)


#class graph(FigureCanvasQTAgg):
#    def __init__(self, parent=Window, width=10, height=10, dpi=100):
#        fig = Figure(figsize=(width, height), dpi=dpi)
#        self.axes = fig.add_subplot(111)
#        super(graph, self).__init__(fig)





app = QApplication(sys.argv)
window = Window()
window.show()

sys.exit(app.exec())