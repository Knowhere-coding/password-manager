from xlwings import App
from datetime import datetime
from re import sub
from csvHandling import readCsvDataWithoutHead
import menu
from termcolor import colored


def createPrintLayoutFile(templateFilePath, AES_key):
    try:
        # Start Visible Excel
        xl_app = App(visible=True, add_book=False)

        # Open template file
        wb = xl_app.books.open(templateFilePath)

        # bring app to foreground
        wb.app.activate(steal_focus=True)

        # add data to each sheet
        for sheet in wb.sheets:
            # insert account data
            writeDataToExcel(sheet, getMasterData(AES_key), getAccountData(sheet.name, AES_key))
            sheet.name = sheet.name[0].upper() + sheet.name[1:] + " List"

        # user prompt
        userPrompt(xl_app, wb)

    except Exception as ex:
        try:
            wb.close()
            xl_app.quit()
        except Exception as ex:
            menu.systemMessage = " Error while writing data to excel!"
        menu.systemMessage = " Error while writing data to excel!"


def getWs():
    pass


def getAccountData(category, AES_key):
    dataFilePath = "/data/account_data.csv"
    accountData = readCsvDataWithoutHead(dataFilePath, AES_key)
    data = []
    for row in accountData:
        row.pop(7)

    for i in range(len(accountData)):
        if accountData[i][7] == category or category == "all":
            data.append(accountData[i])
    return data


def getMasterData(AES_key):
    dataFilePath = "/data/master_account_data.csv"
    return readCsvDataWithoutHead(dataFilePath, AES_key)[0]


def writeDataToExcel(ws, masterData, accountData):
    # insert master data
    ws.range((2, 3)).value = masterData[0]
    ws.range((2, 5)).value = masterData[1]

    # insert account data rows
    ws.range((4, 1)).value = accountData


def userPrompt(xl_app, wb):
    # Save file
    print(" Do you want to {} the print layout? (Y/N)".format(colored("save", "green")))
    choice = True if input(" > ").upper() == "Y" else False
    if choice:
        dstPath = "print_layout/"
        date = sub("\.\d+", "", str(datetime.now())).replace("-", "").replace(" ", "_").replace(":", "")
        fileName = date + "_passwordList.xlsx"
        wb.save(dstPath + fileName)
    try:
        wb.close()
        xl_app.quit()
    except Exception:
        menu.systemMessage = " Please do not close Excel!"
