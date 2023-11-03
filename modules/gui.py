import sys
import random
from PyQt6.QtCore import QSize, Qt, QThreadPool, pyqtSignal, QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QComboBox
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QStackedLayout, QScrollBar, QScrollArea
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QPalette, QColor, QIcon, QPalette, QIcon, QPixmap, QImage
from array import *

import modules.spotify as spotify
from modules.processing import prep_tasks
import modules.state as state
import modules.tasks as tasks
import modules.graphs as graphs

app_path = ""

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)
        self.setMinimumSize(30, 40)
        self.resize(30, 60)

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    # stuff for modules.tasks... it needs to be declared outside of __init__ for some reason? -D
    stopWorkers = pyqtSignal()

    def __init__(mainWindow):
        super().__init__()
        frameCounter = 0
        mainWindow.setWindowTitle("CPU-DJ")
        mainWindow.setWindowIcon(QIcon('../logo.png'))
        mainWindow.setMinimumSize(200, 200)
        mainWindow.resize(1000, 600)
        mainWindow.display = ["empty"]

        # stuff for modules.tasks - ask dan if help needed.  this should always be in __init__ -D
        mainWindow.thread_pool = QThreadPool()
        mainWindow.thread_pool.setMaxThreadCount(50)

        mainWindow.genreList = QComboBox(mainWindow)
        mainWindow.genreList.addItems(state.genreList)
        mainWindow.genreList.move(100,100)
        mainWindow.genreList.setPlaceholderText("iranian")

        mainWindow.dataButton = QPushButton("Data")
        mainWindow.moodButton = QPushButton("Mood")

        mainWindow.generateButton = QPushButton("Generate Song")
        mainWindow.taskButton = QPushButton("Start tasks")
        mainWindow.genreButton = QPushButton("Set Genre")

        mainWindow.oGraphButton1 = QPushButton("Open Graph")
        mainWindow.oGraphButton2 = QPushButton("Open Graph")
        mainWindow.oGraphButton3 = QPushButton("Open Graph")
        mainWindow.oGraphButton4 = QPushButton("Open Graph")
        mainWindow.oGraphButton5 = QPushButton("Open Graph")
        mainWindow.oGraphButton6 = QPushButton("Open Graph")
        mainWindow.cGraphButton = QPushButton("Close Graph")

        mainWindow.generateButton.button_is_checked = False
        mainWindow.taskButton.button_is_checked = False
        mainWindow.dataButton.button_is_checked = False
        mainWindow.moodButton.button_is_checked = False
        
        mainWindow.button_setup()

        #initializing labels
        mainWindow.name            = "Test"
        mainWindow.playlistDisplay = QLabel()
        mainWindow.songEmbed       = QWebEngineView()
        mainWindow.emotionReading  = QLabel()
        mainWindow.genDescription  = QLabel()
        mainWindow.genDescription.setWordWrap(True)
        mainWindow.cpuInfo         = QLabel()
        mainWindow.cpuFreq         = QLabel()
        mainWindow.ramInfo         = QLabel()
        mainWindow.swapInfo        = QLabel()
        mainWindow.fanInfo         = QLabel()
        mainWindow.tempInfo        = QLabel()
        mainWindow.batteryInfo     = QLabel()

        mainWindow.playlistDisplay.setText("Failed - QLabel Set Text")
        mainWindow.playlistDisplay.setText(mainWindow.display[0])

        mainWindow.mood_display = QWidget()
        mainWindow.data_display = QWidget()
        mainWindow.mood_display.setLayout(mainWindow.moodPage())
        mainWindow.data_display.setLayout(mainWindow.dataPage())

        mainWindow.bottom = QStackedLayout()
        mainWindow.bottom.addWidget(mainWindow.mood_display)
        mainWindow.bottom.addWidget(mainWindow.data_display)
        mainWindow.bottom.setCurrentWidget(mainWindow.mood_display)

        mainWindow.top = QWidget()
        mainWindow.top.setLayout(mainWindow.top_bar())

        mainWindow.collector = QVBoxLayout()
        mainWindow.collector.addWidget(mainWindow.top)
        mainWindow.collector.addLayout(mainWindow.bottom)

        mainWindow.layout = mainWindow.collector
        container = QWidget()
        container.setLayout(mainWindow.layout)
        # Set the central widget of the Window.
        mainWindow.setCentralWidget(container)

        # testing displays
        mainWindow.display[0]= "URI Generated. Check console."

        frameCounter+=1
        print(frameCounter)

        #mainWindow.setStyleSheet("background-color: rgb(255,0,0); margin:5px; border:1px solid rgb(0, 255, 0); ")

    def top_bar(mainWindow):
        row1 = QHBoxLayout()

        titleBox = QLabel("CPU-DJ")
        font = titleBox.font()
        font.setPointSize(30)
        titleBox.setFont(font)
        titleBox.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        label = QPixmap('logo.png')
        label = label.scaled(100, 100)

        container = QLabel()
        container.setPixmap(label)

        row1.addWidget(titleBox)
        row1.addWidget(mainWindow.moodButton)
        row1.addWidget(mainWindow.dataButton)
        row1.addWidget(container)

        return row1

    def moodPage(mainWindow):
        mainWindow.moodRow2 = QHBoxLayout()
        mainWindow.moodRow3 = QHBoxLayout()
        mainWindow.moodRow4 = QHBoxLayout()
        mainWindow.moodRow5 = QHBoxLayout()

        genreSelector = QVBoxLayout()
        genreSelector.addWidget(mainWindow.genreList)
        genreSelector.addWidget(mainWindow.generateButton)
        
        mainWindow.moodRow2.addLayout(genreSelector)
        mainWindow.moodRow2.addWidget(mainWindow.taskButton)

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

        containerBench.addLayout(mainWindow.moodRow2)
        containerBench.addLayout(mainWindow.moodRow3)
        containerBench.addLayout(mainWindow.moodRow4)
        containerBench.addLayout(mainWindow.moodRow5)

        return containerBench

    def dataPage(mainWindow):
        mainWindow.dataRow2 = QHBoxLayout()
        mainWindow.dataRow3 = QHBoxLayout()
        mainWindow.dataRow4 = QHBoxLayout()
        mainWindow.dataRow5 = QHBoxLayout()
        mainWindow.dataRow6 = QHBoxLayout()
        mainWindow.dataRow7 = QHBoxLayout()
        
        #start of left side coding stuff
        mainWindow.dataRow2.addWidget(mainWindow.cpuInfo)
        mainWindow.dataRow2.addWidget(mainWindow.oGraphButton1)
        mainWindow.dataRow2.addWidget(Color('purple'))

        mainWindow.dataRow3.addWidget(mainWindow.cpuFreq)
        mainWindow.dataRow3.addWidget(mainWindow.oGraphButton2)
        mainWindow.dataRow3.addWidget(Color('purple'))

        mainWindow.dataRow4.addWidget(mainWindow.ramInfo)
        mainWindow.dataRow4.addWidget(mainWindow.oGraphButton3)
        mainWindow.dataRow4.addWidget(Color('purple'))

        mainWindow.dataRow5.addWidget(mainWindow.swapInfo)
        mainWindow.dataRow5.addWidget(mainWindow.oGraphButton6)
        mainWindow.dataRow5.addWidget(Color('purple'))

        mainWindow.dataRow6.addWidget(mainWindow.tempInfo)
        mainWindow.dataRow6.addWidget(mainWindow.oGraphButton4)
        mainWindow.dataRow6.addWidget(Color('purple'))

        mainWindow.dataRow7.addWidget(mainWindow.fanInfo)
        mainWindow.dataRow7.addWidget(mainWindow.oGraphButton5)
        mainWindow.dataRow7.addWidget(Color('purple'))

        leftSide = QVBoxLayout()
        leftSide.addLayout(mainWindow.dataRow2, 1)
        leftSide.addLayout(mainWindow.dataRow3, 1)
        leftSide.addLayout(mainWindow.dataRow4, 1)
        leftSide.addLayout(mainWindow.dataRow5, 1)
        leftSide.addLayout(mainWindow.dataRow6, 1)
        leftSide.addLayout(mainWindow.dataRow7, 1)

        #left side of data page scrolling section
        scrollField = QScrollArea()
        scrollField.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scrollField.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scrollField.setLayout(leftSide)
        #scrollField.setMaximumSize(500, 400)
        scrollField.resize(500,1000)

        mainWindow.leftContainer = QWidget()
        mainWindow.leftContainer = scrollField
        mainWindow.leftContainer.setMinimumSize(500, 400)
        mainWindow.leftContainer.resize(500, 400)

        #start of right side data page
        mainWindow.cpu_percent_graph = graphs.DataGraph(lambda: state.cpudict["cpu_percent"])
        mainWindow.cpu_speed_graph = graphs.DataGraph(lambda: state.cpudict["cpu_freq"])
        mainWindow.cpu_ram_graph = graphs.DataGraph(lambda: state.cpudict["ram_percent"])
        mainWindow.cpu_swap_graph = graphs.DataGraph(lambda: state.cpudict["swap_percent"])
        mainWindow.cpu_fan_graph = graphs.DataGraph(lambda: state.cpudict["fan_speed"])
        mainWindow.cpu_temp_graph = graphs.DataGraph(lambda: state.cpudict["temp_sensor"])

        mainWindow.rightSide = QStackedLayout()
        mainWindow.rightSide.addWidget(mainWindow.cpu_percent_graph)
        mainWindow.rightSide.addWidget(mainWindow.cpu_speed_graph)
        mainWindow.rightSide.addWidget(mainWindow.cpu_ram_graph)
        mainWindow.rightSide.addWidget(mainWindow.cpu_swap_graph)
        mainWindow.rightSide.addWidget(mainWindow.cpu_fan_graph)
        mainWindow.rightSide.addWidget(mainWindow.cpu_temp_graph)
        mainWindow.rightSide.setCurrentWidget(mainWindow.cpu_percent_graph)

        mainWindow.rightContainer = QWidget()
        mainWindow.rightContainer.setLayout(mainWindow.rightSide)
        mainWindow.rightContainer.resize(500, 400)

        containerBench = QHBoxLayout()
        containerBench.addWidget(mainWindow.leftContainer)
        #containerBench.addWidget(graphs.DataGraph(graphs.test_fxn, mainWindow))
        containerBench.addWidget(mainWindow.rightContainer, 1)

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

        mainWindow.oGraphButton1.setCheckable(True)
        mainWindow.oGraphButton1.setChecked(False)
        mainWindow.oGraphButton1.clicked.connect(mainWindow.oGraphButtonPressed1)
        mainWindow.oGraphButton1.setMinimumSize(45, 60)
        mainWindow.oGraphButton1.resize(60, 60)

        mainWindow.oGraphButton2.setCheckable(True)
        mainWindow.oGraphButton2.setChecked(False)
        mainWindow.oGraphButton2.clicked.connect(mainWindow.oGraphButtonPressed2)
        mainWindow.oGraphButton2.setMinimumSize(45, 60)
        mainWindow.oGraphButton2.resize(60, 60)

        mainWindow.oGraphButton3.setCheckable(True)
        mainWindow.oGraphButton3.setChecked(False)
        mainWindow.oGraphButton3.clicked.connect(mainWindow.oGraphButtonPressed3)
        mainWindow.oGraphButton3.setMinimumSize(45, 60)
        mainWindow.oGraphButton3.resize(60, 60)

        mainWindow.oGraphButton4.setCheckable(True)
        mainWindow.oGraphButton4.setChecked(False)
        mainWindow.oGraphButton4.clicked.connect(mainWindow.oGraphButtonPressed4)
        mainWindow.oGraphButton4.setMinimumSize(45, 60)
        mainWindow.oGraphButton4.resize(60, 60)

        mainWindow.oGraphButton5.setCheckable(True)
        mainWindow.oGraphButton5.setChecked(False)
        mainWindow.oGraphButton5.clicked.connect(mainWindow.oGraphButtonPressed5)
        mainWindow.oGraphButton5.setMinimumSize(45, 60)
        mainWindow.oGraphButton5.resize(60, 60)

        mainWindow.oGraphButton6.setCheckable(True)
        mainWindow.oGraphButton6.setChecked(False)
        mainWindow.oGraphButton6.clicked.connect(mainWindow.oGraphButtonPressed6)
        mainWindow.oGraphButton6.setMinimumSize(45, 60)
        mainWindow.oGraphButton6.resize(60, 60)
        return
    
    def taskButtonPressed(mainWindow):
        mainWindow.taskButton.setChecked(True)
        prep_tasks(mainWindow)
        mainWindow.cpu_percent_graph.start_task()
        mainWindow.cpu_speed_graph.start_task()
        mainWindow.cpu_ram_graph.start_task()
        mainWindow.cpu_swap_graph.start_task()
        mainWindow.cpu_fan_graph.start_task()
        mainWindow.cpu_temp_graph.start_task()
        
        mainWindow.processingUI()
        mainWindow.taskButton.setEnabled(False)
        mainWindow.taskButton.setText("Tasks started.")
        return

    def taskButtonReleased(mainWindow):
        #print(mainWindow.button_is_checked)
        return

    def dataButtonPressed(mainWindow):
        # Set the central widget of the Window.
        mainWindow.bottom.setCurrentWidget(mainWindow.data_display)

        mainWindow.moodButton.setChecked(False)
        mainWindow.dataButton.setChecked(True)

        mainWindow.moodButton.setStyleSheet("background-color: rgb(0,255,0); margin:5px; border:1px solid rgb(0, 0, 255); ")
        mainWindow.dataButton.setStyleSheet("background-color: rgb(255,0,0); margin:5px; border:1px solid rgb(0, 255, 0); ")
        return

    def moodButtonPressed(mainWindow):
        state.currentGenre = mainWindow.genreList.currentText()
        print(state.currentGenre)

        mainWindow.bottom.setCurrentWidget(mainWindow.mood_display)

        mainWindow.dataButton.setChecked(False)
        mainWindow.moodButton.setChecked(True)

        mainWindow.dataButton.setStyleSheet("background-color: rgb(0,255,0); margin:5px; border:1px solid rgb(0, 0, 255); ")
        mainWindow.moodButton.setStyleSheet("background-color: rgb(255,0,0); margin:5px; border:1px solid rgb(0, 255, 0); ")
        return

    def oGraphButtonPressed1(mainWindow):
        mainWindow.rightSide.setCurrentWidget(mainWindow.cpu_percent_graph)
        mainWindow.oGraphButton2.setChecked(False)
        mainWindow.oGraphButton3.setChecked(False)
        mainWindow.oGraphButton4.setChecked(False)
        mainWindow.oGraphButton5.setChecked(False)
        mainWindow.oGraphButton6.setChecked(False)
        mainWindow.oGraphButton1.setChecked(True)
        return

    def oGraphButtonPressed2(mainWindow):
        mainWindow.rightSide.setCurrentWidget(mainWindow.cpu_speed_graph)
        mainWindow.oGraphButton1.setChecked(False)
        mainWindow.oGraphButton3.setChecked(False)
        mainWindow.oGraphButton4.setChecked(False)
        mainWindow.oGraphButton5.setChecked(False)
        mainWindow.oGraphButton6.setChecked(False)
        mainWindow.oGraphButton2.setChecked(True)
        return

    def oGraphButtonPressed3(mainWindow):
        mainWindow.rightSide.setCurrentWidget(mainWindow.cpu_ram_graph)
        mainWindow.oGraphButton1.setChecked(False)
        mainWindow.oGraphButton2.setChecked(False)
        mainWindow.oGraphButton4.setChecked(False)
        mainWindow.oGraphButton5.setChecked(False)
        mainWindow.oGraphButton6.setChecked(False)
        mainWindow.oGraphButton3.setChecked(True)
        return

    def oGraphButtonPressed4(mainWindow):
        mainWindow.rightSide.setCurrentWidget(mainWindow.cpu_fan_graph)
        mainWindow.oGraphButton1.setChecked(False)
        mainWindow.oGraphButton2.setChecked(False)
        mainWindow.oGraphButton3.setChecked(False)
        mainWindow.oGraphButton5.setChecked(False)
        mainWindow.oGraphButton6.setChecked(False)
        mainWindow.oGraphButton4.setChecked(True)
        return

    def oGraphButtonPressed5(mainWindow):
        mainWindow.rightSide.setCurrentWidget(mainWindow.cpu_temp_graph)
        mainWindow.oGraphButton1.setChecked(False)
        mainWindow.oGraphButton2.setChecked(False)
        mainWindow.oGraphButton3.setChecked(False)
        mainWindow.oGraphButton4.setChecked(False)
        mainWindow.oGraphButton6.setChecked(False)
        mainWindow.oGraphButton5.setChecked(True)
        return
    
    def oGraphButtonPressed6(mainWindow):
        mainWindow.rightSide.setCurrentWidget(mainWindow.cpu_swap_graph)
        mainWindow.oGraphButton1.setChecked(False)
        mainWindow.oGraphButton2.setChecked(False)
        mainWindow.oGraphButton3.setChecked(False)
        mainWindow.oGraphButton4.setChecked(False)
        mainWindow.oGraphButton5.setChecked(False)
        mainWindow.oGraphButton6.setChecked(True)
        return

    def generateButtonReleased(mainWindow):
        mainWindow.generateButton.clicked = True
        return
    
    def processingUI(mainWindow):
        item = mainWindow.moodRow3.itemAt(0)
        rm = item.widget()
        rm.deleteLater()
        item = mainWindow.moodRow3.itemAt(1)
        rm = item.widget()
        rm.deleteLater()
        item = mainWindow.moodRow3.itemAt(2)
        rm = item.widget()
        rm.deleteLater()

        mainWindow.emotionReading.setText("...")
        mainWindow.cpuInfo.setText("...")
        mainWindow.moodRow3.addWidget(mainWindow.genDescription)
        mainWindow.moodRow3.addWidget(mainWindow.emotionReading)
        tasks.start(mainWindow.setDictToUI)

    def setDictToUI(mainWindow):
        while not state.mainFinished:
            emotionText = "Your computer is feeling "
            emotionText = emotionText + state.determine_emotion()
            mainWindow.emotionReading.setText(emotionText)

            infoText = "CPU Percent: " + str(state.cpudict["cpu_percent"]) + "%"
            mainWindow.cpuInfo.setText(infoText)
            totalText = infoText

            infoText = "CPU Speed: " + str(state.cpudict["cpu_freq"])
            mainWindow.cpuFreq.setText(infoText)
            totalText = totalText + "\n" + infoText

            infoText = "RAM Usage: " + str(state.cpudict["ram_percent"]) + "%"
            mainWindow.ramInfo.setText(infoText)
            totalText = totalText + "\n" + infoText

            infoText = "RAM Swap: " + str(state.cpudict["swap_percent"]) + "%"
            mainWindow.swapInfo.setText(infoText)
            totalText = totalText + "\n" + infoText

            infoText = "Fan Speed: " + str(state.cpudict["fan_speed"])
            mainWindow.fanInfo.setText(infoText)
            totalText = totalText + "\n" + infoText

            infoText = "Internal Temperature: " + str(state.cpudict["temp_sensor"])
            mainWindow.tempInfo.setText(infoText)
            totalText = totalText + "\n" + infoText

            infoText = "Battery Information: " + str(state.cpudict["battery_info"])
            mainWindow.batteryInfo.setText(infoText)
            totalText = totalText + "\n" + infoText
            mainWindow.genDescription.setText(totalText)
            #print(totalText)
            
            tasks.wait(1000)
        return True
    
    def generate_list(mainWindow):
        print("URI generated!")
        mainWindow.generateButton.setText("Generate New Song")

        if(state.songsGenerated == 0):
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

        if(state.songsGenerated == 0):
            mainWindow.moodRow4.addWidget(mainWindow.songEmbed)
            mainWindow.songEmbed.show()
            mainWindow.playlistDisplay.setText(mainWindow.display[0])
        
        state.songsGenerated += 1
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

    state.window = MainWindow()
    state.window.show()  # IMPORTANT!!!!! Windows are hidden by default.

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
