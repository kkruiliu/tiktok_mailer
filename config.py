import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DEFAULT_SMTP = {
    "smtp_host": os.getenv("DEFAULT_SMTP_HOST"),
    "smtp_port": int(os.getenv("DEFAULT_SMTP_PORT")),
    "username": os.getenv("DEFAULT_USERNAME"),
    "password": os.getenv("DEFAULT_PASSWORD"),
    "tls": True
}
