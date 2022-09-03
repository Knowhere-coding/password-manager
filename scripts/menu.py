from pwinput import pwinput
from pyperclip import copy
from time import time
from os import system, getcwd, startfile, path, mkdir, listdir
from datetime import datetime, timedelta
from colorama import init
from termcolor import colored
from webbrowser import open_new_tab
from textFile import logo
from passwordManagement import createNewPassword
from database import storeData, deleteData, findData, changeData, showDatabase, databaseStatus, checkMasterPassword, \
    checkMaster, getIndices, getColumnData, getRowData
from printLayout import createPrintLayoutFile
from fileHandling import hideFile
from fileEncryption import getAESkey
from backupHandling import createBackupFile, loadBackupFile

# initialize termcolor to work on windows
init()
systemMessage = ""


# default overlay
def optionMenu():
    global systemMessage
    system("cls")

    # show logo
    print(logo)

    # start inactivity timer
    start = time()

    # show system message
    if systemMessage != "":
        print("-" * 30)
        print(systemMessage)
        print("-" * 30)
        systemMessage = ""

    print('-' * 30)
    print(('-' * 12) + " Menu " + ('-' * 12))
    print(" 1 - Create a new {}".format(colored("account", "cyan")))
    print(" 2 - Delete an {}".format(colored("account", "cyan")))
    print(" 3 - Find your {}".format(colored("account data", "cyan")))
    print(" 4 - Change your {}".format(colored("account data", "cyan")))
    print(" 5 - Show all your {}".format(colored("accounts", "cyan")))
    print(" 6 - {} menu".format(colored("Backup", "cyan")))
    print(" 7 - Create {}".format(colored("print layout", "cyan")))
    print(" Q - {}".format(colored("Exit", "cyan")))
    print('-' * 30)
    return input(" > "), start


# give the user a choice
def choicePrompt():
    choice = input(" > ")
    return True if choice.upper() == "Y" else False


# copy data to clipboard
def copyToClipboard(msg):
    copy(msg)
    print('-' * 47)
    print("")
    print(" Your {} has been copied to your {}".format(colored("password", "green"), colored("clipboard", "cyan")))
    print("")
    print('-' * 47)


# open url
def openUrl(url):
    # open url
    print("\n Do you want to open the {}? (Y/N):".format(colored("url", "green")))
    choice = choicePrompt()

    if choice:
        open_new_tab("https://" + url)


# create/change password
def passwordOption():
    # option to generate random password
    print("\n Do you want to generate a random {}? (Y/N):".format(colored("password", "green")))
    choice = choicePrompt()

    # generate random password
    if choice:
        minLength, maxLength = getMinMaxLength()
        specialChars = getSpecialChars()
        password = createNewPassword(minLength, maxLength, specialChars)
    # provide own password
    else:
        print("\n Please provide your own {}:".format(colored("password", "green")))
        password = pwinput(prompt=" > ")

    return password


# let the user define valid special chars for the random generated password
def getSpecialChars():
    print("\n Please specify the given {} besides all letters and digits (if none type -):".format(
        colored("special characters", "green")))
    return input(" > ")


# let the user define the minimum and maximum length of the random generated password
def getMinMaxLength():
    minLength = 0
    maxLength = 0

    try:
        print("\n Please specify the {} length of the password:".format(colored("minimum", "red")))
        minLength = int(input(" > "))
        print("\n Please specify the {} length of the password:".format(colored("maximum", "green")))
        maxLength = int(input(" > "))
    except ValueError:
        print("\n Please input numbers!")

    while minLength <= 0 or maxLength < minLength or maxLength > 64:
        if minLength <= 0:
            print("\n The minimum value can not be 0 or negative!")
        elif maxLength < minLength:
            print("\n The minimum value can not be higher than the maximum value!")
        elif maxLength > 64:
            print("\n The maximum length of the password is 64!")

        try:
            print("\n New {}:".format(colored("minimum", "red")))
            minLength = int(input(" > "))
            print("\n New {}:".format(colored("maximum", "green")))
            maxLength = int(input(" > "))
        except ValueError:
            print("\n Please input numbers!")

    if maxLength > 32:
        print("\n Secure is not enough for you, right? :D")
    return minLength, maxLength


