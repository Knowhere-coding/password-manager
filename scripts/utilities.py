from pyperclip import copy
from webbrowser import open_new_tab
from termcolor import colored


# give the user a choice
def choicePrompt():
    choice = input(" > ")
    return True if choice.upper() == "Y" else False


# copy data to clipboard
def copyToClipboard(msg):
    copy(msg)
    print('-' * 47)
    print("")
    print(" Your {} has been copied to your {}".format(colored("password", "green"), colored("clipboard", "cyan")))
    print("")
    print('-' * 47)


# open url
def openUrl(url):
    # open url
    print("\n Do you want to open the {}? (Y/N):".format(colored("url", "green")))

    if choicePrompt():
        open_new_tab("https://" + url)


# show an options list and return the chosen option
def showOptions(options):
    for key in options:
        print("   {} - {}".format(key, colored(options[key], "white")))
    userInput = input(" > ")
    while userInput not in [str(x) for x in options.keys()]:
        userInput = input(" > ")
    return options[int(userInput)]
