import os
import time
import requests
from datetime import datetime
from dotenv import load_dotenv
import openai

# ─── 1. LOAD YOUR ENVIRONMENT VARIABLES ────────────────────────────────────────
load_dotenv()  # if you have a local .env for testing

TELEGRAM_BOT_TOKEN   = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID     = os.getenv("TELEGRAM_CHAT_ID")
OPENAI_API_KEY       = os.getenv("OPENAI_API_KEY")
FOOTBALL_DATA_API    = os.getenv("FOOTBALL_DATA_API")  # your football-data.org token

if not all([TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, OPENAI_API_KEY, FOOTBALL_DATA_API]):
    raise RuntimeError("One or more required env vars are missing.")

openai.api_key = OPENAI_API_KEY

# ─── 2. FUNCTIONS ───────────────────────────────────────────────────────────────

def fetch_today_matches():
    """Fetch today's football matches from football-data.org."""
    today = datetime.utcnow().strftime("%Y-%m-%d")
    url = f"https://api.football-data.org/v2/matches?dateFrom={today}&dateTo={today}"
    headers = { "X-Auth-Token": FOOTBALL_DATA_API }
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json().get("matches", [])
    matches = []
    for m in data:
        home = m["homeTeam"]["name"]
        away = m["awayTeam"]["name"]
        matches.append({
            "home": home,
            "away": away,
        })
    return matches

def gpt_analysis(home, away):
    """Ask GPT for an expert analysis of this matchup."""
    prompt = (
        f"Sen bir futbol yorumcususun. Oyun öncesi analiz yap:\n\n"
        f"Maç: {home} vs {away}\n"
        f"İstatistikleri ve oranları göz önünde bulundurarak, takımların ",
        "son form durumunu, tahmini skoru ve kazanma yüzdesini kısaca açıkla."
    )
    try:
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return res.choices[0].message.content.strip()
    except Exception:
        return "Analiz alınamadı."

def send_telegram(text):
    """Send a message to the configured Telegram chat."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}
    r = requests.post(url, data=data, timeout=10)
    return r.status_code

def run_cycle():
    print("🚀 Başlıyor:", datetime.utcnow().isoformat(), "UTC")
    matches = fetch_today_matches()
    if not matches:
        print("⚠️ Bugün maç yok.")
        return

    for m in matches:
        home = m["home"]
        away = m["away"]
        analysis = gpt_analysis(home, away)
        message = (
            f"*{home}* vs *{away}*\n\n"
            f"🧠 *Analiz:*\n{analysis}"
        )
        print("📤 Gönderiliyor:", home, "vs", away)
        send_telegram(message)
        time.sleep(2)

# ─── 3. MAIN LOOP ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    while True:
        try:
            run_cycle()
        except Exception as e:
            print("‼️ Hata:", e)
        # Test için 5 dakikada bir; daha sonra 3600 (1 saat) yapabilirsiniz
        time.sleep(5 * 60)





