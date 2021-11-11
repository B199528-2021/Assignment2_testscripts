import os
import sys
import subprocess
import shutil
import glob
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
    #prot_fam = input("Protein family:\n").lower()

    # error traps:
    invalid = True
    while invalid:
        prot_fam = input("\nProtein family:\n").lower()
        # don't allow apostroph or quotation marks, as they could end the string
        prot_fam = prot_fam.replace("'"," ")
        prot_fam = prot_fam.replace('"',' ')
        # check if input is empty
        if not prot_fam:
            print("Please type in a valid protein family!")
            continue
        # check if input is too small or too large
        if (len(prot_fam) < 2) or (len(prot_fam) > 30):
            if len(prot_fam) < 2:
                print(f"{len(prot_fam)} is the length of your input.")
                print("Can a protein family consist of one letter only? Please try again.")
            else:
                print(f"{len(prot_fam)} is the length of your input.")
                print("Maybe you have misread, do not paste in a sequence or so. Please just type in the protein family.")
            continue
        # check if more than 2 spaces side by side in input:
        if (len(prot_fam) - len(prot_fam.lstrip(' '))) >= 2:
            print("You may have mistyped. Please try again.")
            continue
        okay = input(f"Are you sure that you want to search for the protein family '{prot_fam}'? 'Yes'/'No' > ").lower()
        if (okay != "yes") and (okay != "y"):
            continue
        
        # search the query separately without partial sequences
        prot_fam_query = f"esearch -db protein -query '{prot_fam}[PROT] NOT PARTIAL'"
        # check the number of hits
        prot_fam_hits = count_nr_of_esearch_hits(prot_fam_query)
        
        # don't allow an input which has less than 2 hits (needed for clustalo)
        if prot_fam_hits < 2:
            print(f"Number of hits:{prot_fam_hits}")
            print("You have probably mistyped the protein family because you have not enough hits for the analysis.")
            print("Please try again.")
            continue
                
        print(f"{prot_fam_hits} is the number of hits for the protein family '{prot_fam}'.\n")
        okay = input(f"Do you want to continue? 'Yes'/'No' > ").lower()
        if (okay != "yes") and (okay != "y"):
            continue
        
        break
    
    
    
    #------------------taxonomic group---------------------

    # go on with taxonomic group
    print("Please enter the taxonomic group now.")
    
    # error traps:
    invalid = True
    while invalid:
        tax_group = input("\nTaxonomic group:\n").lower()
        # don't allow apostroph or quotation marks, as they could end the string
        tax_group = tax_group.replace("'"," ")
        tax_group = tax_group.replace('"',' ')
        # check if input is empty
        if not tax_group:
            print("Please type in a valid taxonomic group!")
            continue
        # check if input is too small or too large
        if (len(tax_group) < 2) or (len(tax_group) > 30):
            if len(tax_group) < 2:
                print(f"{len(tax_group)} is the length of your input.")
                print("Can a taxonomic group consist of one letter only? Please try again.")
            else:
                print(f"{len(tax_group)} is the length of your input.")
                print("Maybe you have misread, do not paste in a sequence or so. Please just type in the taxonomic group.")
            continue
        # check if more than 2 spaces side by side in input:
        if (len(tax_group) - len(tax_group.lstrip(' '))) >= 2:
            print("You may have mistyped. Please try again.")
            continue
        okay = input(f"Are you sure that you want to search for the taxonomic group '{tax_group}'? 'Yes'/'No' > ").lower()
        if (okay != "yes") and (okay != "y"):
            continue
        
        # search the query separately without partial sequences
        tax_group_query = f"esearch -db protein -query '{tax_group}[ORGN] NOT PARTIAL'"
        # check the number of hits
        tax_group_hits = count_nr_of_esearch_hits(tax_group_query)
        
        # don't allow an input which has less than 2 hits (needed for clustalo)
        if tax_group_hits < 2:
            print(f"Number of hits:{tax_group_hits}")
            print("You have probably mistyped the taxonomic group because you have not enough hits for the analysis.")
            print("Please try again.")
            continue
                
        print(f"{tax_group_hits} is the number of hits for the taxonomic group '{tax_group}'.\n")
        okay = input(f"Do you want to continue? 'Yes'/'No' > ").lower()
        if (okay != "yes") and (okay != "y"):
            continue
        
        break    
    
    exit()
    

    #------------------combination of both---------------------

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
        cont = input("Do you want to continue with this number of sequences? 'Yes'/'No' > ").lower()
        while cont not in ("yes", "y", "no", "n"):
            cont = input("Please type in 'yes'/'y' or 'no'/'n' > ").lower()
        if cont == "yes" or cont == "y":
            print("Okay, the sequences are now being downloaded...")
            break
        elif cont == "no" or cont == "n":
            print("You have decided to stop and start again with a new query.")
            exit()

    # save file in variable and replace special characters
    userquery = f"{tax_group.lower().replace(' ', '_').replace('-', '_')}_{prot_fam.lower().replace(' ', '_').replace('-', '_')}"

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
    # delete "\n" from list elements
    headers = [h.replace("\n","") for h in headers]
    print("This is the result of your query:")
    print("\n".join(headers))   # show them to the user
    print(f"\nNumber of hits: {both_hits}")
    
    # ask user if he wants to delete the predicted sequences 
    while True:
        cont = input("\nDo you want to exclude the sequences with the word 'PREDICTED' in their title?\n'Yes' for 'exclude' / 'No' for 'include' > ").lower()
        while cont not in ("yes", "y", "exclude", "no", "n", "include"):
            cont = input("Please type in 'yes'/'y'/'exclude or 'no'/'n'/'include' > ").lower()
        if cont == "yes" or cont == "y" or cont == "exclude":
            print("Okay, the sequences with 'PREDICTED' are excluded.")
            
            both_query = f"esearch -db protein -query '{prot_fam}[PROT] AND {tax_group}[ORGN] NOT PARTIAL NOT PREDICTED'"
            # check the number of hits
            both_hits = count_nr_of_esearch_hits(both_query)
            print(f"\nThe number of hits for {prot_fam.upper()} and {tax_group.upper()} without PREDICTED in the sequence is {both_hits}.\n")
            
            # set the minimum number of hits (a minimum of 2 is necessary for the multiple sequence alignment)
            # set the maximum number of hits (there is a maximum of 4000 sequences for clustalo)
            if both_hits < 2 or both_hits > 4000:
                if both_hits < 2:
                    print("A minimum of TWO sequences is required for multiple sequence alignment.")
                if both_hits > 4000:
                    print("The maximum number of 4000 sequences is allowed for the multiple sequence tool used in this script.")
                print("Please start again with a query which outputs a valid number of sequences.")
                exit()            
            
            print("The sequences are now being downloaded again...\n")
            # download data with efetch again without predicted in title 
            os.system(f"{both_query} | efetch -format fasta > ./output/{userquery}.fasta")
            # let the user know that old version is overwritten
            print(f"Please find the fasta file '{userquery}.fasta' in the folder 'output'. The old file was removed and replaced by this file.\n")
            
            # read line by line to find out the headers
            with open(f"output/{userquery}.fasta") as fullfastafile:
                fullfastafile = fullfastafile.readlines()
            headers = []
            for lines in fullfastafile:
                if lines.startswith(">"):
                    headers.append(lines)
            # delete "\n" from list elements
            headers = [h.replace("\n","") for h in headers]
            
            break
        elif cont == "no" or cont == "n" or cont == "include":
            print("Okay, the sequences with 'PREDICTED' are included.")
            break
    
    
    print("This is the result of your query:")
    print("\n".join(headers))   # show them to the user
    print(f"\nNumber of hits: {both_hits}")
    
    
    # get the organisms of the headers
    organisms = []
    for headerlines in headers:
        # delete the first part before the bracket
        oneorganism = headerlines.split("[")[1]
        # delete the other part after the bracket
        oneorganism = oneorganism.replace("]", "")
        organisms.append(oneorganism)
    #print(organisms)
    
    
    # get the number of each organism
    df_organisms = pd.DataFrame (organisms, columns = ["organism"])

    # let the user know
    print(f"\nNumber of organisms represented in the dataset: {len(df_organisms['organism'].value_counts())}.")
    print("Here you can see a preview of all organisms and how often they are represented in the data.\
    In the left column you can find the organisms and in the right column how often they are represented:")
    print(df_organisms["organism"].value_counts())

    print(f"\nPlease find the whole csv file in the folder 'output' under the name '{userquery}_organisms_count.csv'.\n")
    df_organisms["organism"].value_counts().to_csv(f"./output/{userquery}_organisms_count.csv", header=False)
    
    
    # ask the user if it is ok to continue
    print("If you are not satisfied with this, you can stop here and start again with a new query.")
    while True:
        cont = input("Do you want to continue with these organisms? 'Yes'/'No' > ").lower()
        while cont not in ("yes", "y", "no", "n"):
            cont = input("Please type in 'yes'/'y' or 'no'/'n' > ").lower()
        if cont == "yes" or cont == "y":
            print("Okay, we continue with the current dataset.")
            break
        elif cont == "no" or cont == "n":
            print("You have decided to stop and start again with a new query.")
            exit()
    
    
    print("Checking user input finished.\n")
    
    # return the variable "userquery", so that it can be used in the next task
    return userquery


