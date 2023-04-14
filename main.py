import modules.processing
import modules.gui
import modules.spotify
import asyncio

cpudict = {"cpu_percent": 0.0, "filler": 0.0}
gpudict = {"filler": 0.0}
asyncio.run(modules.processing.main_setup(cpudict, gpudict))