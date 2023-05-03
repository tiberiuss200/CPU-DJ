import sys
import random
from PyQt6.QtCore import QSize, Qt, QThreadPool, pyqtSignal, QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QPalette, QColor
from array import *

import modules.spotify as spotify
from modules.processing import prep_tasks
import modules.state as state
import modules.tasks as tasks

app_path = ""

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

        mainWindow.display = ["empty"]

        # stuff for modules.tasks - ask dan if help needed.  this should always be in __init__ -D
        mainWindow.thread_pool = QThreadPool()
        mainWindow.thread_pool.setMaxThreadCount(10)

        mainWindow.generateButton = QPushButton("Generate Song")
        mainWindow.taskButton = QPushButton("Start tasks")
        mainWindow.generateButton.button_is_checked = False
        mainWindow.taskButton.button_is_checked = False
        mainWindow.button_setup()

        mainWindow.layout = mainWindow.bench_layout()

        # testing displays
        mainWindow.display[0]= "URI Generated. Check console."

        mainWindow.name = "Test"
        mainWindow.playlistDisplay = QLabel()
        mainWindow.songEmbed = QWebEngineView()
        mainWindow.emotionReading = QLabel()
        mainWindow.cpuInfo = QLabel()

        mainWindow.playlistDisplay.setText("Failed - QLabel Set Text")
        mainWindow.playlistDisplay.setText(mainWindow.display[0])

        container = QWidget()
        container.setLayout(mainWindow.layout)

        # Set the central widget of the Window.
        mainWindow.setCentralWidget(container)

        frameCounter+=1
        print(frameCounter)

    def bench_layout(mainWindow):
        
        mainWindow.row1 = QHBoxLayout()
        mainWindow.row2 = QHBoxLayout()
        mainWindow.row3 = QHBoxLayout()
        mainWindow.row4 = QHBoxLayout()
        mainWindow.row5 = QHBoxLayout()

        mainWindow.row1.addWidget(Color('red'))
        mainWindow.row1.addWidget(mainWindow.generateButton)
        mainWindow.row1.addWidget(mainWindow.taskButton)
        
        mainWindow.row2.addWidget(Color('red'))
        mainWindow.row2.addWidget(Color('yellow'))
        mainWindow.row2.addWidget(Color('purple'))

        mainWindow.row3.addWidget(Color('red'))
        mainWindow.row3.addWidget(Color('yellow'))
        mainWindow.row3.addWidget(Color('purple'))

        mainWindow.row4.addWidget(Color('red'))
        mainWindow.row4.addWidget(Color('yellow'))
        mainWindow.row4.addWidget(Color('purple'))

        mainWindow.row5.addWidget(Color('red'))
        mainWindow.row5.addWidget(Color('yellow'))
        mainWindow.row5.addWidget(Color('purple'))

        containerBench = QVBoxLayout()

        containerBench.addLayout(mainWindow.row1)
        containerBench.addLayout(mainWindow.row2)
        containerBench.addLayout(mainWindow.row3)
        containerBench.addLayout(mainWindow.row4)
        containerBench.addLayout(mainWindow.row5)

        return containerBench

    def button_setup(mainWindow):
        mainWindow.generateButton.setCheckable(True)
        mainWindow.generateButton.clicked.connect(mainWindow.generate_list)
        mainWindow.generateButton.released.connect(mainWindow.the_button_was_released)
        mainWindow.generateButton.setChecked(mainWindow.generateButton.button_is_checked)
        mainWindow.generateButton.setMinimumSize(45, 60)
        mainWindow.generateButton.resize(45, 60)

        mainWindow.taskButton.setCheckable(True)
        mainWindow.taskButton.released.connect(mainWindow.taskButtonPressed)
        mainWindow.taskButton.setChecked(mainWindow.taskButton.button_is_checked)
        mainWindow.taskButton.released.connect(mainWindow.the_button_was_released)
        mainWindow.taskButton.setMinimumSize(45, 60)
        mainWindow.taskButton.resize(45, 60)
        return
    
    def taskButtonPressed(mainWindow):
        prep_tasks(mainWindow)
        mainWindow.processingUI()
        mainWindow.taskButton.setEnabled(False)
        mainWindow.taskButton.setText("Tasks started.")
    
    def processingUI(mainWindow):
        item = mainWindow.row2.itemAt(0)
        rm = item.widget()
        rm.deleteLater()
        item = mainWindow.row2.itemAt(1)
        rm = item.widget()
        rm.deleteLater()
        item = mainWindow.row2.itemAt(2)
        rm = item.widget()
        rm.deleteLater()
        mainWindow.emotionReading.setText("...")
        mainWindow.cpuInfo.setText("...")
        mainWindow.row2.addWidget(mainWindow.emotionReading)
        mainWindow.row2.addWidget(mainWindow.cpuInfo)
        tasks.start(mainWindow, mainWindow.setDictToUI, mainWindow)

    def setDictToUI(mainWindow, testArg, any):
        while not state.mainFinished:
            emotions = ("Happy.", "Stressed.", "Angry.", "Bored.")
            emotionText = "Your computer is feeling "
            if state.cpudict["cpu_percent"] > 90.0:
                emotionText = emotionText + emotions[2]
                state.emotion = emotions[2]
            elif state.cpudict["cpu_percent"] < 5.0:
                emotionText = emotionText + emotions[3]
                state.emotion = emotions[3]
            elif state.cpudict["cpu_percent"] < 50.0:
                emotionText = emotionText + emotions[0]
                state.emotion = emotions[0]
            else:
                emotionText = emotionText + emotions[1]
                state.emotion = emotions[1]
            mainWindow.emotionReading.setText(emotionText)

            infoText = "CPU Percent: " + str(state.cpudict["cpu_percent"]) + "%"
            mainWindow.cpuInfo.setText(infoText)
            tasks.wait(1000)
        return True
    
    def generate_list(mainWindow):
        print("URI generated!")
        mainWindow.generateButton.setText("URI Generated.")
        mainWindow.generateButton.setEnabled(False)

        item = mainWindow.row4.itemAt(0)
        rm = item.widget()
        rm.deleteLater()
        item = mainWindow.row4.itemAt(1)
        rm = item.widget()
        rm.deleteLater()
        item = mainWindow.row4.itemAt(2)
        rm = item.widget()
        rm.deleteLater()

        #mainWindow.row4.addWidget(mainWindow.playlistDisplay)

        songs = spotify.main()
        mainWindow.songEmbed.setHtml(open("embed.html").read())
        mainWindow.row4.addWidget(mainWindow.songEmbed)
        mainWindow.songEmbed.show()

        mainWindow.playlistDisplay.setText(mainWindow.display[0])
        return

    def the_button_was_released(mainWindow):
        mainWindow.generateButton.button_is_checked = True
        mainWindow.taskButton.button_is_checked = True
        #print(mainWindow.button_is_checked)
        return

def show_Playlist(songs, mainWindow, QLabel):
    return
        
    
    # print(str(mainWindow.array3[2])+' '+mainWindow.array3[3])
    

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)
app_path = app.applicationDirPath()

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

