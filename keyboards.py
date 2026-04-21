from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data import FAQ_DATA

menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Спеціальності")],
        [KeyboardButton(text="Розрахунок балу")],
        [KeyboardButton(text="FAQ")],
        [KeyboardButton(text="🔗 Корисні посилання")],
        [KeyboardButton(text="ℹ️ Про нас")],
    ],
    resize_keyboard=True,
)

spec_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="A4.09 | Середня освіта (Інформатика)")],
        [KeyboardButton(text="F1 | Прикладна математика")],
        [KeyboardButton(text="F3 | Комп'ютерні науки")],
        [KeyboardButton(text="F4 | Data Science")],
        [KeyboardButton(text="F5 | Кібербезпека")],
        [KeyboardButton(text="Назад")],
    ],
    resize_keyboard=True,
)

subject_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=subj)] for subj in [
            "Іноземна мова",
            "Фізика",
            "Українська література",
            "Біологія",
            "Хімія",
            "Географія",
        ]
    ] + [[KeyboardButton(text="Назад")]],
    resize_keyboard=True,
)

faq_categories_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=cat)] for cat in FAQ_DATA.keys()
    ] + [[KeyboardButton(text="⬅️ Назад")]],
    resize_keyboard=True,
)

def get_faq_questions_kb(category: str):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=q)]
            for q in FAQ_DATA[category].keys()
        ] + [[KeyboardButton(text="⬅️ Назад")]],
        resize_keyboard=True,
    )

def get_links_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="⬅️ Назад")]],
        resize_keyboard=True,
    )