'''
:name: invoicing.py
:author: Shevon Mendis <shevonmendis@gmail.com>
:purpose: To generate data needed to create invoices.
'''

from modules.util import to_datetime, get_duration_in_hours
from datetime import datetime
from collections import defaultdict as dd

from common.gs_constants import *

def generate_invoice_data(logger, db, start_date, end_date):
    '''
        Converts data read from a google sheet into a format that can be utilised when generating the invoices.

        Arguments:
            logger       (Logger): Logger
            db          (AdHocDB): db
            start_date (datetime): Lower bound for record cut off
            end_date   (datetime): Upper bound for record cut off

        Returns:
            Dictionary: A dictionary containing the info needed to generate and email the invoice PDF
    '''

    invoice_data = dd(list)

    class_records = get_filtered_class_records(logger, db, start_date, end_date)

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
            invoice_data[student].append({
                "tutor": tutor,
                "date": date,
                "duration": duration,
                "cost": cost
            })

    # TODO: add adjustments
    

def get_filtered_class_records(logger, db, start_date, end_date):

    all_class_records = db.getTable(CLASSES_SHEET_ID).items()
    return [record for (key, record) in all_class_records if start_date <= to_datetime(record[CLASSES_DATE]) <= end_date]