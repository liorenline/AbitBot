import logging
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["Спеціальності"],
        ["Допомога"],
        ["Корисні посилання"],
        ["Питання"],
        ["Розрахунок бала"]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Привіт, обери питання:",
        reply_markup=reply_markup
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Спеціальності":
        await update.message.reply_text("1")
    elif text == "Допомога":
        await update.message.reply_text("2")
    elif text == "Корисні посилання":
        await update.message.reply_text("3")
    elif text == "Питання":
        await update.message.reply_text("4")
    elif text == "Розрахунок бала":
        await update.message.reply_text("5")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, status))

app.run_polling()
