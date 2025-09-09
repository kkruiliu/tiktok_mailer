from database import mailboxes_col

mailboxes_col.insert_one({
    "name": "campaignA",
    "smtp_host": "smtp.gmail.com",
    "smtp_port": 587,
    "username": "keruiliu233@gmail.com",
    "password": "kchkrkdeymoniafa",  # In production: encrypt this!
    "tls": True
})


from send_email import send_email

send_email(
    recipient="keruiliu233@gmail.com",
    subject="🔥 TikTok Ads: Try our automation!",
    html_body="""
        <h1>Hello Kerui!</h1>
        <p>This is your personalized TikTok ad system. 🎯</p>
    """,
    mailbox_name="campaignA"
)