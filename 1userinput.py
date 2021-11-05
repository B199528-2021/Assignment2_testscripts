#!/usr/local/bin/python3

import os, sys, subprocess, shutil

# # test the query with test set 
# os.system(
# "esearch -db protein -query 'glucose-6-phosphatase[PROT] AND aves[ORGN]' | efetch -format fasta > ./efetch/testset.fasta"
# )

# save user input into variables
print("Please enter first the protein family and then the taxonomic group.")
prot_fam = input("Protein family:\n")


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
        should have only one condition (without "AND" or "OR")
        e.g. "esearch -db protein -query 'glucose-6-phosphatase[PROT]'"
    """
    os.system(
    f"{query} > esearchoutput.txt"
    )
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

# search the query separately
prot_fam_query = f"esearch -db protein -query '{prot_fam}[PROT]'"
# check the number of hits 
prot_fam_hits = count_nr_of_esearch_hits(prot_fam_query)

# repeat user input as long as the number of hits is zero
while prot_fam_hits == 0:
    print(f"\nYou have probably mistyped the protein family, because there are no hits for you query.")
    prot_fam = input("Please try again. Type in the PROTEIN FAMILY:\n")
    prot_fam_query = f"esearch -db protein -query '{prot_fam}[PROT]'"
    prot_fam_hits = count_nr_of_esearch_hits(prot_fam_query)

print(f"The number of hits is {prot_fam_hits}.")
print(f"Your chosen protein family is '{prot_fam}'.\n")


# go on with taxonomic group
print("Please enter the taxonomic group now.")
tax_group = input("Taxonomic group:\n")

# search the query separately
tax_group_query = f"esearch -db protein -query '{tax_group}[ORGN]'"
# check the number of hits 
tax_group_hits = count_nr_of_esearch_hits(tax_group_query)

# repeat user input as long as the number of hits is zero
while tax_group_hits == 0:
    print(f"\nYou have probably mistyped the taxonomic group, because there are no hits for you query.")
    tax_group = input("Please try again. Type in a valid TAXONOMIC GROUP:\n")
    tax_group_query = f"esearch -db protein -query '{tax_group}[ORGN]'"
    tax_group_hits = count_nr_of_esearch_hits(tax_group_query)

print(f"The number of hits is {tax_group_hits}.")
print(f"Your chosen taxonomic group is '{tax_group}'.\n")



print("FINISHED.")