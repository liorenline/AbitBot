from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from data import SPECIALTIES_INFO, FAQ_DATA, CHOICE_SUBJECTS
from keyboards import (
    menu_kb,
    spec_kb,
    subject_kb,
    faq_categories_kb,
    get_faq_questions_kb,
    get_links_kb,
)

router = Router()

back_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="⬅️ Назад")]],
    resize_keyboard=True,
)

class ScoreForm(StatesGroup):
    choosing_spec = State()
    entering_ukr = State()
    entering_math = State()
    entering_history = State()
    choosing_subject = State()
    entering_choice = State()

class FAQState(StatesGroup):
    category = State()

def is_valid_score(text: str) -> bool:
    return text.isdigit() and 100 <= int(text) <= 200

def get_k4_max(info: dict) -> float:
    return max(info["к4"].values())

def calculate_kb(info, ukr, math, history, choice_subject, choice_score):
    k1 = info["к1"]
    k2 = info["к2"]
    k3 = info["к3"]
    k4 = info["к4"][choice_subject]
    k4_max = get_k4_max(info)
    gk = info.get("гк", 1.0)
    numerator = k1 * ukr + k2 * math + k3 * history + k4 * choice_score
    denominator = k1 + k2 + k3 + (k4_max + k4) / 2
    kb_base = numerator / denominator
    kb_final = min(kb_base * gk, 200)
    return {
        "kb_base": round(kb_base, 3),
        "kb_final": round(kb_final, 3),
        "k1": k1, "k2": k2, "k3": k3, "k4": k4,
        "k4_max": k4_max,
        "denominator": round(denominator, 3),
        "gk": gk,
    }

@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    name = message.from_user.first_name
    await message.answer(
        f"Привіт, {name}! 👋\n\n"
        "Я бот факультету прикладної математики та інформатики ЛНУ ім. Івана Франка.\n\n"
        "Допоможу розібратись зі спеціальностями, розрахувати конкурсний бал "
        "і відповісти на поширені запитання про вступ.\n\n"
        "Обирай розділ 👇",
        reply_markup=menu_kb,
        parse_mode="HTML"
    )

@router.message(F.text == "ℹ️ Про нас")
async def about(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "<b>Факультет прикладної математики та інформатики\n"
        "ЛНУ ім. Івана Франка</b>\n\n"
        "ФПМІ готує фахівців у галузі математики, інформатики, "
        "кібербезпеки та науки про дані.\n\n"
        "🎓 <b>Спеціальності:</b>\n"
        "• Середня освіта (Інформатика)\n"
        "• Прикладна математика\n"
        "• Комп'ютерні науки\n"
        "• Системний аналіз і науки про дані\n"
        "• Кібербезпека та захист інформації\n\n"
        "📍 Львів, вул. Університетська, 1\n"
        "🌐 <a href='https://ami.lnu.edu.ua/'>ami.lnu.edu.ua</a>\n"
        "📧 ami@lnu.edu.ua\n"
        "📞 <a href='https://ami.lnu.edu.ua/about/contacts/'>Контакти кафедр</a>",
        reply_markup=menu_kb,
        parse_mode="HTML"
    )

@router.message(F.text == "🔗 Корисні посилання")
async def useful_links(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "<b>Корисні посилання:</b>\n\n"
        "🎓 <a href='https://admission.lnu.edu.ua'>Сайт вступної кампанії</a>\n"
        "📚 <a href='https://ami.lnu.edu.ua/'>Сайт факультету</a>\n"
        "📊 <a href='https://abit-poisk.org.ua/'>Абіт-пошук</a>\n"
        "🏛 <a href='https://lnu.edu.ua/'>Сайт університету</a>\n"
        "🧮 <a href='https://osvita.ua/consultations/konkurs-ball/'>Розрахунок конкурсного балу</a>\n"
        "🗂 <a href='https://vstup.osvita.ua/'>Вступ.ОСВІТА.UA</a>\n"
        "📝 <a href='https://testportal.gov.ua/'>УЦОЯО</a>\n"
        "🔑 <a href='https://my.testportal.gov.ua/cabinet/login'>Кабінет учасника НМТ</a>\n"
        "📖 <a href='https://ami.lnu.edu.ua/academics/bachelor'>Навчальні плани бакалаврату ФПМІ</a>\n"
        "📜 <a href='https://testportal.gov.ua/vstupna-kampaniya-2026-oprylyudneno-poryadok-pryjomu-do-zakladiv-vyshhoyi-osvity/'>Порядок прийому до закладів вищої освіти</a>\n"
        "📞 <a href='https://admission.lnu.edu.ua/admission-board/contacts/'>Контакти приймальної комісії</a>\n",
    reply_markup=menu_kb,
        parse_mode="HTML"
    )

