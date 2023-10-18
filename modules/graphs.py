#from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
#import state as state
import psutil



def main():
    graph()


def graph():
    ax.clear()
    x = np.linspace(0.0, 10.0, 100)
    y = psutil.cpu_percent()
    ax.plot(x, y)

fig, ax = plt.subplots()

if __name__ == "__main__":
    main()