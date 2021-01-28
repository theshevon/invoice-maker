'''
:name: invoicing.py
:author: Shevon Mendis <shevonmendis@gmail.com>
:purpose: To generate data needed to create invoices.
'''

from modules.util import to_datetime, get_duration_in_hours, recursive_dd
from datetime import datetime

from common.gs_constants import *
from common.op_constants import LESSONS, ADJUSTMENTS, DATE_STR_FORMAT

def generate_invoice_data(logger, db, start_date, end_date, adjustments_date):
    '''
        Converts data read from a google sheet into a format that can be utilised when generating the invoices.

        Arguments:
            logger         (Logger): Logger
            db            (AdHocDB): Database
            start_date       (date): Lower bound (inclusive) for record cut off
            end_date         (date): Upper bound (inclusive) for record cut off
            adjustments_date (date): Date as of which adjustments are outstanding 

        Returns:
            Dictionary: A dictionary containing the info needed to generate and email the invoice PDF
    '''

    invoice_data = recursive_dd()

    # filter records to fit time constraints
    class_records = get_filtered_class_records(logger, db, start_date, end_date)

    # get lesson costs
    for class_record in class_records:

        tutor = class_record[CLASSES_TUTOR]
        subject = class_record[CLASSES_SUBJECT]
        date = class_record[CLASSES_DATE]
        duration = class_record[CLASSES_DURATION]
        duration_in_hours = get_duration_in_hours(duration)
        students = [student.strip() for student in class_record[CLASSES_STUDENTS].split(",")]
        n_students = len(students)

        if n_students == 1:
            rate_per_hour = db.queryTable(LESSONS_SHEET_ID, (tutor, students[0], subject))[LESSONS_HOURLY_RATE]
        else:
            cost_category = MISC_COSTS_CATEGORY__GRP_PREFIX + min(MISC_COSTS_CATEGORY__GRP_MAX_N, n_students)
            rate_per_hour = db.queryTable(MISC_COSTS_SHEET_ID, (MISC_COSTS_CATEGORY,))[MISC_COSTS_COST]
        
        cost = duration_in_hours * rate_per_hour

        for student in students:
            invoice_data[student][LESSONS].append({
                "tutor": tutor,
                "date": date,
                "duration": duration,
                "cost": cost
            })

    # get adjustments costs
    all_adjustments = db.getTable(ADJUSTMENTS_SHEET_ID).items()
    adjustments_records = [record for (key, record) in all_adjustments if to_datetime(record[ADJUSTMENTS_INVOICE_DATE].strip(), DATE_STR_FORMAT) == adjustments_date]

    for adjustments_record in adjustments_records:

        owed_party = adjustments_record[ADJUSTMENTS_OWED_PARTY]
        student = adjustments_record[ADJUSTMENTS_STUDENT]
        amount = adjustments_record[ADJUSTMENTS_AMOUNT]
        reason = adjustments_record[ADJUSTMENTS_REASON]
        
        invoice_data[student][ADJUSTMENTS].append({
            "owed_party": owed_party,
            "amount": amount,
            "reason": reason
        })

    
    return invoice_data
    
    

def get_filtered_class_records(logger, db, start_date, end_date):

    all_class_records = db.getTable(CLASSES_SHEET_ID).items()
    return [record for (key, record) in all_class_records if start_date <= to_datetime(record[CLASSES_DATE]) <= end_date]