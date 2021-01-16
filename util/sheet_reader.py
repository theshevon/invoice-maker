"""
:name: sheet_reader.py
:author: Shevon Mendis <shevonmendis@gmail.com>
:purpose: Reading of data from a Google Sheet.
"""

import gspread
import util.constants as constants

def read_data():
    '''
        Reads data from a google sheet.

        Returns:
            List: A list where each item is a dictionary representing a record from the spreadsheet.
    '''

    gc = gspread.service_account(filename=constants.CREDENTIALS_FILE_PATH)
    spreadsheet = gc.open_by_key(constants.GOOGLE_SHEET_ID)
    worksheet = spreadsheet.sheet1

    return worksheet.get_all_records()