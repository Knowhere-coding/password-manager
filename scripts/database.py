from csv import reader
from os import getcwd, remove
from re import sub
from datetime import datetime
import cryptography.exceptions
from prettytable import PrettyTable
from fileEncryption import encryptFile, decryptFile, saveDecryptFile
from csvHandling import readCsvData, readCsvDataDict, writeCsvData
import menu


# check if the database has entries
def databaseStatus(AES_key):
    if len(readCsvData("/data/account_data.csv", AES_key)) == 1:
        menu.systemMessage = " The database is empty!"
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
                csvReader = reader(csvDataFile, delimiter=',')
                for row in csvReader:
                    status = masterUsername == row[0] and masterPassword == row[1]
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
        csvReader = reader(csvDataFile, delimiter=',')
        for row in csvReader:
            status = row[1] == masterPassword
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
    status = True
    ID = 0
    rows = readCsvData("/data/account_data.csv", AES_key)

    for ID, row in enumerate(rows, 0):
        if row[1:5] == [siteName, url, username, email]:
            menu.systemMessage = " The account already exists!"
            status = False
            break
    if status:
        rows.append([ID, siteName, url, username, email, password, sub("\.\d+", "", str(datetime.now())), expiration, category])
        writeCsvData("/data/account_data.csv", rows, "s", AES_key)
    return status


# option 2 - delete account data from database
def deleteData(ID, AES_key):
    rows = readCsvData("/data/account_data.csv", AES_key)
    for row in rows:
        if row[0] == ID:
            rows.remove(row)
    for i, row in enumerate(rows[1:], 0):
        row[0] = str(i)
    writeCsvData("/data/account_data.csv", rows, "d", AES_key)


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
        menu.systemMessage = " No {} results for: {}".format(searchingField, searchingValue)
        return [], []


# option 4 - change account data
def changeData(ID, fieldName, changeValue, AES_key):
    rows = readCsvDataDict("/data/account_data.csv", AES_key)
    newRows = [rows[0].keys()]
    for row in rows:
        if row["ID"] == str(ID):
            if fieldName.lower() == "password":
                row[fieldName] = changeValue
                row["changeDate"] = sub("\.\d+", "", str(datetime.now()))
            else:
                row[fieldName] = changeValue
        newRows.append(list(row.values()))
    writeCsvData("/data/account_data.csv", newRows, "s", AES_key)


# option 5 - show all database entries sorted
def showDatabase(AES_key, sortedBy=1):
    database = PrettyTable()
    database.field_names = ["ID", "siteName", "url", "username", "email", "password", "changeDate", "exp.", "category"]
    database.align = "l"
    database.align["ID"] = "r"
    entries = []

    for row in readCsvData("/data/account_data.csv", AES_key)[1:]:
        # replace password with *
        row[5] = "*"*len(row[5])

        # shorten url
        if len(row[2]) > 34:
            row[2] = "{}...".format(row[2][:34])

        entries.append(row)
    entries.sort(key=lambda entries: entries[sortedBy])
    for entry in entries:
        database.add_row(entry)
    print()
    print(database)
