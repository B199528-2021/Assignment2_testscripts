#!/usr/local/bin/python3

# 1. stdlib
import os
import sys
import subprocess
import shutil
# a very useful tool for navigating through paths
from pathlib import Path

# 2. 3rd party; e.g. numpy, scipy, matplotlib, ...
import pandas as pd

# 3. own package
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




