mainFinished = False
tasksStarted = False
cpudict = {"cpu_percent": 0.0, "cpu_freq": 0.0, "ram_percent": 0.0, "swap_percent": 0.0, "filler": 0.0}
gpudict = {"filler": 0.0}
emotion = "emotion_default"
window = None

def signalTasks():
    global mainFinished
    mainFinished = True
    return True

def signalStarted():
    global tasksStarted
    tasksStarted = True
    return True

