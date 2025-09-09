import smtplib
from email.mime.text import MIMEText
from email.utils import make_msgid
from database import get_mailbox_config, insert_email_log, is_unsubscribed
from datetime import datetime
import uuid

def generate_message_id():
    return str(uuid.uuid4())

def send_email(recipient, subject, html_body, mailbox_name):
    # 1. Skip if unsubscribed
    if is_unsubscribed(recipient):
        print(f"{recipient} is unsubscribed. Skipping.")
        return

    # 2. Load mailbox config from MongoDB
    smtp_config = get_mailbox_config(mailbox_name)
    if not smtp_config:
        raise ValueError(f"Mailbox config '{mailbox_name}' not found")

    # 3. Create unique message ID
    message_id = generate_message_id()

    # 4. Append tracking pixel and unsubscribe link
    tracking_pixel = f"<img src='http://127.0.0.1:5000/open/{message_id}' width='1' height='1'/>"
    unsubscribe_link = f"<p><a href='http://127.0.0.1:5000/unsubscribe?email={recipient}'>Unsubscribe</a></p>"
    full_html = html_body + tracking_pixel + unsubscribe_link

    # 5. Build email
    msg = MIMEText(full_html, 'html')
    msg['Subject'] = subject
    msg['From'] = smtp_config['username']
    msg['To'] = recipient
    msg['Message-ID'] = make_msgid()

    # 6. Send email
    try:
        if smtp_config.get("tls", True):
            server = smtplib.SMTP(smtp_config['smtp_host'], smtp_config['smtp_port'],timeout=10)
            server.starttls()
        else:
            server = smtplib.SMTP_SSL(smtp_config['smtp_host'], smtp_config['smtp_port'],timeout=10)

        server.login(smtp_config['username'], smtp_config['password'])
        server.sendmail(msg['From'], [msg['To']], msg.as_string())
        server.quit()

        print(f"✅ Email sent to {recipient}")

        # 7. Log to MongoDB
        insert_email_log({
            "recipient": recipient,
            "subject": subject,
            "html": full_html,
            "mailbox_name": mailbox_name,
            "message_id": message_id,
            "opened": False,
            "opened_at": None,
            "sent_at": datetime.utcnow()
        })

    except Exception as e:
        print("Error sending email:", e)
