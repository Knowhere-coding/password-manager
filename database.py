import csv
import os
import re
from datetime import datetime
from prettytable import PrettyTable
from passwordManagement import AESkey, sha512
from fileEncryption import encryptFile, decryptFile, saveDecryptFile
from fileHandling import createZipFile
from csvHandling import readCsvData, readCsvDataDict, writeCsvData


# check if the database has entries
def databaseStatus(AES_key):
    if len(readCsvData("data/account_data.csv", AES_key)) == 1:
        print("")
        print(" The database is empty!")
        print("")
        return False
    else:
        return True


# validate the master account data
def checkMaster(masterUsername, masterPassword, AES_key):
    masterPassword = sha512(masterPassword)
    error = False

    # check AES_key
    saveDecryptFile("data/AES_key.txt.enc", AES_key)
    with open("data/AES_key.txt") as file:
        try:
            text = file.read()
        except UnicodeDecodeError:
            error = True

    os.remove("data/AES_key.txt")
    if error:
        return False

    if text == AES_key:
        # check master account data
        decryptFile("data/master_account_data.csv.enc", AES_key)
        with open("data/master_account_data.csv") as csvDataFile:
            csvReader = csv.reader(csvDataFile, delimiter=',')
            for row in csvReader:
                status = masterUsername == row[0] and masterPassword == row[1]
        encryptFile("data/master_account_data.csv", AES_key)
    else:
        status = False
    return status


# check master password for the password barrier when changing/deleting data from the database
def checkMasterPassword(masterPassword, AES_key):
    masterPassword = sha512(masterPassword)

    decryptFile("data/master_account_data.csv.enc", AES_key)
    with open("data/master_account_data.csv") as csvDataFile:
        csvReader = csv.reader(csvDataFile, delimiter=',')
        for row in csvReader:
            status = row[1] == masterPassword
    encryptFile("data/master_account_data.csv", AES_key)

    return status


# initialization - create master account database .csv file
def createMasterAccountDatabase(masterUsername, masterPassword):
    AES_key = AESkey(masterPassword)
    masterPassword = sha512(masterPassword)

    with open("data/master_account_data.csv", mode="w", newline="") as csvDataFile:
        csv.writer(csvDataFile, delimiter=",").writerows([["masterUsername", "masterPassword"], [masterUsername, masterPassword]])
    encryptFile("data/master_account_data.csv", AES_key)

    with open("data/AES_key.txt", mode="w") as file:
        file.write(AES_key)
    encryptFile("data/AES_key.txt", AES_key)

    print(" All master data stored!")
    createAccountDatabase(AES_key)


# initialization - create account database .csv file
def createAccountDatabase(AES_key):
    with open("data/account_data.csv", mode="w", newline="") as csvDataFile:
        csv.writer(csvDataFile, delimiter=",").writerow(["ID", "siteName", "url", "username", "email", "password", "changeDate", "expiration", "category"])
    encryptFile("data/account_data.csv", AES_key)
    print(" Account database created!")


# get all indices of the entries of the database
def getIndices(AES_key):
    indices = []
    for row in readCsvDataDict("data/account_data.csv", AES_key):
        indices.append(row["ID"])
    return indices


def getData(fieldName, AES_key, unique=True):
    results = []
    rows = readCsvDataDict("data/account_data.csv", AES_key)
    for row in rows:
        if row[fieldName] in results and unique:
            continue
        results.append(row[fieldName])
    return results


# option 1 - store account data in database
def storeData(siteName, url, username, email, password, expiration, category, AES_key):
    status = True
    ID = 0
    rows = readCsvData("data/account_data.csv", AES_key)

    for ID, row in enumerate(rows, 0):
        if row[1:5] == [siteName, url, username, email]:
            print(" The account already exists!")
            status = False
            break
    if status:
        rows.append([ID, siteName, url, username, email, password, re.sub("\.\d+", "", str(datetime.now())), expiration, category])
        writeCsvData("data/account_data.csv", rows, "s", AES_key)
    return status


# option 2 - delete account data from database
def deleteData(ID, AES_key):
    rows = readCsvData("data/account_data.csv", AES_key)
    for row in rows:
        if row[0] == ID:
            rows.remove(row)
    for i, row in enumerate(rows[1:], 0):
        row[0] = str(i)
    writeCsvData("data/account_data.csv", rows, "d", AES_key)


# option 3 - search account data from database
def findData(searchingField, searchingValue, AES_key, output=None):
    if output is None:
        output = ["ID", "siteName", "username", "email", "password", "category"]
    accountData = PrettyTable()
    accountData.field_names = output
    results = []
    indices = []
    outputRows = []

    for row in readCsvDataDict("data/account_data.csv", AES_key):
        if row[searchingField].lower() == searchingValue.lower():
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
        print(" No {} results for: {}".format(searchingField, searchingValue))
        return [], []


# option 4 - change account data
def changeData(ID, fieldName, changeValue, AES_key):
    rows = readCsvDataDict("data/account_data.csv", AES_key)
    newRows = [rows[0].keys()]
    for row in rows:
        if row["ID"] == str(ID):
            if fieldName.lower() == "password":
                row[fieldName] = changeValue
                row["changeDate"] = re.sub("\.\d+", "", str(datetime.now()))
            else:
                row[fieldName] = changeValue
        newRows.append(list(row.values()))
    writeCsvData("data/account_data.csv", newRows, "s", AES_key)


# option 5 - show all database entries sorted
def showDatabase(AES_key, sortedBy=1):
    database = PrettyTable()
    database.field_names = ["ID", "siteName", "url", "username", "email", "password", "changeDate", "expiration", "category"]
    entries = []

    for row in readCsvData("data/account_data.csv", AES_key)[1:]:
        row[5] = "*"*len(row[5])
        entries.append(row)
    entries.sort(key=lambda entries: entries[sortedBy])
    for entry in entries:
        database.add_row(entry)
    print(database)


# option 6 - make backup
def backup(dst_path):
    try:
        createZipFile(dst_path)
        return True
    except FileNotFoundError:
        return False
