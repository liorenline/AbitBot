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


CHOICE_SUBJECTS = [
    "Іноземна мова",
    "Фізика",
    "Українська література",
    "Біологія",
    "Хімія",
    "Географія",
]

SPECIALTIES_INFO = {
    "A4.09 | Середня освіта (Інформатика)": {
        "url": "https://admission.lnu.edu.ua/specialization/informatics-education/",
        "faculty": "Факультет прикладної математики та інформатики",
        "about": (
            "Спеціальність готує вчителів інформатики для закладів середньої освіти. "
            "Студенти поєднують педагогічну підготовку з глибокими знаннями з інформатики, "
            "програмування та математики. Навчання охоплює методику викладання, алгоритмізацію, "
            "бази даних та сучасні освітні технології."
        ),
        "careers": [
            "Вчитель інформатики",
            "Викладач закладу фахової передвищої освіти",
            "Методист із інформатики",
            "Інженер-програміст",
            "Фахівець з інформаційних технологій",
        ],
        "partners": [],
        "links": {
            "admission": "https://admission.lnu.edu.ua/specialization/informatics-education/",
            "program": "https://ami.lnu.edu.ua/academics/bachelor/curriculum-education",
            "abitposhuk": "https://abit-poisk.org.ua/rate2025/direction/1497643",
        },
        "tuition": 39790,
        "coefficients": {
            "Українська мова (К1)": 0.35,
            "Математика (К2)": 0.50,
            "Історія України (К3)": 0.25,
            "Іноземна мова (К4)": 0.30,
            "Фізика (К4)": 0.50,
            "Українська література (К4)": 0.30,
            "Біологія (К4)": 0.30,
            "Хімія (К4)": 0.40,
            "Географія (К4)": 0.25,
        },
        "к1": 0.35,
        "к2": 0.50,
        "к3": 0.25,
        "к4": {
            "Іноземна мова": 0.30,
            "Фізика": 0.50,
            "Українська література": 0.30,
            "Біологія": 0.30,
            "Хімія": 0.40,
            "Географія": 0.25,
        },
        "гк": 1.02,
    },
    "F1 | Прикладна математика": {
        "url": "https://admission.lnu.edu.ua/specialization/applied-mathematics/",
        "faculty": "Факультет прикладної математики та інформатики",
        "about": (
            "Спеціальність формує фахівців, здатних застосовувати сучасні математичні методи "
            "та інформаційні технології для побудови й обслуговування комп'ютеризованих систем "
            "у різних галузях науки і господарства. Студенти набувають глибокі знання з "
            "математичного аналізу, теорії ймовірностей, математичного моделювання та програмування."
        ),
        "careers": [
            "Математик-аналітик",
            "Розробник програмного забезпечення",
            "Data Scientist / аналітик даних",
            "Науковець у НДІ",
            "Фахівець в ІТ-компаніях",
        ],
        "partners": [],
        "links": {
            "admission": "https://admission.lnu.edu.ua/specialization/applied-mathematics/",
            "program": "https://ami.lnu.edu.ua/academics/bachelor/curriculum-applied-mathematics",
            "abitposhuk": "https://abit-poisk.org.ua/rate2025/direction/1480776",
        },
        "tuition": 45150,
        "coefficients": {
            "Українська мова (К1)": 0.30,
            "Математика (К2)": 0.50,
            "Історія України (К3)": 0.20,
            "Іноземна мова (К4)": 0.30,
            "Фізика (К4)": 0.40,
            "Українська література (К4)": 0.20,
            "Біологія (К4)": 0.20,
            "Хімія (К4)": 0.30,
            "Географія (К4)": 0.20,
        },
        "к1": 0.30,
        "к2": 0.50,
        "к3": 0.20,
        "к4": {
            "Іноземна мова": 0.30,
            "Фізика": 0.40,
            "Українська література": 0.20,
            "Біологія": 0.20,
            "Хімія": 0.30,
            "Географія": 0.20,
        },
    },
    "F3 | Комп'ютерні науки": {
        "url": "https://admission.lnu.edu.ua/specialization/informatics/",
        "faculty": "Факультет прикладної математики та інформатики",
        "about": (
            "Освітня програма «Інформатика» готує спеціалістів у сфері комп'ютерних наук. "
            "Студенти вивчають математичні моделі, алгоритми, методи проєктування та розробки "
            "програмних систем, бази даних і сучасні платформи програмування. "
            "Програма складена відповідно до міжнародних рекомендацій Computer Science Curricula "
            "від ACM та IEEE Computer Society."
        ),
        "careers": [
            "Інженер-програміст / розробник ПЗ",
            "Адміністратор баз даних",
            "Архітектор рішень",
            "Тестувальник / QA Engineer",
            "Фахівець з ІТ та інформаційних систем",
        ],
        "partners": [
            "Lviv IT Cluster: https://itcluster.lviv.ua/",
        ],
        "links": {
            "admission": "https://admission.lnu.edu.ua/specialization/informatics/",
            "program": "https://ami.lnu.edu.ua/academics/bachelor/curriculum-computer-sciences",
            "itcluster": "https://itcluster.lviv.ua/",
            "abitposhuk": "https://abit-poisk.org.ua/rate2025/direction/1481286",
        },
        "tuition": 66755,
        "coefficients": {
            "Українська мова (К1)": 0.30,
            "Математика (К2)": 0.50,
            "Історія України (К3)": 0.20,
            "Іноземна мова (К4)": 0.30,
            "Фізика (К4)": 0.40,
            "Українська література (К4)": 0.20,
            "Біологія (К4)": 0.20,
            "Хімія (К4)": 0.30,
            "Географія (К4)": 0.20,
        },
        "к1": 0.30,
        "к2": 0.50,
        "к3": 0.20,
        "к4": {
            "Іноземна мова": 0.30,
            "Фізика": 0.40,
            "Українська література": 0.20,
            "Біологія": 0.20,
            "Хімія": 0.30,
            "Географія": 0.20,
        },
    },
    "F4 | Системний аналіз і науки про дані": {
        "url": "https://admission.lnu.edu.ua/specialization/system-analisys/",
        "faculty": "Факультет прикладної математики та інформатики",
        "about": (
            "Освітня програма «Data Science» готує фахівців для роботи з даними: збір, структурування, "
            "аналіз та моделювання. Студенти навчаються застосовувати методи машинного навчання "
            "та штучного інтелекту до реальних задач. Програма розроблена спільно з ІТ-спеціалістами "
            "провідних компаній Львівського ІТ Кластера, навчання побудовано за принципом роботи "
            "в ІТ-компанії."
        ),
        "careers": [
            "Data Scientist",
            "Data Analyst",
            "Data Engineer",
            "Machine Learning Engineer",
            "Data Modeler",
        ],
        "partners": [
            "Lviv IT Cluster (програма Data Science): https://itcluster.lviv.ua/ds_lnu/",
        ],
        "links": {
            "admission": "https://admission.lnu.edu.ua/specialization/system-analisys/",
            "program": "https://ami.lnu.edu.ua/academics/bachelor/curriculum-system-analysis",
            "itcluster": "https://itcluster.lviv.ua/ds_lnu/",
            "abitposhuk": "https://abit-poisk.org.ua/rate2025/direction/1444601",
        },
        "tuition": 45150,
        "coefficients": {
            "Українська мова (К1)": 0.30,
            "Математика (К2)": 0.50,
            "Історія України (К3)": 0.20,
            "Іноземна мова (К4)": 0.30,
            "Фізика (К4)": 0.40,
            "Українська література (К4)": 0.20,
            "Біологія (К4)": 0.20,
            "Хімія (К4)": 0.30,
            "Географія (К4)": 0.20,
        },
        "к1": 0.30,
        "к2": 0.50,
        "к3": 0.20,
        "к4": {
            "Іноземна мова": 0.30,
            "Фізика": 0.40,
            "Українська література": 0.20,
            "Біологія": 0.20,
            "Хімія": 0.30,
            "Географія": 0.20,
        },
    },
    "F5 | Кібербезпека та захист інформації": {
        "url": "https://admission.lnu.edu.ua/specialization/cybersecurity/",
        "faculty": "Факультет прикладної математики та інформатики",
        "about": (
            "Програма «Кібербезпека» готує висококваліфікованих фахівців із захисту даних та "
            "інформаційних систем. Студенти вчаться виявляти вразливості, відстежувати кіберзагрози "
            "та розробляти стратегії захисту. Програму розроблено спільно з ІТ-спеціалістами "
            "провідних компаній Львівського ІТ Кластера, студенти створюють власні проєкти "
            "і запускають стартапи під менторством досвідчених практиків."
        ),
        "careers": [
            "SOC Analyst / Intrusion Detection",
            "Penetration Tester",
            "Vulnerability Researcher",
            "Cloud Security Analyst",
            "Cyber Security Analyst",
            "Forensics Expert",
            "Incident Response Team Member",
        ],
        "partners": [
            "Lviv IT Cluster (програма Кібербезпека): https://itcluster.lviv.ua/cybersecurity_lnu/",
        ],
        "links": {
            "admission": "https://admission.lnu.edu.ua/specialization/cybersecurity/",
            "program": "https://ami.lnu.edu.ua/academics/bachelor/curriculum-cybersecurity",
            "itcluster": "https://itcluster.lviv.ua/cybersecurity_lnu/",
            "abitposhuk": "https://abit-poisk.org.ua/rate2025/direction/1479637",
        },
        "tuition": 66755,
        "coefficients": {
            "Українська мова (К1)": 0.30,
            "Математика (К2)": 0.50,
            "Історія України (К3)": 0.20,
            "Іноземна мова (К4)": 0.30,
            "Фізика (К4)": 0.40,
            "Українська література (К4)": 0.20,
            "Біологія (К4)": 0.20,
            "Хімія (К4)": 0.30,
            "Географія (К4)": 0.20,
        },
        "к1": 0.30,
        "к2": 0.50,
        "к3": 0.20,
        "к4": {
            "Іноземна мова": 0.30,
            "Фізика": 0.40,
            "Українська література": 0.20,
            "Біологія": 0.20,
            "Хімія": 0.30,
            "Географія": 0.20,
        },
    },
}

