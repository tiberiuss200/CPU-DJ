import platform
from enum import Enum

class CONST_OS(str, Enum):
    WIN = "Windows"
    MAC = "Darwin"
    LINUX = "Linux"

class CONST_STATS(str, Enum):
    CPU_VALUE = "cpu_percent"
    CPU_FREQ = "cpu_freq"
    RAM_PERC = "ram_percent"
    SWAP_PERC = "swap_percent"
    FAN_SPEED = "fan_speed"
    TEMPS = "temp_sensor"
    BATTERY = "battery_info"

class CONST_EMOTE(str, Enum):
    HAPPY = "happy"
    SAD = "sad"
    ANGER = "anger"
    SURPRISE = "surprise"

class CONST_EMOTE_TEXT(str, Enum):
    PLACEHOLDER = "emotion_default"
    HAPPY = "Happy."
    SAD = "Sad."
    ANGRY = "Angry."
    SURPRISED = "Surprised."
    STRESSED = "Stressed."
    NEUTRAL = "Aight."

mainFinished = False
tasksStarted = False
debugMode = True
cpudict = {"cpu_percent": 0.0, "cpu_freq": 0.0, "ram_percent": 0.0, "swap_percent": 0.0, "fan_speed": None, "temp_sensor": None, "battery_info": None, "filler": 0.0}
gpudict = {"filler": 0.0}
current_emotion = "emotion_default"
emotion_dict = {'happy': 0.0, "sad": 0.0, "anger": 0.0, "surprise": 0.0}
window = None
genreList = ["acoustic", "afrobeat", "alt-rock", "alternative", "ambient", "anime", "black-metal", "bluegrass", "blues", "bossanova", "brazil", "breakbeat", "british", "cantopop", "chicago-house", "children", "chill", "classical", "club", "comedy", "country", "dance", "dancehall", "death-metal", "deep-house", "detroit-techno", "disco", "disney", "drum-and-bass", "dub", "dubstep", "edm", "electro", "electronic", "emo", "folk", "forro", "french", "funk", "garage", "german", "gospel", "goth", "grindcore", "groove", "grunge", "guitar", "happy", "hard-rock", "hardcore", "hardstyle", "heavy-metal", "hip-hop", "holidays", "honky-tonk", "house", "idm", "indian", "indie", "indie-pop", "industrial", "iranian", "j-dance", "j-idol", "j-pop", "j-rock", "jazz", "k-pop", "kids", "latin", "latino", "malay", "mandopop", "metal", "metal-misc", "metalcore", "minimal-techno", "movies", "mpb", "new-age", "new-release", "opera", "pagode", "party", "philippines-opm", "piano", "pop", "pop-film", "post-dubstep", "power-pop", "progressive-house", "psych-rock", "punk", "punk-rock", "r-n-b", "rainy-day", "reggae", "reggaeton", "road-trip", "rock", "rock-n-roll", "rockabilly", "romance", "sad", "salsa", "samba", "sertanejo", "show-tunes", "singer-songwriter", "ska", "sleep", "songwriter", "soul", "soundtracks", "spanish", "study", "summer", "swedish", "synth-pop", "tango", "techno", "trance", "trip-hop", "turkish", "work-out", "world-music"]
currentGenre = "iranian"
songsGenerated = 0

current_os = platform.system()

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
    
    return current_emotion

def signalTasks():
    global mainFinished
    mainFinished = True
    return True

def signalStarted():
    global tasksStarted
    tasksStarted = True
    return True

