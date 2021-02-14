'''
:name: gs_constants.py
:author: Shevon Mendis <shevonmendis@gmail.com>
:purpose: To store all the field names/ keys for the sheets in the Google sheet.
'''

# ID of google sheet being accessed
GOOGLE_SHEET_ID = "1v1Leb35stPMgGd6Ut9KA2_8Aa0fj0t6QlKf1lPjWi1g" 

# constants for the "Lesson" sheet
LESSON_SHEET_ID = "Lesson"

LESSON_TUTOR = "Tutor"

LESSON_SUBJECT = "Subject"

LESSON_DATE = "Date"

LESSON_DURATION = "Duration"

LESSON_STUDENTS_PRESENT = "StudentsPresent"

LESSON_STUDENTS_ABSENT = "StudentsAbsent"

LESSON_REMARKS = "Remarks"

LESSON_SHEET_PRIMARY_KEY = (LESSON_TUTOR, LESSON_SUBJECT, LESSON_DATE)

# constants for the "Students" sheet
STUDENT_SHEET_ID = "Student"

STUDENT_STUDENT = "Student"

STUDENT_EMAIL = "Email"

STUDENT_SHEET_PRIMARY_KEY = (STUDENT_STUDENT,)

# constants for the "IndvRates" sheet
INDV_RATE_SHEET_ID = "IndvRate"

INDV_RATE_TUTOR = "Tutor"

INDV_RATE_SUBJECT = "Subject"

INDV_RATE_STUDENT = "Student"

INDV_RATE_HOURLY_RATE = "HourlyRate"

INDV_RATE_SHEET_PRIMARY_KEY = (INDV_RATE_TUTOR, INDV_RATE_SUBJECT, INDV_RATE_STUDENT)

# constants for the "GrpRates" sheet
GRP_RATE_SHEET_ID = "GrpRate"

GRP_RATE_TUTOR = "Tutor"

GRP_RATE_SUBJECT = "Subject"

GRP_RATE_N_STUDENTS = "NStudents"

GRP_RATE_HOURLY_RATE = "HourlyRate"

GRP_RATE_SHEET_PRIMARY_KEY = (GRP_RATE_TUTOR, GRP_RATE_SUBJECT, GRP_RATE_N_STUDENTS)

# constants for the "Adjustments" sheet
ADJUSTMENT_SHEET_ID = "Adjustment"

ADJUSTMENT_INVOICE_DATE = "InvoiceDate"

ADJUSTMENT_TYPE = "Type"

ADJUSTMENT_TYPE__CRED = "Credit"

ADJUSTMENT_TYPE__DEB = "Debit"

ADJUSTMENT_STUDENT = "Student"

ADJUSTMENT_COST = "Cost"

ADJUSTMENT_REASON = "Reason"

ADJUSTMENT_SHEET_PRIMARY_KEY = (ADJUSTMENT_INVOICE_DATE, ADJUSTMENT_STUDENT, ADJUSTMENT_REASON)

# constants for the "Misc" sheet
MISC_SHEET_ID = "Misc"

MISC_KEY = "Key"

MISC_KEY__LATE = "Late Cancellation Fee"

MISC_VALUE = "Value"

MISC_SHEET_PRIMARY_KEY = (MISC_KEY,)