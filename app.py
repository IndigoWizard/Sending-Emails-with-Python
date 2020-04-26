import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sys import argv


sender_email = argv[1]
password = argv[2]
subject = input('Subject: ')

mailSent = 0

for receiver_email in open('emails.txt', 'r').readlines():
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email.strip()

    # Create the plain-text and HTML version of your message
    text = """\
    """ + subject
    html = open(argv[3],
                'r', encoding='utf-8').read()

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
        mailSent += 1
        print(str(mailSent) + '  SENT to: ' + receiver_email.strip())
