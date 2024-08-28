# aliskasprojects@gmail.com
# wpf1jpd5TVZ@hub*brh
# rnin kyho tgui thin


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils.app_config import AppConfig

# Email account credentials
smtp_server = 'smtp.gmail.com'
smtp_port = 587
# sender_email = 'aliskasprojects@gmail.com'
# password = 'rnin kyho tgui thin' 

sender_email = AppConfig.sender_email
password = AppConfig.password

# Email details
receiver_email = 'alisamitchikov@gmail.com'
subject = 'TEST EMAIL'
body = 'This is the body of the email.'

# Create the email
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject

# Attach the email body
msg.attach(MIMEText(body, 'plain'))

# Send the email
try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Upgrade to a secure connection
        server.login(sender_email, password)  # Log in with the App Password
        server.send_message(msg)
        print('Email sent successfully!')
except Exception as e:
    print(f'Error: {e}')




