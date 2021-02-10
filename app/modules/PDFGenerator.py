'''
:name: PDFGenerator.py
:author: Shevon Mendis <shevonmendis@gmail.com>
:purpose: To dynamically generate a PDF. 
'''

import os
import logging
import asyncio
import pathlib

from pyppeteer import launch
from common.inv_constants import *
from common.date_formats import DATE_TIME_STR_FORMAT_STANDARD, DATE_TIME_STR_FORMAT_SPECIAL
from common.gs_constants import ADJUSTMENT_TYPE__DEB
from common.defaults import PDF_STORAGE_PATH
from modules.util import get_date, get_formatted_date_time, get_formatted_duration

PATH_TO_LOGO = "../assets/pdf/"

class PDFGenerator:

    def __init__(self, subfolder_name):
        
        self.logger = logging.getLogger(__name__)

        with open("./assets/pdf/pdf_template.html") as f:
            self.__PDF_TEMPLATE = f.read()

        with open("./assets/pdf/billing_row_template.html") as f:
            self.__BILLING_ROW_TEMPLATE = f.read()

        with open("./assets/pdf/adjustment_template.html") as f:
            self.__ADJUSTMENT_TEMPLATE = f.read()

        # make new folder if needed
        try:
            self.path_to_subfolder = f"{ os.getcwd() }/{ PDF_STORAGE_PATH }{ subfolder_name }"
            os.makedirs(self.path_to_subfolder)
            self.logger.info(f"Created a new directory at: { self.path_to_subfolder }")
        except FileExistsError:
            self.logger.info(f"Directory already exists at: { self.path_to_subfolder }")

    def build(self, curr_date, invoice_no, student, invoice_info):
        '''
            Builds a pdf.

            Arguments:
                curr_date          (date): The current date
                invoice_no          (int): The invoice no. for the PDF that gets generated
                student          (string): The name of the student who the invoice is for
                invoice_info (Dictionary): A dictionary containing all the info needed for the PDF generation
            
            Returns:
                string: Path to the PDF that was generated.
        '''

        # fill up billing row info
        billing_rows = ""
        subtotal = 0
        for lesson in invoice_info[INV_LESSONS]:
            tutor = lesson[INV_TUTOR]
            subject = lesson[INV_SUBJECT]
            date = get_formatted_date_time(lesson[INV_DATE], DATE_TIME_STR_FORMAT_STANDARD, DATE_TIME_STR_FORMAT_SPECIAL)
            duration = get_formatted_duration(lesson[INV_DURATION])
            cost = lesson[INV_COST]
            billing_rows += self.__BILLING_ROW_TEMPLATE.format(subject, tutor, date, duration, cost) + "\n"
            subtotal += cost

        # fill up notes
        notes = ""
        adjustments_total = 0
        for adjustment in invoice_info[INV_ADJUSTMENTS]:
            cost = adjustment[INV_COST]
            reason = adjustment[INV_REASON]
            notes += self.__ADJUSTMENT_TEMPLATE.format(reason) + "\n"

            if adjustment[INV_TYPE] == ADJUSTMENT_TYPE__DEB:
                adjustments_total += cost
            else:
                adjustments_total -= cost

        total = subtotal + adjustments_total

        adjustments_total = self.__get_formatted_cost(adjustments_total)
        total = self.__get_formatted_cost(total)

        # fill up invoice
        invoice_no = f"{invoice_no:06}"
        adjustments_total
        invoice = self.__PDF_TEMPLATE.format(PATH_TO_LOGO, invoice_no, curr_date, curr_date, student, billing_rows, subtotal, adjustments_total, total, notes, True)
        
        # make temp invoice as html
        with open(INVOICE_AS_HTML, "w") as f:
            f.write(invoice)

        path_to_pdf = f"{ self.path_to_subfolder }/#{ invoice_no }.pdf"
        asyncio.get_event_loop().run_until_complete(self.__makePdf(path_to_pdf))
        
        # remove temp file
        os.remove(INVOICE_AS_HTML)

        return path_to_pdf
    
    def __get_formatted_cost(self, cost):
        '''
            Arguments:
                cost (float): 
            
            Returns:
                The formatted cost (+/- sign & currency symbol)
        '''

        if (cost >= 0):
            return "${:.2f}".format(cost)
        else:
            return "-${:.2f}".format(abs(cost))

    async def __makePdf(self, path_to_pdf):
        '''
            Generates a PDF at a specified location.

            Arguments:
                path_to_pdf (string): Path to the PDF that should be generates.
        '''

        browser = await launch()
        page = await browser.newPage()
        await page.goto(f"file://{ pathlib.Path().absolute() }/{ INVOICE_AS_HTML }")
        await page.pdf(options={"format": "A4", "printBackground": True, "path": path_to_pdf })
        await browser.close()