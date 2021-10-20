from Crypto import Random
from Crypto.Cipher import AES
import os


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
    with open(fileName, 'rb') as file:
        text = file.read()
    enc = encrypt(text, key)
    with open(fileName + ".enc", 'wb') as file:
        file.write(enc)
    os.remove(fileName)


# write decrypted text to file and delete .enc file
def decryptFile(fileName, key):
    with open(fileName, 'rb') as file:
        cipherText = file.read()
    dec = decrypt(cipherText, key)
    with open(fileName[:-4], 'wb') as file:
        file.write(dec)
    os.remove(fileName)


# decrypt file w/o deleting .enc file
def saveDecryptFile(fileName, key):
    with open(fileName, 'rb') as file:
        cipherText = file.read()
    dec = decrypt(cipherText, key)
    with open(fileName[:-4], 'wb') as file:
        file.write(dec)


# encryptFile("data/account_data.csv", "5e255f067953623c8b388b4459e13f97")
# decryptFile("data/account_data.csv.enc", "5e255f067953623c8b388b4459e13f97")
# 55501786742257113378764546529932
