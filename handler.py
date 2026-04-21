from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from data import SPECIALTIES_INFO, FAQ_DATA
from keyboards import (
    menu_kb,
    spec_kb,
    subject_kb,
    faq_categories_kb,
    get_faq_questions_kb
)
router = Router()
# ======================
# STATES
# ======================
class ScoreForm(StatesGroup):
    choosing_spec = State()
    entering_ukr = State()
    entering_math = State()
    entering_history = State()
    choosing_subject = State()
    entering_choice = State()
class FAQState(StatesGroup):
    category = State()

@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Привіт 👋", reply_markup=menu_kb)

@router.message(F.text == "FAQ")
async def faq_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Оберіть категорію:", reply_markup=faq_categories_kb)

@router.message(F.text.in_(FAQ_DATA.keys()))
async def faq_category(message: Message, state: FSMContext):
    await state.set_state(FAQState.category)
    await state.update_data(category=message.text)
    await message.answer(
        "Оберіть питання:",
        reply_markup=get_faq_questions_kb(message.text)
    )

@router.message(FAQState.category, F.text == "⬅️ Назад")
async def faq_back(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Оберіть категорію:", reply_markup=faq_categories_kb)

@router.message(FAQState.category)
async def faq_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    category = data["category"]
    if message.text in FAQ_DATA[category]:
        await message.answer(
            f"<b>{message.text}</b>\n\n{FAQ_DATA[category][message.text]}",
            reply_markup=get_faq_questions_kb(category),
            parse_mode="HTML"
        )

@router.message(F.text == "Спеціальності")
async def specs(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Оберіть спеціальність:", reply_markup=spec_kb)