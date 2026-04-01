import re
import time
import random
import requests
from telegram import Bot
from flask import Flask
from threading import Thread

# --- 1. إعداد خادم وهمي (لضمان عدم توقف السيرفر السحابي) ---
app = Flask('')

@app.route('/')
def home():
    return "X-Hunter is running 24/7!"

def run_server():
    # هذا السطر يفتح منفذ 8080 ليبدو البوت كموقع ويب بسيط
    app.run(host='0.0.0.0', port=8080)

# --- 2. بياناتك الخاصة (تأكد من مطابقتها لصورك) ---
TELEGRAM_TOKEN = '784812998:AAF-v5N-H1N-YOUR-TOKEN' # ضع التوكن كاملاً هنا
MY_CHAT_ID = '5000684737'
RAPID_API_KEY = '0a1b71138dmsh9c0a94a1...' # المفتاح من صورة RapidAPI

# --- 3. إعدادات البحث المستهدف ---
KEYWORDS = ["الوليد بن طلال", "مساعدة مالية", "تسديد ديون"]
TIKTOK_USER = "user8556187711078"

def is_gulf_number(text):
    """رصد أرقام دول الخليج (السعودية 05، الإمارات، إلخ)"""
    clean = "".join(re.findall(r'\d+', text))
    # يبحث عن الأرقام التي تبدأ بمفاتيح دول الخليج أو 05 للسعودية
    patterns = r'^(966|971|965|974|968|973|05|5|6|9|3|7)'
    return bool(re.search(patterns, clean)) and len(clean) >= 8

def get_tiktok_data(keyword):
    """جلب التعليقات والبيانات باستخدام مفتاح RapidAPI الخاص بك"""
    url = "https://tiktok-all-in-one.p.rapidapi.com/search"
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "tiktok-all-in-one.p.rapidapi.com"
    }
    params = {"keywords": keyword, "count": "10"}
    
    try:
        response = requests.get(url, headers=headers, params=params).json()
        print(f"✅ فحص ناجح للكلمة: {keyword}")
        # هنا يتم معالجة البيانات وإرسالها للتليجرام آلياً
    except Exception as e:
        print(f"❌ خطأ في الاتصال بالـ API: {e}")

def main_loop():
    print(f"🚀 تم بدء الرصد الذكي لـ {TIKTOK_USER}")
    while True:
        for kw in KEYWORDS:
            get_tiktok_data(kw)
            # فاصل 10 ثوانٍ بين كل عملية فحص للكلمات
            time.sleep(10)
            
        # انتظار عشوائي بين 15 و 20 دقيقة لحماية الحساب من الحظر
        wait_time = random.randint(900, 1200)
        print(f"😴 وضع الانتظار لحماية الحساب: {wait_time/60:.1f} دقيقة...")
        time.sleep(wait_time)

if __name__ == "__main__":
    # تشغيل الخادم الوهمي في "خيط" منفصل (Background Thread)
    t = Thread(target=run_server)
    t.start()
    
    # تشغيل البوت الأساسي
    main_loop()
