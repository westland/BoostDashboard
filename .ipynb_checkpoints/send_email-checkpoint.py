import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv()

def send_personalized_email(to_email: str, subject: str, body: str) -> bool:
    """
    Sends a personalized email via configured SMTP.
    
    WARNINGS:
    - Only use with explicit consent / subscription.
    - Comply with CAN-SPAM (US) and GDPR (EU) regulations.
    - Unsolicited commercial outreach has extremely low conversion rates and high ban risks.
    - Prefer platform-native direct messages (Reddit DMs, Discord) where users opt-in to help requests.
    """
    smtp_email = os.getenv("SMTP_EMAIL")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port_str = os.getenv("SMTP_PORT", "587")

    if not smtp_email or not smtp_password:
        print("SMTP email credentials not set in env variables. Cannot send email.")
        return False

    try:
        smtp_port = int(smtp_port_str)
    except ValueError:
        smtp_port = 587

    msg = MIMEMultipart()
    msg["From"] = smtp_email
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_email, smtp_password)
        server.send_message(msg)
        server.quit()
        print(f"✅ Email successfully sent to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")
        return False

if __name__ == "__main__":
    # Test message warning
    print("Email utility loaded. Usage: from send_email import send_personalized_email")
