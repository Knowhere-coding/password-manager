import pandas as pd
from datetime import datetime, timedelta
from colorama import init
from termcolor import colored
import webbrowser
from passwordManagement import createNewPassword
from database import readCsvDataDict, storeData, deleteData, findData, changeData, showDatabase, databaseStatus

# initialize termcolor to work on windows
init()

# TODO: UI design
# TODO: colors
# TODO: Delete terminal text (maybe not possible?)


# default overlay
def optionMenu():
    print('-'*30)
    print(('-'*12) + " Menu " + ('-'*12))
    print("1 - Create a new {}".format(colored("account", "cyan")))
    print("2 - Delete an {}".format(colored("account", "cyan")))
    print("3 - Find your {}".format(colored("account data", "cyan")))
    print("4 - Change your {}".format(colored("account data", "cyan")))
    print("5 - Show all your {}".format(colored("accounts", "cyan")))
    print("Q - {}".format(colored("Exit", "cyan")))
    print('-' * 30)
    return input("> ")


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
    print("Do you want to open the {}? (Y/N):".format(colored("url", "green")))
    choice = input("> ")
    status = True if choice.upper() == "Y" else False

    if status:
        webbrowser.open(url)


# create/change password
def passwordOption():
    # option to generate random password
    print("Do you want to generate a random {}? (Y/N):".format(colored("password", "cyan")))
    choice = input("> ")
    status = True if choice.upper() == "Y" else False

    # generate random password
    if status:
        print("Please specify the given {} besides all letters and digits (if none type -):".format(colored("specail characters", "cyan")))
        specialChars = input("> ")
        if specialChars == "-":
            password = createNewPassword()
        else:
            password = createNewPassword(specialChars)
    # provide own password
    else:
        print("Please provide your own {}:".format(colored("password", "cyan")))
        password = input("> ")

    return password


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
    expirationNum = input("> ")
    while expirationNum not in ['1', '2', '3', '4', '5', '6']:
        expirationNum = input("> ")
    return period[int(expirationNum)]


# category option
def categoryOption():
    # category
    categories = {1: "email",
                  2: "social media",
                  3: "gaming",
                  4: "coding",
                  5: "shopping",
                  6: "Banking",
                  7: "education",
                  8: "private",
                  9: "other"}

    print("1 - {}".format(colored("Email", "white")))
    print("2 - {}".format(colored("Social media", "white")))
    print("3 - {}".format(colored("Gaming", "white")))
    print("4 - {}".format(colored("Coding", "white")))
    print("5 - {}".format(colored("Shopping", "white")))
    print("6 - {}".format(colored("Banking", "white")))
    print("7 - {}".format(colored("Education", "white")))
    print("8 - {}".format(colored("Private", "white")))
    print("9 - {}".format(colored("Other", "white")))
    categoryNum = input("> ")
    while categoryNum not in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
        categoryNum = input("> ")
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
    print("7 - {}".format(colored(field_names[7], "white")))
    field_nameNum = input("> ")
    while field_nameNum not in ['1', '2', '3', '4', '5', '6', '7']:
        field_nameNum = input("> ")
    return field_names[int(field_nameNum)]


# check change date and change password
def checkChangeDate(ID, changeDate, expiration, AES_key):
    if not expiration == "0":
        changeDate = datetime.strptime(changeDate, "%Y-%m-%d %H:%M:%S")

        if (changeDate + timedelta(days=int(expiration))) < datetime.now():
            print("{} The password-change-date is more than {} days ago {}".format(colored("!!!", "cyan"), expiration,
                                                                                   colored("!!!", "cyan")))
            print("Do you want to change the {}? (Y/N):".format(colored("password", "cyan")))
            choice = input("> ")
            status = True if choice.upper() == "Y" else False
            if status:
                password = passwordOption()
                changeData(ID, "password", password, AES_key)
                return password
            return ""
        else:
            return ""
    return ""


