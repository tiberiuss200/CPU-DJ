from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


#def main():
#    graph()

root = Tk()


fig, ax = plt.subplots()

frame = Frame(root)
frame.pack()

canvas = FigureCanvasTkAgg(fig, master = frame)
canvas.get_tk_widget().pack()

root.mainloop()

#if __name__ == "__main__":
#    main()