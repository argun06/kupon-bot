import requests
import time
import datetime
import os
import openai
import telegram
from apscheduler.schedulers.blocking import BlockingScheduler

# Ortam değişkenlerini yükle
FOOTBALL_DATA_API = os.getenv("FOOTBALL_DATA_API")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

HEADERS = {"X-Auth-Token": FOOTBALL_DATA_API}
API_URL = "https://api.football-data.org/v4/matches?dateFrom={}&dateTo={}"

# Tarihi al
def get_today_matches():
    today = datetime.date.today()
    url = API_URL.format(today, today)
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print("API Hatası:", response.status_code)
        return []
    data = response.json()
    return data.get("matches", [])

# AI analiz fonksiyonu
def analiz_uret(match):
    home = match['homeTeam']['name']
    away = match['awayTeam']['name']
    tarih = match['utcDate'][:10]
    prompt = f"Bugün oynanacak {home} - {away} maçını analiz et. Form durumlarını değerlendir, olası skor tahmini yap, kazanma yüzdesini belirt, varsa oran bilgisi ver ve uzman gibi kısa net bir yorum yap."

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Sen bir futbol analiz uzmanısın."},
                {"role": "user", "content": prompt}
            ]
        )
        analiz = completion.choices[0].message.content
    except Exception as e:
        analiz = f"AI analizi alınamadı: {e}"

    mesaj = f"\n\n📅 *{tarih}*
🏟️ *{home}* vs *{away}*\n\n{analiz}"
    return mesaj

# Telegram'a gönder
def gonder_telegram(mesaj):
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=mesaj, parse_mode=telegram.constants.ParseMode.MARKDOWN)
    except Exception as e:
        print("Telegram gönderim hatası:", e)

# Ana fonksiyon
def gune_ozel_analiz():
    print("🔄 Maçlar alınıyor...")
    matches = get_today_matches()
    print(f"Toplam maç sayısı: {len(matches)}")
    for i, match in enumerate(matches):
        mesaj = analiz_uret(match)
        gonder_telegram(mesaj)
        print(f"✅ {i+1}/{len(matches)} gönderildi")
        time.sleep(300)  # 5 dakika bekle (test için)

# Zamanlayıcı kur
scheduler = BlockingScheduler()
scheduler.add_job(gune_ozel_analiz, 'cron', hour=8, minute=0)

print("⏳ Günlük analiz botu çalışıyor...")
scheduler.start()




