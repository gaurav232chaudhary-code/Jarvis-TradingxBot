import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API = f"https://api.telegram.org/bot{TOKEN}"

MARKETS = {
    "BTC": "Bitcoin",
    "ETH": "Ethereum",
    "SOL": "Solana",
    "GOLD": "Gold",
    "NIFTY": "NIFTY 50",
    "SENSEX": "SENSEX",
    "BANKNIFTY": "BANK NIFTY",
}

def send(chat_id, text):
    requests.post(
        f"{API}/sendMessage",
        json={"chat_id": chat_id, "text": text}
    )

def handle(chat_id, text):
    cmd = text.strip().lower()

    if cmd == "/start":
        send(chat_id,
             "🤖 JARVIS TRADING AI\n\n"
             "Markets: BTC • ETH • SOL • GOLD • NIFTY • SENSEX • BANKNIFTY\n\n"
             "Commands:\n"
             "/markets\n"
             "/signal BTC\n"
             "/signal ETH\n"
             "/signal NIFTY\n"
             "/signal GOLD")
        return

    if cmd == "/markets":
        send(chat_id, "📊 Supported Markets:\n\n" +
             "\n".join(f"• {k} — {v}" for k, v in MARKETS.items()))
        return

    if cmd.startswith("/signal"):
        parts = cmd.split()
        symbol = parts[1].upper() if len(parts) > 1 else ""
        if symbol not in MARKETS:
            send(chat_id, "❌ Market આપો:\n/signal BTC\n/signal ETH\n/signal SOL\n/signal GOLD\n/signal NIFTY\n/signal SENSEX\n/signal BANKNIFTY")
            return

        send(chat_id,
             f"🧠 JARVIS ANALYSIS\n\n"
             f"Market: {MARKETS[symbol]}\n"
             f"Symbol: {symbol}\n\n"
             f"Trading Math: Initializing...\n"
             f"G-Theta: Initializing...\n"
             f"Signal: WAIT\n\n"
             f"⚠️ Live market-data engine હજુ જોડવાનું બાકી છે.")
        return

    send(chat_id, "🤖 JARVIS: /markets અથવા /signal BTC વાપરો.")

def main():
    if not TOKEN:
        print("ERROR: TELEGRAM_BOT_TOKEN missing in .env")
        return

    print("JARVIS Trading Bot ONLINE")

    offset = None
    while True:
        try:
            r = requests.get(
                f"{API}/getUpdates",
                params={"timeout": 30, "offset": offset},
                timeout=35
            ).json()

            for update in r.get("result", []):
                offset = update["update_id"] + 1
                msg = update.get("message", {})
                chat_id = msg.get("chat", {}).get("id")
                text = msg.get("text", "")
                if chat_id and text:
                    handle(chat_id, text)

        except Exception as e:
            print("ERROR:", e)

if __name__ == "__main__":
    main()
