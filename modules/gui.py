import sys
import random
from PyQt6.QtCore import QSize, Qt, QThreadPool, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget
from array import *

import modules.spotify as spotify
from modules.processing import prep_tasks
import modules.state as state

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    # stuff for modules.tasks... it needs to be declared outside of __init__ for some reason? -D
    stopWorkers = pyqtSignal()
    frameCounter = 0

    def __init__(self, frameCounter):
        super().__init__()

        self.setWindowTitle("CPU-DJ")

        self.button_is_checked = True
        self.display = ["empty"]

        # stuff for modules.tasks - ask dan if help needed.  this should always be in __init__ -D
        self.thread_pool = QThreadPool()
        self.thread_pool.setMaxThreadCount(10)

        self.array1 = array
        # array[4] = 
        # self.array1
        self.array2 = [0]
        self.array3 = [0]
        
        self.generateButton = QPushButton("Generate Song")
        self.taskButton = QPushButton("Start tasks")
        self.button_setup()


        # self.input = QLineEdit()
        # self.input.textChanged.connect(self.label.setText)

        self.layout = QVBoxLayout()
        # self.layout.addWidget(self.input)
        self.layout.addWidget(self.generateButton)
        self.layout.addWidget(self.taskButton)

        container = QWidget()
        container.setLayout(self.layout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)


        # testing displays
        self.display[0]="test text"
        
        self.name = "test2"
        self.playlistDisplay = QLabel()

        self.playlistDisplay.setText("Failed - QLabel Set Text")
        self.playlistDisplay.setText(self.display[0])

        frameCounter+=1
        print(frameCounter)
        
    def button_setup(self):
        self.generateButton.setCheckable(True)
        self.generateButton.clicked.connect(self.generate_list)
        self.generateButton.released.connect(self.the_button_was_released)
        self.button.setChecked(self.button_is_checked)
        self.button.setFixedSize(QSize(400, 300))

        self.taskButton.setCheckable(True)
        self.taskButton.released.connect(lambda: prep_tasks(window))
        self.taskButton.setFixedSize(QSize(200,100))


    def generate_list(self):
        print("Song generated!")
        self.button.setText("Song Generated.")
        self.button.setEnabled(False)
        songs = spotify.main()

        # show_Playlist(songs, self, QLabel)

        #to[0] = "Passed - QLabel Set Text"
        array1 = []
        array2 = []

        self.layout.addWidget(self.playlistDisplay)

        for index, item in enumerate(songs, start=1):
            try:
                name = item["track"]["name"]
                # print(index, name)
                array1 += [index, name]
                # print(self.array1)
                

            except TypeError or name == "":
                pass
    
        print("-------------------------------------------")

        self.display[0] = "test text2"
        
        x=0
        while(x<len(array1)):
            array1[x]=str(array1[x])
            x+=1
        
        x=0
        while(x<len(array1)):
            print(array1[x]+" "+array1[x+1])
            x+=2

        # self.display[0] = (str(array2[2])+' '+str(array2[3])) 
        
        # self.display(array2[x])
        # print(array2)

        print(self.display)

        self.playlistDisplay.setText(self.display[0])

    def the_button_was_released(self):
        self.button_is_checked = True
        print(self.button_is_checked)

    def show_Playlist(songs, self, QLabel):
        return
    
        # print(str(self.array3[2])+' '+self.array3[3])
    

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)

# Create a Qt main window, which will be our window.
frameCounter = 0;

window = MainWindow(frameCounter)
window.show()  # IMPORTANT!!!!! Windows are hidden by default.


# an easy way to run the CPU processing tasks in the background!
# this assumes they are always tracking stats currently and does not account for starting/stopping at will.
# # we will have to implement that later
# note: does not currently start tasks?  probably because app.exec hasn't started yet.  find a way to kickstart it.
# edit: moving it below `window.show`
app.lastWindowClosed.connect(state.signalTasks)

# from modules.processing import prep_tasks
# from modules.tasks import startupTasksTimer
# timer_onStartUp = startupTasksTimer(window)
# timer_onStartUp.timeout.connect(lambda: prep_tasks(window))
# timer_onStartUp.start()

# Start the event loop.
app.exec()

# Your application won't reach here until you exit and the event
# loop has stopped.

