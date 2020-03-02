import Passwords
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# The mail addresses and password

def automaticEmail(email_subject, content):
    sender_address = Passwords.gmail_user
    sender_pass = Passwords.gmail_pass
    receiver_address = Passwords.gmail_receiver
    # Setup the MIME
    message = MIMEMultipart()

    mail_content = "" + content

    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = "" + email_subject
    # The subject line
    # The body and the attachments for the mail

    message.attach(MIMEText(mail_content, 'plain'))
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()

