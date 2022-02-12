import sys
from art import tprint
import pwinput
import pyperclip
import time
import os
from menu import optionMenu, createAccount, deleteAccount, findAccounts, changeAccount, showAllAccounts, makeBackup, systemMessage
from database import checkMaster
from initialization import initialization
from passwordManagement import AESkey
import textFile

# resize terminal window
os.system("mode con cols=200 lines=50")

# show logo
print(textFile.logo)

# initialization
status, masterUsername, masterPassword = initialization()

# input master username/password
# for IDE usage:
#if not status:
#    masterUsername = input(" Please enter the master username: ")
#    masterPassword = input(" Please enter the master password: ")

# for terminal usage:
if not status:
    masterUsername = pwinput.pwinput(prompt=" Please enter the master username: ")
    masterPassword = pwinput.pwinput(prompt=" Please enter the master password: ")

AES_key = AESkey(masterPassword)

# check login
if checkMaster(masterUsername, masterPassword, AES_key):
    systemMessage = " You're in!"
else:
    print(" Wrong master username or password!")
    time.sleep(10)
    os.system("cls")
    sys.exit()

# default overlay
option, start = optionMenu()

# handle options
while True:
    # stop inactivity timer
    stop = time.time()

    if stop - start > 60:  # inactivity time in sec.
        pyperclip.copy("")  # clear clipboard
        print(" You have been logged out due to inactivity!")
        time.sleep(10)
        sys.exit()
    elif option == "1": # create account
        option = ""
        pyperclip.copy("")  # clear clipboard
        createAccount(AES_key)
        start = time.time()
    elif option == "2": # delete account data
        option = ""
        pyperclip.copy("")  # clear clipboard
        deleteAccount(AES_key)
        start = time.time()
    elif option == "3": # find account data
        option = ""
        pyperclip.copy("")  # clear clipboard
        findAccounts(AES_key)
        start = time.time()
    elif option == "4": # change account data
        option = ""
        pyperclip.copy("")  # clear clipboard
        changeAccount(AES_key)
        start = time.time()
    elif option == "5": # show all accounts
        option = ""
        pyperclip.copy("")  # clear clipboard
        showAllAccounts(AES_key)
        start = time.time()
    elif option == "6": # make backup
        option = ""
        pyperclip.copy("") # clear clipboard
        makeBackup()
        start = time.time()
    elif option == "Q" or option == "q": # quit
        pyperclip.copy("")  # clear clipboard
        os.system("cls")
        sys.exit()
    else:
        if option != "":
            findAccounts(AES_key, True, option)
        option, start = optionMenu()
