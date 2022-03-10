import zipfile
import os
import re
from datetime import datetime


# create backup .zip file
def createZipFile(dstPath):
    date = re.sub("\.\d+", "", str(datetime.now())).replace("-", "").replace(" ", "_").replace(":", "")
    newFile = dstPath + "\\" + date + "_backup.zip"

    # creating zip file with write mode
    zip = zipfile.ZipFile(newFile, 'w', zipfile.ZIP_DEFLATED)

    # Walk through the files in a directory
    srcPath = os.getcwd() + "\data"
    for srcPath, dir_names, files in os.walk(srcPath):
        filePath = srcPath.replace(srcPath, '')
        filePath = filePath and filePath + os.sep

        # Writing each file into the zip
        for file in files:
            zip.write(os.path.join(srcPath, file), filePath + file)
    zip.close()


# hide files in explorer
def hideFile(fileName):
    os.system("attrib +h " + fileName)
