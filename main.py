import modules.processing as processing
import modules.gui as gui
import modules.spotify as spotify
import modules.state as state

#background_tasks = set()

# async def gui_start():
    
#     state.mainFinished = True
#     #blank

# async def app_start():
#     while not gui.app.startingUp():
#         await asyncio.sleep(1)
#     state.mainStarted = True

# async def main():
#     gui_task = asyncio.create_task(gui_start())
#     background_tasks.add(gui_task)

#     while not state.mainFinished:
#         await asyncio.sleep(1)
#     stop_signal = False
#     await asyncio.sleep(3)

# asyncio.run(main())