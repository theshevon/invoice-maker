'''
:name: util.py
:author: Shevon Mendis <shevonmendis@gmail.com>
:purpose: To contain common helper functions that may be used by the other modules.
'''

from datetime import datetime, timedelta
from collections import defaultdict as dd
from common.defaults import DEFAULT_TIME_PERIOD, OLDEST_START_DATE
from common.op_constants import DATE_TIME_STR_FORMAT, DATE_STR_FORMAT, DATE_TIME_STR_FORMAT_INVOICE

def to_datetime(date_as_str, format=DATE_TIME_STR_FORMAT):
    '''
        Converts a date from a string to a datetime object.

        Arguments:
            date_as_str (string): The date as a string
        
        Returns:
            datetime: The date as a datetime object
    '''

    return datetime.strptime(date_as_str, format).date()

def to_date_string(date, format=DATE_STR_FORMAT):
    '''
        Converts a date object into a string.

        Arguments:
            date (datetime): The date as a date object
        
        Returns:
            string: The date as a string
    '''

    return date.strftime(format)

def get_formatted_date_time(datetime_as_str, format=DATE_TIME_STR_FORMAT_INVOICE):
    '''
    '''

    datetime = to_datetime(datetime_as_str)
    
    return datetime.strftime(format)

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

def get_formatted_duration(duration):
    '''
    '''

    hours, mins, _ = duration.split(":")
    return f"{ int(hours) }H { mins }M"


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

def recursive_dd():
    return dd(lambda: dd(list))