SPEC_NAMES = list(SPECIALTIES_INFO.keys())


def get_k4_max(info: dict) -> float:
    return max(info["к4"].values())


def calculate_kb(
    info: dict,
    ukr: int,
    math: int,
    history: int,
    choice_subject: str,
    choice_score: int,
    rk: float = 1.04,
) -> dict:

    k1 = info["к1"]
    k2 = info["к2"]
    k3 = info["к3"]
    k4 = info["к4"][choice_subject]
    k4_max = get_k4_max(info)
    gk = info.get("гк", 1.0)

    numerator = k1 * ukr + k2 * math + k3 * history + k4 * choice_score
    denominator = k1 + k2 + k3 + (k4_max + k4) / 2
    kb_base = numerator / denominator
    kb_final = min(kb_base * rk * gk, 200)

    return {
        "kb_base": round(kb_base, 3),
        "kb_final": round(kb_final, 3),
        "k1": k1,
        "k2": k2,
        "k3": k3,
        "k4": k4,
        "k4_max": k4_max,
        "denominator": round(denominator, 3),
        "rk": rk,
        "gk": gk,
    }


menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Спеціальності")],
        [KeyboardButton(text="Розрахунок балу")],
        [KeyboardButton(text="Корисні посилання")],
        [KeyboardButton(text="FAQ")],
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


