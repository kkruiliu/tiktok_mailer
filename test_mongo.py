import smtplib
from email.mime.text import MIMEText

msg = MIMEText("This is a test email with Gmail App Password")
msg['Subject'] = "Test SMTP"
msg['From'] = "keruiliu233@gmail.com"
msg['To'] = "keruiliu233@gmail.com"

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("keruiliu233@gmail.com", "kchkrkdeymoniafa")  # No spaces!
    server.sendmail(msg['From'], [msg['To']], msg.as_string())
    server.quit()
    print("Email sent successfully!")
except Exception as e:
    print("SMTP ERROR:", e)
