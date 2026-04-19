from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

class ScoreForm(StatesGroup):
    choosing_spec = State()
    entering_ukr = State()
    entering_math = State()
    entering_history = State()
    choosing_subject = State()
    entering_choice = State()

COEFFICIENTS = {
    "A4.09 | Середня освіта (Інформатика)": {
        "К1": 0.35,
        "К2": 0.50,
        "К3": 0.25,
        "Іноземна мова": 0.30,
        "Фізика": 0.50,
        "Українська література": 0.30,
        "Біологія": 0.30,
        "Хімія": 0.40,
        "Географія": 0.25,
    },
    "F1 | Прикладна математика": {
        "К1": 0.30,
        "К2": 0.50,
        "К3": 0.20,
        "Іноземна мова": 0.30,
        "Фізика": 0.40,
        "Українська література": 0.20,
        "Біологія": 0.20,
        "Хімія": 0.30,
        "Географія": 0.20,
    },
    "F3 | Комп'ютерні науки": {
        "К1": 0.30,
        "К2": 0.50,
        "К3": 0.20,
        "Іноземна мова": 0.30,
        "Фізика": 0.40,
        "Українська література": 0.20,
        "Біологія": 0.20,
        "Хімія": 0.30,
        "Географія": 0.20,
    },
    "F4 | Системний аналіз і науки про дані": {
        "К1": 0.30,
        "К2": 0.50,
        "К3": 0.20,
        "Іноземна мова": 0.30,
        "Фізика": 0.40,
        "Українська література": 0.20,
        "Біологія": 0.20,
        "Хімія": 0.30,
        "Географія": 0.20,
    },
    "F5 | Кібербезпека та захист інформації": {
        "К1": 0.30,
        "К2": 0.50,
        "К3": 0.20,
        "Іноземна мова": 0.30,
        "Фізика": 0.40,
        "Українська література": 0.20,
        "Біологія": 0.20,
        "Хімія": 0.30,
        "Географія": 0.20,
    },
}

CHOICE_SUBJECTS = ["Іноземна мова", "Фізика", "Українська література", "Біологія", "Хімія", "Географія"]


def get_k4_max(coef: dict) -> float:
    return max(coef[s] for s in CHOICE_SUBJECTS)


def calculate_kb(coef: dict, ukr: int, math: int, history: int, choice_subject: str, choice_score: int) -> float:
    k1 = coef["К1"]
    k2 = coef["К2"]
    k3 = coef["К3"]
    k4 = coef[choice_subject]
    k4_max = get_k4_max(coef)

    numerator = k1 * ukr + k2 * math + k3 * history + k4 * choice_score
    denominator = k1 + k2 + k3 + (k4_max + k4) / 2

    kb = numerator / denominator
    return round(min(kb, 200), 3)


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
        [KeyboardButton(text="Українська література")],
        [KeyboardButton(text="Біологія")],
        [KeyboardButton(text="Хімія")],
        [KeyboardButton(text="Географія")],
        [KeyboardButton(text="Назад")],
    ],
    resize_keyboard=True
)


def is_valid_score(text: str) -> bool:
    return text.isdigit() and 100 <= int(text) <= 200


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
    await state.set_state(ScoreForm.choosing_spec)
    await message.answer("Оберіть спеціальність для розрахунку:", reply_markup=spec_kb)


@router.message(ScoreForm.choosing_spec)
async def handle_spec_chosen(message: Message, state: FSMContext):
    if message.text == "Назад":
        await state.clear()
        await message.answer("Головне меню:", reply_markup=menu_kb)
        return

    if message.text not in COEFFICIENTS:
        await message.answer("Оберіть спеціальність зі списку:")
        return

    await state.update_data(spec=message.text)
    await state.set_state(ScoreForm.entering_ukr)
    await message.answer("Введіть бал з <b>Української мови</b> (100–200):")


@router.message(ScoreForm.entering_ukr)
async def handle_ukr(message: Message, state: FSMContext):
    if not is_valid_score(message.text):
        await message.answer("Бал має бути числом від 100 до 200. Спробуйте ще раз:")
        return
    await state.update_data(ukr=int(message.text))
    await state.set_state(ScoreForm.entering_math)
    await message.answer("Введіть бал з <b>Математики</b> (100–200):")


@router.message(ScoreForm.entering_math)
async def handle_math(message: Message, state: FSMContext):
    if not is_valid_score(message.text):
        await message.answer("Бал має бути числом від 100 до 200. Спробуйте ще раз:")
        return
    await state.update_data(math=int(message.text))
    await state.set_state(ScoreForm.entering_history)
    await message.answer("Введіть бал з <b>Історії України</b> (100–200):")


@router.message(ScoreForm.entering_history)
async def handle_history(message: Message, state: FSMContext):
    if not is_valid_score(message.text):
        await message.answer("Бал має бути числом від 100 до 200. Спробуйте ще раз:")
        return
    await state.update_data(history=int(message.text))
    await state.set_state(ScoreForm.choosing_subject)
    await message.answer("Оберіть предмет за вибором:", reply_markup=subject_kb)


@router.message(ScoreForm.choosing_subject)
async def handle_subject_chosen(message: Message, state: FSMContext):
    if message.text == "Назад":
        await state.clear()
        await message.answer("Головне меню:", reply_markup=menu_kb)
        return

    if message.text not in CHOICE_SUBJECTS:
        await message.answer("Оберіть предмет зі списку:")
        return

    await state.update_data(choice_subject=message.text)
    await state.set_state(ScoreForm.entering_choice)
    await message.answer(f"Введіть бал з <b>{message.text}</b> (100–200):")


@router.message(ScoreForm.entering_choice)
async def handle_choice_score(message: Message, state: FSMContext):
    if not is_valid_score(message.text):
        await message.answer("Бал має бути числом від 100 до 200. Спробуйте ще раз:")
        return

    data = await state.get_data()
    spec = data["spec"]
    ukr = data["ukr"]
    math = data["math"]
    history = data["history"]
    choice_subject = data["choice_subject"]
    choice_score = int(message.text)

    coef = COEFFICIENTS[spec]
    k1 = coef["К1"]
    k2 = coef["К2"]
    k3 = coef["К3"]
    k4 = coef[choice_subject]
    k4_max = get_k4_max(coef)

    kb = calculate_kb(coef, ukr, math, history, choice_subject, choice_score)

    await state.clear()
    await message.answer(
        f"<b>Спеціальність:</b> {spec}\n\n"
        f"Українська мова:  {ukr} × {k1} = {ukr * k1:.2f}\n"
        f"Математика:       {math} × {k2} = {math * k2:.2f}\n"
        f"Історія України:  {history} × {k3} = {history * k3:.2f}\n"
        f"{choice_subject}: {choice_score} × {k4} = {choice_score * k4:.2f}\n\n"
        f"К4макс = {k4_max}\n"
        f"Знаменник = {k1} + {k2} + {k3} + ({k4_max} + {k4}) / 2 = {k1 + k2 + k3 + (k4_max + k4) / 2:.2f}\n\n"
        f"<b>Конкурсний бал: {kb:.3f}</b>\n\n"
        f"Регіональний та галузевий коефіцієнти застосовуються окремо залежно від вишу та пріоритету заяви.",
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