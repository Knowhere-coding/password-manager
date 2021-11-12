import csv
from fileEncryption import encryptFile, decryptFile


# read .csv file data
def readCsvData(fileName, AES_key):
    rows = []
    decryptFile((fileName + ".enc"), AES_key)
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
    decryptFile((fileName + ".enc"), AES_key)
    with open(fileName, mode="w", newline="") as csvDataFile:
        csvWriter = csv.writer(csvDataFile, delimiter=",")
        for row in rows:
            csvWriter.writerow(row)
        if case == "d":
            print(" Account deleted!")
        elif case == "s":
            print(" All data stored!")
    encryptFile(fileName, AES_key)
