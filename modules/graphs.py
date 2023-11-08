import sys
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow
from PyQt6.QtGui import QIcon
import matplotlib

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import modules.tasks as tasks
import modules.state as state
from psutil import cpu_percent

###Test Graph Object
class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        layout = QVBoxLayout()                  #Initializes a square layout
        self.setLayout(layout)                  #Sets the window's layout as a box

        test = FigureCanvasQTAgg(fig)           #Starts a graph object
        layout.addWidget(test)                  #Adds the graph widget to the layout

        self.setWindowIcon(QIcon("logo.png"))           #Sets the window's icon in the top left of the window to our logo
        self.setWindowTitle("Graphs Testing")           #Sets the title of the entire window
        #test = graph(self, width=5, height=10, dpi=100)
        #layout = QVBoxLayout()
        #test.axes.plot([0,1,2,3,4], [3,10,2,5,7])
        #layout.addWidget(test)

fig = Figure()
ax = fig.add_subplot()

x = [0,1,2,3,4]                 #Hardcoded test values
y = [3,10,2,5,7]                #Hardcoded test values
ax.plot(x,y)                    #Plots a line graph with the test values
###End Test Graph Object


###Actual Graphing
class DataGraph(QWidget):
    def __init__(self, fptr: callable):
        super(DataGraph, self).__init__()
        self.fptr = fptr                    #
        self.x_values = []                  #Sets an empty array to hold the time
        self.y_values = []                  #Sets an empty array to hold the CPU percentages
        self.timer = 0                      #Sets the initial value of X to 0 seconds
        self.xmax = 10                      #Sets the initial size of the X-axis
        self.fig = Figure()                 #Creates a new figure object

        self.layout = QVBoxLayout()                 #Creates a box style layout
        self.setLayout(self.layout)                 #Sets itself to the box layout that was made
        self.canvas = FigureCanvasQTAgg(self.fig)   #Initilizes a blank graph
        self.layout.addWidget(self.canvas)          #Adds the widget to the box style layout
        self.init_graph()                           #Function call. Sets the default graph

    def init_graph(self):
        self.ax = self.fig.add_subplot()            #Adds an axes object to the figure
        self.line, = self.ax.plot([], [], color='#55e8ff')           #Starts to graph the data on to the graph object
        self.ax.set_xlim(0, 10)                     #Sets the initial size of the x-axis
        self.ax.set_ylim(0, 100)                    #Sets the initial size of the y-axis
        #self.ax.tick_params(labelcolor=('#f0f0f0'))
        self.ax.set_facecolor('#201148')
        
    
    def set_size(self, width : int, height : int):
        self.canvas.setMaximumSize(width, height)
        self.resize(width, height)

    def set_ylim(self, ymin : float, ymax : float):
        self.ax.set_ylim(ymin, ymax)
    
    def start_task(self):
        tasks.start(self.update_graph)              #Function call. Updates the graph with new data
    
    def update_graph(self):
        while not state.mainFinished:               #Loops while the main window isn't closed
            new_yvalue = self.fptr()                #
            self.y_values.append(new_yvalue)        #Adds the new data after one second to the already initialized graph
            self.x_values.append(self.timer)        #Adds the new data after one second to the already initialized graph
            self.timer += 1                         #Adds a second to the timer for the x value

            if (self.timer > self.xmax):
                self.ax.set_xlim(self.timer - 10, self.timer)   #Moves the x-axis when the size gets too big
            
            #if (state.stat == "CPU Percent"):
                #self.ax.set_xlabel("Time in seconds")
                #self.ax.set_ylabel("CPU Usage by percentage")
            #elif (state.stat == "CPU Speed"):
                #self.ax.set_xlabel("Time in seconds")
                #self.ax.set_ylabel("CPU Speed")
            #elif (state.stat == "RAM"):
                #self.ax.set_xlabel("Time in seconds")
                #self.ax.set_ylabel("RAM Usage by percentage")
            #elif (state.stat == "CPU Fan"):
                #self.ax.set_xlabel("Time in seconds")
                #self.ax.set_ylabel("Fan Speed")
            #elif (state.stat == "RAM Swap"):
                #self.ax.set_xlabel("Time in seconds")
                #self.ax.set_ylabel("Ram Swap")
            #elif (state.stat == "CPU Temp"):
                #self.ax.set_xlabel("Time in seconds")
                #self.ax.set_ylabel("CPU Temperature")


            self.canvas.draw()                                  #Displays the new graph
            self.line.set_data(self.x_values, self.y_values)    #Sets the line data
            tasks.wait(1000)                                    #Waits 1000ms (1 second) to then graph the data again


def test_fxn():
    return cpu_percent()                                        #
###End Actual Graphing

###Code Graveyard
#class graph(FigureCanvasQTAgg):
#    def __init__(self, parent=Window, width=10, height=10, dpi=100):
#        fig = Figure(figsize=(width, height), dpi=dpi)
#        self.axes = fig.add_subplot(111)
#        super(graph, self).__init__(fig)
#app = QApplication(sys.argv)
#window = DataGraph(test_fxn)  #Window()
#window.show()

#sys.exit(app.exec())
###End Code Graveyard