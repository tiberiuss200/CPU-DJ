import asyncio
import psutil
import json
import modules.state as state

def main_setup():
    cpu_task = state.background_tasks.create_task(update_cpu_dict(state.cpudict))
    #gpu_task = asyncio.create_task(update_gpu_dict(gpudict))
    debug_task = state.background_tasks.create_task(print_dict(state.cpudict))
    #await gpu_task
    waitUntilFinished = state.background_tasks.create_task(waitFinish())

#update the CPU dictionary variable
async def update_cpu_dict(cpudict):
    print("Tracking.")
    while not state.mainFinished:
        cpudict["cpu_percent"] = psutil.cpu_percent()
        await asyncio.sleep(1)
    print("Update CPU dictionaries task ended.")

async def waitFinish():
    while not state.mainFinished:
        await asyncio.sleep(1)
    stop_signal = False
    await asyncio.sleep(3)

async def print_dict(cpudict):
    if (not state.debug):
        print("Debug flag off.")
        return
    print("Starting.")
    await asyncio.sleep(5)
    while not state.mainFinished:
        prettyPrint = json.dumps(cpudict)
        print(prettyPrint)
        await asyncio.sleep(1)
    print("End.")
    #end


#eof