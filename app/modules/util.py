'''
:name: util.py
:author: Shevon Mendis <shevonmendis@gmail.com>
:purpose: To contain common helper functions that may be used by the other modules.
'''

import sys

from datetime import datetime, timedelta
from collections import defaultdict as dd
from common.defaults import DEFAULT_TIME_PERIOD, OLDEST_START_DATE
from common.date_formats import DATE_STR_FORMAT_CL, DATE_STR_FORMAT_STANDARD

def get_date(date_as_str, format):
    '''
        Converts a date from a string to a date object.

        Arguments:
            date_as_str (string): The date as a string
            format      (string): The format that the date string is in
        
        Returns:
            datetime: The date as a date object
    '''

    return datetime.strptime(date_as_str, format).date()

def get_date_string(date, format):
    '''
        Converts a date object into a string.

        Arguments:
            date    (date): The date as a date object
            format (string): The format that the date string should be in
        
        Returns:
            string: The date as a string
    '''

    return date.strftime(format)

def get_formatted_date_time(datetime_as_str, fromFormat, toFormat):
    '''
        Converts a datetime string from one format to another.

        Arguments:
            date_as_str (string): The datetime as a string
            toFormat    (string): The format that the datetime currently is in
            fromFormat  (string): The format that the datetime should be converted to

        Returns:
            string: The datetime string in the required format
    '''

    datetime = get_date(datetime_as_str, fromFormat)  
    return datetime.strftime(toFormat)

def get_duration_in_hours(duration):
    '''
        Converts a duration into hours.

        Arguments:
            duration (string): The duration as a string

        Returns:
            float: The duration in hours
    '''

    hours, mins, _ = duration.split(':')
    return round(int(hours) + int(mins) / 60, 2)

def get_formatted_duration(duration):
    '''
        Converts a duration into an xxH yyM format.

        Arguments:
            duration (string): The duration in the HH:MM:SS format

        Returns:
            string: The duration in a xxH yyM format
    '''

    hours, mins, _ = duration.split(":")
    return f"{ int(hours) }H { mins }M"


def determine_date_bounds(logger, curr_date, start_date, end_date, time_period):
    '''
        Determines the start and end dates for an invoice based on info presented through the command line
        arguments.

        Arguments:
            logger      (Logger): Logger
            curr_date     (date): The current date
            start_date  (string): Lower bound for record cut off (inclusive)
            end_date    (string): Upper bound for record cut off (exclusive)
            time_period (string): The no. of weeks that the invoices will cover

        Returns:
            start_date (date): Lower bound for record cut off
            end_date   (date): Upper bound for record cut off
    '''

    logger.info("Attempting to determine start and end dates based on supplied values: " + \
                                f"start_date: { start_date}; end_date: { end_date }; time_period: { time_period }")
    
    try:

        if not (start_date or end_date):
            end_date = curr_date
            if not time_period:
                time_period = DEFAULT_TIME_PERIOD
            start_date = end_date - timedelta(weeks=int(time_period))
        elif start_date:
            start_date = get_date(start_date, DATE_STR_FORMAT_CL)
            if time_period:
                end_date = start_date + timedelta(weeks=int(time_period))
            else:
                end_date = datetime.now().date()
        else:
            end_date = get_date(end_date, DATE_STR_FORMAT_CL)
            if time_period:
                start_date = end_date - timedelta(weeks=int(time_period))
            else:
                start_date = OLDEST_START_DATE

        new_start_date = get_date_string(start_date, DATE_STR_FORMAT_STANDARD)
        new_end_date = get_date_string(end_date, DATE_STR_FORMAT_STANDARD)
        logger.info(f"Updated dates: start_date: { new_start_date }; end_date: { new_end_date }")
    
    except:
        
        logger.error("Error while determining date bounds!", exc_info=True)
        sys.exit()
    
    return start_date, end_date

def recursive_dd():
    '''
        Returns:
            A recursive default dictionary where leaf structure is a List.
    '''
    
    return dd(lambda: dd(list))