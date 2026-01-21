import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv


# ================================
# LOAD ENV VARIABLES
# ================================
load_dotenv()  # Loads variables from .env file


# ================================
# SMTP CONFIGURATION
# ================================
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

GMAIL_EMAIL = os.getenv("GMAIL_EMAIL")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")


def send_email(to_email: str, subject: str, body: str):
    """
    Sends an email using Gmail SMTP.
    The AI agent decides WHEN to call this function.
    """

    if not GMAIL_EMAIL or not GMAIL_APP_PASSWORD:
        raise EnvironmentError(
            "GMAIL_EMAIL or GMAIL_APP_PASSWORD not set in .env file"
        )

    if not to_email or not subject or not body:
        raise ValueError("Email fields cannot be empty")

    # Create email message
    msg = MIMEMultipart()
    msg["From"] = GMAIL_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        # Connect to Gmail SMTP server
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(GMAIL_EMAIL, GMAIL_APP_PASSWORD)
            server.send_message(msg)

        print(f"✅ Email sent to {to_email}")

    except Exception as e:
        print("❌ Failed to send email")
        raise e