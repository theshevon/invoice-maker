"""
:name: constants.py
:author: Shevon Mendis <shevonmendis@gmail.com>
:purpose: Collection of operational constants.
"""

from datetime import datetime

# File path to google dev credentials
CREDENTIALS_FILE_PATH = "credentials.json"

# ID of google sheet being accessed
GOOGLE_SHEET_ID = "1VS1B329z-Dzw-G_3zzxrSfFSwg0H_Zzm0aqB0PqrvbY"

# Date string format in google sheet
DATE_STR_FORMAT_1 = "%d/%m/%Y %H:%M:%S"

# Date string format for folder names
DATE_STR_FORMAT_2 = "%d %b %Y"

# Oldest possible start date
OLDEST_START_DATE = datetime.strptime("11-04-98 00:00:00", DATE_STR_FORMAT_1)

# Default time period to generate invoices over (in weeks)
DEFAULT_TIME_PERIOD = 2

# Path to folder that will store the generated PDFs
PDF_STORAGE_PATH = "../invoices/"

INVOICE_FILE_NAME_FORMAT = "{:06d}"