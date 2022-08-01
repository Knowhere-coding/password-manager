from sys import exit
from pwinput import pwinput
from pyperclip import copy
from time import sleep, time
from os import system, getcwd
from menu import optionMenu, createAccount, deleteAccount, findAccounts, changeAccount, showAllAccounts, createBackup, createPrintLayout
from database import checkMaster
from initialization import initialization
from fileEncryption import getAESkey
from textFile import logo
from backupHandling import createAutomaticBackup


def main():
    # resize terminal window
    system("mode con cols=240 lines=50")

    # show logo
    print(logo)

    # initialization
    status, masterUsername, masterPassword = initialization()

    # input master username/password
    # for IDE usage:
    #if not status:
    #    masterUsername = input(" Please enter the master username: ")
    #    masterPassword = input(" Please enter the master password: ")

    # for terminal usage:
    if not status:
        masterUsername = pwinput(prompt=" Please enter the master username: ")
        masterPassword = pwinput(prompt=" Please enter the master password: ")

    AES_key = getAESkey(masterPassword)

    # check login
    if not checkMaster(masterUsername, masterPassword, AES_key):
        print(" Wrong master username or password!")
        sleep(10)
        system("cls")
        exit()
    # create automatic backup
    createAutomaticBackup(getcwd() + "/backup/")

    # default overlay
    option, start = optionMenu()

    # handle options
    while True:
        # stop inactivity timer
        stop = time()

        if stop - start > 60:  # inactivity time in sec.
            copy("")  # clear clipboard
            print("\n You have been logged out due to inactivity!")
            sleep(10)
            system("cls")
            exit()
        elif option == "1": # create account
            option = ""
            copy("")  # clear clipboard
            createAccount(AES_key)
            start = time()
        elif option == "2": # delete account data
            option = ""
            copy("")  # clear clipboard
            deleteAccount(AES_key)
            start = time()
        elif option == "3": # find account data
            option = ""
            copy("")  # clear clipboard
            findAccounts(AES_key)
            start = time()
        elif option == "4": # change account data
            option = ""
            copy("")  # clear clipboard
            changeAccount(AES_key)
            start = time()
        elif option == "5": # show all accounts
            option = ""
            copy("")  # clear clipboard
            showAllAccounts(AES_key)
            start = time()
        elif option == "6": # create backup
            option = ""
            copy("") # clear clipboard
            createBackup()
            start = time()
        elif option == "7": # create print layout
            option = ""
            copy("")
            createPrintLayout(AES_key)
            start = time()
        elif option == "Q" or option == "q": # quit
            copy("")  # clear clipboard
            system("cls")
            exit()
        else:
            if option != "":
                findAccounts(AES_key, True, option)
            option, start = optionMenu()


if __name__ == "__main__":
    main()
