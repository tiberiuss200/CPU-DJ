import tkinter as tk
import tkinter.ttk as ttk
import asyncio
import modules.state as state

window = tk.Tk()
w_width = 700
w_height = 700

def setup():
    #greeting = tk.Label(text="Hello, tkinter")
    #greeting.pack()
    
    window.title("CPU-DJ")
    window.geometry('{}x{}'.format(w_width, w_height))

    topFrame = tk.Frame(window, width = w_width, height = 100)
    f_row1 = tk.Frame(window, width = w_width, height = 200)
    f_row2 = tk.Frame(window, width = w_width, height = 200)
    f_row3 = tk.Frame(window, width = w_width, height = 200)
    f_row4 = tk.Frame(window, width = w_width, height = 200)

    window.columnconfigure(0, weight=1)
    window.rowconfigure(1, weight=1)

    #button example + lambda
    #halfLife = lambda: setup_topFrame(topFrame)
    #button = tk.Button(text="Test Button", command=halfLife)

    topFrame.grid(row = 0, column = 0, sticky = "ew")
    f_row1.grid(row = 1, column = 0, sticky = "ew")
    f_row2.grid(row = 2, column = 0, sticky = "ew")
    f_row3.grid(row = 3, column = 0, sticky = "ew")
    f_row4.grid(row = 4, column = 0, sticky = "ew")
    
    setup_topFrame(topFrame)
    setup_row1(f_row1)
    setup_row3(f_row3)

    #window.mainloop()
    taskWindow = state.background_tasks.create_task(notTkMainloop(window, 1/120))

# Top Frame: 
# Title, with a bench of buttons enabling other things.  This can be mostly blank as long as we are matching prototype.
def setup_topFrame(frame: tk.Frame):
    titleLabel = tk.Label(frame, text="CPU-DJ")
    titleLabel.grid(row = 0, column = 0)

# Row 1:
# Left side: emotion block.
# Right side: basic information block
def setup_row1(row1: tk.Frame):
    row1.columnconfigure(1, weight=1)
    row1.rowconfigure(1, weight=1)

    e_label1 = tk.Label(row1, text = "Your computer is ...", justify=tk.LEFT)
    # further here?

    e_label1.grid(row = 0, column = 0)

    i_label1 = tk.Label(row1, text="CPU Temperature: ", justify=tk.LEFT)
    # further here?

    i_label1.grid(row = 0, column = 1)


# Row 2:
# Currently blank?  I forgot what we were putting here.


# Row 3:
# Spotify view.
def setup_row3(row3: tk.Frame):
    labeltemp = tk.Label(row3, text="We need a new webview library...")
    labeltemp.grid(row = 0, column = 0)
    #we need a new web view library...
    #spotifyview = webview.create_window()

# for tasks to work and while not using Qt's absurd task management...nonsense
# we have to replace tk's mainloop for anything asynchronous to work
# - Dan
async def notTkMainloop(window: tk.Tk, interval: float):
    window.update()
    await asyncio.sleep(interval)
    isActive = True

    while isActive:
        window.update()
        try:
            isActive = window.winfo_exists()
        except:
            isActive = False
        await asyncio.sleep(interval)
        
    state.background_tasks.stop()
    # no need for close statement
    

if __name__ == "__main__":
    setup()