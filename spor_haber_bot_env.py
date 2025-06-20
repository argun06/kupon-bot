import os
import requests
import time
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from telegram import Bot
from openai import OpenAI

# Ortam degiskenlerini yukle
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
openai = OpenAI(api_key=OPENAI_API_KEY)

# Yeni kaynak: BettingTipsToday
URL = "https://www.bettingtipstoday.com/todays-football-tips/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def haberleri_cek():
    response = requests.get(URL, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")
    haberler = []

    # Sitenin haber yapisi
    cards = soup.select(".match-container")[:3]  # ilk 3 haber
    for card in cards:
        try:
            takimlar = card.select_one(".match-teams").text.strip()
            oran = card.select_one(".match-odds").text.strip()
            link = "https://www.bettingtipstoday.com" + card.select_one("a")['href']

            analiz_prompt = f"'{takimlar}' maçı için oran {oran}. Bu maça dair kısa, net ve analitik bir bahis tahmini oluştur."
            analiz = gpt_analiz(analiz_prompt)

            haberler.append({
                "mac": takimlar,
                "oran": oran,
                "link": link,
                "analiz": analiz
            })
        except Exception as e:
            continue

    return haberler

def gpt_analiz(prompt):
    try:
        completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content.strip()
    except:
        return "AI analiz yüklenemedi."

def paylas():
    haberler = haberleri_cek()
    if not haberler:
        print("Haber bulunamadı.")
        return

    for h in haberler:
    mesaj = f"🔎 *{h['mac']}*\n" \
            f"📉 Oran: `{h['oran']}`\n🔗 [Detay]({h['link']})\n" \
            f"*Yorum:* {h['analiz']}"
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=mesaj, parse_mode="Markdown")
    time.sleep(2)


if __name__ == "__main__":
    print("🚀 Bot başlatıldı...")
    paylas()
