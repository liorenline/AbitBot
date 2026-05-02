import asyncio
import logging
import sys
import os
import threading
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from handler import router
from flask import Flask

load_dotenv()

TOKEN = os.environ["BOT_TOKEN"]

app = Flask(__name__)

@app.route("/")
def home():
    return " "

def run_flask():
    app.run(host="0.0.0.0", port=8080)

async def main():
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    threading.Thread(target=run_flask, daemon=True).start()
    asyncio.run(main())