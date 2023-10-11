from tkinter import *
import matplotlib.pyplot as plt
import numpy as np


root = Tk()
root.geometry("600x300")

def graph():
    hardwareValues = np.random.normal(15, 5, 50)
    plt.hist(hardwareValues, 4)
    plt.show()

button = Button(root, text="Graph", command=graph)
button.pack()
root.mainloop()