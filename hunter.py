import telebot
import os
from flask import Flask
from threading import Thread

# 1. إعداد التوكن الجديد
TOKEN = "8654058295:AAEX6SX5kX9H8qVjLa27Rzr3DcTNABz5bdw"
bot = telebot.TeleBot(TOKEN)

# 2. إعداد سيرفر ويب لمنع توقف Render
app = Flask('')

@app.route('/')
def home():
    return "X-Hunter is running 24/7!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 3. أوامر البوت الأساسية
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "✅ تم تفعيل رادار X-Hunter بنجاح!\n\n"
        "البوت الآن متصل بالسيرفر ويراقب الكلمات المفتاحية المتعلقة ببحث الاحتيال الرقمي."
    )
    bot.reply_to(message, welcome_text)

# 4. تشغيل البوت والسيرفر
if __name__ == "__main__":
    print("جاري تشغيل السيرفر والبوت...")
    keep_alive() # تشغيل سيرفر الويب في الخلفية
    bot.infinity_polling() # تشغيل استقبال رسائل تليجرام
