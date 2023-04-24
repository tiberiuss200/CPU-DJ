import asyncio
import psutil
import json
import modules.state as state

cpudict = {"cpu_percent": 0.0, "filler": 0.0}
gpudict = {"filler": 0.0}
background_tasks = set()

#update the CPU dictionary variable
async def update_cpu_dict(cpudict):
    print("Tracking.")
    while not state.mainFinished:
        cpudict["cpu_percent"] = psutil.cpu_percent()
        await asyncio.sleep(1)
    print("Update CPU dictionaries task ended.")




async def print_dict(cpudict):
    print("Starting.")
    await asyncio.sleep(5)
    while not state.mainFinished:
        prettyPrint = json.dumps(cpudict)
        print(prettyPrint)
        await asyncio.sleep(1)
    print("End.")
    #end

#eof