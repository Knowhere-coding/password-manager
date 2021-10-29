import os
import re
from database import createMasterAccountDatabase


# initialization (create Username/Password), build directories
def initialization():
    if os.path.isdir("data"):
        return False, "", ""
    else:
        print("You need to setup your Passwordmanager!")

        # validate username
        # regex -> 4-20 chars / mit a-zA-Z beginndend
        usernamePattern = "^[a-zA-Z]+\w{3,20}$"
        pUsername = re.compile(usernamePattern)

        # username input
        masterUsername = input("Please input your master username: ")

        while not pUsername.match(masterUsername):
            masterUsername = input("Please provide a valid username (4-20 chars, starts with char): ")

        # validate password
        # regex -> min. 8 chars / min. 1x: A-Z / a-z / 0-9 / !#$%&'()*+-./:;<=>?@^_`{|}~\]\[]
        passwordPattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[!#$%&'()*+-./:;<=>?@^_`{|}~\]\[]).{8,}$"
        pPassword = re.compile(passwordPattern)

        # password input
        masterPassword = input("Please input your master password: ")

        while not pPassword.match(masterPassword) or "," in masterPassword:
            masterPassword = input("Please provide a valid password (8-32 chars, (char,num,specialchar)): ")

        os.mkdir("data")
        createMasterAccountDatabase(masterUsername, masterPassword)
        return True, masterUsername, masterPassword
