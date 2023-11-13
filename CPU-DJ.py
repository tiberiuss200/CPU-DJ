"""
This program is going to double as an installer AND a way to simply start the Python main.py module.
If it's not already installed, it runs a first-time setup before booting.  Otherwise, it skips to running the program
Install script written by Daniel Oravetz
CPU-DJ written by Daniel Oravetz, R-E Miller, Tiberius Shaub, and Nathaniel Harris
"""

from venv import create as create_venv
from os.path import join, exists
from os import getcwd
import subprocess
import platform

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
    
VENV_BIN = get_venv_bin_folder()
PYTHON_BIN = join(getcwd(), '.venv', VENV_BIN, 'python')
VENV_START_BIN = join(getcwd(), '.venv', VENV_BIN, 'activate')
VENV_DIR = join(getcwd(), '.venv')
SCRIPT_PATH = join(getcwd(), 'main.py')
REQ_TXT = get_requirements_txt()

print(VENV_START_BIN)

if (not exists(VENV_START_BIN)):
    # start venv setup process
    create_venv(VENV_DIR, with_pip=True)
    subprocess.run(["{VENV_BIN}/pip", "install", "-r", join(getcwd(), REQ_TXT)], cwd=getcwd())

process = subprocess.Popen([PYTHON_BIN, SCRIPT_PATH], shell=True)
process.wait()
