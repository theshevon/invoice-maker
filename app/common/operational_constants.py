from datetime import datetime

# file path to google dev credentials
CREDENTIALS_FILE_PATH = "credentials.json"

# date string format in google sheet
DATE_STR_FORMAT_1 = "%d/%m/%Y %H:%M:%S"

# date string format for folder names
DATE_STR_FORMAT_2 = "%d %b %Y"

# oldest possible start date
OLDEST_START_DATE = datetime.strptime("11/04/1998 12:00:00", DATE_STR_FORMAT_1)

# default time period to generate invoices over (in weeks)
DEFAULT_TIME_PERIOD = 2

# path to folder that will store the generated PDFs
PDF_STORAGE_PATH = "../invoices/"