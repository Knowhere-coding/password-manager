import zipfile
import os
import win32file
import win32con
import re
from datetime import datetime


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


# hide files in explorer
def hideFile(filename):
    flags = win32file.GetFileAttributesW(filename)
    win32file.SetFileAttributes(filename, win32con.FILE_ATTRIBUTE_HIDDEN | flags)
