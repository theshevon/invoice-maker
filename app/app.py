'''
:name: app.py
:author: Shevon Mendis <shevonmendis@gmail.com>
:purpose: To generate invoices and email contacts based on info read from a Google Sheet.
'''

import argparse
import logging
from common.gs_constants import CLASSES_SHEET_ID, STUDENTS_SHEET_ID, LESSONS_SHEET_ID, ADJUSTMENTS_SHEET_ID, \
                                MISC_COSTS_SHEET_ID, CLASSES_PRIMARY_KEY, STUDENTS_PRIMARY_KEY, \
                                LESSONS_PRIMARY_KEY, ADJUSTMENTS_PRIMARY_KEY, MISC_COSTS_PRIMARY_KEY, \
                                GOOGLE_SHEET_ID
from classes.AdHocDB import AdHocDB
from modules.util import determine_date_bounds
from modules.invoicing import generate_invoice_data
from modules.pdf_generator import generate_files
from modules.mailer import send_emails

def init():
    '''
        Initialises the application.
        
        Returns:
            Dictionary: A map of the command line arguments and their values
    '''

    ap = argparse.ArgumentParser()
    # TODO: add debugging levels
    ap.add_argument("-d", "--debug", required=False, help="debugger on", action="store_true")
    ap.add_argument("-sd", "--start-date", required=False, help="start date")
    ap.add_argument("-ed", "--end-date", required=False, help="end date")
    ap.add_argument("-tp", "--time-period", required=False, help="time period")
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

    # set logging
    if debug:
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s: %(message)s")
    else:
        logging.basicConfig(level=logging.CRITICAL)
    logger = logging.getLogger(__name__)

    # determine mail server type
    if use_prod:
        use_prod = True if use_prod == 'p' else False
    else:
        use_prod = True

    logger.info("Beginning...")

    start_date, end_date = determine_date_bounds(logger, start_date, end_date, time_period)

    db = AdHocDB()
    db.build(logger, GOOGLE_SHEET_ID, [
        (CLASSES_SHEET_ID, CLASSES_PRIMARY_KEY),
        (STUDENTS_SHEET_ID, STUDENTS_PRIMARY_KEY),
        (LESSONS_SHEET_ID, LESSONS_PRIMARY_KEY),
        (ADJUSTMENTS_SHEET_ID, ADJUSTMENTS_PRIMARY_KEY),
        (MISC_COSTS_SHEET_ID, MISC_COSTS_PRIMARY_KEY)
    ])

    invoice_data = generate_invoice_data(logger, db, start_date, end_date)

    # stop if no records found
    if not invoice_data:
        logger.info("No records found within the time bounds. Exiting...")
        return

    # mail_data = generate_files(start_date, end_date, invoice_data, logger)
    # n_success, n_total = send_emails(mail_data, use_prod, logger)

    # logger.info(f"{ n_success }/{ n_total } emails sent out.")
    logger.info("Exiting...")

if __name__ == "__main__":
    args = init()
    execute(args)