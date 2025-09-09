from database import mailboxes_col

mailboxes_col.update_one(
    {"name": "campaignA"},
    {"$set": {
        "smtp_host": "smtp.gmail.com",
        "smtp_port": 587,
        "tls": True
    }}
)

print("Updated SMTP config for campaignA.")
