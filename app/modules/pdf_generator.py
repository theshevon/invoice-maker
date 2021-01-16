"""
:name: pdf_generator.py
:author: Shevon Mendis <shevonmendis@gmail.com>
:purpose: To create PDFs based on a template.
"""

import os
from reportlab.pdfgen.canvas import Canvas
from common.constants import PDF_STORAGE_PATH, DATE_STR_FORMAT_2

def generate_files(start_date, end_date, invoice_data, debug):
    """
        Generates a PDF file that represents an invoice statement.

        Arguments:
            start_date     (datetime): Lower bound for record cut off
            end_date       (datetime): Upper bound for record cut off
            invoice_data (Dictionary): Info that needs to be added to the PDF
            debug              (bool): Denotes whether or not logging is required
    """

    subfolder_name = start_date.strftime(DATE_STR_FORMAT_2) + " to " + end_date.strftime(DATE_STR_FORMAT_2) 

    # make new folder if needed
    try:
        path = f"{ os.getcwd() }/{ PDF_STORAGE_PATH }{ subfolder_name }"
        os.makedirs(path)
    except FileExistsError:
        print("File already exists")

    # create PDF for each of the records
    for data in invoice_data:

        client_data = data["client_data"]
        services_data = data["services_data"]
        remarks = data["remarks"]
        
        canvas = Canvas(f"{ PDF_STORAGE_PATH }{ subfolder_name }/{ client_data['name'] }.pdf")
        canvas.drawString(72, 72, client_data['name'])
        canvas.save()