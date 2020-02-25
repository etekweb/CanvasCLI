# Installs CanvasCLI to hidden folder within home folder
# Request Canvas token, store in encrypted form
# Add location to local path

import os.path
from os import path, system, name
import requests
from getpass import getpass
#import json

authFilePath = os.path.join(os.path.dirname(__file__), 'auth')

# Prepares auth token for HTTP requests
class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

# Function to clear console as needed
def clear(): 
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

# Entry Point: Check if an access token and Canvas URL Root are saved. 
# If it is, import those settings.
# If not, prompt user to input their access token
clear()
print("Welcome to CanvasCLI. \nThis program will allow you to submit assignments directly in Linux shell.\n")
if(path.exists(authFilePath)):
    with open(authFilePath, 'r') as auth:
        token = auth.readline().rstrip()
        root = auth.readline()
else:
    print("You will need to obtain a Canvas access token.")
    print("This acts as your Canvas password, so keep it safe!\n")
    print("To get this, log into Canvas online, go to Account -> Settings, \nscroll to Approved Integrations, and press New Access Token.")
    print("For now, set the token to never expire.\n")
    print("Once you have your token, copy and paste it into this window.")
    token = getpass("Token: ")
#   storeOkay = input("Would you like to save this key for future use? (Y/n)")
    print("What is your Canvas root? To find this, fill in the blank with what your school's URL has: https://_____.instructure.com")
    root = input("Canvas root: ")
#   if(storeOkay == "" or storeOkay.upper() == "Y"):
    with open(authFilePath, 'w') as store:
        store.write(token+'\n')
        store.write(root)
print("Logging into Canvas...")
baseURL = 'https://' + root + '.instructure.com'
courses = requests.get(baseURL + '/api/v1/courses?enrollment_state="active"&per_page=100', auth=(BearerAuth(token)))
clear()
# TODO - if 401 returned, ask for credentials again.
#print(courses.json()[1])
for course in courses.json():
    if 'id' in course and 'name' in course:
        print(str(course['id']) + ": " + course['name'])
