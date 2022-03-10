import xlwings as xw
from datetime import datetime
import re
from csvHandling import readCsvDataWithoutHead
import menu
import pwinput


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
        dstPath = "print_layout/"
        date = re.sub("\.\d+", "", str(datetime.now())).replace("-", "").replace(" ", "_").replace(":", "")
        fileName = date + "_passwordList.xlsx"
        wb.save(dstPath + fileName)

        pwinput.pwinput(prompt=" Press enter to continue!", mask="")
        wb.close()

        # Quit Excel
        xl_app.quit()

    except Exception as ex:
        menu.systemMessage = "Error while writing data to excel!"
