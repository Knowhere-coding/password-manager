import xlwings as xw
from datetime import datetime
import re
from csvHandling import readCsvDataWithoutHead
import menu
from termcolor import colored


def getAccountData(AES_key):
    dataFilePath = "/data/account_data.csv"
    accountData = readCsvDataWithoutHead(dataFilePath, AES_key)
    spacer = ["" for _ in range(8)]
    data = []
    temp = ""
    for row in accountData:
        row.pop(7)

    accountData.sort(key=lambda accountData: accountData[7])

    for i in range(len(accountData)):
        if accountData[i][7] != temp:
            temp = accountData[i][7]
            data.append(spacer)
        data.append(accountData[i])
    return data


def getMasterData(AES_key):
    dataFilePath = "/data/master_account_data.csv"
    return readCsvDataWithoutHead(dataFilePath, AES_key)[0]


def writeDataToExcel(templateFilePath, AES_key):
    try:
        # Start Visible Excel
        xl_app = xw.App(visible=True, add_book=False)

        # Open template file
        wb = xl_app.books.open(templateFilePath)

        # Assign the sheet holding the template table to a variable
        ws = wb.sheets("Password List")

        # insert master data
        masterData = getMasterData(AES_key)
        ws.range((2, 3)).value = masterData[1]
        ws.range((2, 5)).value = masterData[0]

        # insert account data rows
        accountData = getAccountData(AES_key)
        ws.range((4, 1)).value = accountData

        # Save file
        print(" Do you want to {} the print layout? (Y/N)".format(colored("save", "green")))
        choice = True if input(" > ").upper() == "Y" else False
        if choice:
            dstPath = "print_layout/"
            date = re.sub("\.\d+", "", str(datetime.now())).replace("-", "").replace(" ", "_").replace(":", "")
            fileName = date + "_passwordList.xlsx"
            wb.save(dstPath + fileName)
        try:
            wb.close()
            xl_app.quit()
        except Exception:
            menu.systemMessage = " Please do not close Excel!"

    except Exception as ex:
            menu.systemMessage = " Error while writing data to excel!"
