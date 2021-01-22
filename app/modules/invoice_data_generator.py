"""
:name: invoice_data_generator.py
:author: Shevon Mendis <shevonmendis@gmail.com>
:purpose: To generate data needed to create invoices.
"""

from modules.util import to_datetime, to_hours
from datetime import datetime
from fields import *

def generate_data(sheet_records, start_date, end_date, logger):
    """
        Converts data read from a google sheet into a format that can be utilised when generating the invoices.

        Arguments:
            sheet_records  (List): A list where each item is a dictionary representing a record from the spreadsheet
            start_date (datetime): Lower bound for record cut off
            end_date   (datetime): Upper bound for record cut off
            logger       (Logger): Logger

        Returns:
            Dictionary: A dictionary containing the info needed to generate and email the invoice PDF
    """

    invoice_data = {}

    # filter records to only retain those within time bounds
    sheet_records = [record for record in sheet_records if start_date <= to_datetime(record["Date"]) <= end_date]

    for record in sheet_records:

        logger.info(f"Processing record: { record }")

        student_data = {}
        student_data["name"] = record[NAME_STUDENT]
        student_data["email"] = record[EMAIL_STUDENT]

        class_data = {}
        class_data["tutor"] = record[NAME_TUTOR]
        class_data["rate"] = record[RATE_TUTOR]
        class_data["duration"] = record[DURATION]
        class_data["cost"] = to_hours(record[DURATION])

        remarks = ""

        invoice_data.append({
            "student_data": student_data,
            "class_data": class_data,
        })

    return invoice_data
