import requests
import os
def send_telegram_message(text):
    bot_token = os.getenv("BOT_TOKEN")
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    print(os.getenv("TELEGRAM_USER_IDS"))
    for chat_id in os.getenv("TELEGRAM_USER_IDS").split(","):
        print(chat_id)
        response = requests.get(url, params={"chat_id": chat_id, "text": text})
        if response.status_code != 200:
            print(f"Failed to send message: {response.status_code} {response.text}")
