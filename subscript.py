import os
import sys
import subprocess
import shutil
from pathlib import Path # a very useful tool for navigating through paths

import pandas as pd
import numpy as np


def task1():

    # # test the query with test set 
    # os.system(
    # "esearch -db protein -query 'glucose-6-phosphatase[PROT] AND aves[ORGN]' | efetch -format fasta > ./efetch/testset.fasta"
    # )

    # # save user input into variables
    # print("Please enter first the protein family and then the taxonomic group.")
    # prot_fam = input("Protein family:\n")

    # check if there are any hits

    # # test without function
    # prot_fam_query = f"esearch -db protein -query '{prot_fam}[PROT]'"
    # os.system(
    # f"{prot_fam_query} > esearchprotfam.txt"
    # )
    # with open("esearchprotfam.txt") as testprotfam:
        # testprotfam = testprotfam.read()
    # # split the esearch result
    # templist = testprotfam.split()
    # # pick the line with the number of hits ("Count")
    # countnumber = []
    # for templistelement in templist:
        # if templistelement.startswith("<Count>"):
            # countnumber.append(templistelement)
    # # pick it as a string (instead of a list)
    # countnumber = countnumber[0]
    # # delete "Count" and brackets
    # countnumber = countnumber.replace("<Count>", "")
    # countnumber = countnumber.replace("</Count>", "")
    # # convert to integer
    # countnumber = int(countnumber)
    # # delete textfile
    # os.remove("esearchprotfam.txt")
    # # print(type(countnumber))
    # print(countnumber)

    # write it into a function

    def count_nr_of_esearch_hits(query):
        """
        Returns the number of esearch hits from entrez direct.
        
        Parameters:
        -----------
        
        query : string
            e.g. "esearch -db protein -query 'glucose-6-phosphatase[PROT]'"
            e.g. "esearch -db protein -query 'glucose-6-phosphatase[PROT] AND aves[ORGN]'"
        """
        os.system(f"{query} > esearchoutput.txt")
        with open("esearchoutput.txt") as checkoutput:
            checkoutput = checkoutput.read()
        # split the esearch result
        templist = checkoutput.split()
        # pick the line with the number of hits ("Count")
        countnumber = []
        for templistelement in templist:
            if templistelement.startswith("<Count>"):
                countnumber.append(templistelement)
        # convert to string, pick number only
        countnumber = countnumber[0].replace("<Count>", "").replace("</Count>", "")
        # convert to integer
        countnumber = int(countnumber)
        # delete textfile
        os.remove("esearchoutput.txt")
        # print(type(countnumber))
        return(countnumber)
    
    # save user input into variables
    print("Please enter first the protein family and then the taxonomic group.")
    prot_fam = input("Protein family:\n").lower()

    # search the query separately without partial sequences
    prot_fam_query = f"esearch -db protein -query '{prot_fam}[PROT] NOT PARTIAL'"
    # check the number of hits 
    prot_fam_hits = count_nr_of_esearch_hits(prot_fam_query)

    # repeat user input as long as the number of hits is not at least 2 (needed for clustalo)
    while prot_fam_hits < 2:
        print(f"Number of hits:{prot_fam_hits}")
        print(f"\nYou have probably mistyped the protein family, because there are either no or not enough hits.")
        prot_fam = input("Please try again. Type in the PROTEIN FAMILY:\n")
        prot_fam_query = f"esearch -db protein -query '{prot_fam}[PROT] NOT PARTIAL'"
        prot_fam_hits = count_nr_of_esearch_hits(prot_fam_query)

    print(f"The number of hits is {prot_fam_hits}.")
    print(f"Your chosen protein family is '{prot_fam}'.\n")


    # go on with taxonomic group
    print("Please enter the taxonomic group now.")
    tax_group = input("Taxonomic group:\n").lower()

    # search the query separately without partial sequences
    tax_group_query = f"esearch -db protein -query '{tax_group}[ORGN] NOT PARTIAL'"
    # check the number of hits 
    tax_group_hits = count_nr_of_esearch_hits(tax_group_query)

    # repeat user input as long as the number of hits is not at least 2 (needed for clustalo)
    while tax_group_hits < 2:
        print(f"Number of hits:{tax_group_hits}")
        print(f"\nYou have probably mistyped the taxonomic group, because there are either no or not enough hits.")
        tax_group = input("Please try again. Type in a valid TAXONOMIC GROUP:\n")
        tax_group_query = f"esearch -db protein -query '{tax_group}[ORGN] NOT PARTIAL'"
        tax_group_hits = count_nr_of_esearch_hits(tax_group_query)

    print(f"The number of hits is {tax_group_hits}.")
    print(f"Your chosen taxonomic group is '{tax_group}'.\n")


    # now check both (prot_fam & tax_group) in combination
    both_query = f"esearch -db protein -query '{prot_fam}[PROT] AND {tax_group}[ORGN] NOT PARTIAL'"
    # check the number of hits 
    both_hits = count_nr_of_esearch_hits(both_query)
    print(f"The number of hits for {prot_fam.upper()} and {tax_group.upper()} is {both_hits}.\n")

    # set the minimum number of hits (a minimum of 2 is necessary for the multiple sequence alignment)
    # set the maximum number of hits (there is a maximum of 4000 sequences for clustalo)
    if both_hits < 2 or both_hits > 4000:
        if both_hits < 2:
            print("A minimum of TWO sequences is required for multiple sequence alignment.")
        if both_hits > 4000:
            print("The maximum number of 4000 sequences is allowed for the multiple sequence tool used in this script.")
        print("Please start again with a query which outputs a valid number of sequences.")
        exit()

    # ask the user if it is ok to continue
    print("If you are not satisfied with this number, you can stop here and start again with a new query.")

    while True:
        cont = input("Do you want to continue with this number of sequences? 'yes'/'no' > ")
        while cont.lower() not in ("yes", "no"):
            cont = input("Please type in 'yes' or 'no' > ")
        if cont.lower() == "yes":
            print("Okay, the sequences are now being downloaded...")
            break
        elif cont.lower() == "no":
            print("You have decided to stop and start again with a new query.")
            exit()

    # save file in variable
    userquery = f"{tax_group.lower().replace(' ', '')}_{prot_fam.lower().replace(' ', '')}"

    # download the data with efetch 
    os.system(
    f"{both_query} | efetch -format fasta > ./output/{userquery}.fasta"
    )

    # the full file
    print(f"Please find the fasta file '{userquery}.fasta' in the folder 'output'.\n")

    # read line by line to find out the headers
    with open(f"output/{userquery}.fasta") as fullfastafile:
        fullfastafile = fullfastafile.readlines()
    headers = []
    for lines in fullfastafile:
        if lines.startswith(">"):
            headers.append(lines)
    #print(headers)

    # get the organisms of the headers
    organisms = []
    for headerlines in headers:
        # delete the first part before the bracket
        oneorganism = headerlines.split("[")[1]
        # delete the other part after the bracket
        oneorganism = oneorganism.replace("]\n", "")
        organisms.append(oneorganism)
    #print(organisms)

    # get the number of each organism
    df_organisms = pd.DataFrame (organisms, columns = ["organism"])

    # let the user know
    print(f"{len(df_organisms['organism'].value_counts())} species are represented in the dataset.\n")

    print("Here you can see a preview of all organisms and how often they are represented in the data.")
    print("In the left column you can find the organisms and in the right column how often they are represented:")
    print(df_organisms["organism"].value_counts())

    print(f"\nPlease find the whole csv file in the folder 'output' under the name '{userquery}_organisms_count.csv'.\n")
    df_organisms["organism"].value_counts().to_csv(f"./output/{userquery}_organisms_count.csv", header=False)


    # ask the user if it is ok to continue
    print("If you are not satisfied with this, you can stop here and start again with a new query.")

    while True:
        cont = input("Do you want to continue with these organisms? 'yes'/'no' > ")
        while cont.lower() not in ("yes", "no"):
            cont = input("Please type in 'yes' or 'no' > ")
        if cont.lower() == "yes":
            print("Okay, we continue with the current dataset...")
            break
        elif cont.lower() == "no":
            print("You have decided to stop and start again with a new query.")
            exit()


    print("Checking user input finished.\n")
    
    # return the variable "userquery", so that it can be used in the next task
    return userquery


