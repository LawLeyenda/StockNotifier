import Passwords
import smtplib
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# The mail addresses and password
class AutomateEmail:
    def basic_automatic_email(self, email_subject, content):
        sender_address = Passwords.gmail_user
        sender_pass = Passwords.gmail_pass
        receiver_address = Passwords.gmail_receiver
        # Setup the MIME
        message = MIMEMultipart()

        mail_content = content

        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = email_subject
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

    def renotify_email(self, stock_info, news):
        if stock_info is None:
            return

        ticker = stock_info[0]
        name = stock_info[1]
        price = stock_info[2]
        change = stock_info[3]

        if change > 0:  # check if change is positive or negative
            changed = "increased"
            news = "Good news!"
        else:
            changed = "decreased"
            news = "Bad news!"

        email_subject = "Update " + name + " (" + ticker + ") "" | $" + str(round(price, 2))
        email_body = str(date.today()) + f"\n{news} " + email_subject + " is currently trading at $" + str(
            price) + f". Today it has {changed} a total of " + str(abs(change)) + "%.\n" + news
        self.basic_automatic_email(email_subject, email_body)

    def notify(self, stock_info, news):
        if stock_info is None:
            return

        ticker = stock_info[0]
        name = stock_info[1]
        price = stock_info[2]
        change = stock_info[3]

        email_subject = name + " (" + ticker + ") "
        # change message based on increase or decrease
        if change > 0:
            changed = "increased"
        else:
            changed = "decreased"
        email_body = str(date.today()) + "\n" + email_subject + f" has {changed} by " + str(
            abs(round(change, 2))) + "% and is currently trading at $" + str(price) + ".\n" + news
        print("Sending " + str(ticker) + " email...")  # for testing purposes
        self.basic_automatic_email(email_subject, email_body)

    def end_of_week(self, database):
        analysts = str(date.today()) + "\n"
        list = database.sql_fetch_many("distinct stock_name, priceTargetHigh, priceTargetAvg, priceTargetLow, numberOfAnalysts", "Analysts group by stock_name having numberOfAnalysts >=10")
        for stock in list:
            analysts = analysts + "::" + str(stock[0]) + "::\nprice target low: $" + str(stock[3]) + "\nprice target high: $" \
                       + str(stock[1]) + "\nprice target average: $" + str(stock[2]) + "\nnumber of analysts: " + str(stock[4]) \
                       + "\n----------------------------------\n"
        email_subject = "Weekly Analyst Forecasts.\n"
        self.basic_automatic_email(email_subject, analysts)
        print("email sent")
        return


