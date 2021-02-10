'''
:name: Invoicing.py
:author: Shevon Mendis <shevonmendis@gmail.com>
:purpose: To generate invoice PDFs and email them.
'''

import os
import logging

from common.inv_constants import *
from common.gs_constants import *
from common.date_formats import DATE_STR_FORMAT_STANDARD, DATE_STR_FORMAT_SPECIAL, DATE_TIME_STR_FORMAT_STANDARD, \
                                DATE_TIME_STR_FORMAT_SPECIAL
from common.defaults import PDF_STORAGE_PATH
from modules.PDFGenerator import PDFGenerator
from modules.util import recursive_dd, get_date, get_duration_in_hours, get_date_string, get_formatted_date_time

SUBFOLDER_NAME_FORMAT = "{} to {}"

LATE_CANCELLATION_MSG = "Late Cancellation ({} with {} on {}): +${:.2f}"

DEBIT_AMT = ": +${:.2f}"

CREDIT_AMT = ": -${:.2f}"

MAX_STUDENTS = 4

class Invoicer:
    '''
        Represents a class responsible for generating invoice PDFs and emailing them.
    '''

    def __init__(self):

        self.logger = logging.getLogger(__name__)

    def generate_and_email_invoices(self, db, invoice_no, curr_date, start_date, end_date, adjustments_date, files_only):
        '''
            Generates invoices and emails them to students.

            Arguments:
                db            (AdHocDB): Database
                invoice_no        (int): Invoice no. of the first invoice that gets created (for this run of the script)
                curr_date        (date): The current date
                start_date       (date): Lower bound (inclusive) for record cut off
                end_date         (date): Upper bound (inclusive) for record cut off
                adjustments_date (date): Date as of which adjustments are outstanding 
                files_only       (bool): True if emailing should be skipped; False o/w
        '''
        
        invoice_data = self.__generate_invoice_data(db, start_date, end_date, adjustments_date)

        if not invoice_data:
            self.logger.info("No records found within the time bounds.")
            return

        start_date = get_date_string(start_date, DATE_STR_FORMAT_SPECIAL)
        end_date = get_date_string(end_date, DATE_STR_FORMAT_SPECIAL)
        subfolder_name = SUBFOLDER_NAME_FORMAT.format(start_date, end_date)
        pdf_generator = PDFGenerator(subfolder_name)
        for student, data in invoice_data.items():
            path_to_pdf = pdf_generator.build(curr_date, invoice_no, student, data)
            if not files_only:
                self.__mail_invoices(db, invoice_data)
            invoice_no += 1

        if files_only:
            return

    def __generate_invoice_data(self, db, start_date, end_date, adjustments_date):
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
        lesson_records = self.__get_lesson_records(db, start_date, end_date)

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
                    rate_per_hour = db.getTableRecordValue(INDV_RATE_SHEET_ID, (tutor, subject, student), INDV_RATE_HOURLY_RATE)
                    self.__add_student_lesson(invoice_data, student, tutor, subject, date, duration, rate_per_hour)
                else:
                    student = students_absent[0]
                    self.__add_student_cancellation_adjustment(db, invoice_data, student, tutor, subject, date)
            else:
                for student in students_present:
                    rate_per_hour = db.getTableRecordValue(GRP_RATE_SHEET_ID, (tutor, subject, n_students), GRP_RATE_HOURLY_RATE)
                    self.__add_student_lesson(invoice_data, student, tutor, subject, date, duration, rate_per_hour)
                for student in students_absent:
                    self.__add_student_cancellation_adjustment(db, invoice_data, student, tutor, subject, date)

        # get adjustments costs
        adjustments_records = self.__get_adjustment_records(db, adjustments_date)

        for adjustments_record in adjustments_records:

            adjustment_time = adjustments_record[ADJUSTMENT_TYPE]
            student = adjustments_record[ADJUSTMENT_STUDENT]
            cost = adjustments_record[ADJUSTMENT_COST]
            reason = adjustments_record[ADJUSTMENT_REASON]
            if adjustment_time == ADJUSTMENT_TYPE__DEB:
                reason += DEBIT_AMT.format(cost)
            else:
                reason += CREDIT_AMT.format(cost)
            
            invoice_data[student][INV_ADJUSTMENTS].append({
                INV_TYPE: adjustment_time,
                INV_COST: cost,
                INV_REASON: reason
            })

        return invoice_data    

    def __get_lesson_records(self, db, start_date, end_date):
        '''
            Retrieves all the lesson records for lessons between the specified date bounds.

            Arguments:
                db         (AdHocDB): Database
                start_date    (date): Lower bound (inclusive) for record cut off
                end_date      (date): Upper bound (inclusive) for record cut off

            Returns:
                List: A list of lesson records
        '''

        all_lessons = db.getTable(LESSON_SHEET_ID).values()
        return [record for record in all_lessons if start_date <= get_date(record[LESSON_DATE], DATE_TIME_STR_FORMAT_STANDARD) <= end_date]

    def __get_students(self, students_as_str):
        '''
            Retrieves a list of students from a string.

            Arguments:
                students_as_str (string): A list of students as a comma-separated string 

            Returns:
                List: A list of students
        '''

        students_as_str = students_as_str.strip()
        if students_as_str:
            return [student.strip() for student in students_as_str.split(",")]
        return []

    def __get_adjustment_records(self, db, adjustments_date):
        '''
            Retrieves all the adjustments records needed for the current invoicing date.

            Arguments:
                db            (AdHocDB): Database
                adjustments_date (date): Date as of which adjustments are outstanding 

            Returns:
                List: A list of outstanding adjustment records
        '''

        all_adjustments = db.getTable(ADJUSTMENT_SHEET_ID).values()
        return [record for record in all_adjustments if get_date(record[ADJUSTMENT_INVOICE_DATE].strip(), DATE_STR_FORMAT_STANDARD) == adjustments_date]

    def __add_student_lesson(self, invoice_data, student, tutor, subject, date, duration, rate):
        '''
            Adds a new student lesson.

            Arguments:
                invoice_data (Dictionary): A dictionary containing all the invoice data
                student          (string): The student's name
                tutor            (string): The tutor's name
                subject          (string): The subject
                date             (string): The datetime on which the lesson took place
                duration         (string): The duration of the lesson
                cost              (float): The cost of the lesson        
        '''

        cost = rate * get_duration_in_hours(duration)
        invoice_data[student][INV_LESSONS].append({
            INV_TUTOR: tutor,
            INV_SUBJECT: subject,
            INV_DATE: date,
            INV_DURATION: duration,
            INV_COST: cost
        })

    def __add_student_cancellation_adjustment(self, db, invoice_data, student, tutor, subject, date):
        '''
            Adds a new student cancellation adjustment.

            Arguments:
                invoice_data (Dictionary): A dictionary containing all the invoice data
                student          (string): The student's name
                tutor            (string): The tutor's name
                subject          (string): The subject
                date             (string): The datetime on which the lesson took place
        '''

        cost = db.getTableRecordValue(MISC_SHEET_ID, (MISC_KEY__LATE, ), MISC_VALUE)
        date = get_formatted_date_time(date, DATE_TIME_STR_FORMAT_STANDARD, DATE_STR_FORMAT_SPECIAL)
        invoice_data[student][INV_ADJUSTMENTS].append({
            INV_TYPE: ADJUSTMENT_TYPE__DEB,
            INV_COST: cost,
            INV_REASON: LATE_CANCELLATION_MSG.format(subject, tutor, date, cost)
        })

    def __mail_invoices(self, db, invoice_data):
        pass

    def __mail_invoice(self):
        pass