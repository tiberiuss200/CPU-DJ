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
        tasks.wait(1000)
    print("Update CPU dictionaries task ended.")
    return True


def print_dict():
    print("Starting.")
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
    tasks.start(print_dict)
    state.signalStarted()

    
    #that's it!  ez






#eof
