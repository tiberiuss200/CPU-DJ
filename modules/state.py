import platform
from enum import Enum

mainFinished = False
tasksStarted = False
cpudict = {"cpu_percent": 0.0, "cpu_freq": 0.0, "ram_percent": 0.0, "swap_percent": 0.0, "fan_speed": None, "temps": None, "battery_info": None, "filler": 0.0}
gpudict = {"filler": 0.0}
emotion = "emotion_default"
window = None
current_os = platform.system()

class CONST_OS(Enum):
    WIN = "Windows"
    MAC = "Darwin"
    LINUX = "Linux"    

def signalTasks():
    global mainFinished
    mainFinished = True
    return True

def signalStarted():
    global tasksStarted
    tasksStarted = True
    return True

