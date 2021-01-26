# ID of google sheet being accessed
GOOGLE_SHEET_ID = "1v1Leb35stPMgGd6Ut9KA2_8Aa0fj0t6QlKf1lPjWi1g" 

# constants for the "Classes" sheet
CLASSES_SHEET_ID = "Classes"

CLASSES_TUTOR = "Tutor"

CLASSES_SUBJECT = "Subject"

CLASSES_DATE = "Date"

CLASSES_DURATION = "Duration"

CLASSES_STUDENTS = "Students"
	
CLASSES_REMARKS = "Remarks"

CLASSES_CANCELLATION = "Cancellation"

CLASSES_PRIMARY_KEY = (CLASSES_TUTOR, CLASSES_SUBJECT, CLASSES_DATE)

# constants for the "Students" sheet
STUDENTS_SHEET_ID = "Students"

STUDENTS_STUDENT = "Student"

STUDENTS_EMAIL = "Email"

STUDENTS_PRIMARY_KEY = (STUDENTS_STUDENT,)

# constants for the "Lessons" sheet
LESSONS_SHEET_ID = "Lessons"

LESSONS_STUDENT = "Student"

LESSONS_TUTOR = "Tutor"

LESSONS_SUBJECT = "Subject"

LESSONS_HOURLY_RATE = "HourlyRate"

LESSONS_PRIMARY_KEY = (LESSONS_TUTOR, LESSONS_STUDENT, LESSONS_STUDENT)

# constants for the "Adjustments" sheet
ADJUSTMENTS_SHEET_ID = "Adjustments"

ADJUSTMENTS_OWED_PARTY = "OwedParty"

ADJUSTMENTS_STUDENT = "Student"

ADJUSTMENTS_INVOICE_DATE = "InvoiceDate"

ADJUSTMENTS_AMOUNT = "Amount"

ADJUSTMENTS_REASON = "Reason"

ADJUSTMENTS_PRIMARY_KEY = (ADJUSTMENTS_OWED_PARTY, ADJUSTMENTS_STUDENT, ADJUSTMENTS_INVOICE_DATE)

# constants for the "MiscCosts" sheet
MISC_COSTS_SHEET_ID = "MiscCosts"

MISC_COSTS_CATEGORY = "Category"

MISC_COSTS_COST = "Cost"

MISC_COSTS_PRIMARY_KEY = (MISC_COSTS_CATEGORY, MISC_COSTS_COST)