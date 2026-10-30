"""Send an HTML email over plain SMTP.

In development we use MailHog (fake SMTP server): every mail sent to
localhost:1025 shows up at http://localhost:8025. If no SMTP server is
running, the mail is printed to the Celery console instead.
"""
import smtplib
from email.mime.text import MIMEText

from flask import current_app


def send_email(to, subject, html):
    msg = MIMEText(html, "html")
    msg["Subject"] = subject
    msg["From"] = current_app.config["MAIL_SENDER"]
    msg["To"] = to
    try:
        with smtplib.SMTP(current_app.config["MAIL_SERVER"], current_app.config["MAIL_PORT"], timeout=5) as smtp:
            smtp.send_message(msg)
        return True
    except OSError:
        print(f"[mail not sent - no SMTP server] To: {to} | {subject}")
        return False
