import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Assuming AppConfig is set up properly and contains sender_email and password
from utils.app_config import AppConfig

# Email account credentials
smtp_server = 'smtp.gmail.com'
smtp_port = 587

sender_email = AppConfig.sender_email
password = AppConfig.password

# Email details
receiver_email = 'alisamitchikov@gmail.com'
subject = 'PDF Report: Israel Wars Analysis'
body = 'Please find attached the PDF report for the Israel Wars analysis.'

# Path to the PDF file
pdf_file_path = 'output.pdf'

# Create the email
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject

# Attach the email body
msg.attach(MIMEText(body, 'plain'))

# Attach the PDF file
try:
    with open(pdf_file_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename={os.path.basename(pdf_file_path)}',
        )
        msg.attach(part)
except Exception as e:
    print(f'Error attaching file: {e}')
    sys.exit(1)

# Send the email
try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Upgrade to a secure connection
        server.login(sender_email, password)  # Log in with the App Password
        server.send_message(msg)
        print('Email sent successfully!')
except Exception as e:
    print(f'Error: {e}')
