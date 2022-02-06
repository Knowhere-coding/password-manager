import pwinput
import pyperclip
import time
import os
from datetime import datetime, timedelta
from colorama import init
from termcolor import colored
import webbrowser
from passwordManagement import createNewPassword
from database import storeData, deleteData, findData, changeData, showDatabase, databaseStatus, backup, checkMasterPassword, getIndices, getColumnData, getRowData
from csvHandling import readCsvDataDict

# initialize termcolor to work on windows
init()


# default overlay
def optionMenu():
    # start inactivity timer
    start = time.time()

    print('-'*30)
    print(('-'*12) + " Menu " + ('-'*12))
    print(" 1 - Create a new {}".format(colored("account", "cyan")))
    print(" 2 - Delete an {}".format(colored("account", "cyan")))
    print(" 3 - Find your {}".format(colored("account data", "cyan")))
    print(" 4 - Change your {}".format(colored("account data", "cyan")))
    print(" 5 - Show all your {}".format(colored("accounts", "cyan")))
    print(" 6 - Make {}".format(colored("backup", "cyan")))
    print(" Q - {}".format(colored("Exit", "cyan")))
    print('-' * 30)
    return input(" > "), start


# give the user a choice
def choicePrompt():
    choice = input(" > ")
    return True if choice.upper() == "Y" else False


# copy data to clipboard
def copyToClipboard(msg):
    pyperclip.copy(msg)
    print('-' * 47)
    print("")
    print(" Your {} has been copied to your {}".format(colored("password", "green"), colored("clipboard", "cyan")))
    print("")
    print('-' * 47)


# open url
def openUrl(url):
    # open url
    print(" Do you want to open the {}? (Y/N):".format(colored("url", "green")))
    choice = choicePrompt()

    if choice:
        webbrowser.open_new_tab("https://" + url)


# create/change password
def passwordOption():
    # option to generate random password
    print(" Do you want to generate a random {}? (Y/N):".format(colored("password", "green")))
    choice = choicePrompt()

    # generate random password
    if choice:
        minLength, maxLength = getMinMaxLength()
        specialChars = getSpecialChars()
        password = createNewPassword(minLength, maxLength, specialChars)
    # provide own password
    else:
        print(" Please provide your own {}:".format(colored("password", "green")))
        password = pwinput.pwinput(prompt=" > ")

    return password


# let the user define valid special chars for the random generated password
def getSpecialChars():
    print(" Please specify the given {} besides all letters and digits (if none type -):".format(colored("specail characters", "green")))
    return input(" > ")


# let the user define the minimum and maximum length of the random generated password
def getMinMaxLength():
    minLength = 1
    maxLength = 0

    try:
        print(" Please specify the {} length of the password:".format(colored("minimum", "red")))
        minLength = int(input(" > "))
        print(" Please specify the {} length of the password:".format(colored("maximum", "green")))
        maxLength = int(input(" > "))
    except ValueError:
        print("Please input numbers!")

    if minLength > maxLength:
        print(" The minimum value is higher than the maximum value:")
    while minLength > maxLength:
        try:
            print(" New {}:".format(colored("minimum", "red")))
            minLength = int(input(" > "))
            print(" New {}:".format(colored("maximum", "green")))
            maxLength = int(input(" > "))
        except ValueError:
            print(" Please input numbers!")

    if maxLength > 100:
        print(" Secure is not enough for you, right? :D")
    return minLength, maxLength


def showOptions(options):
    for key in options:
        print("   {} - {}".format(key, colored(options[key], "white")))
    userInput = input(" > ")
    while userInput not in [str(x) for x in options.keys()]:
        userInput = input(" > ")
    return options[int(userInput)]


# check change date and change password
def checkChangeDate(ID, changeDate, expiration, AES_key):
    if not expiration == "0":
        changeDate = datetime.strptime(changeDate, "%Y-%m-%d %H:%M:%S")

        if (changeDate + timedelta(days=int(expiration))) < datetime.now():
            print(" {} The password-change-date is more than {} days ago {}".format(colored("!!!", "cyan"), expiration,
                                                                                   colored("!!!", "cyan")))
            print(" Do you want to change the {}? (Y/N):".format(colored("password", "green")))
            choice = choicePrompt()
            if choice:
                password = passwordOption()
                if passwordBarrier(AES_key):
                    changeData(ID, "password", password, AES_key)
                    return password
                else:
                    print("The given password was incorrect!")
            return ""
        else:
            return ""
    return ""


# password barrier for changing/deleting data from the database
def passwordBarrier(AES_key):
    masterPassword = pwinput.pwinput(prompt=" Please provide your master password: ")
    return checkMasterPassword(masterPassword, AES_key)


# option 1 - create new account
def createAccount(AES_key):
    # category
    print(" Choose the {} for your new account:".format(colored("category", "green")))
    category = showOptions({1: "email", 2: "social media", 3: "gaming", 4: "coding", 5: "shopping", 6: "Banking", 7: "education", 8: "private", 9: "other"})

    # site name
    print(" Please provide the {} (e.g. reddit) you want to create a new account for:".format(colored("site name", "green")))
    siteName = input(" > ")

    # url
    print(" Please provide the {} (e.g. www.example.com) to the site:".format(colored("url", "green")))
    url = input(" > ")

    # username
    print(" Please provide a {} (if applicable):".format(colored("username", "green")))
    username = input(" > ")
    if not username:
        username = ""

    # email
    print(" Please provide an {} or select an existing {}:".format(colored("email", "green"), colored("email", "green")))
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
    print(" Choose the {} of your password:".format(colored("expiration period", "green")))
    expiration = showOptions({1: 1, 2: 7, 3: 30, 4: 90, 5: 365, 6: 0})

    if storeData(siteName, url, username, email, password, expiration, category, AES_key):
        copyToClipboard(password)


