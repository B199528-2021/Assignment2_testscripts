#!/usr/local/bin/python3

import os, sys, subprocess, shutil
# a very useful tool for navigating through paths
from pathlib import Path

print("This is your current path:")
print(os.getcwd())
print("")

# create a subfolder for all output files (if it already exists, nothing happens)
Path("output").mkdir(exist_ok=True)
Path("efetch").mkdir(exist_ok=True)

print("Please find all your output data in the folder 'output'.\n")

# run the Python scripts

subprocess.call("chmod +x 1userinput.py", shell=True)
subprocess.call("./1userinput.py", shell=True)

subprocess.call("chmod +x 2conservation.py", shell=True)
subprocess.call("./2conservation.py", shell=True)