# option 1 - create new account
def createAccount(AES_key):
    # category
    print("Choose the {} for your new account".format(colored("category", "cyan")))
    category = categoryOption()

    # site name
    print("Please provide the {} (e.g. reddit) you want to create a new account for:".format(colored("site name", "green")))
    siteName = input("> ")

    # url
    print("Please provide the {} (e.g. www.example.com) to the site:".format(colored("url", "green")))
    url = input("> ")

    # username
    print("Please provide a {} (if applicable):".format(colored("username", "green")))
    username = input("> ")
    if not username:
        username = ""

    # email
    print("Please provide an {}:".format(colored("email", "green")))
    email = input("> ")

    # password
    password = passwordOption()

    # expiration date
    print("Choose the {} of your password".format(colored("expiration period", "cyan")))
    expiration = expirationOption()

    if storeData(siteName, url, username, email, password, expiration, category, AES_key):
        copyToClipboard(password)


# option 2 - delete account
def deleteAccount(AES_key):
    if databaseStatus(AES_key):
        showDatabase(AES_key)
        print("Please provide the {} of the account you want to delete:".format(colored("ID", "cyan")))
        ID = input("> ")
        siteName = ""
        for row in readCsvDataDict("data/account_data.csv", AES_key):
            if row["ID"] == ID:
                siteName = row["siteName"]
        print("Are you sure you want to {} the {} account! (Y/N):".format(colored("delete", "cyan"), colored(siteName, "cyan")))
        choice = input("> ")
        status = True if choice.upper() == "Y" else False

        if status:
            deleteData(ID, AES_key)


# option 3 - find account data
def findAccounts(AES_key):
    # field name
    if databaseStatus(AES_key):
        print("Please select the {} you want to search for:".format(colored("field name", "green")))
        searchingField = searchOption()
        # value
        if searchingField == "category":
            print("Choose the {} you want to search for:".format(colored("category", "cyan")))
            searchingValue = categoryOption()
        else:
            print("Please provide the {} you wanna search for:".format(colored(searchingField, "green")))
            searchingValue = input("> ")

        results, indices = findData(searchingField, searchingValue, AES_key)

        if results:
            # user action
            print("Do you want to select an {}? (Y/N):".format(colored("account", "cyan")))
            choice = input("> ")
            status = True if choice.upper() == "Y" else False

            if status:
                if len(results) > 1:
                    print("")
                    accountNum = input("Select the {} of your account: ".format(colored("ID", "green")))

                    while accountNum not in indices:
                        accountNum = input("The ID is not available, try again:")
                    index = indices.index(accountNum)
                    password = checkChangeDate(results[index]["ID"], results[index]["changeDate"], results[index]["expiration"], AES_key)

                    if password == "":
                        copyToClipboard(results[index]["password"])
                    else:
                        copyToClipboard(password)

                    openUrl(results[index]["url"])
                else:
                    print("Automatically selected Account {}!".format(colored(results[0]["ID"], "cyan")))
                    password = checkChangeDate(results[0]["ID"], results[0]["changeDate"], results[0]["expiration"], AES_key)
                    if password == "":
                        copyToClipboard(results[0]["password"])
                    else:
                        copyToClipboard(password)
                    openUrl(results[0]["url"])


# option 4 - change account data
def changeAccount(AES_key):
    if databaseStatus(AES_key):
        showDatabase(AES_key)
        print("Please provide the {} of the account you want to change:".format(colored("ID", "cyan")))
        ID = input("> ")
        print("Please select the {} you want to change:".format(colored("field name", "green")))
        fieldName = searchOption()

        if fieldName == "password":
            changeValue = passwordOption()
            print("Choose the new {} for your password:".format(colored("expiration period", "cyan")))
            expiration = expirationOption()
            changeData(ID, "expiration", expiration, AES_key)
        elif fieldName == "expiration":
            print("Choose the new {} for your password:".format(colored("expiration period", "cyan")))
            changeValue = expirationOption()
        elif fieldName == "category":
            print("Choose the new {} for your account".format(colored("category", "cyan")))
            changeValue = categoryOption()
        else:
            print("Please provide the new {}:".format(colored(fieldName, "green")))
            changeValue = input("> ")

            changeData(ID, fieldName, changeValue, AES_key)


# option 5 - show all accounts
def showAllAccounts(AES_key):
    if databaseStatus(AES_key):
        showDatabase(AES_key)
