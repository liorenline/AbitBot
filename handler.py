from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from data import SPECIALTIES_INFO, CHOICE_SUBJECTS, FAQ_DATA
from keyboards import menu_kb, spec_kb, subject_kb, faq_kb
from utils import calculate_kb, is_valid_score

router = Router()


class ScoreForm(StatesGroup):
    choosing_spec = State()
    entering_ukr = State()
    entering_math = State()
    entering_history = State()
    choosing_subject = State()
    entering_choice = State()


SPEC_NAMES = list(SPECIALTIES_INFO.keys())


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("<b>Привіт!</b>", reply_markup=menu_kb)


@router.message(F.text == "FAQ")
async def handle_faq(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Оберіть питання:", reply_markup=faq_kb)


@router.message(F.text.in_(FAQ_DATA.keys()))
async def handle_faq_answer(message: Message, state: FSMContext):
    await message.answer(
        f"<b>{message.text}</b>\n\n{FAQ_DATA[message.text]}",
        reply_markup=faq_kb,
    )


@router.message(F.text == "Спеціальності")
async def handle_spec_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Оберіть спеціальність:", reply_markup=spec_kb)


@router.message(StateFilter(None), F.text.in_(SPEC_NAMES))
async def handle_spec_info(message: Message, state: FSMContext):
    info = SPECIALTIES_INFO[message.text]

    coef_lines = "\n".join(
        f"  {name}: {val}" for name, val in info["coefficients"].items()
    )
    careers_lines = "\n".join(f"  • {c}" for c in info["careers"])
    partners_lines = "\n".join(f"  • {p}" for p in info.get("partners", []))

    tuition = info["tuition"]
    tuition_formatted = f"{tuition:,}".replace(",", "\u00a0")

    link_admission = info["links"]["admission"]
    link_program = info["links"]["program"]
    link_itcluster = info["links"].get("itcluster", "")
    link_abitposhuk = info["links"].get("abitposhuk", "")

    links_block = (
        f"  🔗 Сторінка вступу: {link_admission}\n"
        f"  🔗 Освітня програма: {link_program}"
    )

    if link_itcluster:
        links_block += f"\n  🔗 IT Cluster: {link_itcluster}"
    if link_abitposhuk:
        links_block += f"\n  🔗 АбітПошук: {link_abitposhuk}"

    text = (
        f"<b>{message.text}</b>\n"
        f"📚 Факультет: {info['faculty']}\n\n"
        f"<b>Про спеціальність:</b>\n{info['about']}\n\n"
        f"<b>Ким можна працювати:</b>\n{careers_lines}\n\n"
    )

    if partners_lines:
        text += f"<b>Партнери:</b>\n{partners_lines}\n\n"

    text += (
        f"<b>Вартість контракту (2025/2026):</b> {tuition_formatted} грн/рік\n\n"
        f"<b>Вагові коефіцієнти НМТ:</b>\n{coef_lines}\n\n"
        f"<b>Посилання:</b>\n{links_block}"
    )

    await message.answer(text, reply_markup=spec_kb)


# 🔴 ВСЯ ЛОГІКА РОЗРАХУНКУ ТАКА САМА ЯК У ТЕБЕ (З ВАЛІДАЦІЄЮ)

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

    if message.text not in SPECIALTIES_INFO:
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
async def handle_subject(message: Message, state: FSMContext):
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

    await state.update_data(choice_score=int(message.text))

    data = await state.get_data()

    r = calculate_kb(
        SPECIALTIES_INFO[data["spec"]],
        data["ukr"],
        data["math"],
        data["history"],
        data["choice_subject"],
        data["choice_score"],
    )

    await state.clear()

    await message.answer(
        f"<b>Конкурсний бал: {r['kb_final']}</b>",
        reply_markup=menu_kb,
    )


@router.message(F.text == "Назад")
async def handle_back(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Головне меню:", reply_markup=menu_kb)