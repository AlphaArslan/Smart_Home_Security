import smtplib, ssl

SMTP_PORT = 465  # For SSL
SMTP_SERVER = "smtp.gmail.com"
SENDER_EMAIL = "dev.script.21@gmail.com"  # Enter your address
RECEIVER_EMAIL = "bluphanc@gmail.com"  # Enter receiver address
SENDER_PASS = "0.9millidev"
EMAIL_CONTENT = """\
Subject: Warning

Unkown person detected."""

context = ssl.create_default_context()
with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
    server.login(SENDER_EMAIL, SENDER_PASS)
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, EMAIL_CONTENT)
