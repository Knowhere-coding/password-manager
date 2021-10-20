import re

passwordPattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[!#$%&'()*+-./:;<=>?@^_`{|}~\]\[]).{8,}$"
pPassword = re.compile(passwordPattern)

# password input
masterPassword = input("Please input your master password: ")
while not pPassword.match(masterPassword) or "," in masterPassword:
    masterPassword = input("Please provide a valid password (8-32 chars, (char,num,specialchar): ")
