from pymongo import MongoClient
from config import MONGO_URI
from datetime import datetime

client = MongoClient(MONGO_URI)
db = client["tiktok_email_ads"]

mailboxes_col = db["mailboxes"]
emails_col = db["emails"]
unsub_col = db["unsubscribed"]

def get_mailbox_config(name):
    return mailboxes_col.find_one({"name": name})

def insert_email_log(doc):
    return emails_col.insert_one(doc)

def mark_email_opened(message_id):
    return emails_col.update_one(
        {"message_id": message_id},
        {"$set": {"opened": True}}
    )

def unsubscribe_user(email):
    return unsub_col.update_one(
        {"email": email},
        {"$set": {"unsubscribed_at": datetime.utcnow()}},
        upsert=True
    )

def is_unsubscribed(email):
    return unsub_col.find_one({"email": email}) is not None
