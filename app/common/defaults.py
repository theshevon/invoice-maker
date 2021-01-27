from datetime import datetime
from common.op_constants import DATE_TIME_STR_FORMAT

# oldest possible start date
OLDEST_START_DATE = datetime.strptime("11/04/1998 00:00:00", DATE_TIME_STR_FORMAT)

# default time period to generate invoices over (in weeks)
DEFAULT_TIME_PERIOD = 2

# path to folder that will store the generated PDFs
PDF_STORAGE_PATH = "../invoices/"