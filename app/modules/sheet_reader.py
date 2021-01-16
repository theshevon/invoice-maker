"""
:name: sheet_reader.py
:author: Shevon Mendis <shevonmendis@gmail.com>
:purpose: Reading of data from a Google Sheet.
"""

import gspread
from common.constants import CREDENTIALS_FILE_PATH, GOOGLE_SHEET_ID

def read_records(logger):
    '''
        Reads data from a google sheet.

        Arguments:
            logger (Logger): Logger

        Returns:
            List: A list where each item is a dictionary representing a record from the spreadsheet
    '''

    logger.info(f"Attempting to read info from Google Sheet with ID: { GOOGLE_SHEET_ID }")

    records = []
    try:
        gc = gspread.service_account(CREDENTIALS_FILE_PATH)
        spreadsheet = gc.open_by_key(GOOGLE_SHEET_ID)
        worksheet = spreadsheet.sheet1
        records = worksheet.get_all_records()
        logger.info("Succesfully read records.")
    except:
        logger.error("Could not read records!", exc_info=True)

    return records