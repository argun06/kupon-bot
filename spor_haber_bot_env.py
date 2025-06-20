import os
import requests
import datetime
import time
from openai import OpenAI
from telegram import Bot

# Ortam değişkenleri
API_TOKEN = os.getenv("FOOTBALL_DATA_API")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Bot ve OpenAI
bot = Bot(token=TELEGRAM_BOT_TOKEN)
openai = OpenAI(api_key=OPENAI_API_KEY)

# Tarih formatı
bugun = datetime.datetime.now().strftime("%Y-%m-%d")

def maclari_getir():
    url = f"https://api.football-data.org/v4/matches?dateFrom={bugun}&dateTo={bugun}"
    headers = {"X-Auth-Token": API_TOKEN}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("matches", [])
    return []

def analiz_uret(ev_takimi, deplasman_takimi):
    mesaj = (
        f"{ev_takimi} ile {deplasman_takimi} arasındaki maç hakkında:
"
        f"1. Takımların form durumu nedir?
"
        f"2. Tahmini skor ne olur?
"
        f"3. Hangi takım kazanır?
"
        f"4. Maç için oran bilgisi olmasa da analiz yap.
"
        f"5. Uzman gibi kısa ve net bir yorum yaz."
    )
    yanit = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Bir bahis uzmanı gibi konuş."},
            {"role": "user", "content": mesaj}
        ],
        temperature=0.7
    )
    return yanit.choices[0].message.content.strip()

def gonder(mesaj):
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=mesaj, parse_mode="Markdown")

def main():
    maclar = maclari_getir()
    if not maclar:
        gonder("⚠️ Bugün için analiz yapılacak maç bulunamadı.")
        return

    for mac in maclar:
        ev = mac["homeTeam"]["name"]
        dep = mac["awayTeam"]["name"]
        saat = mac["utcDate"].split("T")[1][:5]
        try:
            analiz = analiz_uret(ev, dep)
            mesaj = f"📊 *{ev} vs {dep}* ({saat})\n\n{analiz}"
            gonder(mesaj)
            time.sleep(5)  # Flood koruması için
        except Exception as e:
            gonder(f"❌ {ev} vs {dep} maçının analizinde hata: {e}")

if __name__ == "__main__":
    main()




