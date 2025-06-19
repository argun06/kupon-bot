import os
from dotenv import load_dotenv
import feedparser
from bs4 import BeautifulSoup
from telegram import Bot

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = Bot(token=TELEGRAM_BOT_TOKEN)

rss_url = "https://www.ntvspor.net/rss"
feed = feedparser.parse(rss_url)

gonderilen_basliklar = []

for entry in feed.entries[:5]:
    baslik = entry.title
    link = entry.link
    ozet = BeautifulSoup(entry.summary, "html.parser").get_text()

    if baslik not in gonderilen_basliklar:
        mesaj = f"📰 *{baslik}*\n\n📌 {ozet}\n🔗 [Habere Git]({link})"
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=mesaj, parse_mode="Markdown")
        gonderilen_basliklar.append(baslik)
