import platform
from enum import Enum

mainFinished = False
tasksStarted = False
cpudict = {"cpu_percent": 0.0, "cpu_freq": 0.0, "ram_percent": 0.0, "swap_percent": 0.0, "fan_speed": None, "temps": None, "battery_info": None, "filler": 0.0}
gpudict = {"filler": 0.0}
current_emotion = "emotion_default"
emotion_dict = {"happy": 0.0, "sad": 0.0, "anger": 0.0, "surprise": 0.0}
window = None
current_os = platform.system()

class CONST_OS(Enum):
    WIN = "Windows"
    MAC = "Darwin"
    LINUX = "Linux"

class CONST_EMOTE(Enum):
    HAPPY = "happy"
    SAD = "sad"
    ANGER = "anger"
    SURPRISE = "surprise"

class CONST_EMOTE_TEXT(Enum):
    PLACEHOLDER = "emotion_default"
    HAPPY = "Happy."
    SAD = "Sad."
    ANGRY = "Angry."
    SURPRISED = "Surprised."
    STRESSED = "Stressed."
    NEUTRAL = "Aight."

def determine_emotion():
    if (cpudict["cpu_percent"] > 80.0):
        current_emotion = CONST_EMOTE_TEXT.STRESSED
    
    #defaults
    if emotion_dict[CONST_EMOTE.HAPPY] > (emotion_dict[CONST_EMOTE.SAD] + emotion_dict[CONST_EMOTE.ANGER] + emotion_dict[CONST_EMOTE.SURPRISE]):
        current_emotion = CONST_EMOTE_TEXT.HAPPY
    elif emotion_dict[CONST_EMOTE.SAD] > (emotion_dict[CONST_EMOTE.HAPPY] + emotion_dict[CONST_EMOTE.ANGER] + emotion_dict[CONST_EMOTE.SURPRISE]):
        current_emotion = CONST_EMOTE_TEXT.SAD
    elif emotion_dict[CONST_EMOTE.ANGER] > (emotion_dict[CONST_EMOTE.SAD] + emotion_dict[CONST_EMOTE.HAPPY] + emotion_dict[CONST_EMOTE.SURPRISE]):
        current_emotion = CONST_EMOTE_TEXT.ANGRY
    elif emotion_dict[CONST_EMOTE.SURPRISE] > (emotion_dict[CONST_EMOTE.SAD] + emotion_dict[CONST_EMOTE.ANGER] + emotion_dict[CONST_EMOTE.HAPPY]):
        current_emotion = CONST_EMOTE_TEXT.SURPRISED
    else:
        current_emotion = CONST_EMOTE_TEXT.NEUTRAL

def signalTasks():
    global mainFinished
    mainFinished = True
    return True

def signalStarted():
    global tasksStarted
    tasksStarted = True
    return True

