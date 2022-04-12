from csv import reader, DictReader, writer
from os import getcwd
from fileEncryption import encryptFile, decryptFile
import menu


# read .csv file data
def readCsvData(fileName, AES_key):
    rows = []
    decryptFile((fileName + ".enc"), AES_key)
    with open(getcwd() + fileName, mode="r", newline="") as csvDataFile:
        csvReader = reader(csvDataFile, delimiter=",")
        for row in csvReader:
            rows.append(row)
    encryptFile(fileName, AES_key)
    return rows


def readCsvDataWithoutHead(fileName, AES_key):
    return readCsvData(fileName, AES_key)[1:]


# read .csv file data (DictReader)
def readCsvDataDict(fileName, AES_key):
    rows = []
    decryptFile((fileName + ".enc"), AES_key)
    with open(getcwd() + fileName, mode="r", newline="") as csvDataFile:
        csvReader = DictReader(csvDataFile, delimiter=",")
        for row in csvReader:
            rows.append(row)
    encryptFile(fileName, AES_key)
    return rows


# write .csv file data
def writeCsvData(fileName, rows, case, AES_key):
    decryptFile((fileName + ".enc"), AES_key)
    with open(getcwd() + fileName, mode="w", newline="") as csvDataFile:
        csvWriter = writer(csvDataFile, delimiter=",")
        for row in rows:
            csvWriter.writerow(row)
        if case == "d":
            menu.systemMessage = " All data stored!"
        elif case == "s":
            menu.systemMessage = " All data stored!"
    encryptFile(fileName, AES_key)
