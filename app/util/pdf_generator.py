"""
:name: pdf_generator.py
:author: Shevon Mendis <shevonmendis@gmail.com>
:purpose: To create PDFs based on a template.
"""

import os
from reportlab.pdfgen.canvas import Canvas
from common.constants import PDF_STORAGE_PATH

def generate_file(subfolder_name, file_name, data):
    """
        Generates a PDF file that represents an invoice statement.

        Arguments:
            subfolder_name (String): The name of the subfolder that the PDF should be placed in 
            file_name      (String): The name of the PDF file that gets generated
            data                   : Info that needs to be added to the PDF
    """

    # make new folder if needed
    path = f"{ os.getcwd() }/{ PDF_STORAGE_PATH }{ subfolder_name }"
    os.makedirs(path)

    # create PDF
    canvas = Canvas(f"{ PDF_STORAGE_PATH }{ subfolder_name }/{ file_name }.pdf")
    canvas.drawString(72, 72, data)
    canvas.save()