def is_valid_score(text: str) -> bool:
    return text.isdigit() and 100 <= int(text) <= 200


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("<b>Привіт!</b>", reply_markup=menu_kb)


@router.message(F.text == "Спеціальності")
async def handle_spec_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Оберіть спеціальність:", reply_markup=spec_kb)


@router.message(F.text.in_(SPEC_NAMES))
async def handle_spec_info(message: Message, state: FSMContext):
    info = SPECIALTIES_INFO[message.text]
    coef_lines = "\n".join(
        f"  {name}: {val}" for name, val in info["coefficients"].items()
    )
    careers_lines = "\n".join(f"  \u2022 {c}" for c in info["careers"])
    partners_lines = "\n".join(f"  \u2022 {p}" for p in info.get("partners", []))
    tuition = info["tuition"]
    tuition_formatted = f"{tuition:,}".replace(",", "\u00a0")

    link_admission = info["links"]["admission"]
    link_program = info["links"]["program"]
    link_itcluster = info["links"].get("itcluster", "")
    link_abitposhuk = info["links"].get("abitposhuk", "")

    links_block = (
        f"  \U0001f517 Сторінка вступу: {link_admission}\n"
        f"  \U0001f517 Освітня програма: {link_program}"
    )
    if link_itcluster:
        links_block += f"\n  \U0001f517 IT Cluster: {link_itcluster}"
    if link_abitposhuk:
        links_block += f"\n  \U0001f517 АбітПошук: {link_abitposhuk}"

    text = (
        f"<b>{message.text}</b>\n"
        f"\U0001f4da Факультет: {info['faculty']}\n\n"
        f"<b>Про спеціальність:</b>\n{info['about']}\n\n"
        f"<b>Ким можна працювати:</b>\n{careers_lines}\n\n"
    )
    if partners_lines:
        text += f"<b>Партнери:</b>\n{partners_lines}\n\n"
    text += (
        f"<b>Вартість контракту (2025/2026):</b> {tuition_formatted}\u00a0грн/рік\n\n"
        f"<b>Вагові коефіцієнти НМТ:</b>\n{coef_lines}\n\n"
        f"<b>Посилання:</b>\n{links_block}"
    )
    await message.answer(text, reply_markup=spec_kb)


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
    await state.update_data(choice_score=int(message.text))
    await finish_calculation(message, state)


