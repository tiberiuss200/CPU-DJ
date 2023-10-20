import sys
import random
from PyQt6.QtCore import QSize, Qt, QThreadPool, pyqtSignal, QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget
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
        mainWindow.resize(600, 800)
        mainWindow.display = ["empty"]

        # stuff for modules.tasks - ask dan if help needed.  this should always be in __init__ -D
        mainWindow.thread_pool = QThreadPool()
        mainWindow.thread_pool.setMaxThreadCount(10)

        mainWindow.generateButton = QPushButton("Generate Song")
        mainWindow.taskButton = QPushButton("Start tasks")
        mainWindow.dataButton = QPushButton("Data")
        mainWindow.moodButton = QPushButton("Mood")

        mainWindow.generateButton.button_is_checked = False
        mainWindow.taskButton.button_is_checked = False
        mainWindow.dataButton.button_is_checked = False
        mainWindow.moodButton.button_is_checked = False
        
        mainWindow.button_setup()

        
        mainWindow.Collector = QVBoxLayout()
        mainWindow.Collector.addLayout(mainWindow.moodPage())
        mainWindow.Collector.addLayout(mainWindow.dataPage())

        mainWindow.layout = mainWindow.Collector

        container = QWidget()
        container.setLayout(mainWindow.layout)

        # Set the central widget of the Window.
        mainWindow.setCentralWidget(container)

        # testing displays
        mainWindow.display[0]= "URI Generated. Check console."

        mainWindow.name            = "Test"
        mainWindow.playlistDisplay = QLabel()
        mainWindow.songEmbed       = QWebEngineView()
        mainWindow.emotionReading  = QLabel()
        mainWindow.cpuInfo         = QLabel()

        mainWindow.playlistDisplay.setText("Failed - QLabel Set Text")
        mainWindow.playlistDisplay.setText(mainWindow.display[0])

        frameCounter+=1
        print(frameCounter)

        #mainWindow.setStyleSheet("background-color: rgb(255,0,0); margin:5px; border:1px solid rgb(0, 255, 0); ")

    def moodPage(mainWindow):
        
        mainWindow.moodRow1 = QHBoxLayout()
        mainWindow.moodRow2 = QHBoxLayout()
        mainWindow.moodRow3 = QHBoxLayout()
        mainWindow.moodRow4 = QHBoxLayout()
        mainWindow.moodRow5 = QHBoxLayout()

        mainWindow.moodRow1.addWidget(Color('red'))
        mainWindow.moodRow1.addWidget(mainWindow.generateButton)
        mainWindow.moodRow1.addWidget(mainWindow.taskButton)
        
        mainWindow.moodRow2.addWidget(Color('red'))
        mainWindow.moodRow2.addWidget(Color('yellow'))
        mainWindow.moodRow2.addWidget(Color('purple'))

        mainWindow.moodRow3.addWidget(Color('red'))
        mainWindow.moodRow3.addWidget(Color('yellow'))
        mainWindow.moodRow3.addWidget(Color('purple'))

        mainWindow.moodRow4.addWidget(Color('red'))
        mainWindow.moodRow4.addWidget(Color('yellow'))
        mainWindow.moodRow4.addWidget(Color('purple'))

        mainWindow.moodRow5.addWidget(Color('red'))
        mainWindow.moodRow5.addWidget(Color('yellow'))
        mainWindow.moodRow5.addWidget(Color('purple'))

        containerBench = QVBoxLayout()

        containerBench.addLayout(mainWindow.moodRow1)
        containerBench.addLayout(mainWindow.moodRow2)
        containerBench.addLayout(mainWindow.moodRow3)
        containerBench.addLayout(mainWindow.moodRow4)
        containerBench.addLayout(mainWindow.moodRow5)

        return containerBench

    def dataPage(mainWindow):
        
        mainWindow.dataRow1 = QHBoxLayout()
        mainWindow.dataRow2 = QHBoxLayout()
        mainWindow.dataRow3 = QHBoxLayout()
        mainWindow.dataRow4 = QHBoxLayout()
        mainWindow.dataRow5 = QHBoxLayout()

        mainWindow.dataRow1.addWidget(Color('red'))
        mainWindow.dataRow1.addWidget(mainWindow.generateButton)
        mainWindow.dataRow1.addWidget(mainWindow.taskButton)
        
        mainWindow.dataRow2.addWidget(Color('red'))
        mainWindow.dataRow2.addWidget(Color('yellow'))
        mainWindow.dataRow2.addWidget(Color('purple'))

        mainWindow.dataRow3.addWidget(Color('red'))
        mainWindow.dataRow3.addWidget(Color('yellow'))
        mainWindow.dataRow3.addWidget(Color('purple'))

        mainWindow.dataRow4.addWidget(Color('red'))
        mainWindow.dataRow4.addWidget(Color('yellow'))
        mainWindow.dataRow4.addWidget(Color('purple'))

        mainWindow.dataRow5.addWidget(Color('red'))
        mainWindow.dataRow5.addWidget(Color('yellow'))
        mainWindow.dataRow5.addWidget(Color('purple'))

        containerBench = QVBoxLayout()

        containerBench.addLayout(mainWindow.dataRow1)
        containerBench.addLayout(mainWindow.dataRow2)
        containerBench.addLayout(mainWindow.dataRow3)
        containerBench.addLayout(mainWindow.dataRow4)
        containerBench.addLayout(mainWindow.dataRow5)

        return containerBench

    def button_setup(mainWindow):
        mainWindow.generateButton.setCheckable(True)
        mainWindow.generateButton.clicked.connect(mainWindow.generate_list)
        #mainWindow.generateButton.released.connect(mainWindow.generateButtonPressed)
        mainWindow.generateButton.setChecked(False)
        mainWindow.generateButton.setMinimumSize(45, 60)
        mainWindow.generateButton.resize(45, 60)

        mainWindow.taskButton.setCheckable(True)
        mainWindow.taskButton.clicked.connect(mainWindow.taskButtonPressed)
        mainWindow.taskButton.setChecked(False)
        mainWindow.taskButton.released.connect(mainWindow.taskButtonReleased)
        mainWindow.taskButton.setMinimumSize(45, 60)
        mainWindow.taskButton.resize(45, 60)

        mainWindow.dataButton.setCheckable(True)
        mainWindow.dataButton.setChecked(False)
        mainWindow.dataButton.clicked.connect(mainWindow.dataButtonPressed)
        #mainWindow.dataButton.released.connect(mainWindow.dataButtonReleased)
        mainWindow.dataButton.setMinimumSize(45, 60)
        mainWindow.dataButton.resize(45, 60)
        mainWindow.dataButton.setStyleSheet("background-color: rgb(0,255,0); margin:5px; border:1px solid rgb(0, 0, 255); ")

        mainWindow.moodButton.setCheckable(True)
        mainWindow.moodButton.setChecked(False)
        mainWindow.moodButton.clicked.connect(mainWindow.moodButtonPressed)
        #mainWindow.moodButton.released.connect(mainWindow.moodButtonReleased)
        mainWindow.moodButton.setMinimumSize(45, 60)
        mainWindow.moodButton.resize(45, 60)
        return
    
    def taskButtonPressed(mainWindow):
        prep_tasks(mainWindow)
        mainWindow.processingUI()
        mainWindow.taskButton.setEnabled(False)
        mainWindow.taskButton.setText("Tasks started.")
        return

    def taskButtonReleased(mainWindow):
        mainWindow.taskButton.clicked = True
        #print(mainWindow.button_is_checked)
        return

    def dataButtonPressed(mainWindow):
        # Set the central widget of the Window.
        mainWindow.moodPage.hide()
        mainWindow.dataPage.show()
        mainWindow.container = QWidget()
        mainWindow.container.setLayout(mainWindow.dataPage.layout)
        mainWindow.setCentralWidget(mainWindow.container)

        mainWindow.moodButton.setChecked(False)
        mainWindow.dataButton.setChecked(True)

        mainWindow.moodButton.setStyleSheet("background-color: rgb(0,255,0); margin:5px; border:1px solid rgb(0, 0, 255); ")
        mainWindow.dataButton.setStyleSheet("background-color: rgb(255,0,0); margin:5px; border:1px solid rgb(0, 255, 0); ")
        return

    def moodButtonPressed(mainWindow):
        mainWindow.dataButton.setChecked(False)
        mainWindow.moodButton.setChecked(True)

        mainWindow.dataButton.setStyleSheet("background-color: rgb(0,255,0); margin:5px; border:1px solid rgb(0, 0, 255); ")
        mainWindow.moodButton.setStyleSheet("background-color: rgb(255,0,0); margin:5px; border:1px solid rgb(0, 255, 0); ")
        return
    
    def generateButtonReleased(mainWindow):
        mainWindow.generateButton.clicked = True
        return
    
    def processingUI(mainWindow):
        item = mainWindow.moodRow2.itemAt(0)
        rm = item.widget()
        rm.deleteLater()
        item = mainWindow.moodRow2.itemAt(1)
        rm = item.widget()
        rm.deleteLater()
        item = mainWindow.moodRow2.itemAt(2)
        rm = item.widget()
        rm.deleteLater()
        mainWindow.emotionReading.setText("...")
        mainWindow.cpuInfo.setText("...")
        mainWindow.moodRow2.addWidget(mainWindow.emotionReading)
        mainWindow.moodRow2.addWidget(mainWindow.cpuInfo)
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

        item = mainWindow.moodRow4.itemAt(0)
        rm = item.widget()
        rm.deleteLater()
        item = mainWindow.moodRow4.itemAt(1)
        rm = item.widget()
        rm.deleteLater()
        item = mainWindow.moodRow4.itemAt(2)
        rm = item.widget()
        rm.deleteLater()

        #mainWindow.moodRow4.addWidget(mainWindow.playlistDisplay)

        songs = spotify.main()
        mainWindow.songEmbed.setHtml(open("embed.html").read())
        mainWindow.moodRow4.addWidget(mainWindow.songEmbed)
        mainWindow.songEmbed.show()

        mainWindow.playlistDisplay.setText(mainWindow.display[0])
        return

