import os
import requests
import time
from dotenv import load_dotenv
from telegram import Bot

# Ortam değişkenlerini yükle
load_dotenv()

# Telegram ayarları
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)

# football-data.org API bilgileri (şimdilik tanımlı, kullanılabilir)
FOOTBALL_API_TOKEN = os.getenv("FOOTBALL_API_TOKEN")  # .env dosyasına eklersen kullanıma hazır

def get_today_matches():
    """Bugünkü maçları döndüren örnek fonksiyon (placeholder)."""
    # Burada API'den veri çekilecek
    # Şimdilik test amaçlı sahte veri döndürüyoruz
    return [
        {
            "mac": "Galatasaray vs Fenerbahçe",
            "oran": "2.10",
            "link": "https://www.mackolik.com",
            "analiz": "Ev sahibi son 5 maçta yenilmedi. Derbi stresli geçebilir."
        }
    ]

def paylas():
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
        bot.send_message(chat_id=CHAT_ID, text=mesaj, parse_mode="Markdown")
        time.sleep(2)

if __name__ == "__main__":
    print("🚀 Bot başlatıldı...")
    paylas()


