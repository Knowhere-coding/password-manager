from fileHandling import createZipFile
from time import ctime, strptime
from os import path, getcwd, listdir
from datetime import datetime, timedelta
from re import compile
import menu


# option 6 - make backup
def createBackupFile(dst_path):
    try:
        createZipFile(dst_path)
        return True
    except FileNotFoundError:
        return False


def getLastBackupDate(dst_path):
    fileNamePattern = "^\d{4}(?:0[1-9]|1[0-2])(?:[0-2][1-9]|3[0-1])_(?:[0-1]\d|2[0-3])(?:[0-5]\d){2}_backup\.zip$"
    pFileName = compile(fileNamePattern)
    files = listdir(dst_path)
    lastBackupTime = 0
    for file in files:
        if not pFileName.match(file):
            files.remove(file)
        else:
            if path.getctime(dst_path + file) > lastBackupTime:
                lastBackupTime = path.getctime(dst_path + file)
    return datetime.fromtimestamp(lastBackupTime)


def createAutomaticBackup(dst_path):
    if (getLastBackupDate(dst_path) + timedelta(days=30)) < datetime.now():
        createBackupFile(dst_path)
        menu.systemMessage = " Automatic backup saved!"
