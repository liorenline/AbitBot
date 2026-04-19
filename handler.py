from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

class ScoreForm(StatesGroup):
    choosing_subject = State()
    entering_score   = State()

menu_kb = ReplyKeyboardMarkup(
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

spec_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="A4.09 | Середня освіта (Інформатика)")],
        [KeyboardButton(text="F1 | Прикладна математика")],
        [KeyboardButton(text="F3 | Комп'ютерні науки")],
        [KeyboardButton(text="F4 | Системний аналіз і науки про дані")],
        [KeyboardButton(text="F5 | Кібербезпека та захист інформації")],
        [KeyboardButton(text="Назад")],
    ],
    resize_keyboard=True
)

subject_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Іноземна мова")],
        [KeyboardButton(text="Фізика")],
        [KeyboardButton(text="Українська мова та література")],
        [KeyboardButton(text="Біологія")],
        [KeyboardButton(text="Хімія")],
        [KeyboardButton(text="Географія")],
        [KeyboardButton(text="Назад")],
    ],
    resize_keyboard=True
)

SUBJECTS = {
    "Іноземна мова",
    "Фізика",
    "Українська мова та література",
    "Біологія",
    "Хімія",
    "Географія",
}

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("<b>Привіт!</b>", reply_markup=menu_kb)


@router.message(F.text == "Спеціальності")
async def handle_spec(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Оберіть спеціальність:", reply_markup=spec_kb)

@router.message(F.text == "Розрахунок балу")
async def handle_score(message: Message, state: FSMContext):
    await state.set_state(ScoreForm.choosing_subject)
    await message.answer("Оберіть предмет за вибором:", reply_markup=subject_kb)

@router.message(ScoreForm.choosing_subject)
async def handle_subject_chosen(message: Message, state: FSMContext):
    if message.text == "Назад":
        await state.clear()
        await message.answer("Головне меню:", reply_markup=menu_kb)
        return

    await state.update_data(subject=message.text)
    await state.set_state(ScoreForm.entering_score)
    await message.answer(
        f"Предмет: <b>{message.text}</b>\nВведіть ваш бал (100–200):"
    )

@router.message(ScoreForm.entering_score)
async def handle_score_entered(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введіть числове значення балу, наприклад: <b>185</b>")
        return

    score = int(message.text)
    if not (100 <= score <= 200):
        await message.answer("Бал має бути від 100 до 200. Спробуйте ще раз:")
        return

    data = await state.get_data()
    subject = data.get("subject", "—")

    await state.clear()
    await message.answer(
        f"Предмет: <b>{subject}</b>\n"
        f"Ваш бал: <b>{score}</b>\n\n"
        f"Розрахунок завершено!",
        reply_markup=menu_kb
    )

@router.message(F.text == "Корисні посилання")
async def handle_links(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("тут посилання")


@router.message(F.text == "FAQ")
async def handle_faq(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("тут відповіді")


@router.message(F.text == "Техпідтримка")
async def handle_support(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("тут техпідтримка")


@router.message(F.text == "Назад")
async def handle_back(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Головне меню:", reply_markup=menu_kb)