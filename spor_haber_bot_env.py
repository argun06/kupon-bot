import os
import requests
import feedparser
import openai
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

openai.api_key = OPENAI_API_KEY

RSS_URL = "https://www.fotomac.com.tr/rss/anasayfa.xml"

def haberleri_cek():
    feed = feedparser.parse(RSS_URL)
    haberler = []
    for entry in feed.entries[:3]:
        haberler.append({"baslik": entry.title, "icerik": entry.summary})
    return haberler

def gpt_analiz_yap(haber):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Spor haberlerini analiz eden bir asistansın."},
                {"role": "user", "content": f"Haber başlığı: {haber['baslik']}\nİçerik: {haber['icerik']}\nBu haberi 2 cümleyle Türkçe özetle ve analiz et."}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Analiz yapılamadı: {str(e)}"

def telegrama_gonder(mesaj):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mesaj,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Telegram'a gönderilemedi:", e)

def main():
    print("🚀 Bot başlatıldı...\n")
    print("📰 Haber kontrolü başladı...\n")
    haberler = haberleri_cek()
    if not haberler:
        print("⚠️ Haber bulunamadı.")
        return
    for haber in haberler:
        analiz = gpt_analiz_yap(haber)
        mesaj = f"📰 *{haber['baslik']}*\n\n{analiz}"
        telegrama_gonder(mesaj)

if __name__ == "__main__":
    main()