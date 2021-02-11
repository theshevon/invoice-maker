'''
:name: Mailing.py
:author: Shevon Mendis <shevonmendis@gmail.com>
:purpose: To send out emails to their intended recipients.
'''

import os
import sys
import smtplib
import logging

from email.message import EmailMessage
from common.defaults import INVOICE_PDF_NAME_ON_EMAIL
from modules.util import log 

# path to the file containing the invoice in an html format
PATH_TO_EMAIL_TEMPLATE = "./assets/email/email_template.html"

class Mailer:

    def __init__(self, use_prod):
        '''
            Ctor.

            Arguments:
                use_prod (bool): True if production mail server should be used; False o/w
        '''

        self.logger = logging.getLogger(__name__)

        with open(PATH_TO_EMAIL_TEMPLATE) as f:
            self.EMAIL_TEMPLATE = f.read()

        try:  
            if use_prod:
                log("Attempting to connect to production email server...")
                self.smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
                self.username = os.environ.get("EMAIL_USER")
                self.smtp.login(self.username, os.environ.get("EMAIL_PASS"))
            else:
                log("Attempting to connect to test email server")
                self.smtp = smtplib.SMTP("localhost", 1025)
        except:
            self.logger.error("Error connecting to SMTP client!", exc_info=True)
            sys.exit()

    def send_email(self, student_name, student_email, path_to_pdf):
        '''
            Send invoice emails out to the intended recipients.

            Arguments:
                student_name  (string): The student's name
                student_email (string): The student's email address
                path_to_pdf   (string): Path to the students invoice PDF

            Returns:
                bool: True if the email was sent successfully; False o/w
        '''

        try:

            msg = EmailMessage()
            msg["Subject"] = "Invoice"
            msg["From"] = self.username
            msg["To"] = student_email

            # add html message
            msg.add_alternative(self.EMAIL_TEMPLATE, subtype="html")
            
            # add invoice attachment
            with open(path_to_pdf, "rb") as f:
                content = f.read()
                msg.add_attachment(content, maintype='application', subtype='pdf', filename=INVOICE_PDF_NAME_ON_EMAIL)

            self.smtp.send_message(msg)

            log(f"Sent invoice email to { student_name } <{ student_email }>")
            return True

        except:

            self.logger.error(f"Error sending invoice email to { student_name } <{ student_email }>!", exc_info=True)
            return False

    def close_mail_server_connection(self):
        '''
            Closes the mail server connection.
        '''

        try:
            self.smtp.close()
        except:
            return