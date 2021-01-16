"""
:name: util.py
:author: Shevon Mendis <shevonmendis@gmail.com>
:purpose: To contain common helper functions that may be used by the other modules.
"""

from datetime import datetime, timedelta
from common.constants import DEFAULT_TIME_PERIOD, OLDEST_START_DATE, DATE_STR_FORMAT_1, DATE_STR_FORMAT_2

def to_datetime(date_as_str):
    """
        Converts a date from a string to a datetime object.

        Arguments:
            date_as_str (string): The date as a string
        
        Returns:
            datetime: The date as a datetime object
    """

    return datetime.strptime(date_as_str, DATE_STR_FORMAT_1)

def to_date_string(date):
    """
        Converts a date object into a string.

        Arguments:
            date (datetime): The data as a date object
        
        Returns:
            string: The date as a string
    """

    return date.strftime(DATE_STR_FORMAT_2)

def determine_date_bounds(start_date, end_date, time_period, logger):
    """
        Determines the start and end dates for an invoice based on info presented through the command line
        arguments.

        Arguments:
            start_date  (string): Lower bound for record cut off
            end_date    (string): Upper bound for record cut off
            time_period (string): Info that needs to be added to the PDF
            logger      (Logger): Logger

        Returns:
            start_date     (datetime): Lower bound for record cut off
            end_date       (datetime): Upper bound for record cut off
    """

    logger.info("Attempting to determine start and end dates based on supplied values: " + \
                                f"start_date: { start_date}; end_date: { end_date }; time_period: { time_period }")
    
    try:
        if not (start_date or end_date):
            end_date = datetime.now()
            if not time_period:
                time_period = DEFAULT_TIME_PERIOD
            start_date = end_date - timedelta(weeks=int(time_period))
        elif start_date:
            start_date = to_datetime(start_date)
            if time_period:
                end_date = start_date + timedelta(weeks=int(time_period))
            else:
                end_date = datetime.now()
        else:
            end_date = to_datetime(end_date)
            if time_period:
                start_date = end_date - timedelta(weeks=int(time_period))
            else:
                start_date = OLDEST_START_DATE

        logger.info(f"Dates updated: start_date: { to_date_string(start_date) }; end_date: { to_date_string(end_date) }")
    except:
        logger.error("Error while detemining date bounds!", exc_info=True)
    
    return start_date, end_date