def task2clustalo(userquery):
    
    print("Please be patient. Clustal Omega is now producing multiple sequence alignments for your query...\n")
    
    # run clustalo via the shell to get aligned sequences
    subprocess.call(f"clustalo --infile ./output/{userquery}.fasta --outfile ./output/{userquery}_aligned_seqs.fasta -v --force", shell=True)
    
    print(f"\nClustal Omega has finished.\n")
    print(f"Please find the aligned file '{userquery}_aligned_seqs.fasta' in the folder 'output'.\n")
    
    # return the variable "userquery", so that it can be used in the next task
    return userquery 

def task2plotcon(userquery):
    
    print("Plotcon is now doing the conservation plot...\n")
    
    # plot the level of conservation with output to screen
    subprocess.call(f"plotcon ./output/{userquery}_aligned_seqs.fasta -winsize 4 -graph x11 -verbose", shell=True)
    
    # ask the user if he wants to save as svg, ps or both
    while True:
        saveplot = input("\nDo you want to save the plot as 'svg' or 'ps' file? If you want to save it as 'svg' AND 'ps', then type in 'both'.\n 'svg'/'ps'/'both' > ").lower()
        while saveplot not in ("svg", "ps", "both"):
            saveplot = input("Not valid input. Please type in SVG or PS or BOTH! > ").lower()
        if saveplot == "svg":
            subprocess.call(f"plotcon ./output/{userquery}_aligned_seqs.fasta -winsize 4 -graph svg -goutfile {userquery}_plot -gdirectory ./output -verbose", shell=True)
            print(f"\nPlease find the conservation plot in the folder 'output' with the name '{userquery}_plot.svg'.")
            break
        elif saveplot == "ps":
            subprocess.call(f"plotcon ./output/{userquery}_aligned_seqs.fasta -winsize 4 -graph ps -goutfile {userquery}_plot -gdirectory ./output -verbose", shell=True)
            print(f"\nPlease find the conservation plot in the folder 'output' with the name '{userquery}_plot.ps'.")
            break
        else:
            subprocess.call(f"plotcon ./output/{userquery}_aligned_seqs.fasta -winsize 4 -graph svg -goutfile {userquery}_plot -gdirectory ./output -verbose", shell=True)
            subprocess.call(f"plotcon ./output/{userquery}_aligned_seqs.fasta -winsize 4 -graph ps -goutfile {userquery}_plot -gdirectory ./output -verbose", shell=True)
            print(f"\nPlease find the conservation plot in the folder 'output' with the names '{userquery}_plot.svg' and '{userquery}_plot.ps'.")
            break

    print("\nConservation analysis plot finished.\n")
    
    # return the variable "userquery", so that it can be used in the next task
    return userquery  

    
