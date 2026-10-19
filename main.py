import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# CoinGecko IDs
COINS = {
    "btc": {"id": "bitcoin", "symbol": "BTC", "name": "Bitcoin"},
    "eth": {"id": "ethereum", "symbol": "ETH", "name": "Ethereum"},
    "sol": {"id": "solana", "symbol": "SOL", "name": "Solana"},
    "avax": {"id": "avalanche-2", "symbol": "AVAX", "name": "Avalanche"},
}

def get_prices(coin_ids: list[str]) -> dict:
    """Fetch prices from CoinGecko (free, no API key needed)"""
    ids = ",".join(coin_ids)
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd&include_24hr_change=true"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error fetching prices: {e}")
        return {}

def format_price(data: dict, coin_key: str) -> str:
    coin = COINS[coin_key]
    coin_data = data.get(coin["id"], {})
    price = coin_data.get("usd")
    change = coin_data.get("usd_24h_change")

    if price is None:
        return f"❌ {coin['symbol']}: Data unavailable"

    change_str = f"{change:+.2f}%" if change is not None else "N/A"
    emoji = "🟢" if change and change >= 0 else "🔴"

    return f"{emoji} **{coin['symbol']}** (${coin['name']})\n💰 ${price:,.4f}  |  24h: {change_str}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🚀 **Welcome to GEOKBot!**\n\n"
        "Live prices for BTC • ETH • SOL • AVAX\n\n"
        "Commands:\n"
        "/price or /all — Show all coins\n"
        "/btc  /eth  /sol  /avax — Single coin\n\n"
        "Made with ❤️ for fast crypto updates"
    )
    await update.message.reply_text(text, parse_mode="Markdown")

async def price_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ids = [c["id"] for c in COINS.values()]
    data = get_prices(ids)

    if not data:
        await update.message.reply_text("⚠️ Could not fetch prices. Please try again later.")
        return

    messages = [format_price(data, key) for key in COINS]
    text = "📊 **Live Crypto Prices**\n\n" + "\n\n".join(messages)
    await update.message.reply_text(text, parse_mode="Markdown")

async def price_single(update: Update, context: ContextTypes.DEFAULT_TYPE, coin_key: str):
    data = get_prices([COINS[coin_key]["id"]])
    if not data:
        await update.message.reply_text("⚠️ Could not fetch price. Please try again later.")
        return

    text = format_price(data, coin_key)
    await update.message.reply_text(text, parse_mode="Markdown")

async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await price_single(update, context, "btc")

async def eth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await price_single(update, context, "eth")

async def sol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await price_single(update, context, "sol")

async def avax(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await price_single(update, context, "avax")

def main():
    token = os.getenv(
8800269112:AAHN0lcoC6f5I0VguSKNTT0D_t0o1N5sBPM")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price_all))
    app.add_handler(CommandHandler("all", price_all))
    app.add_handler(CommandHandler("btc", btc))
    app.add_handler(CommandHandler("eth", eth))
    app.add_handler(CommandHandler("sol", sol))
    app.add_handler(CommandHandler("avax", avax))

    print("GEOKBot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()