def showOptions(options):
    for key in options:
        print("   {} - {}".format(key, colored(options[key], "white")))
    userInput = input(" > ")
    while userInput not in [str(x) for x in options.keys()]:
        userInput = input(" > ")
    return options[int(userInput)]


# check change date and change password
def checkExpirationDate(ID, changeDate, expiration, AES_key):
    global systemMessage
    if not expiration == "0":
        changeDate = datetime.strptime(changeDate, "%Y-%m-%d %H:%M:%S")

        if (changeDate + timedelta(days=int(expiration))) < datetime.now():
            print("\n {} The password-change-date is more than {} days ago {}".format(colored("!!!", "red"), expiration,
                                                                                    colored("!!!", "red")))
            print("\n Do you want to change the {}? (Y/N):".format(colored("password", "green")))
            choice = choicePrompt()
            if choice:
                password = passwordOption()
                if passwordBarrier(AES_key):
                    changeData(ID, "password", password, AES_key)
                    return password
                else:
                    systemMessage = " The given password was incorrect!"
            return ""
        else:
            return ""
    return ""


# password barrier for changing/deleting data from the database
def passwordBarrier(AES_key):
    masterPassword = pwinput(prompt="\n Please provide your master password: ")
    return checkMasterPassword(masterPassword, AES_key)


# account barrier for loading backup
def accountBarrier():
    print("\n To load the backup you need to {} your account!".format(colored("verify", "red")))
    masterUsername = pwinput(prompt=" Please enter the master username: ")
    masterPassword = pwinput(prompt=" Please enter the master password: ")
    if checkMaster(masterUsername, masterPassword, getAESkey(masterPassword)):
        AES_key = getAESkey(masterPassword)
        return True


# option 1 - create new account
def createAccount(AES_key):
    # category
    print("\n Choose the {} for your new account:".format(colored("category", "green")))
    category = showOptions(
        {1: "email", 2: "social media", 3: "gaming", 4: "coding", 5: "shopping", 6: "banking", 7: "education",
         8: "private", 9: "other"})

    # site name
    print("\n Please provide the {} (e.g. reddit) you want to create a new account for:".format(
        colored("site name", "green")))
    siteName = input(" > ")

    # url
    print("\n Please provide the {} (e.g. www.example.com/login) to the site:".format(colored("login url", "green")))
    url = input(" > ")

    # username
    print("\n Please provide a {} (if applicable):".format(colored("username", "green")))
    username = input(" > ")
    if not username:
        username = ""

    # email
    print(
        "\n Please provide an {} or select an existing {}:".format(colored("email", "green"), colored("email", "green")))
    options = {key: value for (key, value) in enumerate(getColumnData("email", AES_key), 1)}
    for key in options:
        print("   {} - {}".format(key, colored(options[key], "white")))
    userInput = input(" > ")
    if userInput in [str(x) for x in options.keys()]:
        email = options[int(userInput)]
    else:
        email = userInput

    # password
    password = passwordOption()

    # expiration date
    print("\n Choose the {} of your password:".format(colored("expiration period (in days)", "green")))
    expiration = showOptions({1: 1, 2: 7, 3: 30, 4: 90, 5: 365, 6: 0})

    if storeData(siteName, url, username, email, password, expiration, category, AES_key):
        copyToClipboard(password)


