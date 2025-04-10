# telegram_alerts.py

import requests

# ✅ Replace with your actual values
TELEGRAM_TOKEN = "123456789:ABCDefghIjklMnopQRStuvWxyZ"
TELEGRAM_CHAT_ID = "1130756903"

def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"❌ Telegram Error: {e}")
