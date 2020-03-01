# Installs CanvasCLI to hidden folder within home folder
# Request Canvas token, store in encrypted form
# Add location to local path

import os.path
from os import path, system, name
import requests
from getpass import getpass
import sys

authFilePath = os.path.join(os.path.dirname(__file__), 'auth')
token = ""
root = ""

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

# Function to set up new auth file
# Sets token and auth to be user inputs
def setUp():
    print("You will need to obtain a Canvas access token.")
    print("This acts as your Canvas password, so keep it safe!\n")
    print("To get this, log into Canvas online, go to Account -> Settings, \nscroll to Approved Integrations, and press New Access Token.")
    print("For now, set the token to never expire.\n")
    print("Once you have your token, copy and paste it into this window.")
    global token
    token = getpass("Token: ")
#   storeOkay = input("Would you like to save this key for future use? (Y/n)")
    print("What is your Canvas root? To find this, fill in the blank with what your school's URL has: https://_____.instructure.com")
    global root
    root = input("Canvas root: ")
#   if(storeOkay == "" or storeOkay.upper() == "Y"):
    with open(authFilePath, 'w') as store:
        store.write(token+'\n')
        store.write(root)

def submitFileUpload(apiurl, course, assn, file, filename):
    # print(apiurl, course, assn, file)
    preuploadRes = requests.post(apiurl + '/api/v1/courses/' + str(course) + '/assignments/' + str(assn) + '/submissions/self/files', data={'name': filename}, auth=(BearerAuth(token)))
    params = preuploadRes.json()['upload_params']
    uploadRes = requests.post(preuploadRes.json()['upload_url'], files={'file': file}, data=params)
    verifyRes = requests.get(uploadRes.json()['location'], auth=(BearerAuth(token)))
    submitParams = {'submission': {'submission_type': 'online_upload', 'file_ids': [uploadRes.json()['id']]}}
    submitRes = requests.post(apiurl + '/api/v1/courses/' + str(course) + '/assignments/' + str(assn) + '/submissions', json=submitParams, auth=(BearerAuth(token)))
    print(submitRes.status_code)
    if(submitRes.status_code > 199 and submitRes.status_code < 300):
        print('Uploaded and submitted successfully.')

# SCRIPT STARTS HERE
# Login: Check if an access token and Canvas URL Root are saved. 
# If it is, import those settings to define token and auth.
# If not, run set up function.
clear()
print("Welcome to CanvasCLI. \nThis program will allow you to submit assignments directly in Linux shell.\n")
if(path.exists(authFilePath)):
    with open(authFilePath, 'r') as auth:
        token = auth.readline().rstrip()
        root = auth.readline()
else:
    setUp()

# Logging in, token and auth should now be defined
print("Logging into Canvas...")

# Get Courses
baseURL = 'https://' + root + '.instructure.com'
courses = requests.get(baseURL + '/api/v1/courses?enrollment_state="active"&per_page=100', auth=(BearerAuth(token)))
clear()
# TODO - if 401 returned, ask for credentials again.
for i, course in enumerate(courses.json(), start=0):
    if 'id' in course and 'name' in course:
        print(str(i) + ": " + course['name'])
courseIndex = int(input("\nSelect Course Number: "))
courseID = courses.json()[courseIndex]['id']
# TODO - remember last class, store as default in auth file

# Get Assignments for Course
assignments = requests.get(baseURL + '/api/v1/courses/' + str(courseID) + '/assignments/?per_page=100', auth=(BearerAuth(token)))
clear()
# TODO - handle error cases
numOfSubmittableAssignments = 0
for i, assignment in enumerate(assignments.json(), start=0):
    if('online_upload' in assignments.json()[i]['submission_types']):
        print(str(i) + ": " + assignment['name'])
        numOfSubmittableAssignments = numOfSubmittableAssignments + 1
if(numOfSubmittableAssignments == 0):
    print("There are no submittable assignments for this course.")
    quit()
assignmentIndex = int(input("\nSelect Assignment Number: "))
assignmentID = assignments.json()[assignmentIndex]['id']

if('online_upload' in assignments.json()[assignmentIndex]['submission_types']):
    if(len(sys.argv) > 1):        
        try:
            file = open(sys.argv[1], mode='rb').read()
            filename = open(sys.argv[1]).name
            submitFileUpload(baseURL, courseID, assignmentID, file, filename)
        except IOError:
            print("File specified in command line was not found: " + sys.argv[1])
    else:
        print("A file was not specified to submit. Ending here.")
else:
    print("You cannot submit to this assignment.")
    
# TODO - separate upcoming and/or unsubmitted assignments, set next due to default

# TODO - Get file to upload from parameters
# TODO - Upload to Canvas -- see https://canvas.instructure.com/doc/api/file.file_uploads.html
#  - requires getting presigned URL from Canvas endpoint
# TODO - Error handling and input checking of all sections
