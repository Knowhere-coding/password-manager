from string import ascii_letters, digits
from random import choice, randint
from sympy import isprime


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
