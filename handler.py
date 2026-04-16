from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())   #start
async def start(message: Message):
    await message.answer(
        "<b>Привіт!</b>\n"
        "Я бот для абітурієнтів 🎓\n\n"
        "Напиши щось або обери пункт меню (далі додаси кнопки)"
    )

@router.message()
async def echo(message: Message):
    await message.answer(
        f"Ти написав: <b>{message.text}</b>"
    )