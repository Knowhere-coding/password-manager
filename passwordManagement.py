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
def createNewPassword(specialChars="!#$%&'()*+-./:;<=>?@[]^_`{|}~"):
    specialChars.replace(",", "")
    password = ""
    for x in range(randint(16, 32)):
        i = randint(1, 100)
        if isprime(i):
            password += choice(specialChars)
        elif i % 2 == 1:
            password += choice(digits)
        elif i % 2 == 0:
            password += choice(ascii_letters)
    return password


# print(AESkey("1234"))
# print(createNewPassword())

# -------------- Calculation ----------------------------------------------------------------------------- #

# primes, odds, evens = 0, 0, 0
#
# for x in range(100):
#    if isprime(x):
#        primes += 1
#    elif x%2==1:
#        odds += 1
#    elif x%2==0:
#        evens += 1
#
# print("Special characters: {}%\nDigits: {}%\nLetters: {}%\nSum: {}%".format(primes, odds, evens, (primes+odds+evens)))

# -------------------------------------------------------------------------------------------------------- #
