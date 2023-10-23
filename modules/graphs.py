import sys
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow
from PyQt6.QtGui import QIcon
import matplotlib

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import modules.tasks as tasks
from psutil import cpu_percent





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

class DataGraph(QWidget):
    def __init__(self, fptr: callable, mainWindow: QMainWindow):
        super(DataGraph, self).__init__()
        self.fptr = fptr
        self.x_values = []
        self.y_values = []
        self.timer = 0
        self.xmax = 10
        self.fig = Figure()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.layout.addWidget(self.canvas)
        self.init_graph()
        tasks.start(mainWindow, self.update_graph, self)

    def init_graph(self):
        self.ax = self.fig.add_subplot()
        self.line, = self.ax.plot([], [])
        self.ax.set_xlim(0, 10)
    
    def update_graph(self, self2):
        new_yvalue = self2.fptr()
        self2.y_values.append(new_yvalue)
        self2.x_values.append(self.timer)
        self2.timer += 1

        if (self2.timer > self2.xmax):
            self2.ax.set_xlim(self2.timer - 10, self2.timer)
        
        self2.canvas.draw()
        self2.line.set_data(self2.x_values, self2.y_values)
        tasks.wait(1000)


def test_fxn():
    return cpu_percent()

#class graph(FigureCanvasQTAgg):
#    def __init__(self, parent=Window, width=10, height=10, dpi=100):
#        fig = Figure(figsize=(width, height), dpi=dpi)
#        self.axes = fig.add_subplot(111)
#        super(graph, self).__init__(fig)





#app = QApplication(sys.argv)
#window = DataGraph(test_fxn)  #Window()
#window.show()

#sys.exit(app.exec())