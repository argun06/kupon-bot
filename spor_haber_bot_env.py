import requests
import time
from telegram import Bot
from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
API_TOKEN = os.getenv("FOOTBALL_DATA_API_KEY")  # football-data.org token

bot = Bot(token=TELEGRAM_TOKEN)

def haberleri_cek():
    url = "https://api.football-data.org/v4/matches"
    headers = {
        "X-Auth-Token": API_TOKEN
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        haberler = []
        for match in data.get("matches", []):
            home = match['homeTeam']['name']
            away = match['awayTeam']['name']
            utc_time = match['utcDate']
            competition = match['competition']['name']

            haberler.append({
                "mac": f"{home} vs {away}",
                "analiz": f"{competition} - Başlama: {utc_time}",
                "oran": "Veri yok",
                "link": "https://www.football-data.org/"
            })

        return haberler

    except requests.exceptions.RequestException as e:
        print(f"Hata oluştu: {e}")
        return []

def paylas():
    haberler = haberleri_cek()

    if not haberler:
        print("Haber bulunamadı.")
        return

    for h in haberler:
        mesaj = f"📌 *{h['mac']}*\n" \
                f"📊 Oran: `{h['oran']}`\n🔗 [Detay]({h['link']})\n" \
                f"*Yorum:* {h['analiz']}"

        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=mesaj, parse_mode="Markdown")
        time.sleep(2)

if __name__ == "__main__":
    print("Bot baslatildi...")  # Artık emoji yok
    paylas()


