"""
This program is going to double as an installer AND a way to simply start the Python main.py module.
If it's not already installed, it runs a first-time setup before booting.  Otherwise, it skips to running the program
Install script written by Daniel Oravetz
CPU-DJ written by Daniel Oravetz, R-E Miller, Tiberius Shaub, and Nathaniel Harris
"""

from venv import create as create_venv
#from virtualenv import cli_run as create_venv
#import ensurepip
from os.path import join, exists
import sys
import os
import io
import subprocess
from subprocess import PIPE
import platform
from multiprocessing import freeze_support

def getcwd():
    ret = ""
    if getattr(sys, 'frozen', False):
        ret = os.path.dirname(sys.executable)
    elif __file__:
        ret = os.getcwd()
    return ret

def get_venv_bin_folder():
    # I hate platform specific code.......
    ret = ""
    if(platform.system() == "Windows"):
        ret = "Scripts"
    else:
        ret = "bin"
    return ret

def get_requirements_txt():
    ret = ""
    if (platform.system() == "Windows"):
        ret = "require_win.txt"
    elif (platform.system() == "Darwin"):
        ret = "require_mac.txt"
    else:
        ret = "require_linux.txt"
    return ret

def get_pip_cmd() -> list:
    ret = []
    if(platform.system() == "Windows"):
        ret.append(join('.venv', VENV_BIN, 'pip'))
    else:
        ret.append(PYTHON_BIN, '-m', 'pip')
    return ret
    
VENV_BIN = get_venv_bin_folder()
PYTHON_BIN = join(getcwd(), '.venv', VENV_BIN, 'python')
VENV_START_BIN = join(getcwd(), '.venv', '')
VENV_DIR = join(getcwd(), '.venv')
SCRIPT_PATH = join(getcwd(), 'main.py')
REQ_TXT = get_requirements_txt()
CHECK_PACK_PATH = join(getcwd(), '.venv', 'FREEZE.txt')
PIP_PATH = get_pip_cmd()

def set_freeze_text() -> str:
    return subprocess.check_output(get_pip_cmd() + ["freeze"], cwd=getcwd(), capture_output=True, text=True, shell=True)

def main():
    freeze = ""
    #freeze_support()

    if (not exists(VENV_START_BIN)):
        # start venv setup process
        create_venv(".venv")
    else:
        freeze = set_freeze_text()
        freeze_current = ""
        with io.open(CHECK_PACK_PATH, 'r') as fd:
            temp = fd.read()
            # WHY DO I HAVE TO **INCREMENT** THE STRING FOR IT TO BE ACCESSED??? AAAAA
            freeze_current = freeze_current + temp
        if (not freeze_current != freeze):
            os.remove(CHECK_PACK_PATH)
    
    if (not exists(CHECK_PACK_PATH)):
        # install packages
        print("Populating .venv...\n")
        subprocess.run(get_pip_cmd() + ["install", "-r", join(getcwd(), REQ_TXT)], cwd=getcwd(), shell=True)
        freeze = set_freeze_text()
        with io.open(CHECK_PACK_PATH, 'w') as fd:
            fd.write(freeze)
        print("Finished population.")

    #process = subprocess.Popen([PYTHON_BIN, SCRIPT_PATH], shell=True)
    #process.wait()

if __name__ == "__main__":
    main()
