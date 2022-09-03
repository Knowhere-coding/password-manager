from zipfile import ZipFile, ZIP_DEFLATED
from os import getcwd, walk, sep, path, system
from re import sub
from datetime import datetime


# create backup .zip file
def createZipFile(dstPath):
    date = sub("\.\d+", "", str(datetime.now())).replace("-", "").replace(" ", "_").replace(":", "")
    newFile = dstPath + "\\" + date + "_backup.zip"

    # creating zip file with write mode
    zip = ZipFile(newFile, 'w', ZIP_DEFLATED)

    # Walk through the files in a directory
    srcPath = getcwd() + "\data"
    for srcPath, _, files in walk(srcPath):
        filePath = srcPath.replace(srcPath, '')
        filePath = filePath and filePath + sep

        # Writing each file into the zip
        for file in files:
            zip.write(path.join(srcPath, file), filePath + file)
    zip.close()


# hide files in explorer
def hideFile(fileName):
    system("attrib +h " + fileName)


# load backup .zip file
def unzipFile(filePath):
    srcPath = getcwd() + "\data"
    with ZipFile(filePath, mode="r") as zip:
        zip.extractall(srcPath)

        # hide directory and files
        hideFile(srcPath)
        for srcPath, _, files in walk(srcPath):
            for file in files:
                hideFile(srcPath + "/" + file)
