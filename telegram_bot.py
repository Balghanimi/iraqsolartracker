import telebot

def send_to_telegram(offers, chat_id, token):
    if not chat_id or not token:
        print("Missing Telegram chat ID or token")
        return
    try:
        bot = telebot.TeleBot(token)
        message = "عروض الطاقة الشمسية:\n"
        for offer in offers:
            message += f"{offer['title'][:40]} - {offer['price']} {offer['currency']} ({offer['governorate']})\n"
        bot.send_message(chat_id, message)
    except Exception as e:
        print(f"Error sending to Telegram: {e}")
