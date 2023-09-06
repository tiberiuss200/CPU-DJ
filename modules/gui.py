import tkinter as tk

window = tk.Tk()

def main():
    greeting = tk.Label(text="Hello, tkinter")
    greeting.pack()

    window.mainloop()

if __name__ == "__main__":
    main()