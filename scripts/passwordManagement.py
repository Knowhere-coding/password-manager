from string import ascii_letters, digits
from random import choice, randint
from sympy import isprime
from pwinput import pwinput
from termcolor import colored
from datetime import datetime, timedelta
from database import checkMaster, checkMasterPassword
from fileEncryption import getAESkey
from utilities import choicePrompt
import config


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


# create/change password
def passwordOption():
    # option to generate random password
    print("\n Do you want to generate a random {}? (Y/N):".format(colored("password", "green")))

    # generate random password
    if choicePrompt():
        minLength, maxLength = getMinMaxLength()
        specialChars = getSpecialChars()
        password = createNewPassword(minLength, maxLength, specialChars)
    # provide own password
    else:
        print("\n Please provide your own {}:".format(colored("password", "green")))
        password = pwinput(prompt=" > ")

    return password


# let the user define valid special chars for the random generated password
def getSpecialChars():
    print("\n Please specify the given {} besides all letters and digits (if none type -):"
          .format(colored("special characters", "green")))
    return input(" > ")


# let the user define the minimum and maximum length of the random generated password
def getMinMaxLength():
    minLength = 0
    maxLength = 0

    try:
        print("\n Please specify the {} length of the password:".format(colored("minimum", "red")))
        minLength = int(input(" > "))
        print("\n Please specify the {} length of the password:".format(colored("maximum", "green")))
        maxLength = int(input(" > "))
    except ValueError:
        print("\n Please input numbers!")

    while minLength <= 0 or maxLength < minLength or maxLength > 64:
        if minLength <= 0:
            print("\n The minimum value can not be 0 or negative!")
        elif maxLength < minLength:
            print("\n The minimum value can not be higher than the maximum value!")
        elif maxLength > 64:
            print("\n The maximum length of the password is 64!")

        try:
            print("\n New {}:".format(colored("minimum", "red")))
            minLength = int(input(" > "))
            print("\n New {}:".format(colored("maximum", "green")))
            maxLength = int(input(" > "))
        except ValueError:
            print("\n Please input numbers!")

    if maxLength > 32:
        print("\n Secure is not enough for you, right? :D")
    return minLength, maxLength


# check change date and change password
def checkExpirationDate(ID, changeDate, expiration, AES_key):
    if not expiration == "0":
        changeDate = datetime.strptime(changeDate, "%Y-%m-%d %H:%M:%S")

        if (changeDate + timedelta(days=int(expiration))) < datetime.now():
            print("\n {} The password-change-date is more than {} days ago {}".format(colored("!!!", "red"), expiration,
                                                                                      colored("!!!", "red")))
            print("\n Do you want to change the {}? (Y/N):".format(colored("password", "green")))
            choice = choicePrompt()
            if choice:
                password = passwordOption()
                if passwordBarrier(AES_key):
                    changeData(ID, "password", password, AES_key)
                    return password
                else:
                    config.systemMessage = " The given password was incorrect!"
            return ""
        else:
            return ""
    return ""


# password barrier for changing/deleting data from the database
def passwordBarrier(AES_key):
    masterPassword = pwinput(prompt="\n Please provide your master password: ")
    return checkMasterPassword(masterPassword, AES_key)


# account barrier for loading backup
def accountBarrier():
    print("\n To load the backup you need to {} your account!".format(colored("verify", "red")))
    masterUsername = pwinput(prompt=" Please enter the master username: ")
    masterPassword = pwinput(prompt=" Please enter the master password: ")
    if checkMaster(masterUsername, masterPassword, getAESkey(masterPassword)):
        config.AES_key = getAESkey(masterPassword)
        return True
