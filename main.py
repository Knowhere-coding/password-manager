import sys
from art import *
import pwinput
import time
from menu import optionMenu, createAccount, deleteAccount, findAccounts, changeAccount, showAllAccounts
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
    masterUsername = input("Please enter the master username: ")
    masterPassword = input("Please enter the master password: ")

# for terminal usage:
# TODO: position indicator while typing a password/username - ✓
#if not status:
#    masterUsername = pwinput.pwinput(prompt="Please enter the master username: ")
#    masterPassword = pwinput.pwinput(prompt="Please enter the master password: ")

AES_key = AESkey(masterPassword)

# check login
if checkMaster(masterUsername, masterPassword, AES_key):
    print("You're in!")
else:
    print("Wrong master username or password!")
    time.sleep(10)
    sys.exit()

# default overlay
option = optionMenu()

# handle options
while True:
    if option == "1":
        option = ""
        createAccount(AES_key)
    elif option == "2":
        option = ""
        deleteAccount(AES_key)
    elif option == "3":
        option = ""
        findAccounts(AES_key)
    elif option == "4":
        option = ""
        #changeAccount(AES_key) # TODO: change account data
    elif option == "5":
        option = ""
        showAllAccounts(AES_key)
    elif option == "Q" or option == "q":
        sys.exit()
    else:
        option = optionMenu()
