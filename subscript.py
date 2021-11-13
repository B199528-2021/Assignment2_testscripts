import os
import sys
import subprocess
import shutil
import glob
from pathlib import Path # a very useful tool for navigating through paths

import pandas as pd
import numpy as np


def task1():


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

    # error traps:
    invalid = True
    while invalid:
        prot_fam = input("\nPROTEIN FAMILY:\n").lower()
        # don't allow apostroph or quotation marks, as they could end the string
        prot_fam = prot_fam.replace("'"," ")
        prot_fam = prot_fam.replace('"',' ')
        # check if input is empty
        if not prot_fam:
            print("\nPlease type in a valid protein family!")
            continue
        # check if input is too small or too large
        if (len(prot_fam) < 2) or (len(prot_fam) > 30):
            if len(prot_fam) < 2:
                print(f"\n{len(prot_fam)} is the length of your input.")
                print("Can a protein family consist of one letter only? Please try again.")
            else:
                print(f"\n{len(prot_fam)} is the length of your input.")
                print("Maybe you have misread, do not paste in a sequence or so. Please just type in the protein family.")
            continue
        # check if more than 2 spaces side by side in input:
        if (len(prot_fam) - len(prot_fam.lstrip(' '))) >= 2:
            print("\nYou may have mistyped. Please try again.")
            continue
        okay = input(f"\nAre you sure that you want to search for the protein family '{prot_fam}'?\n'Yes'/'No' > ").lower()
        if (okay != "yes") and (okay != "y"):
            continue
        
        # search the query separately without partial sequences
        prot_fam_query = f"esearch -db protein -query '{prot_fam}[PROT] NOT PARTIAL'"
        # check the number of hits
        prot_fam_hits = count_nr_of_esearch_hits(prot_fam_query)
        
        # don't allow an input which has less than 2 hits (needed for clustalo)
        if prot_fam_hits < 2:
            print(f"Number of hits: {prot_fam_hits}")
            print("You have probably mistyped the protein family because you have not enough hits for the analysis.")
            print("Please try again.")
            continue
                
        print(f"{prot_fam_hits} is the number of hits for the protein family '{prot_fam}'.\n")
        okay = input(f"Do you want to continue? 'Yes'/'No' > ").lower()
        if okay not in ("yes", "y"):
            continue
        
        break
    
    
    
    #------------------taxonomic group---------------------

    # go on with taxonomic group
    print("Please enter the taxonomic group now.")
    
    # error traps:
    invalid = True
    while invalid:
        tax_group = input("\nTAXONOMIC GROUP:\n").lower()
        # don't allow apostroph or quotation marks, as they could end the string
        tax_group = tax_group.replace("'"," ")
        tax_group = tax_group.replace('"',' ')
        # check if input is empty
        if not tax_group:
            print("\nPlease type in a valid taxonomic group!")
            continue
        # check if input is too small or too large
        if (len(tax_group) < 2) or (len(tax_group) > 30):
            if len(tax_group) < 2:
                print(f"\n{len(tax_group)} is the length of your input.")
                print("Can a taxonomic group consist of one letter only? Please try again.")
            else:
                print(f"\n{len(tax_group)} is the length of your input.")
                print("Maybe you have misread, do not paste in a sequence or so. Please just type in the taxonomic group.")
            continue
        # check if more than 2 spaces side by side in input:
        if (len(tax_group) - len(tax_group.lstrip(' '))) >= 2:
            print("\nYou may have mistyped. Please try again.")
            continue
        okay = input(f"\nAre you sure that you want to search for the taxonomic group '{tax_group}'?\n'Yes'/'No' > ").lower()
        if (okay != "yes") and (okay != "y"):
            continue
        
        # search the query separately without partial sequences
        tax_group_query = f"esearch -db protein -query '{tax_group}[ORGN] NOT PARTIAL'"
        # check the number of hits
        tax_group_hits = count_nr_of_esearch_hits(tax_group_query)
        
        # don't allow an input which has less than 2 hits (needed for clustalo)
        if tax_group_hits < 2:
            print(f"Number of hits: {tax_group_hits}")
            print("You have probably mistyped the taxonomic group because you have not enough hits for the analysis.")
            print("Please try again.")
            continue
                
        print(f"{tax_group_hits} is the number of hits for the taxonomic group '{tax_group}'.\n")
        okay = input(f"Do you want to continue? 'Yes'/'No' > ").lower()
        if okay not in ("yes", "y"):
            continue
        
        break    
    
    

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
    print("Do you want to continue with this number of sequences?")
    print("Please be aware: If you say 'No', you will have to start the whole query again!")

    invalid = True
    while invalid:
        cont = input("\nPlease type in 'Yes' to continue (or 'No' if you want to start again).\n'Yes'/'No' > ").lower()
        if cont not in ("yes", "y", "no", "n"):
            print("Please try again.")
            continue
        if cont in ("yes", "y"):
            print("\nOkay, the sequences are now being downloaded...")
            break
        else:
            print("You have decided to stop and start this programme again with a new query.")
            exit()
    
    
    #------------------save file---------------------
    
    # save file in variable and replace special characters
    userquery_replaced = f"{tax_group.lower().replace(' ', '_').replace('-', '_')}_{prot_fam.lower().replace(' ', '_').replace('-', '_')}"

    # download the data with efetch 
    os.system(f"{both_query} | efetch -format fasta > ./output/{userquery_replaced}.fasta")

    # the full file
    print(f"\nPlease find the fasta file '{userquery_replaced}.fasta' in the folder 'output'.")
    # make sure that user has read this information
    input("Press Enter to continue...")
    
    def find_headers(fastafile):
        """
        Reads a text file line by line to find out the headers.
        Returns the header of a FASTA file.
        
        Parameters:
        -----------
        
        fastafile : string
        """
        with open(fastafile) as fullfastafile:
            fullfastafile = fullfastafile.readlines()
        headers = []
        for lines in fullfastafile:
            if lines.startswith(">"):
                headers.append(lines)
        # delete "\n" from list elements
        headers = [h.replace("\n","") for h in headers]
        return headers
    
    # # test function
    # print(find_headers(f"output/{userquery_replaced}.fasta"))
    
    # use function
    headers = find_headers(f"output/{userquery_replaced}.fasta")
    
    print("\nThis is the result of your query:")
    print("\n".join(headers))   # show them to the user
    print(f"\nNumber of hits: {both_hits}")
    
    # ask user if he wants to delete the predicted sequences 
    invalid = True
    while invalid:
        cont = input("\nDo you want to exclude the sequences with the word 'PREDICTED' in their title?\n If no sequence has 'PREDICTED' in its title, you can type in 'Yes'.\n'Yes' for 'exclude' / 'No' for 'include' > ").lower()
        if cont not in ("yes", "y", "exclude", "no", "n", "include"):
            print("Please try again.")
            continue
            
        if cont in ("yes", "y", "exclude"):
            print("Okay, the sequences with 'PREDICTED' are excluded.")
            
            both_query = f"esearch -db protein -query '{prot_fam}[PROT] AND {tax_group}[ORGN] NOT PARTIAL NOT PREDICTED'"
            # check the number of hits
            both_hits = count_nr_of_esearch_hits(both_query)
            print(f"The number of hits for {prot_fam.upper()} and {tax_group.upper()} without PREDICTED in the sequence is {both_hits}.\n")
            
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
            
            # save file in variable and replace special characters
            userquery_replaced = f"{tax_group.lower().replace(' ', '_').replace('-', '_')}_{prot_fam.lower().replace(' ', '_').replace('-', '_')}"
            
            # download data with efetch again without predicted in title 
            os.system(f"{both_query} | efetch -format fasta > ./output/{userquery_replaced}.fasta")
            # let the user know that old version is overwritten
            print(f"Please find the fasta file '{userquery_replaced}.fasta' in the folder 'output'. The old file was removed and replaced by this file.\n")
            # make sure that user has read this information
            input("Press Enter to continue...\n")
            
            # use function
            headers = find_headers(f"output/{userquery_replaced}.fasta")
            
            break
            
        if cont in ("no", "n", "include"):
            print("Okay, the sequences with 'PREDICTED' are included.\n")
            break
    
    userquery = userquery_replaced
    
    print("This is the result of your query:")
    print("\n".join(headers))   # show them to the user
    print(f"\nNumber of hits: {both_hits}")
    # make sure that user has read this information
    
    
    #------------------get organisms---------------------
    def get_organisms(fastaheaderfile):
        """
        Reads a text file which contains FASTA headers only
        line by line to find out the organisms.
        Returns a list of organisms.
        
        Parameters:
        -----------
        
        fastaheaderfile : string
        """    
        organisms = []
        for headerlines in headers:
            # delete the first part before the bracket
            oneorganism = headerlines.split("[")[1]
            # delete the other part after the bracket
            oneorganism = oneorganism.replace("]", "")
            organisms.append(oneorganism) 
        return organisms
    
    organisms = get_organisms(headers)
    
    # get the number of each organism
    df_organisms = pd.DataFrame (organisms, columns = ["organism"])

    # let the user know
    print(f"Number of organisms represented in the dataset: {len(df_organisms['organism'].value_counts())}.")
    # make sure that user has read this information
    input("Press Enter to continue...\n")
    print("Here you can see a preview of all organisms and how often they are represented in the data.\nIn the left column you can find the organisms and in the right column how often they are represented:")
    print(df_organisms["organism"].value_counts())
    # make sure that user has read this information
    input("Press Enter to continue...")
    df_organisms["organism"].value_counts().to_csv(f"./output/{userquery}_organisms_count.csv", header=False)
    print(f"\nPlease find the whole csv file in the folder 'output' under the name '{userquery}_organisms_count.csv'.")
    # make sure that user has read this information
    input("Press Enter to continue...\n")    
    
    # ask the user if it is ok to continue
    print("If you are not satisfied with this, you can stop here and start again with a new query.")
    print("Do you want to continue with these organisms?")
    print("Please be aware: If you say 'No', you will have to start the whole query again!")
    invalid = True
    while invalid:
        cont = input("\nPlease type in 'Yes' to continue (or 'No' if you want to start again).\n'Yes'/'No' > ").lower()
        if cont not in ("yes", "y", "no", "n"):
            print("Please try again.")
            continue
        if cont in ("yes", "y"):
            print("Okay, we continue with the current dataset.")
            break
        if cont in ("no", "n"):
            print("You have decided to stop and start again with a new query.")
            exit()
    
    # return the variable "userquery", so that it can be used in the next task
    return userquery


