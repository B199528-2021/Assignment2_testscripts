#!/usr/local/bin/python3

import os
import sys
import subprocess
import shutil
from pathlib import Path # a very useful tool for navigating through paths

import pandas as pd
import numpy as np

# my own packages - please find them in the script 'subscript.py'
from subscript import task1
from subscript import task2


print("This is your current path:")
print(os.getcwd())
print("")

# create a subfolder for all output files (if it already exists, nothing happens)
Path("output").mkdir(exist_ok=True)

print("Please find all your output data in the folder 'output'.\n")

task1() # check user input

task2() # conservation analysis plot

print("FINISHED")

exit()




