import smtplib

# from config import ADMIN_EMAIL, ADMIN_EMAIL_PASSWORD, SMTP_PORT, SMTP_SERVER
# not in config yet
ADMIN_EMAIL="klukinprog@gmail.com"
ADMIN_EMAIL_PASSWORD="eqlqobtrmjevhvxw "
SMTP_SERVER="smtp.gmail.com"
SMTP_PORT=587
# eqlq obtr mjev hvxw


class EmailSender:
    def __init__(self):
        self.mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        self.sender = ADMIN_EMAIL
        self.password = ADMIN_EMAIL_PASSWORD
    def start(self):
        self.mail.ehlo()
        self.mail.starttls()
        self.mail.login(self.sender, self.password)
    def send(self, addressee, subject, content):
        header = f'To: {addressee}\nFrom: {self.sender}\nSubject: {subject}\n'
        message = header + content
        self.mail.sendmail(self.sender, addressee, message)
