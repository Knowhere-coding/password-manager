from csv import reader, DictReader, writer, DictWriter
from os import getcwd
from fileEncryption import encryptFile, decryptFile
import config


# read .csv file data
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
def writeCsvDataDict(fileName, rows, case, AES_key):
    decryptFile((fileName + ".enc"), AES_key)
    with open(getcwd() + fileName, mode="w", newline="") as csvDataFile:
        csvWriter = DictWriter(csvDataFile, rows[0].keys(), delimiter=",")
        csvWriter.writeheader()

        for row in rows:
            csvWriter.writerow(row)

        if case == "s":
            config.systemMessage = " All data stored!"
        elif case == "d":
            config.systemMessage = " Account deleted!"
        elif case == "c":
            config.systemMessage = " Account updated!"
    encryptFile(fileName, AES_key)
