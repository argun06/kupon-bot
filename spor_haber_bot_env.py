import os
import requests
import datetime
import time
import asyncio
import openai
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FOOTBALL_API_KEY = os.getenv("FOOTBALL_DATA_API")

openai.api_key = OPENAI_API_KEY
bot = Bot(token=TELEGRAM_TOKEN)

def get_today_matches():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    url = f"https://api.football-data.org/v4/matches?dateFrom={today}&dateTo={today}"
    headers = {"X-Auth-Token": FOOTBALL_API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("matches", [])
    else:
        print("API Hatası:", response.status_code, response.text)
        return []

def generate_prompt(match):
    home = match["homeTeam"]["name"]
    away = match["awayTeam"]["name"]
    return (
        f"{home} vs {away} maçını analiz et.\n"
        f"- Takımların son form durumu\n"
        f"- Tahmini skor\n"
        f"- Kazanma yüzdesi\n"
        f"- Varsa oran bilgisi\n"
        f"- AI uzman yorumu şeklinde detaylı analiz yap. Türkçe yaz."
    )

def get_ai_analysis(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print("OpenAI Hatası:", e)
        return "AI analiz alınamadı."

async def paylaş():
    print("🚀 Bot başlatıldı...")
    matches = get_today_matches()
    if not matches:
        print("⚠️ Bugün maç bulunamadı.")
        return

    for idx, match in enumerate(matches):
        home = match["homeTeam"]["name"]
        away = match["awayTeam"]["name"]
        match_time = match.get("utcDate", "")[:16].replace("T", " ")
        prompt = generate_prompt(match)
        analiz = get_ai_analysis(prompt)
        mesaj = (
            f"*{home} vs {away}*\n"
            f"🕒 Maç Saati: `{match_time}`\n"
            f"🧠 *Yorum:*\n{analiz}"
        )

        try:
            await bot.send_message(chat_id=CHAT_ID, text=mesaj, parse_mode="Markdown")
            print(f"✅ {home} vs {away} paylaşıldı.")
        except Exception as e:
            print(f"Telegram Hatası: {e}")

        await asyncio.sleep(300)  # 5 dakika bekle (test için)

if __name__ == "__main__":
    asyncio.run(paylaş())



