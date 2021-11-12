import os
import re
from database import createMasterAccountDatabase
from fileEncryption import hideFile


# initialization (create Username/Password), build directories
def initialization():
    if os.path.isdir("data") and os.path.isfile("data/AES_key.txt.enc") and os.path.isfile("data/master_account_data.csv.enc") and os.path.isfile("data/account_data.csv.enc"):
        return False, "", ""
    else:
        print(" You need to setup your Passwordmanager!")

        # validate username
        # regex -> 4-20 chars / mit a-zA-Z beginndend
        usernamePattern = "^[a-zA-Z]+\w{3,20}$"
        pUsername = re.compile(usernamePattern)

        # username input
        masterUsername = input(" Please input your master username: ")

        while not pUsername.match(masterUsername):
            masterUsername = input(" Please provide a valid username (4-20 chars, starts with char): ")

        # validate password
        # regex -> min. 8 chars / min. 1x: A-Z / a-z / 0-9 / !#$%&'()*+-./:;<=>?@^_`{|}~\]\[]
        passwordPattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[!#$%&'()*+-./:;<=>?@^_`{|}~\]\[]).{8,}$"
        pPassword = re.compile(passwordPattern)

        # password input
        masterPassword = input(" Please input your master password: ")

        while not pPassword.match(masterPassword) or "," in masterPassword:
            masterPassword = input(" Please provide a valid password (8-32 chars, (char,num,specialchar)): ")

        if not os.path.isdir("data"):
            os.mkdir("data")
            hideFile("data")

        if not os.path.isdir("backup"):
            os.mkdir("backup")
            hideFile("backup")

        createMasterAccountDatabase(masterUsername, masterPassword)
        return True, masterUsername, masterPassword
