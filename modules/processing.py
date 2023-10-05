import asyncio
import psutil
import json
import modules.state as state

def main_setup():
    #cpu_task = state.background_tasks.create_task(update_cpu_dict(state.cpudict))
    #gpu_task = asyncio.create_task(update_gpu_dict(gpudict))
    #debug_task = state.background_tasks.create_task(print_dict(state.cpudict))
    #await gpu_task
    #waitUntilFinished = state.background_tasks.create_task(waitFinish())
    update_cpu_dict()
    print_dict()

#update the CPU dictionary variable
def update_cpu_dict():
    def task():
         state.cpudict["cpu_percent"] = psutil.cpu_percent()
         state.wait(1000, lambda: task())

    print("Tracking.")
    task()

    
   
    #print("Update CPU dictionaries task ended.")

#async def waitFinish():
#    while True:
#        await asyncio.sleep(1)
    #stop_signal = False
#    await asyncio.sleep(3)

def print_dict():
    def task():
        prettyPrint = json.dumps(state.cpudict)
        print(prettyPrint)
        state.wait(1000, lambda: task())
    
    if (not state.debug):
        print("Debug flag off.")
        return
    print("Starting.")
    state.wait(2000, lambda: task())

    

    #print("End.")


#eof