import pandas as pd
import random
import copy
import os


# WRITE INSTRUCTIONS TO IMPORT CSV

# INSTRUCTIONS ON WHERE TO FIND THE SIGN UP FORM
url_form = "https://forms.gle/W8XpQSZdBfpMQmij6"
print(f"Welcome to the program for the coffee meeting pairing. To let people participate in the meetings, make sure they sign up through this form ({url_form})")

# INSTRUCTIONS ON HOW TO DOWNLOAD THE CSV FILE FROM THE GOOGLE FORM (CHANGE IF WE MANAGE TO IMPORT DIRECTLY FROM INTERNET)
print("To run the program, a csv file with the names and emails of the participants needs to be downloaded. To do so, go to the google form and in the 'responses' tab, download the responses as a csv file.")
print("Make sure you save the csv file in the same folder as this program, otherwise the program will not be able to access it.")
print("Also make sure that the names in the csv file are stored in a column with the header 'Name', and the emails under 'E-mail'.")

# (WE CAN ALSO MAKE THE PROGRAM STOP AUTOMATICALLY BUT I THINK WE HAVE TO PUT THE ENTIRE CODE IN A LOOP SO DIDN'T DO THAT NOW)
input("If you have completed the steps above type 'start', if not, please stop the program and follow the instructions first.")

# IMPORT A RANDOM CONVERSATION STARTER (FROM ONLINE FILE +/ WHICH WAS NOT USED BEFORE)

import csv

# IMPLEMENT NEW CSV FILE 
# (IMPORT FROM INTERNET)
# sheet_id = "2PACX-1vRFAUb3UXMtBLyRIG-34OdQOod1WdQEceKBohQCpq5kowvdZeWsBKSLonZRG3oTcehGtqQTLlTAFE_u"
# url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRFAUb3UXMtBLyRIG-34OdQOod1WdQEceKBohQCpq5kowvdZeWsBKSLonZRG3oTcehGtqQTLlTAFE_u/pub?output=csv"

# participants_csv = pd.read_csv(url)
# print(participants_csv)

# path to the CSV files with participant data
# FROM DOWNLOADED CSV
participants_csv = "Coffee meeting form.csv" # REPLACE THIS LINE WITH THE IMPORT FROM INTERNET PART IF THAT WORKS

# header names in the CSV file (name and e-mail of participants)
header_name = "Name"
header_email = "E-mail"

# path to TXT file that stores the pairings of this round
new_pairs_txt = "Coffee Partner Lottery new pairs.txt"

# path to CSV file that stores the pairings of this round
new_pairs_csv = "Coffee Partner Lottery new pairs.csv"

# path to CSV file that stores all pairings (to avoid repetition)
all_pairs_csv = "Coffee Partner Lottery all pairs.csv"
        
# init set of old pairs
opairs = set()

DELIMITER=','

# load all previous pairings (to avoid redundancies)
if os.path.exists(all_pairs_csv):
    with open(all_pairs_csv, "r") as file:
        csvreader = csv.reader(file, delimiter=DELIMITER)
        for row in csvreader:
            group = []
            for i in range(0,len(row)):
                group.append(row[i])                        
            opairs.add(tuple(group))

# load participant's data
formdata = pd.read_csv(participants_csv, sep=DELIMITER)

# create duplicate-free list of participants
participants = list(set(formdata[header_email]))

 # init set of new pairs
npairs = set()

# running set of participants
nparticipants = copy.deepcopy(participants)

# Boolean flag to check if new pairing has been found
new_pairs_found = False

# try creating new pairing until successful 
# IMPLEMENT USER INPUT GROUP SIZE AND RANDOM ASSIGNMENT (CHECK IF ALSO RANDOM WITH BIGGER GROUPS AND MORE PEOPLE)
while not new_pairs_found:   # to do: add a maximum number of tries
  
    # if odd number of participants, create one triple, then pairs
    if len(participants)%2 != 0:
        
        # take three random participants from list of participants
        p1 = random.choice(nparticipants)
        nparticipants.remove(p1)
    
        p2 = random.choice(nparticipants)
        nparticipants.remove(p2)
        
        p3 = random.choice(nparticipants)
        nparticipants.remove(p3)
        
        # create alphabetically sorted list of participants
        plist = [p1, p2, p3]
        plist.sort()
                        
        # add alphabetically sorted list to set of pairs
        npairs.add(tuple(plist))

  
    # while still participants left to pair...
    while len(nparticipants) > 0:

        # take two random participants from list of participants
        p1 = random.choice(nparticipants)
        nparticipants.remove(p1)
    
        p2 = random.choice(nparticipants)
        nparticipants.remove(p2)
                
        # create alphabetically sorted list of participants
        plist = [p1, p2]
        plist.sort()
                        
        # add alphabetically sorted list to set of pairs
        npairs.add(tuple(plist))

 
    # check if all new pairs are indeed new, else reset
    if npairs.isdisjoint(opairs):
        new_pairs_found = True
    else:
        npairs = set()
        nparticipants = copy.deepcopy(participants)


# assemble output for printout
# PRINT GROUPS ON SCREEN
# MSG TO GROUP IN INDIVIDUAL TXT FILES; INCLUDING CONVERSATION STARTER (SEND OUT BY MAIL)
output_string = ""

output_string += "------------------------\n"
output_string += "Today's coffee partners:\n"
output_string += "------------------------\n"

for pair in npairs:
    pair = list(pair)
    output_string += "* "
    for i in range(0,len(pair)):
        name_email_pair = f"{formdata[formdata[header_email] == pair[i]].iloc[0][header_name]} ({pair[i]})"
        if i < len(pair)-1:
            output_string += name_email_pair + ", "
        else:
            output_string += name_email_pair + "\n"
    
# write output to console
print(output_string)

# write output into text file for later use
with open(new_pairs_txt, "wb") as file:
    file.write(output_string.encode("utf8"))

# write new pairs into CSV file (for e.g. use in MailMerge)
with open(new_pairs_csv, "w") as file:
    header = ["name1", "email1", "name2", "email2", "name3", "email3"]
    file.write(DELIMITER.join(header) + "\n")
    for pair in npairs:
        pair = list(pair)
        for i in range(0,len(pair)):
            name_email_pair = f"{formdata[formdata[header_email] == pair[i]].iloc[0][header_name]}{DELIMITER} {pair[i]}"
            if i < len(pair)-1:
                file.write(name_email_pair + DELIMITER + " ")
            else:
                file.write(name_email_pair + "\n")
            
# append pairs to history file
if os.path.exists(all_pairs_csv):
    mode = "a"
else:
    mode = "w"

with open(all_pairs_csv, mode) as file:
    for pair in npairs:
        pair = list(pair)
        for i in range(0,len(pair)):
            if i < len(pair)-1:
                file.write(pair[i] + DELIMITER)
            else:
                file.write(pair[i] + "\n")


             
# print finishing message
print()
print("Job done.")
