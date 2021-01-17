"""
:name: app.py
:author: Shevon Mendis <shevonmendis@gmail.com>
:purpose: To generate invoices and email contacts based on info read from a Google Sheet.
"""

import argparse
import logging
from modules.sheet_reader import read_records
from modules.util import determine_date_bounds
from modules.invoice_data_generator import generate_data
from modules.pdf_generator import generate_files
from modules.mailer import send_emails

def init():
    """
        Initialises the application.
        
        Returns:
            Dictionary: A map of the command line arguments and their values
    """

    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--debug", required=False, help="debugger on", action="store_true")
    ap.add_argument("-sd", "--start-date", required=False, help="start date")
    ap.add_argument("-ed", "--end-date", required=False, help="end date")
    ap.add_argument("-tp", "--time-period", required=False, help="time period")
    ap.add_argument("-ms", "--mail-server", required=False, help="mail server type (p: production; t: test)", choices=['p', 't'])

    return vars(ap.parse_args())

def execute(args):
    """
        Executes the application.

        Arguments:
            args (Dictionary): A map of the command line arguments and their values
    """

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
    sheet_records = read_records(logger)
    start_date, end_date = determine_date_bounds(start_date, end_date, time_period, logger)
    invoice_data = generate_data(sheet_records, start_date, end_date, logger)

    # stop if no records found
    if not invoice_data:
        logger.info("No records found within the time bounds. Exiting...")
        return

    mail_data = generate_files(start_date, end_date, invoice_data, logger)
    n_success, n_total = send_emails(mail_data, use_prod, logger)

    logger.info(f"{ n_success }/{ n_total } emails sent out.")
    logger.info("Exiting...")

if __name__ == "__main__":
    args = init()
    execute(args)