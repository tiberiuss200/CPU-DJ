import traceback
import time
from PyQt6.QtCore import (Q_ARG, QMetaObject, QMutex, QMutexLocker, QObject,
                          QRunnable, Qt, QThreadPool, pyqtSignal, pyqtSlot, QTimer)
import modules.state as state

# unabashedly using this as a base
# https://github.com/mochisue/pyqt-async-sample/blob/main/src/sample.py
# it's really useful for learning this
# while not identical, a good chunk of code is lifted from it

class TaskSignal(QObject):
    finish = pyqtSignal()
    error = pyqtSignal(str)
    result = pyqtSignal(object)

class Task(QRunnable):
    def __init__(self, fn_run: callable, *args, **kwargs):
        # inheritance from QRunnable
        super(Task, self).__init__()
        self.fn_run = fn_run
        self.args = args
        self.kwargs = kwargs
        self.signals = TaskSignal()
        self.mutex = QMutex()
        self.is_stop = False
    
    # directly lifted from the sample
    # runs a thread and handles the individual signals using a simple try-catch block
    @pyqtSlot()
    def run(self):
        try:
            with QMutexLocker(self.mutex):
                self.is_stop = False
            result = self.fn_run(*self.args, **self.kwargs)
        except:
            self.signals.error.emit(traceback.format_exc())
        else:
            #self.signals.result.emit(result)
            #vestigial?
            temp = True
        finally:
            #self.signals.finish.emit()
            #vestigial
            temp = True

    def stop(self):
        with QMutexLocker(self.mutex):
            self.is_stop = True
    
# that's where the class ends but I think it would be worthwhile to provide helper functions within the class itself, so I'll provide some simple ones

# lifting my wait syntax from Danmakufu stuff, but instead of using frames as the time reference, I'm using milliseconds
# for reference, the minimum time gap needed for processing.py is somewhere in the range of 100 milliseconds per psutil access.  I use 1000 in my examples to be safe.
def wait(msec):
    time.sleep(msec / 1000)

# default signal handler functions
# might be needed depending on your task
def finish_default():
    print("task finish")
    return True

def error_default(message):
    print(message)
    return True

def result_default():
    print("task result")
    return True

# note to Ty:
# gui.py will need something implemented akin to this in the sample:
# self.thread_pool = QThreadPool()
# self.thread_pool.setMaxThreadCount(10)
# this max thread count is arbitrary, we should adjust it as needed
# this goes in the __init__ function.  i don't want to mess with it unless we can be in call or the same room, but just to let you know
# edit: never mind no merge conflicts we ball.  but we should separate the GUI stuff into its own function at least.

# GUESS WHO CREATED A FUNCTION DEDICATED TO STARTING TASKS AS IF THEY ARE COROUTINES BUT ACTUALLY THREADS!!  THIS GUY!!
# It's pretty easy to use, check processing.py in prep_tasks for an example.

def start(fxn_thread, *args, **kwargs):
    # window in gui.py is literally just called window.  circular imports stopped this from being awesome...
    # from modules.gui import window
    handle_finish=finish_default
    handle_error=error_default
    handle_result=result_default
    window = state.window

    workerObj = None
    if window.thread_pool.activeThreadCount() < window.thread_pool.maxThreadCount():
        workerObj = Task(fxn_thread, *args, **kwargs)
        workerObj.window = window
        window.stopWorkers.connect(workerObj.stop)
        workerObj.signals.finish.connect(handle_finish)
        workerObj.signals.error.connect(handle_error)
        workerObj.signals.result.connect(handle_result)
        window.thread_pool.start(workerObj)
    return workerObj

# need some kind of function to signal to app when things have started...
def startupTasksTimer(window):
    timer_onStartUp = QTimer(window)
    timer_onStartUp.setSingleShot(True)
    timer_onStartUp.setInterval(0)
    return timer_onStartUp

def finishScanTimer(window):
    timer_finishScan = QTimer(window)
    timer_finishScan.setSingleShot(True)
    timer_finishScan.setInterval(state.SCAN_LENGTH * 1000 + 2000)
    return timer_finishScan

#eof


