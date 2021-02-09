import os
import logging
import asyncio
from pyppeteer import launch
from datetime import datetime
from common.gs_constants import *
from common.defaults import PDF_STORAGE_PATH
from common.op_constants import INVOICE_AS_HTML, LESSONS, ADJUSTMENTS
from modules.util import to_datetime, get_formatted_date_time, get_formatted_duration, to_date_string

class PDFGenerator:

    def __init__(self, subfolder_name):
        
        self.logger = logging.getLogger(__name__)

        with open("./assets/pdf/pdf_template.html") as f:
            self.__PDF_TEMPLATE = f.read()

        with open("./assets/pdf/billing_row_template.html") as f:
            self.__BILLING_ROWTEMPLATE = f.read()

        with open("./assets/pdf/note_template.html") as f:
            self.__NOTE_TEMPLATE = f.read()

        # make new folder if needed
        try:
            self.path_to_subfolder = f"{ os.getcwd() }/{ PDF_STORAGE_PATH }{ subfolder_name }"
            os.makedirs(self.path_to_subfolder)
            self.logger.info(f"Created a new directory at: { self.path_to_subfolder }")
        except FileExistsError:
            self.logger.info(f"Directory already exists at: { self.path_to_subfolder }")

    def build(self, invoice_no, student, invoice_info):
        '''
            Builds a pdf

            Arguments:
                invoice_info (Dictionary):
            
            Returns:
                String: Path to the pdf that was generated.
        '''

        # fill up billing row info
        billing_rows = ""
        subtotal = 0
        for lesson in invoice_info[LESSONS]:
            tutor = lesson["tutor"]
            subject = lesson["subject"]
            date = get_formatted_date_time(lesson["date"])
            duration = get_formatted_duration(lesson["duration"])
            cost = lesson["cost"]
            billing_rows += self.__BILLING_ROWTEMPLATE.format(subject, tutor, date, duration, cost) + "\n"
            subtotal += cost

        # fill up notes
        notes = ""
        adjustments_total = 0
        for adjustment in invoice_info[ADJUSTMENTS]:
            amount = adjustment["amount"]
            reason = adjustment["reason"]
            notes += self.__NOTE_TEMPLATE.format(reason) + "\n"

            if adjustment["type"] == ADJUSTMENT_TYPE__DEB:
                adjustments_total += amount
            else:
                adjustments_total -= amount

        total = subtotal + adjustments_total

        adjustments_total = self.__get_formatted_cost(adjustments_total)
        total = self.__get_formatted_cost(total)

        # fill up invoice
        invoice_no = f"{invoice_no:06}"
        curr_date = to_date_string(datetime.now().date(), "%d %b %Y")
        adjustments_total
        invoice = self.__PDF_TEMPLATE.format("../assets/pdf/", invoice_no, curr_date, curr_date, student, billing_rows, subtotal, adjustments_total, total, notes, True)
        
        # make temp invoice as html
        with open(INVOICE_AS_HTML, "w") as f:
            f.write(invoice)

        path_to_pdf = f"{ self.path_to_subfolder }/#{ invoice_no }.pdf"
        asyncio.get_event_loop().run_until_complete(self.__makePdf(path_to_pdf))
        
        # remove temp file
        os.remove(INVOICE_AS_HTML)

        return path_to_pdf
    
    def __get_formatted_cost(self, cost):

        if (cost >= 0):
            return "${:.2f}".format(cost)
        else:
            return "-${:.2f}".format(abs(cost))

    async def __makePdf(self, path_to_pdf):
        browser = await launch()
        page = await browser.newPage()
        await page.goto("file:///Users/mendis/Desktop/Mendis/Projects/invoice-maker/app/modules/invoice.html")
        await page.pdf(options={"format": "A4", "printBackground": True, "path": path_to_pdf })
        await browser.close()