import xlwings as xw
from datetime import datetime
import re
from csvHandling import readCsvDataWithoutHead
import menu
from termcolor import colored


def writeDataToExcel(templateFilePath, dataFilePath, AES_key):
    try:
        rows = readCsvDataWithoutHead(dataFilePath, AES_key)

        # Start Visible Excel
        xl_app = xw.App(visible=True, add_book=False)

        # Open template file
        wb = xl_app.books.open(templateFilePath)

        # Assign the sheet holding the template table to a variable
        ws = wb.sheets("Password List")

        # First cell of the template (blank) table
        rowAnchor = 3
        columnAnchor = 1

        # Insert rows
        ws.range((rowAnchor, columnAnchor)).value = rows

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
