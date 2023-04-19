import asyncio
import psutil
import json
import state

stop_signal = True
cpudict = {"cpu_percent": 0.0, "filler": 0.0}
gpudict = {"filler": 0.0}
background_tasks = set()

#update the CPU dictionary variable
async def update_cpu_dict(cpudict):
    print("Tracking.")
    while stop_signal:
        cpudict["cpu_percent"] = psutil.cpu_percent()
        await asyncio.sleep(1)
    print("Update CPU dictionaries task ended.")

async def main_setup(cpudict, gpudict):
    cpu_task = asyncio.create_task(update_cpu_dict(cpudict))
    #gpu_task = asyncio.create_task(update_gpu_dict(gpudict))
    debug_task = asyncio.create_task(print_dict(cpudict))
    #await gpu_task
    background_tasks.add(cpu_task)
    background_tasks.add(debug_task)
    while not state.mainFinished:
        await asyncio.sleep(1)
    stop_signal = False
    await asyncio.sleep(3)


async def print_dict(cpudict):
    print("Starting.")
    await asyncio.sleep(5)
    while stop_signal:
        prettyPrint = json.dumps(cpudict)
        print(prettyPrint)
        await asyncio.sleep(1)
    print("End.")
    #end

asyncio.run(main_setup(cpudict, gpudict))

#eof