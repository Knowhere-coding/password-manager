import csv
import os
import re
from datetime import datetime
from prettytable import PrettyTable
from passwordManagement import AESkey, sha512
from fileEncryption import encryptFile, decryptFile, saveDecryptFile


# TODO: add password reset timer
# TODO: encryption on error

# read .csv file data
def readCsvData(fileName, AES_key):
    rows = []
    decryptFile((fileName+".enc"), AES_key)
    with open(fileName, mode="r", newline="") as csvDataFile:
        csvReader = csv.reader(csvDataFile, delimiter=",")
        for row in csvReader:
            rows.append(row)
    encryptFile(fileName, AES_key)
    return rows


# read .csv file data (DictReader)
def readCsvDataDict(fileName, AES_key):
    rows = []
    decryptFile((fileName + ".enc"), AES_key)
    with open(fileName, mode="r", newline="") as csvDataFile:
        csvReader = csv.DictReader(csvDataFile, delimiter=",")
        for row in csvReader:
            rows.append(row)
    encryptFile(fileName, AES_key)
    return rows


# write .csv file data
def writeCsvData(fileName, rows, case, AES_key):
    decryptFile((fileName+".enc"), AES_key)
    with open(fileName, mode="w", newline="") as csvDataFile:
        csvWriter = csv.writer(csvDataFile, delimiter=",")
        for row in rows:
            csvWriter.writerow(row)
        if case == "d":
            print("Account deleted!")
        elif case == "s":
            print("All data stored!")
    encryptFile(fileName, AES_key)


# check if the database has entries
def databaseStatus(AES_key):
    if len(readCsvData("data/account_data.csv", AES_key)) == 1:
        print("")
        print("No data found!")
        print("")
        return False
    else:
        return True


def checkMaster(masterUsername, masterPassword, AES_key):
    #AES_key = AESkey(masterPassword)
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

    print("All master data stored!")
    createAccountDatabase(AES_key)


# initialization - create account database .csv file
def createAccountDatabase(AES_key):
    with open("data/account_data.csv", mode="w", newline="") as csvDataFile:
        csv.writer(csvDataFile, delimiter=",").writerow(["ID", "siteName", "url", "username", "email", "password", "changeDate", "expiration", "category"])
    encryptFile("data/account_data.csv", AES_key)
    print("Account database created")


# option 1 - store account data in database
def storeData(siteName, url, username, email, password, expiration, category, AES_key):
    status = True
    ID = 0
    rows = readCsvData("data/account_data.csv", AES_key)

    for ID, row in enumerate(rows, 0):
        if row[1:-3] == [siteName, url, username, email]:
            print("The account already exists")
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
        output = ["ID", "siteName", "url", "username", "email", "password", "changeDate", "expiration", "category"]
    accountData = PrettyTable()
    accountData.field_names = output
    results = []
    indices = []
    outputRow2 = []

    if not databaseStatus(AES_key):
        return [], []
    else:
        for row in readCsvDataDict("data/account_data.csv", AES_key):
            if row[searchingField].lower() == searchingValue.lower():
                results.append(row)

        for row in results:
            outputRow = []
            indices.append(row["ID"])
            for element in output:
                outputRow.append(row[element])
            outputRow2.append(outputRow)
        outputRow2.sort(key=lambda row: row[1])
        for row in outputRow2:
            accountData.add_row(row)
        print("")
        print("Results for: " + searchingValue)
        print(accountData)
        return results, indices


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

    if databaseStatus(AES_key):
        for row in readCsvData("data/account_data.csv", AES_key)[1:]:
            entries.append(row)
        entries.sort(key=lambda entries: entries[sortedBy])
        for entry in entries:
            database.add_row(entry)
        print(database)