def task2clustalo(userquery):
    
    print("Please be patient. Clustal Omega is now producing multiple sequence alignments for your query...\n")
    
    # run clustalo via the shell to get aligned sequences
    subprocess.call(f"clustalo --infile ./output/{userquery}.fasta --outfile ./output/{userquery}_aligned_seqs.fasta -v --force", shell=True)
    
    print(f"\nClustal Omega has finished. Please find the aligned file '{userquery}_aligned_seqs.fasta' in the folder 'output'.\n")
    

def task2plotcon(userquery):
    
    print("Plotcon is now doing the conservation plot...\n")
    
    # plot the level of conservation with output to screen
    ###subprocess.call(f"plotcon ./output/{userquery}_aligned_seqs.fasta -winsize 4 -graph x11 -verbose", shell=True)
    
    # ask the user if he wants to save as svg, ps or both
    while True:
        saveplot = input("\nDo you want to save the plot as 'svg' or 'ps' file? If you want to save it as 'svg' AND 'ps', then type in 'both'.\n 'svg'/'ps'/'both' > ").lower()
        while saveplot not in ("svg", "ps", "both"):
            saveplot = input("Not valid input. Please type in SVG or PS or BOTH! > ").lower()
        if saveplot == "svg":
            subprocess.call(f"plotcon ./output/{userquery}_aligned_seqs.fasta -winsize 4 -graph svg -goutfile {userquery}_plot -gdirectory ./output -verbose", shell=True)
            print(f"Please find the conservation plot in the folder 'output' with the name '{userquery}_plot.svg'.")
            break
        elif saveplot == "ps":
            subprocess.call(f"plotcon ./output/{userquery}_aligned_seqs.fasta -winsize 4 -graph ps -goutfile {userquery}_plot -gdirectory ./output -verbose", shell=True)
            print(f"Please find the conservation plot in the folder 'output' with the name '{userquery}_plot.ps'.")
            break
        else:
            subprocess.call(f"plotcon ./output/{userquery}_aligned_seqs.fasta -winsize 4 -graph svg -goutfile {userquery}_plot -gdirectory ./output -verbose", shell=True)
            subprocess.call(f"plotcon ./output/{userquery}_aligned_seqs.fasta -winsize 4 -graph ps -goutfile {userquery}_plot -gdirectory ./output -verbose", shell=True)
            print(f"Please find the conservation plot in the folder 'output' with the names '{userquery}_plot.svg' and '{userquery}_plot.ps'.")
            break

    print("\nfinished dfldkncaöodkaif")
    exit()
    
    # save as a svg file
    subprocess.call(f"plotcon ./output/{userquery}_aligned_seqs.fasta -winsize 4 -graph svg -goutfile {userquery}_plot -gdirectory ./output -verbose", shell=True)
    
    print(f"\nPlease find the conservation plot in the folder 'output' with the name '{userquery}_plot.svg'.\n")
    
    print(f"TODO plotcon {userquery}")
    print("TODO task2")
