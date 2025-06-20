import requests
import time
import openai
from telegram import Bot
import os

# Ortam Değişkenlerinden verileri al
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FOOTBALL_DATA_API_KEY = "078fb7b8c4654e5693049a7dcec56fbb"

# OpenAI ayarları
openai.api_key = OPENAI_API_KEY
bot = Bot(token=TELEGRAM_BOT_TOKEN)


def cevir_ve_ozetle(ingilizce_metin):
    prompt = f"""
    Şu metni hem Türkçeye çevir hem de bahis grubunda paylaşılabilecek şekilde özetle:

    {ingilizce_metin}
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()


def maclari_cek():
    url = "https://api.football-data.org/v4/matches"
    headers = {"X-Auth-Token": FOOTBALL_DATA_API_KEY}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"API hatası: {response.status_code}")
        return []

    data = response.json()
    return data.get("matches", [])


def paylas():
    maclar = maclari_cek()
    if not maclar:
        print("Bugün için maç bilgisi yok.")
        return

    for mac in maclar[:5]:  # Güncel ilk 5 maçı paylaşalım
        home = mac['homeTeam']['name']
        away = mac['awayTeam']['name']
        date = mac['utcDate'].split("T")[0]

        icerik = f"{date} tarihinde oynanacak {home} vs {away} maçına dair bilgiler:"
        analiz = cevir_ve_ozetle(icerik)

        mesaj = f"\ud83c\udfdf {home} vs {away}\n\ud83d\udcc5 Tarih: {date}\n\n\ud83d\udd39 *Analiz:* {analiz}"

        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=mesaj, parse_mode="Markdown")
        time.sleep(2)


if __name__ == "__main__":
    print("\ud83d\ude80 Bot başlatıldı...")
    paylas()

