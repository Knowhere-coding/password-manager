from pwinput import pwinput
from time import time
from os import system, getcwd, startfile, path, mkdir
from termcolor import colored
from textFile import logo
from passwordManagement import createNewPassword, passwordOption, checkExpirationDate, passwordBarrier, accountBarrier
from database import storeData, deleteData, findData, changeData, showDatabase, databaseStatus, getIndices, getColumnData, getRowData
from printLayout import createPrintLayoutFile
from fileHandling import hideFile
from fileEncryption import getAESkey
from backupHandling import createBackupFile, getBackupFiles, showBackupFileList, loadBackupFile
from utilities import choicePrompt, copyToClipboard, openUrl, showOptions
import config


# default overlay
def optionMenu():
    system("cls")

    # show logo
    print(logo)

    # start inactivity timer
    start = time()

    # show system message
    if config.systemMessage != "":
        print("-" * 30)
        print(config.systemMessage)
        print("-" * 30)
        config.systemMessage = ""

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


# option 1 - create new account
def createAccount(AES_key):
    # category
    print("\n Choose the {} for your new account:".format(colored("category", "green")))
    category = showOptions(
        {1: "email",
         2: "social media",
         3: "gaming",
         4: "coding",
         5: "shopping",
         6: "banking",
         7: "education",
         8: "private",
         9: "other"})

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
    print("\n Please provide an {} or select an existing {}:"
          .format(colored("email", "green"), colored("email", "green")))
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
    if databaseStatus(AES_key):
        showDatabase(AES_key)
        print("\n Please provide the {} of the account you want to delete:".format(colored("ID", "red")))
        ID = input(" > ")

        if ID not in getIndices(AES_key):
            config.systemMessage = " The ID doesn't exists!"
            return

        print("\n Are you sure you want to {} the {} account? (Y/N):"
              .format(colored("delete", "red"), colored(getRowData(ID, AES_key)["siteName"], "green")))
        if choicePrompt():
            if passwordBarrier(AES_key):
                deleteData(ID, AES_key)
            else:
                config.systemMessage = " The given password was incorrect!"


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
            print("\n Select the {} of your account or press {} to go back to the menu: "
                  .format(colored("ID", "red"), colored("ENTER", "red")))
            accountNum = input(" > ")

            if not accountNum:
                return
            while accountNum not in indices:
                print("\n The ID is not available, try again!")
                accountNum = input(" > ")
                if not accountNum:
                    return
            index = indices.index(accountNum)

        password = checkExpirationDate(results[index]["ID"],
                                       results[index]["changeDate"],
                                       results[index]["expiration"],
                                       AES_key)
        if password == "":
            copyToClipboard(results[index]["password"])
        else:
            copyToClipboard(password)

        openUrl(results[index]["url"])


# option 4 - change account data
def changeAccount(AES_key):
    if databaseStatus(AES_key):
        showDatabase(AES_key)
        print("\n Please provide the {} of the account you want to change:".format(colored("ID", "green")))
        ID = input(" > ")

        if ID not in getIndices(AES_key):
            config.systemMessage = " The ID doesn't exists!"
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
        print("\n Are you sure you want to {} the {} of the {} account? (Y/N):"
              .format(colored("change", "red"), colored(fieldName, "green"), colored(getRowData(ID, AES_key)["siteName"], "red")))

        if choicePrompt():
            if passwordBarrier(AES_key):
                changeData(ID, fieldName, changeValue, AES_key)
                if fieldName == "password":
                    changeData(ID, "expiration", expiration, AES_key)
            else:
                config.systemMessage = " The given password is incorrect!"


# option 5 - show all accounts
def showAllAccounts(AES_key):
    if databaseStatus(AES_key):
        showDatabase(AES_key)
        pwinput(prompt=" Press enter to continue!", mask="")


# option 6 - make backup
def backupMenu():
    defaultPath = getcwd() + "/backup/"

    print()
    print('-' * 30)
    print(" 1 - Create {}".format(colored("backup", "cyan")))
    print(" 2 - Load {}".format(colored("backup", "cyan")))
    print('-' * 30)
    choice = input(" > ")

    if choice == "1":
        dirPath = defaultPath
        print("\n Please specify the {} you want to save the backup to or press {} to save the backup in the default path:"
              .format(colored("path", "green"), colored("ENTER", "red")))
        backupStatus = False
        while not backupStatus:
            userPath = input(" > ")
            if userPath:
                dirPath = userPath + "\\" if userPath[-1] != "\\" else userPath
            else:
                if not path.isdir(defaultPath):
                    mkdir(defaultPath)
                    hideFile(defaultPath)
                dirPath = defaultPath
            backupStatus = createBackupFile(dirPath)
            if not backupStatus:
                print("\n Couldn't save backup to: {}".format(dirPath))
        config.systemMessage = " The backup was saved!"
        startfile(dirPath)
    elif choice == "2":
        files = None
        dirPath = defaultPath

        print("\n Please specify the {} you want to load the backup from or press {} if the backup is in the default path:"
              .format(colored("path", "green"), colored("ENTER", "red")))
        while not files:
            userPath = input(" > ")
            if userPath:
                dirPath = userPath + "\\" if userPath[-1] != "\\" else userPath
            else:
                dirPath = defaultPath
            files = getBackupFiles(dirPath)

        print("\n Please select an existing {} or press {} to return"
              .format(colored("file", "green"), colored("ENTER", "red")))
        indices = showBackupFileList(files, dirPath)
        userInput = input(" > ")

        while userInput not in indices:
            if not userInput:
                config.systemMessage = " No backup was loaded!"
                return
            print(" The index is not available, try again!")
            userInput = input(" > ")
        filePath = dirPath + "\\" + files[int(userInput)]
        config.systemMessage = " The backup was loaded!" if loadBackupFile(filePath) else " Couldn't load backup. Changes reverted!"
    else:
        return


# option 7 - print layout
def createPrintLayout(AES_key):
    templateFilePath = "print_layout/printLayout.xlsx"
    createPrintLayoutFile(templateFilePath, AES_key)
