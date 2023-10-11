import tkinter as tk
import tkinter.ttk as ttk
import asyncio
import modules.state as state
from modules.state import window
import tkinterweb as tkw
from os import getcwd

w_width = 700
w_height = 700
pageList = ['page1', 'page2', 'page3']

def setup():
    #greeting = tk.Label(text="Hello, tkinter")
    #greeting.pack()
    
    window.title("CPU-DJ")
    window.geometry('{}x{}'.format(w_width, w_height))

    container = tk.Frame(window, width = w_width, height = 0)
    
    window.columnconfigure(0, weight=1)
    window.rowconfigure(1, weight=1)

    #button example + lambda
    #halfLife = lambda: setup_topFrame(topFrame)
    
    #button = tk.Button(text="Test Button", command=halfLife)

    container.grid(           row = 0, column = 0, sticky = "ew")
    setup_container(container)

    #taskWindow = state.background_tasks.create_task(notTkMainloop(window, 1/120))

# Top Frame: 
# Title, with a bench of buttons enabling other things.  This can be mostly blank as long as we are matching prototype.

def setup_container(frame: tk.Frame):

    page1 = tk.Frame(window, width = w_width, height = 0)
    display_page1(page1)
    page1.grid(row = 1, column = 0, sticky = "ew")

    page2 = tk.Frame(window, width = w_width, height = 0)
    display_page2(page2)
    page2.grid(row = 1, column = 0, sticky = "ew")
    page2.grid_remove()

    page3 = tk.Frame(window, width = w_width, height = 0)
    display_page3(page3)
    page3.grid(row = 1, column = 0, sticky = "ew")
    page3.grid_remove()

    pageList = [page1, page2, page3]

    topFrame = tk.Frame(window, width = w_width, height = 0)
    setup_topFrame(topFrame, window, pageList)
    topFrame.grid(            row = 0, column = 0, sticky = "ew")

def setup_topFrame(frame: tk.Frame, window, pageList):
    titleLabel = tk.Label(frame, text="CPU-DJ")
    titleLabel.grid(row = 0, column = 0)
    button1 = tk.Button(frame, text = 'Page 1', command = lambda: change_page(window, pageList, 0))
    button1.grid(row = 0, column =1)
    button2 = tk.Button(frame, text = 'Page 2', command = lambda: change_page(window, pageList, 1))
    button2.grid(row = 0, column =2)
    button3 = tk.Button(frame, text = 'Page 3', command = lambda: change_page(window, pageList, 2))
    button3.grid(row = 0, column =3)

def change_page(window: tk.Frame, pageList, num):
    if (state.pageSelect == num):
        return
    if (num == 0):
        state.pageSelect = num
        pageList[0].grid()
        pageList[1].grid_remove()
        pageList[2].grid_remove()
        print("page 1")
        return
    if (num == 1):
        state.pageSelect = num
        pageList[0].grid_remove()
        pageList[1].grid()
        pageList[2].grid_remove()
        print("page 2")
        return
    if (num == 2):
        state.pageSelect = num
        pageList[0].grid_remove()
        pageList[1].grid_remove()
        pageList[2].grid()
        print("page 3")
        return
    else:
        return

def display_page1(frame: tk.Frame):

    f_row1 = tk.Frame(frame, width = w_width, height = 200)
    f_row2 = tk.Frame(frame, width = w_width, height = 200)
    f_row3 = tk.Frame(frame, width = w_width, height = 200)
    f_row4 = tk.Frame(frame, width = w_width, height = 200)

    f_row1.grid(row = 1, column = 0, sticky = "ew")
    f_row2.grid(row = 2, column = 0, sticky = "ew")
    f_row3.grid(row = 3, column = 0, sticky = "ew")
    f_row4.grid(row = 4, column = 0, sticky = "ew")

    page1_row1(f_row1)
    page1_row3(f_row3)


def display_page2(frame: tk.Frame):
    titleLabel = tk.Label(frame, text="Page 2")
    titleLabel.grid(row = 0, column = 0)

def display_page3(frame: tk.Frame):
    titleLabel = tk.Label(frame, text="Page 3")
    titleLabel.grid(row = 0, column = 0)

# Row 1:
# Left side: emotion block.
# Right side: basic information block
def page1_row1(row1: tk.Frame):
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
def page1_row3(row3: tk.Frame):
    #labeltemp = tk.Label(row3, text="We need a new webview library...")
    #labeltemp.grid(row = 0, column = 0)
    url = "file:///" + getcwd() + "\embed.html"
    url = url.replace('\\', '/')
    spotifyframe = tkw.HtmlFrame(row3, messages_enabled=False)
    spotifyframe.load_file(url)
    spotifyframe.grid(row = 0, column = 0)


# for tasks to work and while not using Qt's absurd task management...nonsense
# we have to replace tk's mainloop for anything asynchronous to work
# - Dan

# lol nvm -Dan

#async def notTkMainloop(window: tk.Tk, interval: float):
#    window.update()
#    await asyncio.sleep(interval)
#    isActive = True
#
#    while isActive:
#        window.update()
#        try:
#            isActive = window.winfo_exists()
#        except:
#            isActive = False
#        await asyncio.sleep(interval)
#        
#    state.background_tasks.stop()
    # no need for close statement
    
if __name__ == "__main__":
    pageSelect = 0
    setup()