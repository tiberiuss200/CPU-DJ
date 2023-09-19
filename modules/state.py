from asyncio import get_event_loop

mainFinished = False
tasksStarted = False
cpudict = {"cpu_percent": 0.0, "filler": 0.0}
gpudict = {"filler": 0.0}
emotion = "emotion_default"
background_tasks = get_event_loop()

pageSelect = 0;

def signalTasks():
    global mainFinished
    mainFinished = True
    return True

def signalStarted():
    global tasksStarted
    tasksStarted = True
    return True

