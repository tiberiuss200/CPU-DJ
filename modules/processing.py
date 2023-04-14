import asyncio
import psutil

stop_signal = False

#update the CPU dictionary variable
async def update_cpu_dict(cpudict):
    while ~stop_signal:
        cpudict["cpu_percent"] = psutil.cpu_percent()
        await asyncio.sleep(1)
    print("Update CPU dictionaries task ended.")

async def main_setup(cpudict, gpudict):
    #cpu_task = asyncio.create_task()
    #gpu_task = asyncio.create_task(update_gpu_dict(gpudict))
    #debug_task = asyncio.create_task()
    await update_cpu_dict(cpudict)
    await print_dict(cpudict)
    #await gpu_task

async def print_dict(cpudict):
    await asyncio.sleep(5)
    while ~stop_signal:
        print(cpudict)
        await asyncio.sleep(1)
    #end



#eof