"""
This program is going to double as an installer AND a way to simply start the Python main.py module.
If it's not already installed, it runs a first-time setup before booting.  Otherwise, it skips to running the program
Install script written by Daniel Oravetz
CPU-DJ written by Daniel Oravetz, R-E Miller, Tiberius Shaub, and Nathaniel Harris
"""

from venv import create as create_venv
from os.path import join, exists, is_dir
from os import getcwd
import subprocess

PYTHON_BIN = join(getcwd(), '.venv', 'bin', 'python')
VENV_START_BIN = join(getcwd(), '.venv', 'bin', 'activate')
VENV_DIR = join(getcwd(), '.venv')

if (~exists(VENV_START_BIN)):
    # start venv setup process
    create_venv(VENV_DIR, with_pip=True)
    subprocess.run(["bin/pip", "install", "-r", join(getcwd(), "requirements.txt")], cwd=getcwd())