def task2clustalo(userquery):
    
    print("Please be patient. Clustal Omega is now producing multiple sequence alignments for your query...\n")
    
    # run clustalo via the shell to get aligned sequences
    subprocess.call(f"clustalo --infile ./output/{userquery}.fasta --outfile ./output/{userquery}_aligned_seqs.fasta -v --force", shell=True)
    
    print(f"\nClustal Omega has finished.\n")
    print(f"Please find the aligned file '{userquery}_aligned_seqs.fasta' in the folder 'output'.")
    # make sure that user has read this information
    input("Press Enter to continue...")
    
    # return the variable "userquery", so that it can be used in the next task
    return userquery 


def task2plotcon(userquery):
    
    print("\nPlotcon is now doing the conservation plot...\n")
    
    # plot the level of conservation with output to screen
    subprocess.call(f"plotcon ./output/{userquery}_aligned_seqs.fasta -winsize 4 -graph x11 -verbose", shell=True)
    
    # ask the user if he wants to save as svg, ps or both
    while True:
        saveplot = input("\nDo you want to save the plot as 'svg' or 'ps' file? If you want to save it as 'svg' AND 'ps', then type in 'both'.\n 'svg'/'ps'/'both' > ").lower()
        if saveplot not in ("svg", "ps", "both"):
            print("Not valid format. Please type in SVG or PS or BOTH!")
            continue
        if saveplot == "svg":
            subprocess.call(f"plotcon ./output/{userquery}_aligned_seqs.fasta -winsize 4 -graph svg -goutfile {userquery}_plot -gdirectory ./output -verbose", shell=True)
            print(f"\nPlease find the conservation plot in the folder 'output' with the name '{userquery}_plot.svg'.")
            break
        if saveplot == "ps":
            subprocess.call(f"plotcon ./output/{userquery}_aligned_seqs.fasta -winsize 4 -graph ps -goutfile {userquery}_plot -gdirectory ./output -verbose", shell=True)
            print(f"\nPlease find the conservation plot in the folder 'output' with the name '{userquery}_plot.ps'.")
            break
        else:
            subprocess.call(f"plotcon ./output/{userquery}_aligned_seqs.fasta -winsize 4 -graph svg -goutfile {userquery}_plot -gdirectory ./output -verbose", shell=True)
            subprocess.call(f"plotcon ./output/{userquery}_aligned_seqs.fasta -winsize 4 -graph ps -goutfile {userquery}_plot -gdirectory ./output -verbose", shell=True)
            print(f"\nPlease find the conservation plot in the folder 'output' with the names '{userquery}_plot.svg' and '{userquery}_plot.ps'.")
            break
    
    # save data of plot and let the user know
    subprocess.call(f"plotcon ./output/{userquery}_aligned_seqs.fasta -winsize 4 -graph data -goutfile {userquery}_plot -gdirectory ./output -verbose", shell=True)
    print(f"Please find the exact values of this plot in the file '{userquery}_plot1.dat' in the folder 'output'.")
    # make sure that user has read this information
    input("Press Enter to continue...")
    
    print("\nConservation analysis plot finished.\n")
    
    # return the variable "userquery", so that it can be used in the next task
    return userquery  

    
