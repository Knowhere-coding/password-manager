from time import ctime, strptime
from os import path, getcwd, listdir, rename, remove
from shutil import rmtree
from datetime import datetime, timedelta
from termcolor import colored
from re import compile
from fileHandling import createZipFile, unzipFile
from passwordManagement import accountBarrier
import config


# option 6 - make backup
def createBackupFile(dst_path):
    try:
        createZipFile(dst_path)
        return True
    except FileNotFoundError:
        print(" \n File path not found or empty!")
        return False
    except PermissionError:
        print(" \n Permission denied!")
        return False


def getLastBackupDate(dst_path):
    fileNamePattern = "^\d{4}(?:0[1-9]|1[0-2])(?:[0-2][1-9]|3[0-1])_(?:[0-1]\d|2[0-3])(?:[0-5]\d){2}_backup\.zip$"
    pFileName = compile(fileNamePattern)
    files = listdir(dst_path)
    lastBackupTime = 0
    for file in files:
        if not pFileName.match(file):
            continue
        else:
            if path.getctime(dst_path + file) > lastBackupTime:
                lastBackupTime = path.getctime(dst_path + file)
    return datetime.fromtimestamp(lastBackupTime)


def createAutomaticBackup(dst_path):
    if (getLastBackupDate(dst_path) + timedelta(days=30)) < datetime.now():
        createBackupFile(dst_path)
        config.systemMessage = " Automatic backup saved!"


def getBackupFiles(dirPath):
    try:
        return listdir(dirPath)
    except FileNotFoundError:
        print(" \n File path not found or empty!")
        return None
    except PermissionError:
        print(" \n Permission denied!")
        return None


def showBackupFileList(files, dirPath):
    indices = []
    for i, file in enumerate(files):
        indices.append(str(i))
        backupAge = datetime.now() - datetime.fromtimestamp(path.getctime(dirPath + file))
        print("   {} - {:30} {:4d} days ago".format(colored(i, "cyan"), file, backupAge.days))
    return indices


def loadBackupFile(filePath):
    if (getLastBackupDate(getcwd() + "/backup/") + timedelta(days=1)) < datetime.now():
        createBackupFile(getcwd() + "/backup/")
    # remove directory if it exists
    try:
        rmtree(getcwd() + "\data_old")
    except:
        pass
    rename(getcwd() + "\data", getcwd() + "\data_old")
    try:
        unzipFile(filePath)
        if accountBarrier():
            rmtree(getcwd() + "\data_old")
            return True
        else:
            rmtree(getcwd() + "\data")
            rename(getcwd() + "\data_old", getcwd() + "\data")
            return False
    except Exception:
        # remove directory if it exists
        try:
            rmtree(getcwd() + "\data")
        except:
            pass
        rename(getcwd() + "\data_old", getcwd() + "\data")
        return False
