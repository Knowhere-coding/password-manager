import hashlib
from string import ascii_letters, digits
from random import choice, randint
from sympy import *


# master password hash
def sha512(password):
    return hashlib.sha512(password.encode('utf-8')).hexdigest()


# create AES key for file encryption from master password hash
def AESkey(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()[23:55]


# create a random password
def createNewPassword(minLength, maxLength, specialChars):
    if specialChars == "-":
        specialChars = "!#$%&'()*+-./:;<=>?@[]^_`{|}~"
    specialChars.replace(",", "")
    password = ""
    for x in range(randint(minLength, maxLength)):
        i = randint(1, 100)
        if isprime(i):
            password += choice(specialChars)
        elif i % 2 == 1:
            password += choice(digits)
        elif i % 2 == 0:
            password += choice(ascii_letters)
    return password
