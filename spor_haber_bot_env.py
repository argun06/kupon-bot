import feedparser
from datetime import datetime
import time
from telegram import Bot
import os

# .env dosyasındaki API anahtarlarını kullanmak için:
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def haberleri_cek():
    url = "https://www.ntvspor.net/rss.xml"
    feed = feedparser.parse(url)
    bugun = datetime.now().date()

    haberler = []
    for entry in feed.entries:
        try:
            yayin_tarihi = datetime(*entry.published_parsed[:6]).date()
            if yayin_tarihi == bugun:
                haber = {
                    "mac": entry.title,
                    "link": entry.link,
                    "oran": "Oran bilgisi yok",
                    "analiz": "AI analizi eklenecek..."
                }
                haberler.append(haber)
        except:
            continue

    return haberler

def paylas():
    haberler = haberleri_cek()
    if not haberler:
        print("⚠️ Haber bulunamadı.")
        return

    for h in haberler:
        mesaj = f"🔎 *{h['mac']}*\n" \
                f"🧮 Oran: `{h['oran']}`\n🔗 [Detay]({h['link']})\n" \
                f"*Yorum:* {h['analiz']}"
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=mesaj, parse_mode="Markdown")
        time.sleep(2)

if __name__ == "__main__":
    print("🚀 Bot başlatıldı...")
    paylas()