def task3scanwithmotifs(userquery):
    
    print("\nPatmatmotifs is now reading your protein sequences and searches them against the PROSITE database of motifs...\n")
    
    # patmatmotifs scans only one protein sequence at a time, so the FASTA file needs to be split
    # with open(f"./output/{userquery}.fasta") as fastafile
    
    with open(f"output/{userquery}.fasta") as fullfastafile:
        fullfastafile = fullfastafile.read()
    
    # delete first ">"
    fastalist = fullfastafile[1:]
    # split the fasta sequences    
    fastalist = fastalist.split(">")
    
    
    def find_headers(fastafile):
        """
        Reads a text file line by line to find out the headers.
        Returns the header of a FASTA file.
        
        Parameters:
        -----------
        
        fastafile : string
        """
        with open(fastafile) as fullfastafile:
            fullfastafile = fullfastafile.readlines()
        headers = []
        for lines in fullfastafile:
            if lines.startswith(">"):
                headers.append(lines)
        # delete "\n" from list elements
        headers = [h.replace("\n","") for h in headers]
        return headers    
    # test function
    headers = find_headers(f"output/{userquery}.fasta")
    #print(headers)
    
    def get_acc(fastaheaderfile):
        """
        Reads a text file which contains FASTA headers only
        line by line to find out the accession numbers.
        Returns a list of accession numbers.
        
        Parameters:
        -----------
        
        fastaheaderfile : string
        """    
        acc_list = []
        for headerlines in headers:
            # pick the first item, delete the bracket ">"
            one_acc = headerlines.split()[0].replace(">", "")
            # append it to list
            acc_list.append(one_acc)
        return acc_list
    # test function
    accessions = get_acc(headers)
    #print(accessions)
    
    def get_organisms(fastaheaderfile):
        """
        Reads a text file which contains FASTA headers only
        line by line to find out the organisms.
        Returns a list of organisms.
        
        Parameters:
        -----------
        
        fastaheaderfile : string
        """    
        organisms = []
        for headerlines in headers:
            # delete the first part before the bracket
            oneorganism = headerlines.split("[")[1]
            # delete the other part after the bracket
            oneorganism = oneorganism.replace("]", "")
            organisms.append(oneorganism) 
        return organisms
    # test function
    organisms = get_organisms(headers)
    # print(organisms)
    
    def extract_hitcount(patmatfile):   
        """
        Reads a patmatmotifs file line by line, 
        which contains the number of hitcounts.
        Returns the number of hitcounts.
        
        Parameters:
        -----------
        
        patmatfile : string
            e.g. "seq_2.patmatmotifs"
        """        
        with open(patmatfile) as patfile:
            patfile = patfile.readlines()
        # iterate through lines
        for line in patfile:
            # pick lines that start with "# HitCount"
            if line.startswith("# HitCount"):
                # get index and letter from this line
                for index,letter in enumerate(line):
                    # if it's a digit, pick it
                    if line[index].isdigit():
                        # return the digit
                        return line[index]
    # test the function
    #hitcount = extract_hitcount(f"./output/seq_0.patmatmotifs")
    #print(hitcount)
    #hitcount = extract_hitcount(f"./output/seq_24.patmatmotifs")
    #print(hitcount)
    
    def extract_motifs(patmatfile):   
        """
        Reads a patmatmotifs file line by line, 
        which contains the motif(s).
        Returns a list of motivs.
        If there aren't any motivs, it returns an empty list.
        
        Parameters:
        -----------
        
        patmatfile : string
            e.g. "seq_2.patmatmotifs"
        """        
        with open(patmatfile) as patfile:
            patfile = patfile.readlines()
        # iterate through lines and append motifs in list
        motiflist = []
        for line in patfile:
            # pick lines that start with "Motif"
            if line.startswith("Motif"):
                # delete first part of listelement: "Motif ="
                motifline = line.replace("Motif = ", "")
                # append to list without "\n" in list element
                motiflist.append(motifline.rstrip())
        return motiflist
    # test the function
    #motifs = extract_motifs(f"./output/seq_24.patmatmotifs")
    #print(motifs)
    
    
    # create lists for hitcount, motifs and patfiles
    hitcountlist = []
    motifslist = []
    patfilelist = []
    
    # # check if correct assigned:
    # header_check = []
    
    # loop through each sequences of fastafile
    for count,content in enumerate(fastalist):
        # save into a file
        with open(f"output/seq_{count}.fasta", "w") as eachseqfile:
            # add ">" to header again (needed for patmatmotifs)
            eachseqfile.write(f">{content}")
        # run patmatmotifs for each file
        with open(f"output/seq_{count}.fasta") as eachseqfile:
            # save patmatmotifs as file
            subprocess.call(f"patmatmotifs ./output/seq_{count}.fasta ./output/seq_{count}.patmatmotifs", shell=True)
        # create a list with patmatmotifs files
        patfilelist.append(f"seq_{count}.patmatmotifs")
        
        # pick hitcount from patmatmotifs file and append to file
        hitcount = extract_hitcount(f"./output/seq_{count}.patmatmotifs")
        hitcountlist.append(hitcount)
        
        # pick motifs from patmatmotifs file and append to file
        motifs = extract_motifs(f"./output/seq_{count}.patmatmotifs")
        motifslist.append(motifs)
        
        # # for checking if correct assigned:
        # header_check.append(headers[count])
    
    # # check loop
    # print("\nhitcountlist")
    # print(hitcountlist)
    # print("\nmotifslist")
    # print(motifslist)
    # print("\nheader_check")
    # print(header_check)
    # print("\npatfilelist")
    # print(patfilelist)
    
    # update user
    print("\nA dataframe is being created for you now...")
    
    # write into a dict
    data = {}
    data["accession_number"] = accessions
    data["organism"] = organisms
    data["nr_of_motifs"] = hitcountlist
    data["motifnames"] = motifslist
    data["patmatmotifs_file"] = patfilelist # this is for the user to find the files
    
    # convert into dataframe
    df = pd.DataFrame(data)
    # save as csv file and let the user know
    df.to_csv(f"./output/summary_{userquery}.csv", index=False)
    print(f"\nPlease find the motifs of your sequences in the csv file 'summary_{userquery}.csv' in the folder 'output'.")
    # make sure that user has read this information
    input("Press Enter to continue...")
    
    # move seq data into subfolder to have a better overview and tell user
    source = f"./output/seq_*"
    destination = f"./output/{userquery}_patmatmotif_files"
    # move to folder and tell user
    for file in glob.glob(source):
        shutil.move(file, destination)
    print(f"\nPlease find the FASTA and patmatmotifs files for each sequence in the folder 'output' in the subfolder '{userquery}_patmatmotif_files', in case you want to see each motif in greater detail.")
    # make sure that user has read this information
    input("Press Enter to continue...")
    
    
