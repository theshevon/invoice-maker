from datetime import datetime

# file path to google dev credentials
CREDENTIALS_FILE_PATH = "credentials.json"

# ID of google sheet being accessed
GOOGLE_SHEET_ID = "1MJBI2ibiTooLI851VrwnY6S-oNxedgJDiq8ivhAFx5w"

# date string format in google sheet
DATE_STR_FORMAT_1 = "%d-%m-%y"

# date string format for folder names
DATE_STR_FORMAT_2 = "%d %b %Y"

# oldest possible start date
OLDEST_START_DATE = datetime.strptime("11-04-98", DATE_STR_FORMAT_1)

# default time period to generate invoices over (in weeks)
DEFAULT_TIME_PERIOD = 2

# path to folder that will store the generated PDFs
PDF_STORAGE_PATH = "../invoices/"