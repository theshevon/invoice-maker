'''
:name: pdf_generator.py
:author: Shevon Mendis <shevonmendis@gmail.com>
:purpose: To create PDFs based on a template.
'''

import os
from reportlab.pdfgen.canvas import Canvas
from common.defaults import PDF_STORAGE_PATH
from modules.util import to_date_string

def generate_files(start_date, end_date, invoice_data, logger):
    '''
        Generates a PDF file that represents an invoice statement.

        Arguments:
            start_date     (datetime): Lower bound for record cut off
            end_date       (datetime): Upper bound for record cut off
            invoice_data (Dictionary): Info that needs to be added to the PDF
            logger           (Logger): Logger

        Returns:
            Dictionary: A dictionary containing the information needed to generate and send the emails
    '''

    subfolder_name = to_date_string(start_date) + " to " + to_date_string(end_date)

    # make new folder if needed
    try:
        path = f"{ os.getcwd() }/{ PDF_STORAGE_PATH }{ subfolder_name }"
        os.makedirs(path)
        logger.info(f"Created a new directory at: { path }")
    except FileExistsError:
        logger.info(f"Directory already exists at: { path }")

    # create PDF for each of the records
    mail_data = []
    for data in invoice_data:

        client_data = data["client_data"]
        services_data = data["services_data"]
        remarks = data["remarks"]
        
        path_to_pdf = f"{ PDF_STORAGE_PATH }{ subfolder_name }/{ client_data['name'] }.pdf"

        # create PDF
        # TODO: replace with injected template
        canvas = Canvas(path_to_pdf)
        canvas.drawString(72, 72, client_data['name'])
        canvas.save()

        mail_data.append({
            "client_data": client_data,
            "path_to_pdf": path_to_pdf
        })

    return mail_data