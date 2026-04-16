from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

router = Router()

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Спеціальності")],
        [KeyboardButton(text="Розрахунок балу")],
        [KeyboardButton(text="Корисні посилання")],
        [KeyboardButton(text="FAQ")],
        [KeyboardButton(text="Техпідтримка")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Оберіть пункт меню..."
)

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "<b>Привіт!</b>",
        reply_markup=menu
    )