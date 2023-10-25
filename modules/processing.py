#import asyncio
import psutil
import json
import modules.state as state
import modules.tasks as tasks

#background_tasks = set()
# ^ originally using asyncio, will not work anymore.

#update the CPU dictionary variable
def update_cpu_dict():
    print("Tracking.")
    while not state.mainFinished:
        state.cpudict["cpu_percent"] = psutil.cpu_percent()
        freq = psutil.cpu_freq() #(freq.current - freq.min) * 100 / (freq.max - freq.min)
        state.cpudict["cpu_freq"] = freq.current
        state.cpudict["ram_percent"] = psutil.virtual_memory().percent
        state.cpudict["swap_percent"] = psutil.swap_memory().percent

        if state.current_os == state.CONST_OS.LINUX:
            state.cpudict["fan_speed"] = psutil.sensors_fans()
            state.cpudict["temps"] = psutil.sensors_temperatures()

        state.cpudict["battery_info"] = psutil.sensors_battery()

        tasks.wait(1000)
    print("Update CPU dictionaries task ended.")
    return True


def print_dict():
    print("[debug] Print task started.")
    tasks.wait(5000)
    while not state.mainFinished:
        prettyPrint = json.dumps(state.cpudict)
        print(prettyPrint)
        tasks.wait(1000)
    print("End.")
    return True
    #end

def prep_tasks(window):
    #test
    tasks.start(update_cpu_dict)
    if (state.debugMode):
        tasks.start(print_dict)
    
    state.signalStarted()

    
    #that's it!  ez






#eof
