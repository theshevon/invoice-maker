'''
:name: app.py
:author: Shevon Mendis <shevonmendis@gmail.com>
:purpose: To generate invoices and email contacts based on info read from a Google Sheet.
'''

import argparse
import logging

from datetime import datetime
from common.gs_constants import GOOGLE_SHEET_ID, LESSON_SHEET_ID, LESSON_SHEET_PRIMARY_KEY, STUDENT_SHEET_ID, \
                                STUDENT_SHEET_PRIMARY_KEY, INDV_RATE_SHEET_ID, INDV_RATE_SHEET_PRIMARY_KEY, \
                                GRP_RATE_SHEET_ID, GRP_RATE_SHEET_PRIMARY_KEY, ADJUSTMENT_SHEET_ID, \
                                ADJUSTMENT_SHEET_PRIMARY_KEY, MISC_SHEET_ID, MISC_SHEET_PRIMARY_KEY
from common.date_formats import DATE_STR_FORMAT_STANDARD
from modules.Invoicing import Invoicer
from modules.Storage import AdHocDB
from modules.util import determine_date_bounds, get_date, log

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
    ap.add_argument("-fo", "--files-only", required=False, help="only generate files (no emailing)", action="store_true")

    return vars(ap.parse_args())

def execute(args):
    '''
        Executes the application.

        Arguments:
            args (Dictionary): A map of the command line arguments and their values
    '''

    print("Hello ツ\n") 

    # extract command line argument values
    start_date = args["start_date"]
    end_date = args["end_date"]
    time_period = args["time_period"]
    debug = args["debug"]
    use_prod = args["mail_server"]
    adjustments_date = args["adjustments_date"]
    files_only = args["files_only"]

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

    # get starting invoice #
    while True:
        try:
            invoice_no = input("Please enter the starting Invoice #: ")
            invoice_no = int(invoice_no)
            if invoice_no >= 0: 
                print()
                break
            else:
                print("The Invoice # must be an *integer* >= 0!")
        except:
            print("The Invoice # must be an integer >= 0!")
            continue
    
    log("Beginning...")

    curr_date = datetime.now().date()
    start_date, end_date = determine_date_bounds(logger, curr_date, start_date, end_date, time_period)

    if end_date < curr_date and not adjustments_date:
        logger.error("The adjustments_date must be supplied when the end_date is set to a date prior to the current date")
        log("Exiting...")
        return 
    elif not adjustments_date or get_date(adjustments_date, DATE_STR_FORMAT_STANDARD) > curr_date:
        log(f"Resetting adjustments date from { adjustments_date } to { curr_date }")
        adjustments_date = curr_date
    else:
        adjustments_date = get_date(adjustments_date, DATE_STR_FORMAT_STANDARD)

    db = AdHocDB()
    db.build(GOOGLE_SHEET_ID, [
        (LESSON_SHEET_ID, LESSON_SHEET_PRIMARY_KEY),
        (STUDENT_SHEET_ID, STUDENT_SHEET_PRIMARY_KEY),
        (INDV_RATE_SHEET_ID, INDV_RATE_SHEET_PRIMARY_KEY),
        (GRP_RATE_SHEET_ID, GRP_RATE_SHEET_PRIMARY_KEY),
        (ADJUSTMENT_SHEET_ID, ADJUSTMENT_SHEET_PRIMARY_KEY),
        (MISC_SHEET_ID, MISC_SHEET_PRIMARY_KEY)
    ])

    invoicer = Invoicer()
    n_success, n_total = invoicer.generate_and_email_invoices(db, invoice_no, curr_date, start_date, end_date, \
                                                                adjustments_date, files_only, use_prod)

    log(f"{ n_success }/{ n_total } emails sent out.")
    log("Exiting...")

    print("\nBye! (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧")

if __name__ == "__main__":
    args = init()
    execute(args)