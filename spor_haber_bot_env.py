import os
import asyncio
from dotenv import load_dotenv
from telegram import Bot

# Ortam değişkenlerini yükle (.env veya Render ortamı)
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)

def get_today_matches():
    return [
        {
            "mac": "Galatasaray vs Fenerbahçe",
            "oran": "2.10",
            "link": "https://www.mackolik.com",
            "analiz": "Ev sahibi son 5 maçta yenilmedi. Derbi stresli geçebilir."
        }
    ]

async def paylas():
    haberler = get_today_matches()

    if not haberler:
        print("⚠️ Haber bulunamadı.")
        return

    for h in haberler:
        mesaj = (
            f"🔍 *{h['mac']}*\n"
            f"📊 Oran: `{h['oran']}`\n🔗 [Detay]({h['link']})\n"
            f"🧠 *Yorum:* {h['analiz']}"
        )
        await bot.send_message(chat_id=CHAT_ID, text=mesaj, parse_mode="Markdown")
        await asyncio.sleep(2)

if __name__ == "__main__":
    print("🚀 Bot başlatıldı...")
    asyncio.run(paylas())



