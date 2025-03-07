import pandas as pd
import random
import copy
import os


# WRITE INSTRUCTIONS TO IMPORT CSV

# IMPORT A RANDOM CONVERSATION STARTER (FROM ONLINE FILE +/ WHICH WAS NOT USED BEFORE)

import csv


# path to the CSV files with participant data
# IMPLEMENT NEW CSV FILE (IMPORT FROM INTERNET)
participants_csv = "Coffee Partner Lottery participants.csv"

# header names in the CSV file (name and e-mail of participants)
header_name = "Your name:"
header_email = "Your e-mail:"

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
max_group_size = 14
min_group_size = 2
#group_size = int(input(f"What size do you want the group to be? Please give an integer number between {min_group_size} and {max_group_size}: "))
group_size = 10

if group_size == len(nparticipants)-1:
    group_size = len(nparticipants)
    
else:

    if group_size>max_group_size:
        print(f"The entered group size of {group_size} people is too large! The max group size is {max_group_size} people")
        group_size = max_group_size
        
    elif group_size<min_group_size:
        print(f"The entered group size of {group_size} people is too small! The min group size is {min_group_size} people")
        group_size = min_group_size
        
    elif group_size>len(nparticipants):
        print(f"The entered group size of {group_size} people is too large for the number of people who signed up! The max group size is {len(nparticipants)} people")
        group_size = len(nparticipants)  
      
    else:
        print(f"The entered group size of {group_size} people is confirmed")

print(f"Number of participants: {len(nparticipants)}")
print(f"Goup size: {group_size}")

tries = 0  #Number of tries to find new groups 
End = False
while not new_pairs_found:  
    tries += 1
    # if odd number of participants and group_size is even (or vice versa), create one triple, remaining groups have group_size
    if len(nparticipants)%2 != 0 and group_size%2 == 0 or len(nparticipants)%2 == 0 and group_size%2 != 0 :
        print("In first loop")
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

  
    # while still participants left to group in group_size...
    while len(nparticipants) >= group_size:
        
        plist = []
        for persons in range(group_size):
            p = random.choice(nparticipants)
            nparticipants.remove(p)
            plist.append(p)
        plist.sort()
        npairs.add(tuple(plist))
        
    print(len(nparticipants))    
    if len(nparticipants) == 2:
        print("In 3rd loop")
        # take three random participants from list of participants
        p1 = random.choice(nparticipants)
        nparticipants.remove(p1)
    
        p2 = random.choice(nparticipants)
        nparticipants.remove(p2)
        
        # create alphabetically sorted list of participants
        plist = [p1, p2]
        plist.sort()
                        
        # add alphabetically sorted list to set of pairs
        npairs.add(tuple(plist))
            
    
#        # take group_size random participants from list of participants   OLD CODE
#        p1 = random.choice(nparticipants)
#        nparticipants.remove(p1)
#    
#        p2 = random.choice(nparticipants)
#        nparticipants.remove(p2)
#                
#        # create alphabetically sorted list of participants
#        plist = [p1, p2]
#        plist.sort()
#                        
#        # add alphabetically sorted list to set of pairs
#        npairs.add(tuple(plist))
      

    # check if all new pairs are indeed new, else reset
    if npairs.isdisjoint(opairs):
        new_pairs_found = True
    else:
        npairs = set()
        nparticipants = copy.deepcopy(participants)
        
    if tries > 100:
        print("No new group cominations possible. Please clear 'All pairs' document or add new participants!")
        End = True
        break

if not End:
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
