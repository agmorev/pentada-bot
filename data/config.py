import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = "5770040764:AAHZDPOOfphwcfdMZU---QqwBnd3ArSXAM0"
admins = [
    1061732281
]

ip = os.getenv("ip")

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}

# webhook settings
WEBHOOK_HOST = "https://agmorev.pythonanywhere.com"
WEBHOOK_PORT = 8443
WEBHOOK_PATH = f"/{BOT_TOKEN}/"
WEBHOOK_URL = f"{WEBHOOK_HOST}:{WEBHOOK_PORT}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = "https://agmorev.pythonanywhere.com"  # or ip
# WEBAPP_PORT = os.getenv("WEBAPP_PORT")
WEBAPP_PORT = 3001

WEBHOOK_SSL_CERT = "webhook_cert.pem"
WEBHOOK_SSL_PRIV = "webhook_pkey.pem"