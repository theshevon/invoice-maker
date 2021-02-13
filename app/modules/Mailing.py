'''
:name: Mailing.py
:author: Shevon Mendis <shevonmendis@gmail.com>
:purpose: To send out emails to their intended recipients.
'''

import os
import sys
import smtplib
import logging

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from common.defaults import INVOICE_PDF_NAME_ON_EMAIL
from modules.util import log 

PATH_TO_MSG_HTML = "./assets/email/msg.html"
PATH_TO_MSG_TEXT = "./assets/email/msg.txt"
PATH_TO_MSG_IMGS = "./assets/email/"

class Mailer:

    def __init__(self, use_prod):
        '''
            Ctor.

            Arguments:
                use_prod (bool): True if production mail server should be used; False o/w
        '''

        self.logger = logging.getLogger(__name__)

        msg_alt = MIMEMultipart("alternative")

        # add msg as plain text (if receiver has disabled html)
        with open(PATH_TO_MSG_TEXT) as f:
            msg_text = MIMEText(f.read())
            msg_alt.attach(msg_text)

        # add msg as html
        with open(PATH_TO_MSG_HTML) as f:
            msg_html = MIMEText(f.read())
            msg_html.replace_header("Content-Type", "text/html")
            msg_alt.attach(msg_html)

        self.msg_alt = msg_alt

        # add images that would be embedded into the msg
        msg_images = []
        for img in ["icon_social.png", "icon_email.png"]:
            with open(PATH_TO_MSG_IMGS + img, "rb") as f:
                name, _ = img.split('.')
                msg_img = MIMEImage(f.read())
                msg_img.add_header("Content-ID", f"<{ name }>")
                msg_images.append(msg_img)
        self.msg_images = msg_images

        try:  
            if use_prod:
                log("Attempting to connect to production mail server...")
                self.smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
                self.username = os.environ.get("EMAIL_USER")
                self.smtp.login(self.username, os.environ.get("EMAIL_PASS"))
            else:
                log("Attempting to connect to test mail server...")
                self.smtp = smtplib.SMTP("localhost", 1025)
            log("Succesfully connected to mail server.")
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

            msg = MIMEMultipart('related')
            msg["Subject"] = "Invoice"
            msg["From"] = self.username
            msg["To"] = student_email

            # add msg
            msg.attach(self.msg_alt)

            # add embedded images
            for img in self.msg_images:
                msg.attach(img)
            
            # add invoice attachment
            with open(path_to_pdf, "rb") as f:
                msg_pdf = MIMEApplication(f.read(), _subtype="pdf")
                msg_pdf.add_header("Content-Disposition", "attachment", filename=INVOICE_PDF_NAME_ON_EMAIL)
                msg.attach(msg_pdf)
                # msg.attach(content, maintype='application', subtype='pdf', filename=INVOICE_PDF_NAME_ON_EMAIL)

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