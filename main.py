import modules.processing as processing
import modules.gui as gui
import modules.state as state

# maybe main can be the shell after all!
def main():
    processing.main_setup()
    gui.setup()
    state.window.mainloop()
    #state.background_tasks.run_forever()

if __name__ == "__main__":
    main()