from signal_parser import parse_signal

import telebot
import os

# Вземаме токена от системна променлива или го пишем директно
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "ТУК_СЛОЖИ_ТВОЯ_ТОКЕН")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Здравей, генерале! 🤖 Ботът е активен и чака сигнали.")

# Това е за ping/health проверка
@bot.message_handler(commands=['ping'])
def handle_ping(message):
    bot.reply_to(message, "✅ Alive and operational, шефе.")

# Стартираме бота
if __name__ == "__main__":
    print("Ботът е стартиран...")
    bot.infinity_polling()
