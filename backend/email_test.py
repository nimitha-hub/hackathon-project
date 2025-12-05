import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# Load .env from backend folder
BASE_DIR = os.path.dirname(__file__)
env_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
TO_EMAIL = os.getenv('TEST_RECIPIENT', SENDER_EMAIL)

def send_test_email():
    if not all([SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD]):
        print('Missing SMTP configuration. Please set SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, and SENDER_PASSWORD in backend/.env or the environment.')
        return

    msg = EmailMessage()
    msg['Subject'] = 'HealthPal - Test Email'
    msg['From'] = SENDER_EMAIL
    msg['To'] = TO_EMAIL
    msg.set_content('This is a test email sent from HealthPal backend email_test.py')

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as s:
            s.ehlo()
            if SMTP_PORT in (587, 25):
                s.starttls()
                s.ehlo()
            s.login(SENDER_EMAIL, SENDER_PASSWORD)
            s.send_message(msg)
        print(f'Email sent successfully to {TO_EMAIL}')
    except Exception as e:
        print('Failed to send email:')
        print(e)

if __name__ == '__main__':
    send_test_email()