# option 2 - delete account
def deleteAccount(AES_key):
    global systemMessage
    if databaseStatus(AES_key):
        showDatabase(AES_key)
        print("\n Please provide the {} of the account you want to delete:".format(colored("ID", "red")))
        ID = input(" > ")

        if ID not in getIndices(AES_key):
            systemMessage = " The ID doesn't exists!"
            return

        print("\n Are you sure you want to {} the {} account? (Y/N):".format(colored("delete", "red"),
                                                                           colored(getRowData(ID, AES_key)["siteName"],
                                                                                   "green")))
        choice = choicePrompt()
        if choice:
            if passwordBarrier(AES_key):
                deleteData(ID, AES_key)
            else:
                systemMessage = " The given password was incorrect!"


# option 3 - find account data
def findAccounts(AES_key, shortcut=False, shortcutInput=None):
    # field name
    output = None
    # result
    results = None
    # account indices
    indices = None

    if shortcut:
        results, indices = findData("siteName", shortcutInput, AES_key, output)
    elif databaseStatus(AES_key):
        print("\n Please select the {} you want to search for:".format(colored("field name", "green")))
        searchingField = showOptions(
            {1: "siteName", 2: "url", 3: "username", 4: "email", 5: "password", 6: "expiration", 7: "category"})
        # value
        if searchingField == "category":
            print("\n Choose the {} you want to search for:".format(colored("category", "green")))
            searchingValue = showOptions(
                {1: "email", 2: "social media", 3: "gaming", 4: "coding", 5: "shopping", 6: "banking", 7: "education",
                 8: "private", 9: "other"})
        elif searchingField == "expiration":
            print("\n Choose the {} you want to search for:".format(colored("expiration period (in days)", "green")))
            searchingValue = str(showOptions({1: 1, 2: 7, 3: 30, 4: 90, 5: 365, 6: 0}))
            output = ["ID", "siteName", "username", "email", "password", "expiration", "category"]
        elif searchingField == "password":
            print("\n Please provide the {} you wanna search for:".format(colored(searchingField, "green")))
            searchingValue = pwinput(prompt=" > ")
        else:
            if searchingField == "url":
                output = ["ID", "siteName", "url", "username", "email", "password", "category"]
            print("\n Please provide the {} you wanna search for:".format(colored(searchingField, "green")))
            searchingValue = input(" > ")

        results, indices = findData(searchingField, searchingValue, AES_key, output)

    if results:
        if shortcut and len(results) == 1:
            print("\n Automatically selected Account {}!".format(colored(results[0]["ID"], "cyan")))
            index = 0
        else:
            print("\n Select the {} of your account or press {} to go back to the menu: ".format(colored("ID", "red"),
                                                                                               colored("ENTER", "red")))
            accountNum = input(" > ")

            if not accountNum:
                return
            while accountNum not in indices:
                print("\n The ID is not available, try again!")
                accountNum = input(" > ")
                if not accountNum:
                    return
            index = indices.index(accountNum)

        password = checkExpirationDate(results[index]["ID"], results[index]["changeDate"], results[index]["expiration"],
                                       AES_key)
        if password == "":
            copyToClipboard(results[index]["password"])
        else:
            copyToClipboard(password)

        openUrl(results[index]["url"])


