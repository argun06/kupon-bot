import os
import requests
import time
from datetime import datetime
from telegram import Bot
from dotenv import load_dotenv

# Ortam değişkenlerini yükle
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
FOOTBALL_DATA_API = os.getenv("FOOTBALL_DATA_API")

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def get_today_matches():
    url = "https://api.football-data.org/v4/matches"
    headers = {
        "X-Auth-Token": FOOTBALL_DATA_API
    }
    params = {
        "dateFrom": datetime.today().strftime('%Y-%m-%d'),
        "dateTo": datetime.today().strftime('%Y-%m-%d')
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        return data.get("matches", [])
    else:
        print("API Hatası:", response.status_code, response.text)
        return []

def analyze_match(match):
    home = match['homeTeam']['name']
    away = match['awayTeam']['name']
    match_info = f"{home} vs {away}"

    prompt = f"""
    Aşağıda verilen futbol maçı için profesyonel bir yorumcu gibi analiz yap:

    Maç: {home} vs {away}
    
    1. Takımlıların son form durumu
    2. Beklenen skor tahmini
    3. Kazanma yüzdeleri (tahmini)
    4. Genel değerlendirme ve yorum

    Kısa, net ve anlaşılır yaz. Tahminlerinde iddialı ol.
    """

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        content = response.json()['choices'][0]['message']['content']
        return content
    else:
        return "AI analiz yüklenemedi."

def analiz_mesaj_olustur(analiz, home, away, tarih):
    mesaj = f"""
📅 *{tarih}*
🏟️ *{home}* vs *{away}*

{analiz}
"""
    return mesaj

def gonder():
    matches = get_today_matches()

    if not matches:
        print("Bugün maç bulunamadı.")
        return

    print("Analizler başlıyor...")

    for match in matches[:5]:  # Test için sadece ilk 5 maça analiz
        home = match['homeTeam']['name']
        away = match['awayTeam']['name']
        tarih = match['utcDate'].split("T")[0]

        analiz = analyze_match(match)
        mesaj = analiz_mesaj_olustur(analiz, home, away, tarih)

        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=mesaj, parse_mode="Markdown")
        time.sleep(10)

if __name__ == "__main__":
    print("🚀 Bot başlatıldı...")
    gonder()





