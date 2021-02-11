'''
:name: defaults.py
:author: Shevon Mendis <shevonmendis@gmail.com>
:purpose: To store all the (configurable) defaults for the main script.
'''

from datetime import datetime
from common.date_formats import DATE_STR_FORMAT_STANDARD

# oldest possible start date
OLDEST_START_DATE = datetime.strptime("11/04/1998", DATE_STR_FORMAT_STANDARD).date()

# default time period to generate invoices over (in weeks)
DEFAULT_TIME_PERIOD = 2

# path to folder that will store the generated PDFs
PDF_STORAGE_PATH = "../invoices/"

# Name of the invoice PDF as it appears on the email
INVOICE_PDF_NAME_ON_EMAIL = "Invoice.pdf"

# file path to google dev credentials
CREDENTIALS_FILE_PATH = "credentials.json"