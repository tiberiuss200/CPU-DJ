import sys
import random
from PyQt6.QtCore import QSize, Qt, QThreadPool, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget
from array import *

import modules.spotify as spotify

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    # stuff for modules.tasks... it needs to be declared outside of __init__ for some reason? -D
    stopWorkers = pyqtSignal()

    def __init__(mainWindow):
        super().__init__()

        mainWindow.setWindowTitle("CPU-DJ")

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

        mainWindow.button = QPushButton("Generate Song")
        mainWindow.button.setCheckable(True)
        mainWindow.button.clicked.connect(mainWindow.the_button_was_clicked)
        mainWindow.button.released.connect(mainWindow.the_button_was_released)
        mainWindow.button.setChecked(mainWindow.button_is_checked)
        mainWindow.button.setFixedSize(QSize(400, 300))

        from modules.processing import prep_tasks
        mainWindow.taskButton = QPushButton("Start tasks")
        mainWindow.taskButton.setCheckable(True)
        mainWindow.taskButton.released.connect(lambda: prep_tasks(window))
        mainWindow.taskButton.setFixedSize(QSize(200,100))

        # mainWindow.input = QLineEdit()
        # mainWindow.input.textChanged.connect(mainWindow.label.setText)

        mainWindow.layout = QVBoxLayout()
        # mainWindow.layout.addWidget(mainWindow.input)
        mainWindow.layout.addWidget(mainWindow.button)
        mainWindow.layout.addWidget(mainWindow.taskButton)

        container = QWidget()
        container.setLayout(mainWindow.layout)


        # Set the central widget of the Window.
        mainWindow.setCentralWidget(container)


        mainWindow.display[0]="test text"
        
        mainWindow.name = "test2"
        mainWindow.label = QLabel()

        mainWindow.label.setText("Failed - QLabel Set Text")
        mainWindow.label.setText(mainWindow.display[0])
    
    def the_button_was_clicked(mainWindow):
        print("Song generated!")
        mainWindow.button.setText("Song Generated.")
        mainWindow.button.setEnabled(False)
        songs = spotify.main()

        # show_Playlist(songs, mainWindow, QLabel)

        #to[0] = "Passed - QLabel Set Text"
        array1 = []
        array2 = []
        array3 = []

        mainWindow.layout.addWidget(mainWindow.label)

        for index, item in enumerate(songs, start=1):
            try:
                name = item["track"]["name"]
                # print(index, name)
                array1 = [index, name]
                # print(mainWindow.array1)
                array3 = array3 + array2
                array2 = array2 + array1
                

            except TypeError or name == "":
                pass
    
        print("-------------------------------------------")

        mainWindow.display[0] = "test text2"
        mainWindow.display[0] = (str(array2[2])+' '+str(array2[3])) 
        
        # print(array2)
     
        print(array2)  

        print(mainWindow.display)

        mainWindow.label.setText(mainWindow.display[0])

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
# from modules.processing import prep_tasks
# from modules.tasks import startupTasksTimer
# timer_onStartUp = startupTasksTimer(window)
# timer_onStartUp.timeout.connect(lambda: prep_tasks(window))
# timer_onStartUp.start()

# Start the event loop.
app.exec()

# Your application won't reach here until you exit and the event
# loop has stopped.