def task3scanwithmotifs(userquery):
    
    print("Patmatmotifs is now reading your protein sequences and searches them against the PROSITE database of motifs...\n")
    
    # patmatmotifs scans only one protein sequence at a time, so the FASTA file needs to be split
    # with open(f"./output/{userquery}.fasta") as fastafile
    
    with open(f"output/{userquery}.fasta") as fullfastafile:
        fullfastafile = fullfastafile.read()
    
    # delete first ">"
    fastalist = fullfastafile[1:]
    
    # split the fasta sequences    
    fastalist = fastalist.split(">")
    
    
    # extract the headerlines
    with open(f"output/{userquery}.fasta") as fullfastafile:
        fullfastafile = fullfastafile.readlines()
    headers = []
    for lines in fullfastafile:
        if lines.startswith(">"):
            headers.append(lines)
    # delete "\n" from list elements
    headers = [h.replace("\n","") for h in headers]     # list of headers

    

    def get_hitcount_motifs(patf):    
        # test for 1 patmatmotifs file first
        # patf = "seq_2.patmatmotifs" # seq
        # extract HitCount
        with open(f"./output/{patf}") as patfile:
            patfile = patfile.readlines()
        
        # get hitcount and motifs from file 
        hitcount = []
        for line in patfile:
            if "# HitCount: 0" == True:
                hitcount.append("HitCount: 0")
            else:
                if line.startswith("# HitCount"):
                    hitcount.append(line.rstrip().replace("# ",""))
                # get motif from file
                if line.startswith("Motif"):
                    hitcount.append(line.rstrip())
        return hitcount
        
    #TODO====================UNCOMMENT===================================
    # loop through each sequence
    motifslist = []
    for count,content in enumerate(fastalist):
        # save into a file
        with open(f"output/seq_{count}.fasta", "w") as eachseqfile:
            # add ">" to header again
            eachseqfile.write(f">{content}")
        # run patmatmotifs for each file
        with open(f"output/seq_{count}.fasta") as eachseqfile:
            subprocess.call(f"patmatmotifs ./output/seq_{count}.fasta ./output/seq_{count}.patmatmotifs", shell=True)
        # for all patmatmotifs files 
        # get header and use function get_hitcount_motifs 
        motifslist.append((headers[count], get_hitcount_motifs(f"seq_{count}.patmatmotifs")))
        #.append(get_hitcount_motifs(f"seq_{count}.patmatmotifs"))
    
    #print(motifslist[0])
    
    # convert into  dataframe for user
    df_motifs = pd.DataFrame(motifslist, columns = ["FASTA header", "motifs"])
    
    print(df_motifs)
    
    # save as csv file and let user know
    df_motifs.to_csv(f"./output/motifs_{userquery}.csv", index=False)
    print(f"Please find the motifs of your sequences in the csv file 'motifs_{userquery}.csv' in the folder 'output'.")
    
    # move seq data into subfolder and tell user
    source = f"./output/seq_*"
    destination = f"./output/{userquery}_patmatmotifs"
    for file in glob.glob(source):
        shutil.move(file, destination)    
    print(f"Please find the FASTA textfile and the patmatmotifs file for each sequence in the folder 'output' in the subfolder '{userquery}'.")

    print("Finished moved files.")
    
    exit()
    

    
    

    

    # TODO:
    # make csv file more beautiful
    # move patmatmotifs files into a separate folder and let user know
    # run plotcon with output file data --> numbers of conservation
    # make blast analyses? for conservation analysis? to get the degree of similarity within the sequence chosen?
    
    
    
    
    
    

    
    
    
    # run patmatmotifs
    subprocess.call(f"patmatmotifs ./output/{userquery}_aligned_seqs.fasta ./output/{userquery}.patmatmotifs", shell=True)
    
    
    
    print("TODO")
    print(f"test{userquery}")
    
    
