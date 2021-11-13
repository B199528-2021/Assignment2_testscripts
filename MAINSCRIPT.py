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
from subscript import task3scanwithmotifs


# create a subfolder for all output files (if it already exists, nothing happens)
Path("output").mkdir(exist_ok=True)

print("Please find all your output data in the folder 'output'.\n")

# return the userinput and save it into the variable "userquery"
userquery = task1() # check user input

# use the userinput in the next task
userquery = task2clustalo(userquery)

# conservation analysis plot
userquery = task2plotcon(userquery)

# create a subfolder for the patmatmotif files
destination = f"./output/{userquery}_patmatmotif_files"
dirpath = Path(destination)
# delete folder if already exists
if dirpath.exists() and dirpath.is_dir():
    shutil.rmtree(dirpath)
# create the subfolder
Path(destination).mkdir()

# scan with motifs from PROSITE database 
task3scanwithmotifs(userquery)


# last messages to user
print("""\nI hope this script was useful for you!\n
You can run it again with other protein families or taxonomic groups. Just be aware
that outputs of the same protein family and taxonomic group will be overwritten.
You can avoid overwriting if you change the name of the output folder, so that a 
new output folder will be created.
""")





