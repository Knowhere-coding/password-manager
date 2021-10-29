import pandas as pd
from datetime import datetime, timedelta
from colorama import init
from termcolor import colored
import webbrowser
from passwordManagement import createNewPassword
from database import readCsvDataDict, storeData, deleteData, findData, changeData, showDatabase

# initialize termcolor to work on windows
init()

# TODO: UI design
# TODO: colors
# TODO: Delete terminal text (maybe not possible?)
# TODO: let the user choose the password reset timer


# default overlay
def optionMenu():
    print('-'*30)
    print(('-'*12) + " Menu " + ('-'*12))
    print("1 - Create a new {}".format(colored("account", "red")))
    print("2 - Delete an {}".format(colored("account", "red")))
    print("3 - Find your {}".format(colored("account data", "red")))
    print("4 - Change your {}".format(colored("account data", "red")))
    print("5 - Show all your {}".format(colored("accounts", "red")))
    print("Q - {}".format(colored("Exit", "red")))
    print('-' * 30)
    return input(": ")


# copy data to clipboard
# TODO: Delete Clipboard after X sec.
def copyToClipboard(msg):
    dataFrame = pd.DataFrame([msg])
    dataFrame.to_clipboard(index=False, header=False)
    print('-' * 47)
    print("")
    print("Your password has been copied to your clipboard")
    print("")
    print('-' * 47)


# open url
def openUrl(url):
    # open url
    print("Do you want to open the url? (Y/N):")
    choice = input()
    status = True if choice.upper() == "Y" else False

    if status:
        webbrowser.open(url)


# create/change password
def passwordOption():
    # option to generate random password
    print("Do you want to generate a random password? (Y/N):")
    choice = input()
    status = True if choice.upper() == "Y" else False

    # generate random password
    if status:
        print("Please specify the given special characters besides all letters and digits (if none type -):")
        specialChars = input()
        if specialChars == "-":
            password = createNewPassword()
        else:
            password = createNewPassword(specialChars)
    # provide own password
    else:
        print("Please provide your own {}:".format(colored("password", "red")))
        password = input()

    # expiration Option
    print("Do you want to define an expiration period for your password? (Y/N):")
    choice = input(": ")
    status2 = True if choice.upper() == "Y" else False

    if status2:
        expiration = expirationOption()
        return password, expiration

    return password, 0


# expiration option
def expirationOption():
    # option to define an expiration period for the password
    period = {1: 1,     # daily
              2: 7,     # weekly
              3: 30,    # monthly
              4: 90,    # quarterly
              5: 365,   # yearly
              6: 0}     # never

    # choose expiration period
    print("1 - {}".format(colored("daily", "white")))
    print("2 - {}".format(colored("weekly", "white")))
    print("3 - {}".format(colored("monthly", "white")))
    print("4 - {}".format(colored("quarterly", "white")))
    print("5 - {}".format(colored("yearly", "white")))
    print("6 - {}".format(colored("never", "white")))
    expirationNum = input(": ")
    while expirationNum not in ['1', '2', '3', '4', '5', '6']:
        expirationNum = input(": ")
    return period[int(expirationNum)]


# category option
def categoryOption():
    # category
    categories = {1: "email",
                  2: "social media",
                  3: "gaming",
                  4: "shopping",
                  5: "Banking",
                  6: "education",
                  7: "private",
                  8: "other"}

    print("1 - {}".format(colored("Email", "white")))
    print("2 - {}".format(colored("Social media", "white")))
    print("3 - {}".format(colored("Gaming", "white")))
    print("4 - {}".format(colored("Shopping", "white")))
    print("5 - {}".format(colored("Banking", "white")))
    print("6 - {}".format(colored("Education", "white")))
    print("7 - {}".format(colored("Private", "white")))
    print("8 - {}".format(colored("Other", "white")))
    categoryNum = input(": ")
    while categoryNum not in ['1', '2', '3', '4', '5', '6', '7', '8']:
        categoryNum = input(": ")
    return categories[int(categoryNum)]


# search option
def searchOption():
    # field names
    field_names = {1: "siteName", 2: "url", 3: "username", 4: "email", 5: "password", 6: "expiration", 7: "category"}
    print("1 - {}".format(colored(field_names[1], "white")))
    print("2 - {}".format(colored(field_names[2], "white")))
    print("3 - {}".format(colored(field_names[3], "white")))
    print("4 - {}".format(colored(field_names[4], "white")))
    print("5 - {}".format(colored(field_names[5], "white")))
    print("6 - {}".format(colored(field_names[6], "white")))
    field_nameNum = input(": ")
    while field_nameNum not in ['1', '2', '3', '4', '5', '6']:
        field_nameNum = input(": ")
    return field_names[int(field_nameNum)]


