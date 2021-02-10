'''
:name: invoicing.py
:author: Shevon Mendis <shevonmendis@gmail.com>
:purpose: To generate data needed to create invoices.
'''

import os
from modules.util import to_datetime, get_duration_in_hours, recursive_dd, to_date_string, get_formatted_date_time
from datetime import datetime
import logging
from common.gs_constants import *
from common.op_constants import LESSONS, ADJUSTMENTS, DATE_STR_FORMAT, MAX_STUDENTS, DATE_STR_FORMAT_FOLDER
from common.defaults import PDF_STORAGE_PATH
from modules.PDFGenerator import PDFGenerator

SUBFOLDER_NAME_FORMAT = "{} to {}"
LATE_CANCELLATION_MSG = "Late Cancellation ({} with {} on {}): +${:.2f}"
DEBIT_AMT = ": +${:.2f}"
CREDIT_AMT = ": -${:.2f}"

class Invoicer:

    def __init__(self):

        self.logger = logging.getLogger(__name__)

    def generate_and_mail_invoices(self, db, invoice_no, start_date, end_date, adjustments_date, files_only):
        '''
        '''
        
        invoice_data = self.generate_invoice_data(db, start_date, end_date, adjustments_date)

        if not invoice_data:
            self.logger.info("No records found within the time bounds. Exiting...")

        subfolder_name = SUBFOLDER_NAME_FORMAT.format(to_date_string(start_date, "%d %b %Y"), to_date_string(end_date, "%d %b %Y"))
        pdf_generator = PDFGenerator(subfolder_name)
        for student, data in invoice_data.items():
            path_to_pdf = pdf_generator.build(invoice_no, student, data)
            if not files_only:
                self.__mail_invoices(db, invoice_data)
            invoice_no += 1

        if files_only:
            return

        

    
    def generate_invoice_data(self, db, start_date, end_date, adjustments_date):
        '''
            Converts data read from a google sheet into a format that can be utilised when generating the invoices.

            Arguments:
                db            (AdHocDB): Database
                start_date       (date): Lower bound (inclusive) for record cut off
                end_date         (date): Upper bound (inclusive) for record cut off
                adjustments_date (date): Date as of which adjustments are outstanding 

            Returns:
                Dictionary: A dictionary containing the info needed to generate and email the invoice PDF
        '''

        invoice_data = recursive_dd()

        # filter records to fit time constraints
        lesson_records = self.__get_filtered_lesson_records(db, start_date, end_date)

        # get lesson costs
        for lesson_record in lesson_records:

            tutor = lesson_record[LESSON_TUTOR]
            subject = lesson_record[LESSON_SUBJECT]
            date = lesson_record[LESSON_DATE]
            duration = lesson_record[LESSON_DURATION]

            students_present = self.__get_students(lesson_record[LESSON_STUDENTS_PRESENT])
            students_absent = self.__get_students(lesson_record[LESSON_STUDENTS_ABSENT])
            n_students = (len(students_present) + len(students_absent)) 
            n_students = MAX_STUDENTS if n_students >= MAX_STUDENTS else n_students

            if n_students == 1:
                if len(students_present):
                    student = students_present[0]
                    rate_per_hour = db.queryTable(INDV_RATE_SHEET_ID, (tutor, subject, student), INDV_RATE_HOURLY_RATE)
                    self.__add_student_lesson(invoice_data, student, tutor, subject, date, duration, rate_per_hour)
                else:
                    student = students_absent[0]
                    self.__add_student_adjustment(db, invoice_data, student, tutor, subject, date)
            else:
                for student in students_present:
                    rate_per_hour = db.queryTable(GRP_RATE_SHEET_ID, (tutor, subject, n_students), GRP_RATE_HOURLY_RATE)
                    self.__add_student_lesson(invoice_data, student, tutor, subject, date, duration, rate_per_hour)
                for student in students_absent:
                    self.__add_student_adjustment(db, invoice_data, student, tutor, subject, date)

        # get adjustments costs
        all_adjustments = db.getTable(ADJUSTMENT_SHEET_ID).items()
        adjustments_records = [record for (key, record) in all_adjustments if to_datetime(record[ADJUSTMENT_INVOICE_DATE].strip(), DATE_STR_FORMAT) == adjustments_date]

        for adjustments_record in adjustments_records:

            type_ = adjustments_record[ADJUSTMENT_TYPE]
            student = adjustments_record[ADJUSTMENT_STUDENT]
            amount = adjustments_record[ADJUSTMENT_AMOUNT]
            reason = adjustments_record[ADJUSTMENT_REASON]
            if type_ == ADJUSTMENT_TYPE__DEB:
                reason += DEBIT_AMT.format(amount)
            else:
                reason += CREDIT_AMT.format(amount)
            
            invoice_data[student][ADJUSTMENTS].append({
                "type": type_,
                "amount": amount,
                "reason": reason
            })

        return invoice_data    

    def __get_filtered_lesson_records(self, db, start_date, end_date):

        all_lesson_records = db.getTable(LESSON_SHEET_ID).items()
        return [record for (key, record) in all_lesson_records if start_date <= to_datetime(record[LESSON_DATE]) <= end_date]

    def __get_students(self, students_as_str):

        students_as_str = students_as_str.strip()
        if students_as_str:
            return [student.strip() for student in students_as_str.split(",")]
        return []

    def __add_student_lesson(self, invoice_data, student, tutor, subject, date, duration, rate):
        cost = rate * get_duration_in_hours(duration)
        invoice_data[student][LESSONS].append({
            "tutor": tutor,
            "subject": subject,
            "date": date,
            "duration": duration,
            "cost": cost
        })

    def __add_student_adjustment(self, db, invoice_data, student, tutor, subject, date):
        amount = db.queryTable(MISC_SHEET_ID, (MISC_KEY__LATE, ), MISC_VALUE)
        date = get_formatted_date_time(date, DATE_STR_FORMAT_FOLDER)
        invoice_data[student][ADJUSTMENTS].append({
            "type": ADJUSTMENT_TYPE__DEB,
            "amount": amount,
            "reason": LATE_CANCELLATION_MSG.format(subject, tutor, date, amount)
        })

    def __mail_invoices(self, db, invoice_data):
        pass

    def __mail_invoice(self):
        pass