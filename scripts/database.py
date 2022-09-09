from csv import DictReader
from os import getcwd, remove
from re import sub
from datetime import datetime
from prettytable import PrettyTable
from fileEncryption import encryptFile, decryptFile, saveDecryptFile
from csvHandling import readCsvDataDict, writeCsvDataDict
import config


# check if the database has entries
def databaseStatus(AES_key):
    if len(readCsvDataDict("/data/account_data.csv", AES_key)) == 0:
        config.systemMessage = " The database is empty!"
        return False
    else:
        return True


# validate the master account data
def checkMaster(masterUsername, masterPassword, AES_key):
    try:
        error = False

        # check AES_key
        saveDecryptFile("/data/AES.key.enc", AES_key)
        with open(getcwd() + "/data/AES.key") as file:
            try:
                text = file.read()
            except UnicodeDecodeError:
                error = True

        remove(getcwd() + "/data/AES.key")
        if error:
            return False

        if bytes(text, "utf-8") == AES_key:
            # check master account data
            decryptFile("/data/master_account_data.csv.enc", AES_key)
            with open(getcwd() + "/data/master_account_data.csv") as csvDataFile:
                csvReader = DictReader(csvDataFile, delimiter=',')
                for row in csvReader:
                    status = masterUsername == row["masterUsername"] and masterPassword == row["masterPassword"]
            encryptFile("/data/master_account_data.csv", AES_key)
        else:
            status = False
        return status
    except Exception:
        return False


# check master password for the password barrier when changing/deleting data from the database
def checkMasterPassword(masterPassword, AES_key):
    decryptFile("/data/master_account_data.csv.enc", AES_key)
    with open(getcwd() + "/data/master_account_data.csv") as csvDataFile:
        csvReader = DictReader(csvDataFile, delimiter=',')
        for row in csvReader:
            status = row["masterPassword"] == masterPassword
    encryptFile("/data/master_account_data.csv", AES_key)
    return status


# get all indices of the entries of the database
def getIndices(AES_key):
    indices = []
    for row in readCsvDataDict("/data/account_data.csv", AES_key):
        indices.append(row["ID"])
    return indices


def getColumnData(fieldName, AES_key, unique=True):
    results = []
    rows = readCsvDataDict("/data/account_data.csv", AES_key)
    for row in rows:
        if row[fieldName] in results and unique:
            continue
        results.append(row[fieldName])
    return results


def getRowData(ID, AES_key):
    rows = readCsvDataDict("/data/account_data.csv", AES_key)
    for row in rows:
        if row["ID"] == ID:
            return row
    return False


# option 1 - store account data in database
def storeData(siteName, url, username, email, password, expiration, category, AES_key):
    rows = readCsvDataDict("/data/account_data.csv", AES_key)

    for row in rows:
        if row["siteName"] == siteName and row["url"] == url and row["username"] == username and row["email"] == email:
            config.systemMessage = " The account already exists!"
            return False

    rows.append({"ID": len(rows),
                 "siteName": siteName,
                 "url": url,
                 "username": username,
                 "email": email,
                 "password": password,
                 "changeDate": sub("\.\d+", "", str(datetime.now())),
                 "expiration": expiration,
                 "category": category})
    writeCsvDataDict("/data/account_data.csv", rows, "s", AES_key)
    return True


# option 2 - delete account data from database
def deleteData(ID, AES_key):
    rows = readCsvDataDict("/data/account_data.csv", AES_key)
    for row in rows:
        if row["ID"] == ID:
            rows.remove(row)
    for i, row in enumerate(rows, 0):
        row["ID"] = str(i)
    writeCsvDataDict("/data/account_data.csv", rows, "d", AES_key)


# option 3 - search account data from database
def findData(searchingField, searchingValue, AES_key, output=None):
    if output is None:
        output = ["ID", "siteName", "username", "email", "password", "category"]
    accountData = PrettyTable()
    accountData.field_names = output
    accountData.align = "l"
    accountData.align["ID"] = "r"
    results = []
    indices = []
    outputRows = []

    for row in readCsvDataDict("/data/account_data.csv", AES_key):
        if searchingValue.lower() in row[searchingField].lower():
            results.append(row)
    if results:
        for row in results:
            outputRow = []
            indices.append(row["ID"])
            for element in output:
                if element == "password":
                    outputRow.append("*"*len(row[element]))
                else:
                    outputRow.append(row[element])
            outputRows.append(outputRow)
        outputRows.sort(key=lambda row: row[1])
        for row in outputRows:
            accountData.add_row(row)
        print("")
        print(" {} results for: {}".format(searchingField, searchingValue))
        print(accountData)
        return results, indices
    else:
        config.systemMessage = " No {} results for: {}".format(searchingField, searchingValue)
        return [], []


# option 4 - change account data
def changeData(ID, fieldName, changeValue, AES_key):
    rows = readCsvDataDict("/data/account_data.csv", AES_key)
    for row in rows:
        if row["ID"] == str(ID):
            if row[fieldName] == changeValue:
                config.systemMessage = " Nothing to change here!"
                return
            else:
                if fieldName == "password":
                    row[fieldName] = changeValue
                    row["changeDate"] = sub("\.\d+", "", str(datetime.now()))
                else:
                    row[fieldName] = changeValue
    writeCsvDataDict("/data/account_data.csv", rows, "c", AES_key)


# option 5 - show all database entries sorted
def showDatabase(AES_key, sortedBy=1):
    database = PrettyTable()
    database.field_names = ["ID", "siteName", "url", "username", "email", "password", "changeDate", "exp.", "category"]
    database.align = "l"
    database.align["ID"] = "r"
    entries = []

    for row in readCsvDataDict("/data/account_data.csv", AES_key):
        # replace password with *
        row["password"] = "*"*len(row["password"])

        # shorten url
        if len(row["url"]) > 34:
            row["url"] = "{}...".format(row["url"][:34])

        entries.append(list(row.values()))
    entries.sort(key=lambda entries: entries[sortedBy])
    for entry in entries:
        database.add_row(entry)
    print()
    print(database)
