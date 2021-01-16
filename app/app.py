"""
:name: app.py
:author: Shevon Mendis <shevonmendis@gmail.com>
:purpose: To generate invoices and email contacts based on info read from a Google Sheet.
"""

import util.sheet_reader as sheet_reader
import util.pdf_generator as pdf_generator

def execute():
    data = sheet_reader.read_data()
    pdf_generator.generate_file("week2", "test2", str(data))

if __name__ == "__main__":
    execute()