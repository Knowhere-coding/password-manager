from hashlib import sha256
from base64 import b64encode
from cryptography.fernet import Fernet
from os import getcwd, remove
from fileHandling import hideFile


# generate AESkey and save it to a encrypted file
def generateAndSaveAESkey(password):
    AES_key = getAESkey(password)
    with open(getcwd() + "/data/AES.key", mode="wb") as file:
        file.write(AES_key)
    encryptFile("/data/AES.key", AES_key)


def getAESkey(password):
    return b64encode(sha256(password.encode("utf-8")).hexdigest()[23:55].encode("utf-8"))


# write encrypted text to file and delete decrypted file
def encryptFile(fileName, AESkey):
    absFilePath = getcwd() + fileName
    fernet = Fernet(AESkey)
    with open(absFilePath, "rb") as file:
        decData = file.read()
    encData = fernet.encrypt(decData)
    with open(absFilePath + ".enc", "wb") as file:
        file.write(encData)
    remove(absFilePath)
    hideFile(absFilePath + ".enc")


# write decrypted text to file and delete .enc file
def decryptFile(fileName, AESkey):
    saveDecryptFile(fileName, AESkey)
    remove(getcwd() + fileName)


# decrypt file w/o deleting .enc file
def saveDecryptFile(fileName, AESkey):
    absFilePath = getcwd() + fileName
    fernet = Fernet(AESkey)
    with open(absFilePath, "rb") as file:
        encData = file.read()
    decData = fernet.decrypt(encData)
    with open(absFilePath[:-4], "wb") as file:
        file.write(decData)
