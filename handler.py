from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Спеціальності", callback_data="spec")],
    [InlineKeyboardButton(text="Розрахунок балу", callback_data="calc")],
    [InlineKeyboardButton(text="FAQ", callback_data="faq")],
    [InlineKeyboardButton(text="Техпідтримка", callback_data="support")],
])

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "<b>Привіт!</b>",
        reply_markup=menu
    )