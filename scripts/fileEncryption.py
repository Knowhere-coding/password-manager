from Crypto import Random
from Crypto.Cipher import AES
import os
from fileHandling import hideFile


# encrypt text
def encrypt(message, key, key_size=256):
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key.encode("utf8"), AES.MODE_CFB, iv)
    return iv + cipher.encrypt(message)


# decrypt text
def decrypt(cipherText, key):
    iv = cipherText[:AES.block_size]
    cipher = AES.new(key.encode("utf8"), AES.MODE_CFB, iv)
    text = cipher.decrypt(cipherText[AES.block_size:])
    return text.rstrip(b"\0")


# write encrypted text to file and delete decrypted file
def encryptFile(fileName, key):
    with open(os.getcwd() + fileName, 'rb') as file:
        text = file.read()
    enc = encrypt(text, key)
    with open(os.getcwd() + fileName + ".enc", 'wb') as file:
        file.write(enc)
    os.remove(os.getcwd() + fileName)
    hideFile(os.getcwd() + fileName + ".enc")


# write decrypted text to file and delete .enc file
def decryptFile(fileName, key):
    with open(os.getcwd() + fileName, 'rb') as file:
        cipherText = file.read()
    dec = decrypt(cipherText, key)
    with open(os.getcwd() + fileName[:-4], 'wb') as file:
        file.write(dec)
    os.remove(os.getcwd() + fileName)


# decrypt file w/o deleting .enc file
def saveDecryptFile(fileName, key):
    with open(os.getcwd() + fileName, 'rb') as file:
        cipherText = file.read()
    dec = decrypt(cipherText, key)
    with open(os.getcwd() + fileName[:-4], 'wb') as file:
        file.write(dec)
