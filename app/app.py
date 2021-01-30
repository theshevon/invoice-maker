'''
:name: app.py
:author: Shevon Mendis <shevonmendis@gmail.com>
:purpose: To generate invoices and email contacts based on info read from a Google Sheet.
'''

import argparse
import logging
from datetime import datetime
from common.gs_constants import CLASSES_SHEET_ID, STUDENTS_SHEET_ID, LESSONS_SHEET_ID, ADJUSTMENTS_SHEET_ID, \
                                MISC_COSTS_SHEET_ID, CLASSES_PRIMARY_KEY, STUDENTS_PRIMARY_KEY, \
                                LESSONS_PRIMARY_KEY, ADJUSTMENTS_PRIMARY_KEY, MISC_COSTS_PRIMARY_KEY, \
                                GOOGLE_SHEET_ID
from common.op_constants import DATE_STR_FORMAT
from modules.Storage import AdHocDB
from modules.Invoicing import Invoicer
from modules.util import determine_date_bounds, to_datetime
from modules.pdf_generator import generate_files
from modules.mailer import send_emails

def init():
    '''
        Initialises the application.
        
        Returns:
            Dictionary: A map of the command line arguments and their values
    '''

    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--debug", required=False, help="debugger on", action="store_true")
    ap.add_argument("-sd", "--start-date", required=False, help="start date (dd/mm/yy)")
    ap.add_argument("-ed", "--end-date", required=False, help="end date (dd/mm/yy)")
    ap.add_argument("-tp", "--time-period", required=False, help="time period")
    ap.add_argument("-ad", "--adjustments-date", required=False, help="date as of which adjustments are still outstanding (dd/mm/yy)")
    ap.add_argument("-ms", "--mail-server", required=False, help="mail server type (p: production; t: test)", choices=['p', 't'])

    return vars(ap.parse_args())

def execute(args):
    '''
        Executes the application.

        Arguments:
            args (Dictionary): A map of the command line arguments and their values
    '''

    # extract command line argument values
    start_date = args["start_date"]
    end_date = args["end_date"]
    time_period = args["time_period"]
    debug = args["debug"]
    use_prod = args["mail_server"]
    adjustments_date = args["adjustments_date"]

    # set logging
    if debug:
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s]: %(message)s")
    else:
        logging.basicConfig(level=logging.ERROR, format="%(asctime)s [%(levelname)s]: %(message)s")
    logger = logging.getLogger(__name__)

    # determine mail server type
    if use_prod:
        use_prod = True if use_prod == 'p' else False
    else:
        use_prod = True

    logger.info("Beginning...")

    start_date, end_date = determine_date_bounds(logger, start_date, end_date, time_period)

    curr_date = datetime.now().date()
    if end_date < curr_date and not adjustments_date:
        logger.error("The adjustments_date must be supplied when the end_date is set to a date prior to the current date")
        logger.info("Exiting...")
        return 
    elif not adjustments_date or to_datetime(adjustments_date, DATE_STR_FORMAT) > curr_date:
        logger.info(f"Resetting adjustments date from { adjustments_date } to { curr_date }")
        adjustments_date = curr_date
    else:
        adjustments_date = to_datetime(adjustments_date, DATE_STR_FORMAT)

    db = AdHocDB()
    db.build(GOOGLE_SHEET_ID, [
        (CLASSES_SHEET_ID, CLASSES_PRIMARY_KEY),
        (STUDENTS_SHEET_ID, STUDENTS_PRIMARY_KEY),
        (LESSONS_SHEET_ID, LESSONS_PRIMARY_KEY),
        (ADJUSTMENTS_SHEET_ID, ADJUSTMENTS_PRIMARY_KEY),
        (MISC_COSTS_SHEET_ID, MISC_COSTS_PRIMARY_KEY)
    ])

    invoicer = Invoicer()
    invoicer.generate_and_mail_invoices(db, start_date, end_date, adjustments_date)

    # mail_data = generate_files(start_date, end_date, invoice_data, logger)
    # n_success, n_total = send_emails(mail_data, use_prod, logger)

    # logger.info(f"{ n_success }/{ n_total } emails sent out.")
    logger.info("Exiting...")

if __name__ == "__main__":
    args = init()
    execute(args)