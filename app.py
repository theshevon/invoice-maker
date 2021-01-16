"""
:name: app.py
:author: Shevon Mendis <shevonmendis@gmail.com>
:purpose: To generate invoices and email contacts based on info read from a Google Sheet.
"""

import util.sheet_reader as sheet_reader

def execute():
    data = sheet_reader.read_data()

if __name__ == "__main__":
    execute()