"""
:name: sheet_reader.py
:author: Shevon Mendis <shevonmendis@gmail.com>
:purpose: Reading of data from a Google Sheet.
"""

import gspread
from common.constants import CREDENTIALS_FILE_PATH, GOOGLE_SHEET_ID

def read_records(debug):
    '''
        Reads data from a google sheet.

        Arguments:
            debug (bool): Denotes whether or not logging is required

        Returns:
            List: A list where each item is a dictionary representing a record from the spreadsheet
    '''

    gc = gspread.service_account(CREDENTIALS_FILE_PATH)
    spreadsheet = gc.open_by_key(GOOGLE_SHEET_ID)
    worksheet = spreadsheet.sheet1

    return worksheet.get_all_records()