from os import getcwd, path, mkdir
from csv import writer
from re import compile
from fileHandling import hideFile
from fileEncryption import generateAndSaveAESkey, getAESkey, encryptFile
import config


# initialization (create Username/Password), build directories
def initialization():
    cwd = getcwd()
    if path.isdir(cwd + "/data") and path.isfile(cwd + "/data/AES.key.enc") and path.isfile(cwd + "/data/master_account_data.csv.enc") and path.isfile(cwd + "/data/account_data.csv.enc"):
        return False, "", ""
    else:
        print(" You need to setup your Passwordmanager!")

        # validate username
        # regex -> 4-20 chars / beginning with letter a-zA-Z
        usernamePattern = "^[a-zA-Z]+\w{3,20}$"
        pUsername = compile(usernamePattern)

        # username input
        masterUsername = input(" Please input your master username: ")

        while not pUsername.match(masterUsername):
            masterUsername = input(" Please provide a valid username (4-20 chars, starts with char): ")

        # validate password
        # regex -> min. 8 chars / min. 1x: A-Z / a-z / 0-9 / !#$%&'()*+-./:;<=>?@^_`{|}~\]\[]
        passwordPattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[!#$%&'()*+-./:;<=>?@^_`{|}~\]\[]).{8,}$"
        pPassword = compile(passwordPattern)

        # password input
        masterPassword = input(" Please input your master password: ")

        while not pPassword.match(masterPassword) or "," in masterPassword:
            masterPassword = input(" Please provide a valid password (8-32 chars, (char,num,specialchar)): ")

        if not path.isdir(cwd + "/data"):
            mkdir(cwd + "/data")
            hideFile(cwd + "/data")

        if not path.isdir(cwd + "/backup"):
            mkdir(cwd + "/backup")
            hideFile(cwd + "/backup")

        createMasterAccountDatabase(masterUsername, masterPassword)
        return True, masterUsername, masterPassword


# initialization - create master account database .csv file
def createMasterAccountDatabase(masterUsername, masterPassword):
    generateAndSaveAESkey(masterPassword)
    AES_key = getAESkey(masterPassword)

    with open(getcwd() + "/data/master_account_data.csv", mode="w", newline="") as csvDataFile:
        writer(csvDataFile, delimiter=",").writerows([["masterUsername", "masterPassword"], [masterUsername, masterPassword]])
    encryptFile("/data/master_account_data.csv", AES_key)

    config.systemMessage = " All master data stored!"
    createAccountDatabase(AES_key)


# initialization - create account database .csv file
def createAccountDatabase(AES_key):
    with open(getcwd() + "/data/account_data.csv", mode="w", newline="") as csvDataFile:
        writer(csvDataFile, delimiter=",").writerow(["ID", "siteName", "url", "username", "email", "password", "changeDate", "expiration", "category"])
    encryptFile("/data/account_data.csv", AES_key)
    config.systemMessage = " Account database created!"
