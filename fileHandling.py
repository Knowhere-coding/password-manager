import csv
import zipfile
import os
import re
from datetime import datetime
from fileEncryption import encryptFile, decryptFile, saveDecryptFile


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
            print(" Account deleted!")
        elif case == "s":
            print(" All data stored!")
    encryptFile(fileName, AES_key)


# create .zip file
def createZipFile(dst_path):
    date = "_" + re.sub("\.\d+", "", str(datetime.now())).replace("-", "").replace(" ", "_").replace(":", "")
    new_file = dst_path + "\\" + "backup" + date + '.zip'

    # creating zip file with write mode
    zip = zipfile.ZipFile(new_file, 'w', zipfile.ZIP_DEFLATED)

    # Walk through the files in a directory
    src_path = os.path.dirname(os.path.abspath(__file__)) + "\data"
    for src_path, dir_names, files in os.walk(src_path):
        f_path = src_path.replace(src_path, '')
        f_path = f_path and f_path + os.sep

        # Writing each file into the zip
        for file in files:
            zip.write(os.path.join(src_path, file), f_path + file)
    zip.close()
