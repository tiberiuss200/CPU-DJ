from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
#import state as state
import psutil



#def main():
#    graph()

root = Tk()


def graph():

    x = np.linspace(0, 10, 100)
    y = psutil.cpu_percent()
    ax.plot(x, y)

    canvas.draw()




fig, ax = plt.subplots()
frame = Frame(root)

canvas = FigureCanvasTkAgg(fig, master = frame)
canvas.get_tk_widget().pack()

frame.pack()


button=Button(root, text="Graph", command=graph)
button.pack()

root.mainloop()

#if __name__ == "__main__":
#    main()