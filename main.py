import sys
from art import *
import pwinput
import pyperclip
import time
from menu import optionMenu, createAccount, deleteAccount, findAccounts, changeAccount, showAllAccounts, makeBackup
from database import checkMaster
from initialization import initialization
from passwordManagement import AESkey


tprint("---------------")
tprint("Passwordmanager")
tprint("---------------")

# initialization
status, masterUsername, masterPassword = initialization()

# input master username/password
# for IDE usage:
if not status:
    masterUsername = input(" Please enter the master username: ")
    masterPassword = input(" Please enter the master password: ")

# for terminal usage:
#if not status:
#    masterUsername = pwinput.pwinput(prompt=" Please enter the master username: ")
#    masterPassword = pwinput.pwinput(prompt=" Please enter the master password: ")

AES_key = AESkey(masterPassword)

# check login
if checkMaster(masterUsername, masterPassword, AES_key):
    print(" You're in!")
else:
    print(" Wrong master username or password!")
    time.sleep(10)
    sys.exit()

# default overlay
option, start = optionMenu()

# handle options
while True:
    # stop inactivity timer
    stop = time.time()

    if stop - start > 60:  # inactivity time in sec.
        pyperclip.copy("")  # clear clipboard
        print("You have been logged out due to inactivity!")
        time.sleep(10)
        sys.exit()
    elif option == "1":
        option = ""
        pyperclip.copy("")  # clear clipboard
        createAccount(AES_key)
        start = time.time()
    elif option == "2":
        option = ""
        pyperclip.copy("")  # clear clipboard
        deleteAccount(AES_key)
        start = time.time()
    elif option == "3":
        option = ""
        pyperclip.copy("")  # clear clipboard
        findAccounts(AES_key)
        start = time.time()
    elif option == "4":
        option = ""
        pyperclip.copy("")  # clear clipboard
        changeAccount(AES_key)
        start = time.time()
    elif option == "5":
        option = ""
        pyperclip.copy("")  # clear clipboard
        showAllAccounts(AES_key)
        start = time.time()
    elif option == "6":
        option = ""
        pyperclip.copy("") # clear clipboard
        makeBackup()
        start = time.time()
    elif option == "Q" or option == "q":
        pyperclip.copy("")  # clear clipboard
        sys.exit()
    else:
        option, start = optionMenu()
