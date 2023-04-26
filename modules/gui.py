import sys
import random
from PyQt6.QtCore import QSize, Qt, QThreadPool, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget
from PyQt6.QtGui import QPalette, QColor
from array import *

import modules.spotify as spotify
from modules.processing import prep_tasks
import modules.state as state

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)
        self.setMinimumSize(45, 60)
        self.resize(45, 60)


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    # stuff for modules.tasks... it needs to be declared outside of __init__ for some reason? -D
    stopWorkers = pyqtSignal()


    def __init__(mainWindow):
        super().__init__()
        frameCounter = 0
        mainWindow.setWindowTitle("CPU-DJ")
        mainWindow.setMinimumSize(200, 200)
        mainWindow.resize(200, 200)

        mainWindow.button_is_checked = True
        mainWindow.display = ["empty"]

        # stuff for modules.tasks - ask dan if help needed.  this should always be in __init__ -D
        mainWindow.thread_pool = QThreadPool()
        mainWindow.thread_pool.setMaxThreadCount(10)

        mainWindow.array1 = array
        # array[4] = 
        # mainWindow.array1
        mainWindow.array2 = [0]
        mainWindow.array3 = [0]
        
        mainWindow.generateButton = QPushButton("Generate Song")
        mainWindow.taskButton = QPushButton("Start tasks")
        mainWindow.button_setup()

        # self.input = QLineEdit()
        # self.input.textChanged.connect(self.playlistDisplay.setText)

        mainWindow.layout = QVBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()
        row4 = QHBoxLayout()
        row5 = QHBoxLayout()

        row1.addWidget(Color('red'))

        row1.addWidget(mainWindow.generateButton)
        row1.addWidget(mainWindow.taskButton)

        row2.addWidget(Color('red'))
        row2.addWidget(Color('yellow'))
        row2.addWidget(Color('purple'))

        row3.addWidget(Color('red'))
        row3.addWidget(Color('yellow'))
        row3.addWidget(Color('purple'))

        row4.addWidget(Color('red'))
        row4.addWidget(Color('yellow'))
        row4.addWidget(Color('purple'))

        row5.addWidget(Color('red'))
        row5.addWidget(Color('yellow'))
        row5.addWidget(Color('purple'))

        mainWindow.layout.addLayout(row1)
        mainWindow.layout.addLayout(row2)
        mainWindow.layout.addLayout(row3)
        mainWindow.layout.addLayout(row4)
        mainWindow.layout.addLayout(row5)


        # mainWindow.layout.addWidget(mainWindow.input)


        # testing displays
        mainWindow.display[0]="test text"
        
        mainWindow.name = "test2"
        mainWindow.playlistDisplay = QLabel()

        mainWindow.playlistDisplay.setText("Failed - QLabel Set Text")
        mainWindow.playlistDisplay.setText(mainWindow.display[0])

        container = QWidget()
        container.setLayout(mainWindow.layout)

        # Set the central widget of the Window.
        mainWindow.setCentralWidget(container)

        frameCounter+=1
        print(frameCounter)


    def button_setup(mainWindow):
        mainWindow.generateButton.setCheckable(True)
        mainWindow.generateButton.clicked.connect(mainWindow.generate_list)
        mainWindow.generateButton.released.connect(mainWindow.the_button_was_released)
        mainWindow.generateButton.setChecked(mainWindow.button_is_checked)
        mainWindow.generateButton.setMinimumSize(45, 60)
        mainWindow.generateButton.resize(45, 60)

        mainWindow.taskButton.setCheckable(True)
        mainWindow.taskButton.released.connect(lambda: prep_tasks(window))

        mainWindow.setMinimumSize(45, 60)
        mainWindow.resize(45, 60)
    
    def generate_list(mainWindow):
        print("Song generated!")
        mainWindow.generateButton.setText("Song Generated.")
        mainWindow.generateButton.setEnabled(False)


        songs = spotify.main()

        # show_Playlist(songs, mainWindow, QLabel)

        #to[0] = "Passed - QLabel Set Text"
        array1 = []
        array2 = []

        mainWindow.layout.addWidget(mainWindow.playlistDisplay)

        for index, item in enumerate(songs, start=1):
            try:
                name = item["track"]["name"]
                uri = item["track"]["uri"]
                # print(index, name)
                arrayNU = [name, uri]
                # print(mainWindow.array1)
                array1 = arrayNU + [index]
                array2 = array2 + array1


            except TypeError or name == "":
                pass

        print("-------------------------------------------")

        #mainWindow.display[0] = "test text2"
        mainWindow.display[0] = (str(array2[2])+' '+str(array2[0])+' '+str(array2[1]))
        # index 2 of array2 = song number
        # index 0 of array2 = song title
        # index 1 of array2 = URI
        from modules.processing import uri_to_embed
        uri_to_embed(str(array2[1]))
        
        # print(array2)
     
        print(array2)

        print(mainWindow.display)

        mainWindow.playlistDisplay.setText(mainWindow.display[0])

    def the_button_was_released(mainWindow):
        mainWindow.button_is_checked = True
        print(mainWindow.button_is_checked)

def show_Playlist(songs, mainWindow, QLabel):
    return
        
    
    # print(str(mainWindow.array3[2])+' '+mainWindow.array3[3])
    

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)

# Create a Qt main window, which will be our window.

window = MainWindow()
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

