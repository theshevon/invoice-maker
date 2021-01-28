'''
:name: util.py
:author: Shevon Mendis <shevonmendis@gmail.com>
:purpose: To contain common helper functions that may be used by the other modules.
'''

from datetime import datetime, timedelta
from collections import defaultdict as dd
from common.defaults import DEFAULT_TIME_PERIOD, OLDEST_START_DATE
from common.op_constants import DATE_TIME_STR_FORMAT, DATE_STR_FORMAT

def to_datetime(date_as_str, format=DATE_TIME_STR_FORMAT):
    '''
        Converts a date from a string to a datetime object.

        Arguments:
            date_as_str (string): The date as a string
        
        Returns:
            datetime: The date as a datetime object
    '''

    return datetime.strptime(date_as_str, format).date()


def to_date_string(date):
    '''
        Converts a date object into a string.

        Arguments:
            date (datetime): The data as a date object
        
        Returns:
            string: The date as a string
    '''

    return date.strftime(DATE_STR_FORMAT)

def get_duration_in_hours(duration):
    '''
        Converts a duration into hours.

        Arguments:
            duration (String): The duration as a string

        Returns:
            float: The duration as a float
    '''

    hours, mins, _ = duration.split(':')
    
    return round(int(hours) + int(mins) / 60, 2)


def determine_date_bounds(logger, start_date, end_date, time_period):
    '''
        Determines the start and end dates for an invoice based on info presented through the command line
        arguments.

        Arguments:
            logger      (Logger): Logger
            start_date  (string): Lower bound for record cut off
            end_date    (string): Upper bound for record cut off
            time_period (string): Info that needs to be added to the PDF

        Returns:
            start_date     (datetime): Lower bound for record cut off
            end_date       (datetime): Upper bound for record cut off
    '''

    logger.info("Attempting to determine start and end dates based on supplied values: " + \
                                f"start_date: { start_date}; end_date: { end_date }; time_period: { time_period }")
    
    try:
        if not (start_date or end_date):
            end_date = datetime.now().date()
            if not time_period:
                time_period = DEFAULT_TIME_PERIOD
            start_date = end_date - timedelta(weeks=int(time_period))
        elif start_date:
            start_date = to_datetime(start_date, DATE_STR_FORMAT)
            if time_period:
                end_date = start_date + timedelta(weeks=int(time_period))
            else:
                end_date = datetime.now().date()
        else:
            end_date = to_datetime(end_date, DATE_STR_FORMAT)
            if time_period:
                start_date = end_date - timedelta(weeks=int(time_period))
            else:
                start_date = OLDEST_START_DATE

        logger.info(f"Dates updated: start_date: { to_date_string(start_date) }; end_date: { to_date_string(end_date) }")
    except:
        logger.error("Error while detemining date bounds!", exc_info=True)
    
    return start_date, end_date


def generate_invoice_data(db, start_date, end_date, logger):
    '''
        Converts data read from a google sheet into a format that can be utilised when generating the invoices.

        Arguments:
            db          (AdHocDB): DB of records
            start_date (datetime): Lower bound for record cut off
            end_date   (datetime): Upper bound for record cut off
            logger       (Logger): Logger

        Returns:
            Dictionary: A dictionary containing the info needed to generate and email the invoice PDF
    '''

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

def recursive_dd():
    return dd(lambda: dd(list))