def show_Playlist(songs, mainWindow, QLabel):
    return
        
    
    # print(str(mainWindow.array3[2])+' '+mainWindow.array3[3])
    

def main():
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


"""

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
        mainWindow.setMinimumSize(600, 400)
        mainWindow.resize(200, 200)
        mainWindow.display = ["empty"]

        # stuff for modules.tasks - ask dan if help needed.  this should always be in __init__ -D
        mainWindow.thread_pool = QThreadPool()
        mainWindow.thread_pool.setMaxThreadCount(10)

        mainWindow.generateButton = QPushButton("Generate Song")
        mainWindow.taskButton = QPushButton("Start tasks")
        mainWindow.dataButton = QPushButton("Data")
        mainWindow.moodButton = QPushButton("Mood")

        mainWindow.generateButton.button_is_checked = False
        mainWindow.taskButton.button_is_checked = False
        mainWindow.dataButton.button_is_checked = False
        mainWindow.moodButton.button_is_checked = False

        mainWindow.button_setup()

        mainWindow.moodPage = QWidget()

        # Set the central widget of the Window.

        mainWindow.dataPage = QWidget()
        mainWindow.dataPage.hide()
        mainWindow.moodPage.show()
        mainWindow.container = QWidget()
        mainWindow.container.setLayout(mainWindow.moodPage.layout)
        mainWindow.setCentralWidget(mainWindow.container)

        mainWindow.moodPage.layout = mainWindow.mood_layout()
        mainWindow.dataPage.layout = mainWindow.data_layout()

        mainWindow.container = QWidget()
        mainWindow.container.setLayout(mainWindow.moodPage.layout)
        mainWindow.setCentralWidget(mainWindow.container)

        # testing displays
        mainWindow.display[0]= "URI Generated. Check console."

        mainWindow.name            = "Test"
        mainWindow.playlistDisplay = QLabel()
        mainWindow.songEmbed       = QWebEngineView()
        mainWindow.emotionReading  = QLabel()
        mainWindow.cpuInfo         = QLabel()

        mainWindow.playlistDisplay.setText("Failed - QLabel Set Text")
        mainWindow.playlistDisplay.setText(mainWindow.display[0])

        frameCounter+=1
        print(frameCounter)

        mainWindow.setStyleSheet("background-color: rgb(255,0,0); margin:5px; border:1px solid rgb(0, 255, 0); ")

    def top_bar(mainWindow):

        row1 = QHBoxLayout()

        titleBox = QLabel("CPU-DJ")
        font = titleBox.font()
        font.setPointSize(30)
        titleBox.setFont(font)
        titleBox.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        row1.addWidget(titleBox)
        row1.addWidget(mainWindow.dataButton)
        row1.addWidget(mainWindow.moodButton)
        row1.addWidget(Color('blue'))

        return row1

    def mood_layout(mainWindow):

        containerBench = QVBoxLayout()

        #mainWindow.moodRow1 = mainWindow.top_bar()

        mainWindow.moodRow1 = QHBoxLayout()

        titleBox = QLabel("CPU-DJ")
        font = titleBox.font()
        font.setPointSize(30)
        titleBox.setFont(font)
        titleBox.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        mainWindow.moodRow1.addWidget(titleBox)
        mainWindow.moodRow1.addWidget(mainWindow.dataButton)
        mainWindow.moodRow1.addWidget(mainWindow.moodButton)
        mainWindow.moodRow1.addWidget(Color('blue'))

        containerBench.addLayout(mainWindow.moodRow1)

        mainWindow.moodRow2 = QHBoxLayout()
        mainWindow.moodRow3 = QHBoxLayout()
        mainWindow.moodRow4 = QHBoxLayout()
        mainWindow.moodRow5 = QHBoxLayout()
        
        mainWindow.moodRow2.addWidget(Color('red'))
        mainWindow.moodRow2.addWidget(Color('yellow'))
        mainWindow.moodRow2.addWidget(Color('purple'))

        mainWindow.moodRow3.addWidget(Color('red'))
        mainWindow.moodRow3.addWidget(Color('yellow'))
        mainWindow.moodRow3.addWidget(Color('purple'))

        mainWindow.moodRow4.addWidget(Color('red'))
        mainWindow.moodRow4.addWidget(Color('yellow'))
        mainWindow.moodRow4.addWidget(Color('purple'))

        mainWindow.moodRow5.addWidget(Color('red'))
        mainWindow.moodRow5.addWidget(mainWindow.generateButton)
        mainWindow.moodRow5.addWidget(mainWindow.taskButton)

        containerBench.addLayout(mainWindow.moodRow2)
        containerBench.addLayout(mainWindow.moodRow3)
        containerBench.addLayout(mainWindow.moodRow4)
        containerBench.addLayout(mainWindow.moodRow5)

        return containerBench
    
    def data_layout(mainWindow):

        containerBench = QVBoxLayout()

        #mainWindow.dataRow1 = mainWindow.top_bar()
        mainWindow.dataRow1 = QHBoxLayout()

        titleBox = QLabel("CPU-DJ")
        font = titleBox.font()
        font.setPointSize(30)
        titleBox.setFont(font)
        titleBox.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        mainWindow.dataRow1.addWidget(titleBox)
        mainWindow.dataRow1.addWidget(mainWindow.dataButton)
        mainWindow.dataRow1.addWidget(mainWindow.moodButton)
        mainWindow.dataRow1.addWidget(Color('blue'))

        containerBench.addLayout(mainWindow.dataRow1)

        mainWindow.dataRow2 = QHBoxLayout()
        mainWindow.dataRow3 = QHBoxLayout()
        mainWindow.dataRow4 = QHBoxLayout()
        mainWindow.dataRow5 = QHBoxLayout()

        mainWindow.dataRow2.addWidget(Color('red'))
        mainWindow.dataRow2.addWidget(Color('yellow'))
        mainWindow.dataRow2.addWidget(Color('purple'))

        mainWindow.dataRow3.addWidget(Color('red'))
        mainWindow.dataRow3.addWidget(Color('yellow'))
        mainWindow.dataRow3.addWidget(Color('purple'))

        mainWindow.dataRow4.addWidget(Color('red'))
        mainWindow.dataRow4.addWidget(Color('yellow'))
        mainWindow.dataRow4.addWidget(Color('purple'))

        mainWindow.dataRow5.addWidget(Color('red'))
        mainWindow.dataRow5.addWidget(Color('yellow'))
        mainWindow.dataRow5.addWidget(Color('purple'))

        containerBench = QVBoxLayout()

        containerBench.addLayout(mainWindow.dataRow2)
        containerBench.addLayout(mainWindow.dataRow3)
        containerBench.addLayout(mainWindow.dataRow4)
        containerBench.addLayout(mainWindow.dataRow5)

        return containerBench

    def button_setup(mainWindow):
        mainWindow.generateButton.setCheckable(True)
        mainWindow.generateButton.clicked.connect(mainWindow.generate_list)
        #mainWindow.generateButton.released.connect(mainWindow.generateButtonPressed)
        mainWindow.generateButton.setChecked(False)
        mainWindow.generateButton.setMinimumSize(45, 60)
        mainWindow.generateButton.resize(45, 60)

        mainWindow.taskButton.setCheckable(True)
        mainWindow.taskButton.clicked.connect(mainWindow.taskButtonPressed)
        mainWindow.taskButton.setChecked(False)
        mainWindow.taskButton.released.connect(mainWindow.taskButtonReleased)
        mainWindow.taskButton.setMinimumSize(45, 60)
        mainWindow.taskButton.resize(45, 60)

        mainWindow.dataButton.setCheckable(True)
        mainWindow.dataButton.setChecked(False)
        mainWindow.dataButton.clicked.connect(mainWindow.dataButtonPressed)
        #mainWindow.dataButton.released.connect(mainWindow.dataButtonReleased)
        mainWindow.dataButton.setMinimumSize(45, 60)
        mainWindow.dataButton.resize(45, 60)
        mainWindow.dataButton.setStyleSheet("background-color: rgb(0,255,0); margin:5px; border:1px solid rgb(0, 0, 255); ")

        mainWindow.moodButton.setCheckable(True)
        mainWindow.moodButton.setChecked(False)
        mainWindow.moodButton.clicked.connect(mainWindow.moodButtonPressed)
        #mainWindow.moodButton.released.connect(mainWindow.moodButtonReleased)
        mainWindow.moodButton.setMinimumSize(45, 60)
        mainWindow.moodButton.resize(45, 60)
        
        return
    
    def taskButtonPressed(mainWindow):
        prep_tasks(mainWindow)
        mainWindow.processingUI()
        mainWindow.taskButton.setEnabled(False)
        mainWindow.taskButton.setText("Tasks started.")
        return

    def dataButtonPressed(mainWindow):
        # Set the central widget of the Window.
        mainWindow.moodPage.hide()
        mainWindow.dataPage.show()
        mainWindow.container = QWidget()
        mainWindow.container.setLayout(mainWindow.dataPage.layout)
        mainWindow.setCentralWidget(mainWindow.container)

        mainWindow.moodButton.setChecked(False)
        mainWindow.dataButton.setChecked(True)

        mainWindow.moodButton.setStyleSheet("background-color: rgb(0,255,0); margin:5px; border:1px solid rgb(0, 0, 255); ")
        mainWindow.dataButton.setStyleSheet("background-color: rgb(255,0,0); margin:5px; border:1px solid rgb(0, 255, 0); ")
        return

    def moodButtonPressed(mainWindow):
        mainWindow.dataButton.setChecked(False)
        mainWindow.moodButton.setChecked(True)

        mainWindow.dataButton.setStyleSheet("background-color: rgb(0,255,0); margin:5px; border:1px solid rgb(0, 0, 255); ")
        mainWindow.moodButton.setStyleSheet("background-color: rgb(255,0,0); margin:5px; border:1px solid rgb(0, 255, 0); ")
        return
    
    def processingUI(mainWindow):
        item = mainWindow.moodRow2.itemAt(0)
        rm = item.widget()
        rm.deleteLater()
        item = mainWindow.moodRow2.itemAt(1)
        rm = item.widget()
        rm.deleteLater()
        item = mainWindow.moodRow2.itemAt(2)
        rm = item.widget()
        rm.deleteLater()
        mainWindow.emotionReading.setText("...")
        mainWindow.cpuInfo.setText("...")
        mainWindow.moodRow2.addWidget(mainWindow.emotionReading)
        mainWindow.moodRow2.addWidget(mainWindow.cpuInfo)
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

        item = mainWindow.moodRow3.itemAt(0)
        rm = item.widget()
        rm.deleteLater()
        item = mainWindow.moodRow3.itemAt(1)
        rm = item.widget()
        rm.deleteLater()
        item = mainWindow.moodRow3.itemAt(2)
        rm = item.widget()
        rm.deleteLater()


        songs = spotify.main()
        mainWindow.songEmbed.setHtml(open("embed.html").read())
        mainWindow.moodRow3.addWidget(mainWindow.songEmbed)
        mainWindow.songEmbed.show()

        mainWindow.playlistDisplay.setText(mainWindow.display[0])
        return

    def generateButtonReleased(mainWindow):
        mainWindow.generateButton.clicked = True
        return

    def taskButtonReleased(mainWindow):
        mainWindow.taskButton.clicked = True
        #print(mainWindow.button_is_checked)
        return

def show_Playlist(songs, mainWindow, QLabel):
    return
        
    
    # print(str(mainWindow.array3[2])+' '+mainWindow.array3[3])
    

def main():
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


"""