# Installs CanvasCLI to hidden folder within home folder
# Request Canvas token, store in encrypted form
# Add location to local path

import os.path
from os import path

print("Welcome to CanvasCLI. This program will allow you to submit assignments directly in Linux shell.")
if(path.exists('auth')):
    with open('auth', 'r') as auth:
        token = auth.read()
else:
    print("You will need to obtain a Canvas access token. This acts as your Canvas password, so keep it safe!")
    print("To do this, log into Canvas online, go to Account -> Settings, scroll to Approved Integrations, and press New Access Token.")
    print("Your token can be optionally be set to expire. If set, when it expires, you will need to do this process again.")
    print("Once you have your token, copy and paste it into this window.")
    token = input("Token: ")
    storeOkay = input("Would you like to save this key for future use? (Y/n)")
    if(storeOkay == "" or storeOkay.upper() == "Y"):
        with open('auth', 'w') as store:
            store.write(token)
print("Logging into Canvas...")