@router.message(F.text == "FAQ")
async def faq_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Оберіть категорію:", reply_markup=faq_categories_kb)

@router.message(StateFilter(None), F.text.in_(FAQ_DATA.keys()))
async def faq_category(message: Message, state: FSMContext):
    await state.set_state(FAQState.category)
    await state.update_data(category=message.text)
    await message.answer("Оберіть питання:", reply_markup=get_faq_questions_kb(message.text))

@router.message(FAQState.category, F.text == "⬅️ Назад")
async def faq_back_to_categories(message: Message, state: FSMContext):
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

@router.message(F.text == "⬅️ Назад")
async def back_to_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Оберіть розділ:", reply_markup=menu_kb)

@router.message(F.text == "Спеціальності")
async def specs(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Оберіть спеціальність:", reply_markup=spec_kb)

@router.message(StateFilter(None), F.text.in_(SPECIALTIES_INFO.keys()))
async def spec_info(message: Message, state: FSMContext):
    info = SPECIALTIES_INFO[message.text]
    careers = "\n".join(f"• {c}" for c in info["careers"])
    links = info["links"]

    partners_text = ""
    if info.get("partners"):
        partners_text = "\n\n🤝 <b>Партнери:</b>\n" + "\n".join(f"• {p}" for p in info["partners"])

    text = (
        f"<b>{message.text}</b>\n\n"
        f"🏫 {info['faculty']}\n\n"
        f"📖 <b>Про спеціальність:</b>\n{info['about']}\n\n"
        f"💼 <b>Кар'єра:</b>\n{careers}\n\n"
        f"💰 <b>Контракт:</b> {info['tuition']} грн/рік"
        f"{partners_text}"
    )

    coeff_text = "\n\n📊 <b>Коефіцієнти:</b>\n" + "\n".join(
        f"• {k}: {v}" for k, v in info["coefficients"].items()
    )

    links_text = (
        f"\n\n🔗 <b>Посилання:</b>\n"
        f"• <a href='{links['admission']}'>Вступ</a>\n"
        f"• <a href='{links['program']}'>Навчальна програма</a>\n"
        f"• <a href='{links['abitposhuk']}'>Абіт-пошук (рейтинг)</a>"
    )
    if "itcluster" in links:
        links_text += f"\n• <a href='{links['itcluster']}'>IT Cluster</a>"

    await message.answer(
        text + coeff_text + links_text,
        reply_markup=spec_kb,
        parse_mode="HTML"
    )

@router.message(F.text == "⬅️ Назад")
async def back_from_specs(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Оберіть розділ:", reply_markup=menu_kb)

@router.message(F.text == "Розрахунок балу")
async def score_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(ScoreForm.choosing_spec)
    await message.answer("Оберіть спеціальність для розрахунку:", reply_markup=spec_kb)

@router.message(ScoreForm.choosing_spec, F.text == "⬅️ Назад")
async def score_back_from_spec(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Оберіть розділ:", reply_markup=menu_kb)

@router.message(ScoreForm.choosing_spec, F.text.in_(SPECIALTIES_INFO.keys()))
async def score_chose_spec(message: Message, state: FSMContext):
    await state.update_data(spec=message.text)
    await state.set_state(ScoreForm.entering_ukr)
    await message.answer("Введіть бал з <b>Української мови</b> (100–200):", reply_markup=back_kb, parse_mode="HTML")

@router.message(ScoreForm.entering_ukr, F.text == "⬅️ Назад")
async def score_back_to_spec(message: Message, state: FSMContext):
    await state.set_state(ScoreForm.choosing_spec)
    await message.answer("Оберіть спеціальність:", reply_markup=spec_kb)

@router.message(ScoreForm.entering_ukr)
async def score_ukr(message: Message, state: FSMContext):
    if not is_valid_score(message.text):
        await message.answer("❌ Введіть число від 100 до 200:")
        return
    await state.update_data(ukr=int(message.text))
    await state.set_state(ScoreForm.entering_math)
    await message.answer("Введіть бал з <b>Математики</b> (100–200):", reply_markup=back_kb, parse_mode="HTML")

@router.message(ScoreForm.entering_math, F.text == "⬅️ Назад")
async def score_back_to_ukr(message: Message, state: FSMContext):
    await state.set_state(ScoreForm.entering_ukr)
    await message.answer("Введіть бал з <b>Української мови</b> (100–200):", reply_markup=back_kb, parse_mode="HTML")

@router.message(ScoreForm.entering_math)
async def score_math(message: Message, state: FSMContext):
    if not is_valid_score(message.text):
        await message.answer("❌ Введіть число від 100 до 200:")
        return
    await state.update_data(math=int(message.text))
    await state.set_state(ScoreForm.entering_history)
    await message.answer("Введіть бал з <b>Історії України</b> (100–200):", reply_markup=back_kb, parse_mode="HTML")

@router.message(ScoreForm.entering_history, F.text == "⬅️ Назад")
async def score_back_to_math(message: Message, state: FSMContext):
    await state.set_state(ScoreForm.entering_math)
    await message.answer("Введіть бал з <b>Математики</b> (100–200):", reply_markup=back_kb, parse_mode="HTML")

@router.message(ScoreForm.entering_history)
async def score_history(message: Message, state: FSMContext):
    if not is_valid_score(message.text):
        await message.answer("❌ Введіть число від 100 до 200:")
        return
    await state.update_data(history=int(message.text))
    await state.set_state(ScoreForm.choosing_subject)
    await message.answer("Оберіть <b>предмет за вибором</b>:", reply_markup=subject_kb, parse_mode="HTML")

@router.message(ScoreForm.choosing_subject, F.text == "⬅️ Назад")
async def score_back_to_history(message: Message, state: FSMContext):
    await state.set_state(ScoreForm.entering_history)
    await message.answer("Введіть бал з <b>Історії України</b> (100–200):", reply_markup=back_kb, parse_mode="HTML")

@router.message(ScoreForm.choosing_subject)
async def score_subject(message: Message, state: FSMContext):
    if message.text not in CHOICE_SUBJECTS:
        await message.answer("Оберіть предмет із клавіатури:")
        return
    await state.update_data(subject=message.text)
    await state.set_state(ScoreForm.entering_choice)
    await message.answer(f"Введіть бал з <b>{message.text}</b> (100–200):", reply_markup=back_kb, parse_mode="HTML")

@router.message(ScoreForm.entering_choice, F.text == "⬅️ Назад")
async def score_back_to_subject(message: Message, state: FSMContext):
    await state.set_state(ScoreForm.choosing_subject)
    await message.answer("Оберіть <b>предмет за вибором</b>:", reply_markup=subject_kb, parse_mode="HTML")

@router.message(ScoreForm.entering_choice)
async def score_choice(message: Message, state: FSMContext):
    if not is_valid_score(message.text):
        await message.answer("❌ Введіть число від 100 до 200:")
        return
    data = await state.get_data()
    await state.clear()

    info = SPECIALTIES_INFO[data["spec"]]
    result = calculate_kb(
        info,
        data["ukr"],
        data["math"],
        data["history"],
        data["subject"],
        int(message.text)
    )

    gk_text = f" × {result['gk']} (галузевий коефіцієнт)" if result["gk"] != 1.0 else ""

    await message.answer(
        f"📊 <b>Результат розрахунку</b>\n\n"
        f"Спеціальність: <b>{data['spec']}</b>\n\n"
        f"Українська мова: <b>{data['ukr']}</b> (К1={result['k1']})\n"
        f"Математика: <b>{data['math']}</b> (К2={result['k2']})\n"
        f"Історія України: <b>{data['history']}</b> (К3={result['k3']})\n"
        f"{data['subject']}: <b>{message.text}</b> (К4={result['k4']})\n\n"
        f"Знаменник: <b>{result['denominator']}</b>\n"
        f"Базовий КБ: <b>{result['kb_base']}</b>{gk_text}\n\n"
        f"✅ <b>Конкурсний бал: {result['kb_final']}</b>",
        reply_markup=menu_kb,
        parse_mode="HTML"
    )