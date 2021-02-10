'''
:name: date_formats.py
:author: Shevon Mendis <shevonmendis@gmail.com>
:purpose: To store all the date formats that get used for invoice generation
'''

# standard date time string format (eg. "25/12/2020 13:00:00")
DATE_TIME_STR_FORMAT_STANDARD = "%d/%m/%Y %H:%M:%S"

# standard date string format (eg. "25/12/2020")
DATE_STR_FORMAT_STANDARD = "%d/%m/%Y"

# command line date string format (eg. "25/12/20")
DATE_STR_FORMAT_CL = "%d/%m/%Y"

# special date string format (eg. "12 Jan 2021")
DATE_STR_FORMAT_SPECIAL = "%d %b %Y"

# specialdate time string format (eg. "12:00pm on 12 Jan 2021")
DATE_TIME_STR_FORMAT_SPECIAL = "%I:%M%p on %d %b %Y"