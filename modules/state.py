mainFinished = False
mainStarted = False
cpudict = {"cpu_percent": 0.0, "filler": 0.0}
gpudict = {"filler": 0.0}

def signalTasks():
    global mainFinished
    mainFinished = True

