"""
:name: invoice_data_generator.py
:author: Shevon Mendis <shevonmendis@gmail.com>
:purpose: To generate data needed to create invoices.
"""

from modules.util import to_datetime
from datetime import datetime

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

    invoice_data = []

    # filter records to only retain those within time bounds
    sheet_records = [record for record in sheet_records if start_date <= to_datetime(record["Date"]) <= end_date]

    for record in sheet_records:

        # only look at approved entries
        if (record["Approved"].lower() != "true"):
            logger.info(f"Skipping unapproved record: { record }")
            continue

        logger.info(f"Processing record: { record }")

        client_data = {}
        client_data["name"] = record["First Name"] + " " + record["Last Name"]
        client_data["email"] = record["Email"]

        services_data = []
        remarks = ""

        invoice_data.append({
            "client_data": client_data,
            "services_data": services_data,
            "remarks": remarks
        })

    return invoice_data