# option 2 - delete account
def deleteAccount(AES_key):
    if databaseStatus(AES_key):
        showDatabase(AES_key)
        print(" Please provide the {} of the account you want to delete:".format(colored("ID", "red")))
        ID = input(" > ")

        if ID not in getIndices(AES_key):
            print(" The ID doesn't exists!")
            return

        print(" Are you sure you want to {} the {} account! (Y/N):".format(colored("delete", "red"), colored(getRowData(ID, AES_key)["siteName"], "green")))
        choice = choicePrompt()
        if choice:
            if passwordBarrier(AES_key):
                deleteData(ID, AES_key)
            else:
                print(" The given password was incorrect!")


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
        print(" Please select the {} you want to search for:".format(colored("field name", "green")))
        searchingField = showOptions({1: "siteName", 2: "url", 3: "username", 4: "email", 5: "password", 6: "expiration", 7: "category"})
        # value
        if searchingField == "category":
            print(" Choose the {} you want to search for:".format(colored("category", "green")))
            searchingValue = showOptions({1: "email", 2: "social media", 3: "gaming", 4: "coding", 5: "shopping", 6: "Banking", 7: "education", 8: "private", 9: "other"})
        elif searchingField == "expiration":
            print(" Choose the {} you want to search for:".format(colored("expiration period", "green")))
            searchingValue = str(showOptions({1: 1, 2: 7, 3: 30, 4: 90, 5: 365, 6: 0}))
            output = ["ID", "siteName", "username", "email", "password", "expiration", "category"]
        elif searchingField == "password":
            print(" Please provide the {} you wanna search for:".format(colored(searchingField, "green")))
            searchingValue = pwinput.pwinput(prompt=" > ")
        else:
            if searchingField == "url":
                output = ["ID", "siteName", "url", "username", "email", "password", "category"]
            print(" Please provide the {} you wanna search for:".format(colored(searchingField, "green")))
            searchingValue = input(" > ")

        results, indices = findData(searchingField, searchingValue, AES_key, output)

    if results:
        if len(results) > 1:
            print(" Select the {} of your account: ".format(colored("ID", "red")))
            accountNum = input(" > ")

            while accountNum not in indices:
                accountNum = input(" The ID is not available, try again: ")
            index = indices.index(accountNum)
        else:
            print(" Automatically selected Account {}!".format(colored(results[0]["ID"], "cyan")))
            index = 0

        password = checkChangeDate(results[index]["ID"], results[index]["changeDate"], results[index]["expiration"], AES_key)
        if password == "":
            copyToClipboard(results[index]["password"])
        else:
            copyToClipboard(password)

        openUrl(results[index]["url"])


# option 4 - change account data
def changeAccount(AES_key):
    if databaseStatus(AES_key):
        showDatabase(AES_key)
        print(" Please provide the {} of the account you want to change:".format(colored("ID", "green")))
        ID = input(" > ")

        if ID not in getIndices(AES_key):
            print(" The ID doesn't exists!")
            return

        print(" Please select the {} you want to change:".format(colored("field name", "green")))
        fieldName = showOptions({1: "siteName", 2: "url", 3: "username", 4: "email", 5: "password", 6: "expiration", 7: "category"})
        expiration = 0

        if fieldName == "password":
            changeValue = passwordOption()
            print(" Choose the new {} for your password:".format(colored("expiration period", "green")))
            expiration = showOptions({1: 1, 2: 7, 3: 30, 4: 90, 5: 365, 6: 0})
        elif fieldName == "expiration":
            print(" Choose the new {} for your password:".format(colored("expiration period", "green")))
            changeValue = showOptions({1: 1, 2: 7, 3: 30, 4: 90, 5: 365, 6: 0})
        elif fieldName == "category":
            print(" Choose the new {} for your account:".format(colored("category", "green")))
            changeValue = showOptions({1: "email", 2: "social media", 3: "gaming", 4: "coding", 5: "shopping", 6: "Banking", 7: "education", 8: "private", 9: "other"})
        else:
            print(" Please provide the new {}:".format(colored(fieldName, "green")))
            changeValue = input(" > ")
        print(" Are you sure you want to {} the {} of the {} account! (Y/N):".format(colored("change", "red"), colored(fieldName, "green"), colored(getRowData(ID, AES_key)["siteName"], "red")))
        choice = choicePrompt()

        if choice:
            if passwordBarrier(AES_key):
                changeData(ID, fieldName, changeValue, AES_key)
                if fieldName == "password":
                    changeData(ID, "expiration", expiration, AES_key)
            else:
                print("The given password was incorrect!")


# option 5 - show all accounts
def showAllAccounts(AES_key):
    if databaseStatus(AES_key):
        showDatabase(AES_key)
    pwinput.pwinput(prompt=" Press enter to continue!", mask="")


# option 6 - make backup
def makeBackup():
    default_path = os.getcwd() + "\\backup"

    print(" Do you want to specify a backup destination? (Y/N):".format())
    choice = choicePrompt()

    if choice:
        print("Please specify the destination path you want to save the backup to:")
        dst_path = input(" > ")
        backupStatus = backup(dst_path)
        if backupStatus:
            print("The backup was saved!")
            os.startfile(dst_path)
        else:
            print("The given destination path is not accessable, please specify a different path!")
            makeBackup()
    else:
        backup(default_path)
        print("The backup was saved!")
        os.startfile(default_path)
