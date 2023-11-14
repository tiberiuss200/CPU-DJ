import sys
import random
from PyQt6.QtCore import QSize, Qt, QThreadPool, pyqtSignal, QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QComboBox
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QStackedLayout, QScrollBar, QScrollArea
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QPalette, QColor, QIcon, QPixmap, QImage
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
        mainWindow.setWindowIcon(QIcon('logo.ico'))
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
        mainWindow.scanButton = QPushButton("Scan")
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
        mainWindow.scanButton.button_is_checked = False
        mainWindow.moodButton.button_is_checked = True
        
        mainWindow.button_setup()

       # mainWindow.scanButton.setStyleSheet("background-color: rgb(0,255,0); margin:2px; border:1px solid rgb(0, 0, 255); ")
       # mainWindow.dataButton.setStyleSheet("background-color: rgb(0,255,0); margin:2px; border:1px solid rgb(0, 0, 255); ")

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
        mainWindow.graphDesc       = QLabel()

        mainWindow.playlistDisplay.setText("Failed - QLabel Set Text")
        mainWindow.playlistDisplay.setText(mainWindow.display[0])

        mainWindow.songEmbed.setHtml("<html><body style='background-color:#33475b'</body></html>")
        mainWindow.songEmbed.show()

        mainWindow.mood_display = QWidget()
        mainWindow.data_display = QWidget()
        mainWindow.scan_display = QWidget()
        mainWindow.mood_display.setLayout(mainWindow.moodPage())
        mainWindow.data_display.setLayout(mainWindow.dataPage())
        mainWindow.scan_display.setLayout(mainWindow.scanPage())

        mainWindow.bottom = QStackedLayout()
        mainWindow.bottom.addWidget(mainWindow.mood_display)
        mainWindow.bottom.addWidget(mainWindow.data_display)
        mainWindow.bottom.addWidget(mainWindow.scan_display)
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

        mainWindow.setStyleSheet("""
            QMainWindow {
                background-color: #33475b; /* Light gray background */
                color: white; /* Dark gray text */
            }
            QPushButton {
                background-color: #68369B; /* Purple buttons */
                color: white;
                border-radius: 5px;
                padding: 10px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLabel {
                color: white; /*White text */
            }
            QComboBox {
                border: 1px solid #68369B; /* Purple border */
                border-radius: 3px;
                padding: 5px;
                min-width: 6em;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left-width: 1px;
                border-left-color: ##68369B; /* Purple border */
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
        """)

        frameCounter+=1
        print(frameCounter)

        #mainWindow.setStyleSheet("background-color: rgb(255,0,0); margin:2px; border:1px solid rgb(0, 255, 0); ")

    def top_bar(mainWindow):
        #create layouts
        row1 = QHBoxLayout()



        iconBox = QLabel()
        logoBox = QLabel()
        icon = QPixmap('icon.png')
        logo = QPixmap('logo.png')

        #setting up variables
        icon = icon.scaled(100, 100)
        logo = logo.scaled(290, 80)

        #applying variables
        iconBox.setPixmap(icon)
        logoBox.setPixmap(logo)

        iconBox.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        logoBox.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        #add widgets
        row1.addWidget(iconBox)
        row1.addWidget(logoBox)
        row1.addWidget(mainWindow.moodButton)
        row1.addWidget(mainWindow.scanButton)
        row1.addWidget(mainWindow.dataButton)
        return row1

    def moodPage(mainWindow):
        #create layouts
        containerBench = QVBoxLayout()

        mainWindow.moodRow2 = QHBoxLayout()
        mainWindow.moodRow3 = QHBoxLayout()
        mainWindow.moodRow4 = QHBoxLayout()
        mainWindow.moodRow5 = QHBoxLayout()

        #add widgets
        mainWindow.moodRow2.addWidget(mainWindow.genreList)
        mainWindow.moodRow2.addWidget(mainWindow.generateButton)
        mainWindow.moodRow2.addWidget(mainWindow.taskButton)

        mainWindow.moodRow3.addWidget(Color('#8B0000'))
        mainWindow.moodRow3.addWidget(Color('yellow'))
        mainWindow.moodRow3.addWidget(Color('purple'))

        mainWindow.moodRow4.addWidget(mainWindow.songEmbed)
        #mainWindow.moodRow5.addWidget(Color('red'))
        #mainWindow.moodRow5.addWidget(Color('yellow'))
        #mainWindow.moodRow5.addWidget(Color('purple'))
        #add layouts
        containerBench.addLayout(mainWindow.moodRow2)
        containerBench.addLayout(mainWindow.moodRow3)
        containerBench.addLayout(mainWindow.moodRow4)
        #containerBench.addLayout(mainWindow.moodRow5)

        return containerBench
    
    def scanPage(mainWindow):
        #create layouts
        containerBench = QVBoxLayout()



        mainWindow.scanRowBasic = QHBoxLayout()
        mainWindow.scanRow2 = QHBoxLayout()
        mainWindow.scanRow3 = QHBoxLayout()
        mainWindow.scanRow4 = QHBoxLayout()
        mainWindow.scanRow5 = QHBoxLayout()

        #add widgets
        mainWindow.scanRow2.addWidget(Color('#8B0000'))
        mainWindow.scanRow2.addWidget(Color('yellow'))
        mainWindow.scanRow2.addWidget(Color('purple'))

        mainWindow.scanRow3.addWidget(Color('#8B0000'))
        mainWindow.scanRow3.addWidget(Color('yellow'))
        mainWindow.scanRow3.addWidget(Color('purple'))

        mainWindow.scanRow4.addWidget(Color('#8B0000'))
        mainWindow.scanRow4.addWidget(Color('yellow'))
        mainWindow.scanRow4.addWidget(Color('purple'))

        mainWindow.scanRow5.addWidget(Color('red'))
        mainWindow.scanRow5.addWidget(Color('yellow'))
        mainWindow.scanRow5.addWidget(Color('purple'))

        #add layouts
        containerBench.addLayout(mainWindow.scanRow2)
        containerBench.addLayout(mainWindow.scanRow3)
        containerBench.addLayout(mainWindow.scanRow4)
        containerBench.addLayout(mainWindow.scanRow5)

        return containerBench

    def dataPage(mainWindow):
        #create layouts
        containerBench      = QHBoxLayout()
        mainWindow.rightSide = QStackedLayout()
        leftSide            = QVBoxLayout()    

        mainWindow.dataRow2 = QHBoxLayout()     #creating leftside layout rows
        mainWindow.dataRow3 = QHBoxLayout()
        mainWindow.dataRow4 = QHBoxLayout()
        mainWindow.dataRow5 = QHBoxLayout()
        mainWindow.dataRow6 = QHBoxLayout()
        mainWindow.dataRow7 = QHBoxLayout()

        #create widgets
        mainWindow.leftContainer = QWidget()
        mainWindow.rightContainer = QWidget() #creating rightside widgets

        scrollField = QScrollArea() #used for left side scrolling
        mainWindow.leftContainer = scrollField

        mainWindow.cpu_percent_graph = graphs.DataGraph(lambda: state.cpudict["cpu_percent"]) #creating large graph widgets
        mainWindow.cpu_speed_graph = graphs.DataGraph(lambda: state.cpudict["cpu_freq"])
        mainWindow.cpu_ram_graph = graphs.DataGraph(lambda: state.cpudict["ram_percent"])
        mainWindow.cpu_swap_graph = graphs.DataGraph(lambda: state.cpudict["swap_percent"])
        mainWindow.cpu_fan_graph = graphs.DataGraph(lambda: state.cpudict["fan_speed"])
        mainWindow.cpu_temp_graph = graphs.DataGraph(lambda: state.cpudict["temp_sensor"])

        mainWindow.cpu_percent_graph_s = graphs.DataGraph(lambda: state.cpudict["cpu_percent"]) #creating small graph widgets
        mainWindow.cpu_speed_graph_s = graphs.DataGraph(lambda: state.cpudict["cpu_freq"])
        mainWindow.cpu_ram_graph_s = graphs.DataGraph(lambda: state.cpudict["ram_percent"])
        mainWindow.cpu_swap_graph_s = graphs.DataGraph(lambda: state.cpudict["swap_percent"])
        
        #swap settings
        mainWindow.rightSide.setCurrentWidget(mainWindow.cpu_percent_graph)
        mainWindow.rightContainer.setLayout(mainWindow.rightSide)

        #graphs boundaries
        mainWindow.cpu_speed_graph_s.set_ylim(0, 4000) #CPU Speed graph y-axis bounds
        mainWindow.cpu_speed_graph.set_ylim(0, 4000) #CPU Speed graph y-axis bounds

        #graphs styling
        mainWindow.cpu_percent_graph_s.set_size(150, 100) #setting sizes of small graphs
        mainWindow.cpu_speed_graph_s.set_size(150, 100)
        mainWindow.cpu_ram_graph_s.set_size(150, 100)
        mainWindow.cpu_swap_graph_s.set_size(150, 100)

        #style work for data page
        leftSide.setContentsMargins(1, 1, 1, 1);
        mainWindow.dataRow2.setContentsMargins(1, 1, 1, 1); #setting row content margins
        mainWindow.dataRow3.setContentsMargins(1, 1, 1, 1);
        mainWindow.dataRow4.setContentsMargins(1, 1, 1, 1);
        mainWindow.dataRow5.setContentsMargins(1, 1, 1, 1);
        mainWindow.dataRow6.setContentsMargins(1, 1, 1, 1);
        mainWindow.dataRow7.setContentsMargins(1, 1, 1, 1);
        
        #leftside stylesheets
        #mainWindow.cpuInfo.setStyleSheet("background-color: rgb(100,150,122); margin:1px; border:1px solid rgb(0, 255, 122); ")
        #mainWindow.oGraphButton1.setStyleSheet("background-color: rgb(100,150,122); margin:1px; border:1px solid rgb(0, 255, 122); ")
        #mainWindow.cpu_percent_graph_s.setStyleSheet("background-color: rgb(100,150,122); margin:1px; border:1px solid rgb(0, 255, 122); ")
        #mainWindow.leftContainer.setStyleSheet("background-color: rgb(200,50,122); margin:1px; border:1px solid rgb(0, 255, 122); ")
        #mainWindow.rightContainer.setStyleSheet("background-color: rgb(255,0,0); margin:0px; border:10px solid rgb(0, 255, 0); ")

        #widget resizing
        scrollField.resize(500,1000)
        mainWindow.leftContainer.setMinimumSize(500, 400)
        mainWindow.leftContainer.resize(500, 400)
        mainWindow.rightContainer.resize(500, 400)

        #add widgets
        containerBench.addWidget(mainWindow.leftContainer, 1) #adding widgets to container bench
        #containerBench.addWidget(graphs.DataGraph(graphs.test_fxn, mainWindow))
        containerBench.addWidget(mainWindow.rightContainer, 1)

        #adding widgets to leftside layouts
        mainWindow.dataRow2.addWidget(mainWindow.cpuInfo)   #adding widgets to rows
        mainWindow.dataRow2.addWidget(mainWindow.oGraphButton1)
        mainWindow.dataRow2.addWidget(mainWindow.cpu_percent_graph_s)

        mainWindow.dataRow3.addWidget(mainWindow.cpuFreq)       
        mainWindow.dataRow3.addWidget(mainWindow.oGraphButton2)
        mainWindow.dataRow3.addWidget(mainWindow.cpu_speed_graph_s)

        mainWindow.dataRow4.addWidget(mainWindow.ramInfo)
        mainWindow.dataRow4.addWidget(mainWindow.oGraphButton3)
        mainWindow.dataRow4.addWidget(mainWindow.cpu_ram_graph_s)

        mainWindow.dataRow5.addWidget(mainWindow.swapInfo)
        mainWindow.dataRow5.addWidget(mainWindow.oGraphButton6)
        mainWindow.dataRow5.addWidget(mainWindow.cpu_swap_graph_s)

        mainWindow.dataRow6.addWidget(mainWindow.tempInfo)
        mainWindow.dataRow6.addWidget(mainWindow.oGraphButton4)
        mainWindow.dataRow6.addWidget(Color('purple'))

        mainWindow.dataRow7.addWidget(mainWindow.fanInfo)
        mainWindow.dataRow7.addWidget(mainWindow.oGraphButton5)
        mainWindow.dataRow7.addWidget(Color('purple'))

        #adding widgets to rightside layout
        mainWindow.rightSide.addWidget(mainWindow.cpu_percent_graph)
        mainWindow.rightSide.addWidget(mainWindow.cpu_speed_graph)
        mainWindow.rightSide.addWidget(mainWindow.cpu_ram_graph)
        mainWindow.rightSide.addWidget(mainWindow.cpu_swap_graph)
        mainWindow.rightSide.addWidget(mainWindow.cpu_fan_graph)
        mainWindow.rightSide.addWidget(mainWindow.cpu_temp_graph)
        #add layouts
        leftSide.addLayout(mainWindow.dataRow2, 1)  #Adding rows to leftside display
        leftSide.addLayout(mainWindow.dataRow3, 1)
        leftSide.addLayout(mainWindow.dataRow4, 1)
        leftSide.addLayout(mainWindow.dataRow5, 1)
        #leftSide.addLayout(mainWindow.dataRow6, 1) 
        #leftSide.addLayout(mainWindow.dataRow7, 1)

        #left side of data page scrolling section
        scrollField.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scrollField.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scrollField.setLayout(leftSide)
        #scrollField.setMaximumSize(500, 400)


        return containerBench

    def button_setup(mainWindow):

        #button checkability
        mainWindow.generateButton.setCheckable(True)
        mainWindow.taskButton.setCheckable(True)
        mainWindow.dataButton.setCheckable(True)
        mainWindow.moodButton.setCheckable(True)
        mainWindow.scanButton.setCheckable(True)

        mainWindow.oGraphButton1.setCheckable(True)
        mainWindow.oGraphButton2.setCheckable(True)
        mainWindow.oGraphButton3.setCheckable(True)
        mainWindow.oGraphButton4.setCheckable(True)
        mainWindow.oGraphButton5.setCheckable(True)
        mainWindow.oGraphButton6.setCheckable(True)

        #button checked status
        mainWindow.generateButton.setChecked(False)
        mainWindow.taskButton.setChecked(False)
        mainWindow.dataButton.setChecked(False)
        mainWindow.moodButton.setChecked(True)
        mainWindow.scanButton.setChecked(False)

        mainWindow.oGraphButton1.setChecked(False)
        mainWindow.oGraphButton2.setChecked(False)
        mainWindow.oGraphButton3.setChecked(False)
        mainWindow.oGraphButton4.setChecked(False)
        mainWindow.oGraphButton5.setChecked(False)
        mainWindow.oGraphButton6.setChecked(False)

        #button connections
        mainWindow.generateButton.clicked.connect(mainWindow.generate_list)
        mainWindow.taskButton.clicked.connect(mainWindow.taskButtonPressed)
        mainWindow.taskButton.released.connect(mainWindow.taskButtonReleased)
        mainWindow.dataButton.clicked.connect(mainWindow.dataButtonPressed)
        mainWindow.moodButton.clicked.connect(mainWindow.moodButtonPressed)
        mainWindow.scanButton.clicked.connect(mainWindow.scanButtonPressed)

        mainWindow.oGraphButton1.clicked.connect(mainWindow.oGraphButtonPressed1)
        mainWindow.oGraphButton2.clicked.connect(mainWindow.oGraphButtonPressed2)
        mainWindow.oGraphButton3.clicked.connect(mainWindow.oGraphButtonPressed3)
        mainWindow.oGraphButton4.clicked.connect(mainWindow.oGraphButtonPressed4)
        mainWindow.oGraphButton5.clicked.connect(mainWindow.oGraphButtonPressed5)
        mainWindow.oGraphButton6.clicked.connect(mainWindow.oGraphButtonPressed6)

        #button minimum sizes
        mainWindow.generateButton.setMinimumSize(45, 60)
        mainWindow.taskButton.setMinimumSize(45, 60)
        mainWindow.dataButton.setMinimumSize(45, 60)
        mainWindow.moodButton.setMinimumSize(45, 60)
        mainWindow.scanButton.setMinimumSize(45, 60)

        mainWindow.oGraphButton1.setMinimumSize(45, 60)
        mainWindow.oGraphButton2.setMinimumSize(45, 60)
        mainWindow.oGraphButton3.setMinimumSize(45, 60)
        mainWindow.oGraphButton4.setMinimumSize(45, 60)
        mainWindow.oGraphButton5.setMinimumSize(45, 60)
        mainWindow.oGraphButton6.setMinimumSize(45, 60)

        #button resizing
        mainWindow.generateButton.resize(45, 60)
        mainWindow.taskButton.resize(45, 60)
        mainWindow.dataButton.resize(45, 60)
        mainWindow.moodButton.resize(45, 60)
        mainWindow.scanButton.resize(45, 60)

        mainWindow.oGraphButton1.resize(60, 60)
        mainWindow.oGraphButton2.resize(60, 60)
        mainWindow.oGraphButton3.resize(60, 60)
        mainWindow.oGraphButton4.resize(60, 60)
        mainWindow.oGraphButton5.resize(60, 60)
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

        mainWindow.cpu_percent_graph_s.start_task()
        mainWindow.cpu_speed_graph_s.start_task()
        mainWindow.cpu_ram_graph_s.start_task()
        mainWindow.cpu_swap_graph_s.start_task()
        
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

        mainWindow.scanButton.setChecked(False)
        mainWindow.moodButton.setChecked(False)
        mainWindow.dataButton.setChecked(True)

       # mainWindow.moodButton.setStyleSheet("background-color: rgb(0,255,0); margin:2px; border:1px solid rgb(0, 0, 255); ")
       # mainWindow.scanButton.setStyleSheet("background-color: rgb(0,255,0); margin:2px; border:1px solid rgb(0, 0, 255); ")
       # mainWindow.dataButton.setStyleSheet("background-color: rgb(255,0,0); margin:2px; border:1px solid rgb(0, 255, 0); ")
        return

    def scanButtonPressed(mainWindow):
        # Set the central widget of the Window.
        mainWindow.bottom.setCurrentWidget(mainWindow.scan_display)

        mainWindow.scanButton.setChecked(True)
        mainWindow.moodButton.setChecked(False)
        mainWindow.dataButton.setChecked(False)

        #mainWindow.moodButton.setStyleSheet("background-color: rgb(0,255,0); margin:2px; border:1px solid rgb(0, 0, 255); ")
        #mainWindow.dataButton.setStyleSheet("background-color: rgb(0,255,0); margin:2px; border:1px solid rgb(0, 0, 255); ")
        #mainWindow.scanButton.setStyleSheet("background-color: rgb(255,0,0); margin:2px; border:1px solid rgb(0, 255, 0); ")
        return

    def moodButtonPressed(mainWindow):
        mainWindow.bottom.setCurrentWidget(mainWindow.mood_display)

        mainWindow.scanButton.setChecked(False)
        mainWindow.dataButton.setChecked(False)
        mainWindow.moodButton.setChecked(True)

        #mainWindow.scanButton.setStyleSheet("background-color: rgb(0,255,0); margin:2px; border:1px solid rgb(0, 0, 255); ")
        #mainWindow.dataButton.setStyleSheet("background-color: rgb(0,255,0); margin:2px; border:1px solid rgb(0, 0, 255); ")
        #mainWindow.moodButton.setStyleSheet("background-color: rgb(255,0,0); margin:2px; border:1px solid rgb(0, 255, 0); ")
        return

    def oGraphButtonPressed1(mainWindow):
        mainWindow.rightSide.setCurrentWidget(mainWindow.cpu_percent_graph)
        #state.stat = "CPU Percent"
        mainWindow.oGraphButton2.setChecked(False)
        mainWindow.oGraphButton3.setChecked(False)
        mainWindow.oGraphButton4.setChecked(False)
        mainWindow.oGraphButton5.setChecked(False)
        mainWindow.oGraphButton6.setChecked(False)
        mainWindow.oGraphButton1.setChecked(True)
        return

    def oGraphButtonPressed2(mainWindow):
        mainWindow.rightSide.setCurrentWidget(mainWindow.cpu_speed_graph)
        #state.stat = "CPU Speed"
        mainWindow.oGraphButton1.setChecked(False)
        mainWindow.oGraphButton3.setChecked(False)
        mainWindow.oGraphButton4.setChecked(False)
        mainWindow.oGraphButton5.setChecked(False)
        mainWindow.oGraphButton6.setChecked(False)
        mainWindow.oGraphButton2.setChecked(True)
        return

    def oGraphButtonPressed3(mainWindow):
        mainWindow.rightSide.setCurrentWidget(mainWindow.cpu_ram_graph)
        #state.stat = "RAM"
        mainWindow.oGraphButton1.setChecked(False)
        mainWindow.oGraphButton2.setChecked(False)
        mainWindow.oGraphButton4.setChecked(False)
        mainWindow.oGraphButton5.setChecked(False)
        mainWindow.oGraphButton6.setChecked(False)
        mainWindow.oGraphButton3.setChecked(True)
        return

    def oGraphButtonPressed4(mainWindow):
        mainWindow.rightSide.setCurrentWidget(mainWindow.cpu_fan_graph)
        #state.stat = "CPU Fan"
        mainWindow.oGraphButton1.setChecked(False)
        mainWindow.oGraphButton2.setChecked(False)
        mainWindow.oGraphButton3.setChecked(False)
        mainWindow.oGraphButton5.setChecked(False)
        mainWindow.oGraphButton6.setChecked(False)
        mainWindow.oGraphButton4.setChecked(True)
        return

    def oGraphButtonPressed5(mainWindow):
        mainWindow.rightSide.setCurrentWidget(mainWindow.cpu_temp_graph)
        #state.stat = "CPU Temp"
        mainWindow.oGraphButton1.setChecked(False)
        mainWindow.oGraphButton2.setChecked(False)
        mainWindow.oGraphButton3.setChecked(False)
        mainWindow.oGraphButton4.setChecked(False)
        mainWindow.oGraphButton6.setChecked(False)
        mainWindow.oGraphButton5.setChecked(True)
        return
    
    def oGraphButtonPressed6(mainWindow):
        mainWindow.rightSide.setCurrentWidget(mainWindow.cpu_swap_graph)
        #state.stat = "RAM Swap"
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

            descText = "CPU Percentage out of 100%"
            mainWindow.graphDesc.setText(descText)
            tasks.wait(1000)
        return True
    
    def generate_list(mainWindow):
        state.currentGenre = mainWindow.genreList.currentText()
        print(state.currentGenre)

        print("URI generated!")
        mainWindow.generateButton.setText("Generate New Song")

        #mainWindow.moodRow4.addWidget(mainWindow.playlistDisplay)

        songs = spotify.main()
        
        if(state.songsGenerated == 0):
            mainWindow.songEmbed.setHtml(open("embed.html").read())
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

    # ok so this just WORKS so we don't need to adjust this in how it works
    # the only change that needs to be made is what it calls 
    from modules.tasks import startupTasksTimer
    timer_onStartUp = startupTasksTimer(state.window)
    timer_onStartUp.timeout.connect(lambda: state.window.taskButtonPressed())
    timer_onStartUp.start()


    # Start the event loop.
    app.exec()

    # Your application won't reach here until you exit and the event
    # loop has stopped.