# option 4 - change account data
def changeAccount(AES_key):
    global systemMessage
    if databaseStatus(AES_key):
        showDatabase(AES_key)
        print("\n Please provide the {} of the account you want to change:".format(colored("ID", "green")))
        ID = input(" > ")

        if ID not in getIndices(AES_key):
            systemMessage = " The ID doesn't exists!"
            return

        print("\n Please select the {} you want to change:".format(colored("field name", "green")))
        fieldName = showOptions(
            {1: "siteName", 2: "url", 3: "username", 4: "email", 5: "password", 6: "expiration", 7: "category"})
        expiration = 0

        if fieldName == "password":
            changeValue = passwordOption()
            print("\n Choose the new {} for your password:".format(colored("expiration period (in days)", "green")))
            expiration = showOptions({1: 1, 2: 7, 3: 30, 4: 90, 5: 365, 6: 0})
        elif fieldName == "expiration":
            print("\n Choose the new {} for your password:".format(colored("expiration period (in days)", "green")))
            changeValue = showOptions({1: 1, 2: 7, 3: 30, 4: 90, 5: 365, 6: 0})
        elif fieldName == "category":
            print("\n Choose the new {} for your account:".format(colored("category", "green")))
            changeValue = showOptions(
                {1: "email", 2: "social media", 3: "gaming", 4: "coding", 5: "shopping", 6: "banking", 7: "education",
                 8: "private", 9: "other"})
        else:
            print("\n Please provide the new {}:".format(colored(fieldName, "green")))
            changeValue = input(" > ")
        print("\n Are you sure you want to {} the {} of the {} account? (Y/N):".format(colored("change", "red"),
                                                                                     colored(fieldName, "green"),
                                                                                     colored(getRowData(ID, AES_key)[
                                                                                                 "siteName"], "red")))
        choice = choicePrompt()

        if choice:
            if passwordBarrier(AES_key):
                changeData(ID, fieldName, changeValue, AES_key)
                if fieldName == "password":
                    changeData(ID, "expiration", expiration, AES_key)
            else:
                systemMessage = " The given password is incorrect!"


# option 5 - show all accounts
def showAllAccounts(AES_key):
    if databaseStatus(AES_key):
        showDatabase(AES_key)
    pwinput(prompt=" Press enter to continue!", mask="")


# option 6 - make backup
def backupMenu():
    global systemMessage
    defaultPath = getcwd() + "/backup/"

    print()
    print('-' * 30)
    print(" 1 - Create {}".format(colored("backup", "cyan")))
    print(" 2 - Load {}".format(colored("backup", "cyan")))
    print('-' * 30)
    choice = input(" > ")

    if choice == "1":
        print("\n Do you want to specify a backup destination? (Y/N):")
        choice = choicePrompt()

        if choice:
            print("\n Please specify the destination path you want to save the backup to:")
            dstPath = input(" > ")
            backupStatus = createBackupFile(dstPath)
            if backupStatus:
                systemMessage = " The backup was saved!"
                startfile(dstPath)
            else:
                print("\n The given destination path is not accessible, please specify a different path!")
                backupMenu()
        else:
            if not path.isdir(defaultPath):
                mkdir(defaultPath)
                hideFile(defaultPath)
            createBackupFile(defaultPath)
            systemMessage = " The backup was saved!"
            startfile(defaultPath)
    elif choice == "2":
        files = None
        indices = []
        dirPath = defaultPath

        print("\n Please specify the {} you want to load the backup from or press {} if the backup is in the default path:".format(colored("path", "green"), colored("ENTER", "red")))
        while not files:
            userPath = input(" > ")
            if userPath:
                dirPath = userPath + "\\" if userPath[-1] != "\\" else userPath
            else:
                dirPath = defaultPath
            try:
                files = listdir(dirPath)
            except FileNotFoundError:
                print(" \n File path not found or empty!")

        print("\n Please select an existing {} or press {} to return".format(colored("file", "green"),
                                                                           colored("ENTER", "red")))
        for i, file in enumerate(files):
            indices.append(str(i))
            backupAge = datetime.now() - datetime.fromtimestamp(path.getctime(dirPath + file))
            print("   {} - {} {:4d} days ago".format(colored(i, "cyan"), file, backupAge.days))
        userInput = input(" > ")

        while userInput not in indices:
            if not userInput:
                return
            print(" The index is not available, try again!")
            userInput = input(" > ")
        filePath = dirPath + "\\" + files[int(userInput)]
        if loadBackupFile(filePath):
            systemMessage = " The backup was loaded!"
        else:
            systemMessage = " Couldn't load backup. Changes reverted!"
    else:
        return


# option 7 - print layout
def createPrintLayout(AES_key):
    templateFilePath = "print_layout/printLayout.xlsx"
    createPrintLayoutFile(templateFilePath, AES_key)
