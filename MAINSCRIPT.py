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
from subscript import task2clustalo
from subscript import task2plotcon


print("\nThis is your current path:")
print(os.getcwd())
print("")

# create a subfolder for all output files (if it already exists, nothing happens)
Path("output").mkdir(exist_ok=True)

print("Please find all your output data in the folder 'output'.\n")

# return the userinput and save it into the variable "userquery"
#=======================================TODO: uncomment!!!====================
#userquery = task1() # check user input

#=======================================TODO: delete!!!====================
userquery = "aves_glucose-6-phosphatase"

# use the userinput in the next task
#=======================================TODO: uncomment!!!====================
#userquery = task2clustalo(userquery)

# conservation analysis plot
task2plotcon(userquery)

print("END OF MAINSCRIPT.PY")

exit()




