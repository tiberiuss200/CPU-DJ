from asyncio import get_event_loop

# CPU info storage
cpudict = {"cpu_percent": 0.0, "filler": 0.0}
# GPU info storage
gpudict = {"filler": 0.0}
# the current read emotion
emotion = "emotion_default"
# the event loop for asyncio
background_tasks = get_event_loop()
# debug flag
debug = True

