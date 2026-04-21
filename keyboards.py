from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data import FAQ_DATA

menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Спеціальності")],
        [KeyboardButton(text="Розрахунок балу")],
        [KeyboardButton(text="Корисні посилання")],
        [KeyboardButton(text="FAQ")],
        [KeyboardButton(text="Про нас")],
        [KeyboardButton(text="Техпідтримка")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Оберіть пункт меню...",
)

spec_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="A4.09 | Середня освіта (Інформатика)")],
        [KeyboardButton(text="F1 | Прикладна математика")],
        [KeyboardButton(text="F3 | Комп'ютерні науки")],
        [KeyboardButton(text="F4 | Системний аналіз і науки про дані")],
        [KeyboardButton(text="F5 | Кібербезпека та захист інформації")],
        [KeyboardButton(text="Назад")],
    ],
    resize_keyboard=True,
)

subject_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Іноземна мова")],
        [KeyboardButton(text="Фізика")],
        [KeyboardButton(text="Українська література")],
        [KeyboardButton(text="Біологія")],
        [KeyboardButton(text="Хімія")],
        [KeyboardButton(text="Географія")],
        [KeyboardButton(text="Назад")],
    ],
    resize_keyboard=True,
)

faq_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=q)] for q in FAQ_DATA.keys()] + [[KeyboardButton(text="Назад")]],
    resize_keyboard=True,
)