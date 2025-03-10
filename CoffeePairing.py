import pandas as pd
import random
import copy
import os


# WRITE INSTRUCTIONS TO IMPORT CSV

# INSTRUCTIONS ON WHERE TO FIND THE SIGN UP FORM
url_form = "https://forms.gle/W8XpQSZdBfpMQmij6"
print(f"Welcome to the program for the coffee meeting pairing. To let people participate in the meetings, make sure they sign up through this form ({url_form})")
print("------------------------\n")

# INSTRUCTIONS ON HOW TO DOWNLOAD THE CSV FILE FROM THE GOOGLE FORM (CHANGE IF WE MANAGE TO IMPORT DIRECTLY FROM INTERNET)
print("To run the program, a csv file with the names and emails of the participants needs to be downloaded. To do so, go to the google form and in the 'responses' tab, download the responses as a csv file.")
print("Make sure you save the csv file in the same folder as this program, otherwise the program will not be able to access it.")
print("Also make sure that the names in the csv file are stored in a column with the header 'Name', and the emails under 'E-mail'.")

# (DON'T THINK THIS WILL SUFFICE AS IMPORT NEW USERS EVERY ROUND BUT IF WE MANAGE TO LINK THE ONLINE FILE IT WILL BE AUTOMATED)
print("Lastly, if this is not the first round of meetings and new participant signed up since the previous round, download the csv again.")
print("------------------------\n")

# (WE CAN ALSO MAKE THE PROGRAM STOP AUTOMATICALLY BUT I THINK WE HAVE TO PUT THE ENTIRE CODE IN A LOOP SO DIDN'T DO THAT NOW)
#input("If you have completed the steps above type 'start', if not, please stop the program and follow the instructions first.")

# IMPORT A RANDOM CONVERSATION STARTER (FROM ONLINE FILE +/ WHICH WAS NOT USED BEFORE)

import csv

# IMPLEMENT NEW CSV FILE 
# (IMPORT FROM INTERNET)
# sheet_id = "2PACX-1vRFAUb3UXMtBLyRIG-34OdQOod1WdQEceKBohQCpq5kowvdZeWsBKSLonZRG3oTcehGtqQTLlTAFE_u"
# url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRFAUb3UXMtBLyRIG-34OdQOod1WdQEceKBohQCpq5kowvdZeWsBKSLonZRG3oTcehGtqQTLlTAFE_u/pub?output=csv"

# participants_csv = pd.read_csv(url)
# print(participants_csv)

conversation_starters = []
with open('conversation_starters.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    header = next(csvreader) #skip the header row
    for row in csvreader:
        conversation_starters.append(row[1])

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

# path to csv file that stores the messages sent to all groups
msg_to_groups = "Message to groups.txt"


        
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
max_group_size = 13
min_group_size = 2
group_size = int(input(f"What size do you want the groups to be? We try to consider your preferences. If not possible, the group size is changed automatically. Please give an integer number between {min_group_size} and {max_group_size}: "))
#group_size = 14
OG_group_size = True #Boolean used to see if the entered group size is used
print(f"Entered group size: {group_size}")

# resets the group size if necessary

if group_size >= min_group_size and group_size <= max_group_size:
    if group_size == len(nparticipants)-1:
        if len(nparticipants) >= max_group_size:
            group_size = len(nparticipants)-2
            OG_group_size = False
        else:
            group_size = len(nparticipants)
            OG_group_size = False
        
elif group_size < min_group_size:
    group_size = min_group_size
    OG_group_size = False
    if group_size == len(nparticipants)-1:
        group_size = len(nparticipants)

elif group_size > max_group_size:
    group_size = max_group_size
    OG_group_size = False
    if group_size == len(nparticipants)-1:
        group_size = len(nparticipants) -2


# Checks if original group size is used  
if OG_group_size:
    print(f"The entered group size of {group_size} people is confirmed")
else:
    print(f"The group size has been changed to {group_size} people!")

print(f"Number of participants: {len(nparticipants)}")

tries = 0  #Number of tries to find new groups 
End = False # Boolean used to break out of the loop if tries exceeds maximum

while not new_pairs_found:  
    tries += 1
    # if odd number of participants and group_size is even (or vice versa), create one triple, remaining groups have either group_size or are in a groups of 2
    if len(nparticipants)%2 != 0 and group_size%2 == 0 or len(nparticipants)%2 == 0 and group_size%2 != 0 :
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
         
    while len(nparticipants)%2 == 0 and len(nparticipants) > 0:
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
            
    
    # check if all new pairs are indeed new, else reset
    if npairs.isdisjoint(opairs):
        new_pairs_found = True
    else:
        npairs = set()
        nparticipants = copy.deepcopy(participants)
    
    #if the loop is run through more than 100 times, then it is assumed that there are no more possible group divisions which have not been made before
    if tries > 100:
        print("No new group combinations possible. Please clear 'All pairs' document or add new participants!")
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
    
    #this is to select a random conversation starter for each group
    random_conversation_starters = random.choice(conversation_starters)
        
    for pair in npairs:
        pair = list(pair)
        output_string += "* "
        for i in range(0,len(pair)):
            name_email_pair = f"{formdata[formdata[header_email] == pair[i]].iloc[0][header_name]} ({pair[i]})"
            if i < len(pair)-1:
                output_string += name_email_pair + ", "
            else:
                output_string += name_email_pair + "\n"
        
        #this is to add the random conversation starter to the output string
        output_string += f"Conversation starter: {random_conversation_starters}\n\n"
    
                    
    with open(msg_to_groups, "w") as file:  
        #header = ["name1", "email1", "name2", "email2", "name3", "email3"]    
        #file.write(DELIMITER.join(header) + "\n")
        for pair in npairs:
            pair = list(pair)
            for i in range(0,len(pair)):
                #name_email_pair = f"{formdata[formdata[header_email] == pair[i]].iloc[0][header_name]}{DELIMITER} {pair[i]}"   #This outputs name + email
                name_email_pair = formdata[formdata[header_email] == pair[i]].iloc[0][header_name]                              #This outputs only the name)
                if i ==0:
                    file.write("Dear ")
                    file.write(name_email_pair)
                elif i < len(pair)-1 :
                    file.write(DELIMITER + " dear " + name_email_pair)
                else:
                    file.write(" and dear " + name_email_pair + "\n")
                    if len(pair) == 2:
                        X = "The"
                    else:
                        X = "All"
                    file.write(f"{X} {len(pair)} of you have been put together in today's group. The conversation starter is: {random_conversation_starters}\n")
                    file.write("------------------------------------------------------------------------------------------------------------------------------------------------------\n")
                    
    
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



















