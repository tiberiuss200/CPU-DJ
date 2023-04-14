import asyncio
import psutil

#update the CPU dictionary variable
async def update_cpu_dict(cpudict):
    while True:
        cpudict["cpu_percent"] = psutil.cpu_percent()
        await asyncio.sleep(1)
    print("Update CPU dictionaries task ended.")

async def main_setup(cpudict, gpudict):
    cpu_task = asyncio.create_task(update_cpu_dict(cpudict))
    #gpu_task = asyncio.create_task(update_gpu_dict(gpudict))
    debug_task = asyncio.create_task(print_dict(cpudict))
    await debug_task
    await cpu_task
    #await gpu_task

async def print_dict(cpudict):
    while True:
        print(cpudict)
        await asyncio.sleep(1)
    #end

#eof