# change password
def changePassword(ID, AES_key):
    print("Do you want to change the password? (Y/N):")
    choice = input()
    status = True if choice.upper() == "Y" else False
    if status:
        password, expiration = passwordOption()
        changeData(ID, "password", password, AES_key)
        changeData(ID, "expiration", expiration, AES_key)
        return password
    else:
        return ""


# check change date
def checkChangeDate(ID, changeDate, expiration, AES_key):
    if not expiration == 0:
        changeDate = datetime.strptime(changeDate, "%Y-%m-%d %H:%M:%S")

        if (changeDate + timedelta(days=expiration)) < datetime.now():
            print("{} The password-change-date is more than {} days ago {}".format(colored("!!!", "red"), str(days),
                                                                                   colored("!!!", "red")))
            return changePassword(ID, AES_key)
        else:
            return ""
    return ""


# option 1 - create new account
def createAccount(AES_key):
    # category
    print("Choose the {} for your new account".format(colored("category", "red")))
    category = categoryOption()

    # site name
    print("Please provide the {} (e.g. reddit) you want to create a new account for:".format(colored("site name", "blue")))
    siteName = input()

    # url
    print("Please provide the {} (e.g. www.example.com) to the site:".format(colored("url", "blue")))
    url = input()

    # username
    print("Please provide a {} (if applicable):".format(colored("username", "blue")))
    username = input()
    if not username:
        username = ""

    # email
    print("Please provide an {}:".format(colored("email", "blue")))
    email = input()

    # password and expiration date
    password, expiration = passwordOption()

    if storeData(siteName, url, username, email, password, expiration, category, AES_key):
        copyToClipboard(password)


# option 2 - delete account
def deleteAccount(AES_key):
    showDatabase(AES_key)
    print("Please provide the {} of the account you want to delete:".format(colored("ID", "red")))
    ID = input()
    siteName = ""
    for row in readCsvDataDict("data/account_data.csv", AES_key):
        if row["ID"] == ID:
            siteName = row["siteName"]
    print("Are you sure you want to {} the {} account! (Y/N):".format(colored("delete", "red"), colored(siteName, "red")))
    choice = input()
    status = True if choice.upper() == "Y" else False

    if status:
        deleteData(ID, AES_key)


# option 3 - find account data
def findAccounts(AES_key):
    # field name
    print("Please select the {} you want to search for:".format(colored("field name", "blue")))
    searchingField = searchOption()
    # value
    if searchingField == "category":
        print("Choose the {} you want to search for:".format(colored("category", "red")))
        searchingValue = categoryOption()
    else:
        print("Please provide the {} you wanna search for:".format(colored(searchingField, "blue")))
        searchingValue = input()

    results, indices = findData(searchingField, searchingValue, AES_key)

    if results:
        # user action
        print("Do you want to select an account? (Y/N):")
        choice = input()
        status = True if choice.upper() == "Y" else False

        if status:
            if len(results) > 1:
                print("")
                accountNum = input("Select the ID of your account: ")

                while accountNum not in indices:
                    accountNum = input("The number is not available, try again:")
                index = indices.index(accountNum)
                password = checkChangeDate(results[index]["ID"], results[index]["changeDate"], results[index]["expiration"], AES_key)

                if password == "":
                    copyToClipboard(results[index]["password"])
                else:
                    copyToClipboard(password)

                openUrl(results[index]["url"])
            else:
                print("Automatically selected Account " + results[0]["ID"] + "!")
                password = checkChangeDate(results[0]["ID"], results[0]["changeDate"], results[0]["expiration"], AES_key)
                if password == "":
                    copyToClipboard(results[0]["password"])
                else:
                    copyToClipboard(password)
                openUrl(results[0]["url"])


# option 4 - change account data
def changeAccount(AES_key):
    showDatabase(AES_key)
    print("Please provide the {} of the account you want to change:".format(colored("ID", "red")))
    ID = input()
    print("Please select the {} you want to change:".format(colored("field name", "blue")))
    fieldName = searchOption()

    if fieldName == "password":
        changeValue, expiration = passwordOption()
        changeData(ID, "expiration", expiration, AES_key)
    elif fieldName == "expiration":
        print("Define the new expiration period for your password:")
        changeValue = expirationOption()
    elif fieldName == "category":
        print("Choose the new {} for your account".format(colored("category", "red")))
        changeValue = categoryOption()
    else:
        print("Please provide the new {}:".format(colored(fieldName, "blue")))
        changeValue = input()

    changeData(ID, fieldName, changeValue, AES_key)


# option 5 - show all accounts
def showAllAccounts(AES_key):
    showDatabase(AES_key)
