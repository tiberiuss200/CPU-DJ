#import asyncio
import psutil
import json
import modules.state as state
import modules.tasks as tasks
from random import shuffle

#background_tasks = set()
# ^ originally using asyncio, will not work anymore.

#update the CPU dictionary variable
def update_cpu_dict():
    print("Tracking.\n")
    while not state.mainFinished:
        state.cpudict["cpu_percent"] = psutil.cpu_percent()
        freq = psutil.cpu_freq() #(freq.current - freq.min) * 100 / (freq.max - freq.min)
        state.cpudict["cpu_freq"] = freq.current
        state.cpudict["ram_percent"] = psutil.virtual_memory().percent
        state.cpudict["swap_percent"] = psutil.swap_memory().percent

        state.sumdict["cpu_percent"] = state.sumdict["cpu_percent"] + state.cpudict["cpu_percent"]
        state.sumdict["cpu_freq"] = state.sumdict["cpu_freq"] + state.cpudict["cpu_freq"]
        state.sumdict["ram_percent"] = state.sumdict["ram_percent"] + state.cpudict["ram_percent"]
        state.sumdict["swap_percent"] = state.sumdict["swap_percent"] + state.cpudict["swap_percent"]
        state.sumdict["timer"] = state.sumdict["timer"] + 1

        if state.sumdict["timer"] < 3:
            state.mindict["cpu_percent"] = state.cpudict["cpu_percent"]
            state.mindict["cpu_freq"] = state.cpudict["cpu_freq"]
            state.mindict["ram_percent"] = state.cpudict["ram_percent"]
            state.mindict["swap_percent"] = state.cpudict["swap_percent"]
        else:
            if (state.mindict["cpu_percent"] > state.cpudict["cpu_percent"]):
                state.mindict["cpu_percent"] = state.cpudict["cpu_percent"]
            if (state.maxdict["cpu_percent"] < state.cpudict["cpu_percent"]):
                state.maxdict["cpu_percent"] = state.cpudict["cpu_percent"]
            
            if (state.mindict["cpu_freq"] > state.cpudict["cpu_freq"]):
                state.mindict["cpu_freq"] = state.cpudict["cpu_freq"]
            if (state.maxdict["cpu_freq"] < state.cpudict["cpu_freq"]):
                state.maxdict["cpu_freq"] = state.cpudict["cpu_freq"]

            if (state.mindict["ram_percent"] > state.cpudict["ram_percent"]):
                state.mindict["ram_percent"] = state.cpudict["ram_percent"]
            if (state.maxdict["ram_percent"] < state.cpudict["ram_percent"]):
                state.maxdict["ram_percent"] = state.cpudict["ram_percent"]
            
            if (state.mindict["swap_percent"] > state.cpudict["swap_percent"]):
                state.mindict["swap_percent"] = state.cpudict["swap_percent"]
            if (state.maxdict["swap_percent"] < state.cpudict["swap_percent"]):
                state.maxdict["swap_percent"] = state.cpudict["swap_percent"]

        if state.current_os == state.CONST_OS.LINUX:
            state.cpudict["fan_speed"] = psutil.sensors_fans()
            state.cpudict["temps"] = psutil.sensors_temperatures()

        state.cpudict["battery_info"] = psutil.sensors_battery()

        tasks.wait(1000)
    print("Update CPU dictionaries task ended.")
    return True

def mood_vals_determine():
    # oh boy here we go
    print("Mooding.\n")
    rolls = [state.CONST_STATS.CPU_VALUE, state.CONST_STATS.CPU_FREQ, state.CONST_STATS.RAM_PERC, state.CONST_STATS.SWAP_PERC]
    shuffle(rolls)
    state.random_rolls[state.CONST_EMOTE.HAPPY] = rolls[0]
    state.random_rolls[state.CONST_EMOTE.SAD] = rolls[1]
    state.random_rolls[state.CONST_EMOTE.SURPRISE] = rolls[2]
    state.random_rolls[state.CONST_EMOTE.ANGER] = rolls[3]
    print(state.random_rolls)

    while not state.mainFinished:
        state.emotion_dict[state.CONST_EMOTE.HAPPY] = state.clamp((state.avg_stat_value(state.random_rolls[state.CONST_EMOTE.HAPPY]) - state.cpudict[state.random_rolls[state.CONST_EMOTE.HAPPY]])*3, 0, 100)
        state.emotion_dict[state.CONST_EMOTE.SAD] = state.clamp(100 / (state.range_stat_value(state.random_rolls[state.CONST_EMOTE.SAD]) + 1), 0, 100)
        state.emotion_dict[state.CONST_EMOTE.SURPRISE] = (abs(state.perc_range_stat_value(state.random_rolls[state.CONST_EMOTE.SURPRISE]) - 50) / 5) ** 2
        state.emotion_dict[state.CONST_EMOTE.ANGER] = state.clamp( (state.avg_stat_value(state.random_rolls[state.CONST_EMOTE.ANGER]) * state.perc_range_stat_value(state.random_rolls[state.CONST_EMOTE.ANGER])) / (max(200 - state.timer_val(),90)), 0, 100) 

        #state.spotify_dict
        tasks.wait(1000)
    return True
    


def print_dict():
    print("[debug] Print task started.")
    tasks.wait(5000)
    while not state.mainFinished:
        prettyPrint = json.dumps(state.cpudict)
        print(prettyPrint)
        prettyPrint = json.dumps(state.emotion_dict)
        print(prettyPrint)
        tasks.wait(1000)
    print("End.")
    return True
    #end

def prep_tasks(window):
    #test
    tasks.start(update_cpu_dict)
    tasks.start(mood_vals_determine)
    if (state.debugMode):
        tasks.start(print_dict)
    
    state.signalStarted()

    
    #that's it!  ez






#eof
