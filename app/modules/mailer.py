"""
:name: mailer.py
:author: Shevon Mendis <shevonmendis@gmail.com>
:purpose: To send out emails to their intended recipients.
"""

import os
import smtplib
from email.message import EmailMessage

def send_emails(mail_data, use_prod, logger):
    """
        Send invoice emails out to the intended recipients.

        Arguments:
            mail_data (Dictionary): A dictionary containing the information needed to generate and send the emails
            use_prod     (boolean): Flag denoting whether or not to use the production server
            logger        (Logger): Logger

        Returns:
            (int , int): A 2-tuple where the elements, in order, represent: 
                            [0]- The number of emails were actually sent out
                            [1]- The number of emails that had to be sent out
    """

    username = os.environ.get("EMAIL_USER")
    password = os.environ.get("EMAIL_PASS")

    # connect to smtp client
    try:  
        if use_prod:
            logger.info("Attempting to connect to production email server...")
            smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            smtp.login(username, password)
        else:
            logger.info("Attempting to connect to test email server")
            smtp = smtplib.SMTP("localhost", 1025)
    except:
        logger.error("Error connecting to SMTP client!", exc_info=True)
        return

    emails_sent = 0
    for record in mail_data:

        client_data = record["client_data"]
        path_to_pdf = record["path_to_pdf"]

        client_name = client_data["name"]
        client_email = client_data["email"]

        try:

            msg = EmailMessage()
            msg["Subject"] = "Invoice"
            msg["From"] = username
            # TODO: check if multiple recipients needed
            msg["To"] = client_data["email"]
            
            # add fallback in case the recipient has disabled html
            msg.set_content("Test")

            # add html message
            with open("./assets/email_template.html", "r") as f:
                html_content = f.read()
                msg.add_alternative(html_content.format(client_name), subtype="html")
            
            with open(path_to_pdf, "rb") as f:
                content = f.read()
                msg.add_attachment(content, maintype='application', subtype='pdf', filename='invoice.pdf')

            smtp.send_message(msg)
            emails_sent += 1
            logger.info(f"Sent invoice to { client_name } <{ client_email }>")
        
        except:
            # TODO: should we stop here or keep going?
            logger.error(f"Error in trying to send email to { client_name } <{ client_email }>!", exc_info=True)
            continue

    smtp.close()

    return emails_sent, len(mail_data)