async def finish_calculation(message: Message, state: FSMContext):
    data = await state.get_data()
    spec = data["spec"]
    ukr = data["ukr"]
    math = data["math"]
    history = data["history"]
    choice_subject = data["choice_subject"]
    choice_score = data["choice_score"]

    info = SPECIALTIES_INFO[spec]
    r = calculate_kb(info, ukr, math, history, choice_subject, choice_score)

    await state.clear()

    # Рядок з ГК показуємо лише якщо він відрізняється від 1.0
    gk_line = f"× ГК ({r['gk']}) = " if r["gk"] != 1.0 else ""

    await message.answer(
        f"<b>Спеціальність:</b> {spec}\n\n"
        f"Українська мова:  {ukr} × {r['k1']} = {ukr * r['k1']:.2f}\n"
        f"Математика:       {math} × {r['k2']} = {math * r['k2']:.2f}\n"
        f"Історія України:  {history} × {r['k3']} = {history * r['k3']:.2f}\n"
        f"{choice_subject}: {choice_score} × {r['k4']} = {choice_score * r['k4']:.2f}\n\n"
        f"К4макс = {r['k4_max']}\n"
        f"Знаменник = {r['denominator']}\n\n"
        f"Базовий КБ = {r['kb_base']}\n"
        f"× РК ({r['rk']}) {gk_line}= <b>Конкурсний бал: {r['kb_final']}</b>",
        reply_markup=menu_kb,
    )

@router.message(F.text == "Корисні посилання")
async def handle_links(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🔗 <b>Корисні посилання</b>\n\n"
        "🎓 <b>Університет</b>\n"
        "• Сайт ЛНУ імені Івана Франка: https://lnu.edu.ua\n"
        "• Сайт ФПМІ: https://ami.lnu.edu.ua\n\n"
        "📋 <b>Вступ</b>\n"
        "• Вступна кампанія ЛНУ: https://admission.lnu.edu.ua\n"
        "• Спеціальності ФПМІ: https://admission.lnu.edu.ua/applicants/speciality-searching/?unit=ami\n"
        "• АбітПошук ЛНУ: https://abit-poisk.org.ua/rate2025/univer/282#google_vignette\n"
        "• Кабінет вступника (ЄДЕБО): https://vstup.edbo.gov.ua\n"
        "• Вагові коефіцієнти НМТ: https://osvita.ua/consultations/bachelor/10025/\n"
        "• Калькулятор конкурсного балу: https://osvita.ua/consultations/konkurs-ball/\n\n"
        "• Email приймальної комісії: pkunivlv@lnu.edu.ua\n"
        "🤝 <b>Партнери факультету</b>\n"
        "• Lviv IT Cluster: https://itcluster.lviv.ua\n"
        "• GlobalLogic: https://www.globallogic.com/ua\n"
        "• EPAM: https://careers.epam.ua\n"
        "• ELEKS: https://eleks.com/uk\n"
        "• N-iX: https://www.n-ix.com\n\n",
        reply_markup=menu_kb
    )

@router.message(F.text == "FAQ")
async def handle_faq(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "<b>Часті запитання:</b>\n\n"
        "<b>Який предмет за вибором вигідніший?</b>\n"
        "Для A4.09 — Фізика (К4=0.50). "
        "Для F1/F3/F4/F5 — Фізика (К4=0.40). "
        "Але важливіший реальний бал: вища оцінка з «слабшого» предмета може дати кращий КБ.\n\n"
        "<b>Скільки коштує навчання (контракт, 2025/2026)?</b>\n"
        "• A4.09 Середня освіта (Інформатика) — 39\u00a0790\u00a0грн/рік\n"
        "• F1 Прикладна математика — 45\u00a0150\u00a0грн/рік\n"
        "• F4 Системний аналіз і науки про дані — 45\u00a0150\u00a0грн/рік\n"
        "• F3 Комп'ютерні науки — 66\u00a0755\u00a0грн/рік\n"
        "• F5 Кібербезпека та захист інформації — 66\u00a0755\u00a0грн/рік",
        reply_markup=menu_kb,
    )

@router.message(F.text == "Техпідтримка")
async def handle_support(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Якщо виникли питання або помилки — напишіть адміністратору.",
        reply_markup=menu_kb,
    )

@router.message(F.text == "Назад")
async def handle_back(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Головне меню:", reply_markup=menu_kb)