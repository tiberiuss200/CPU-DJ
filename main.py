import modules.processing as processing
import modules.gui as gui
import modules.spotify as spotify
import asyncio
import modules.state as state

background_tasks = set()

async def gui_start():
    gui.app.exec()
    #state.mainFinished = True
    #blank

async def main():
    cpu_task = asyncio.create_task(processing.update_cpu_dict(processing.cpudict))
    #gpu_task = asyncio.create_task(update_gpu_dict(gpudict))
    debug_task = asyncio.create_task(processing.print_dict(processing.cpudict))

    gui_task = asyncio.create_task(gui_start())
    #await gpu_task

    #Processing tasks
    background_tasks.add(cpu_task)
    background_tasks.add(debug_task)

    #GUI tasks
    background_tasks.add(gui_task)

    while not state.mainFinished:
        await asyncio.sleep(1)
    #stop_signal = False
    await asyncio.sleep(3)

asyncio.run(main())