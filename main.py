from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI(title="Олимпиады 2026-2027")

# ============ ОЛИМПИАДЫ И КОНКУРСЫ ============
OLYMPIADS = [
    {"name": "Всероссийская олимпиада школьников (ВсОШ) — школьный этап", "type": "Олимпиада", "subject": "Все предметы", "grades": "4–11", "date": "01.09.2026 – 31.10.2026", "level": "Всероссийская", "url": "https://olimpiada.ru"},
    {"name": "ВсОШ — муниципальный этап", "type": "Олимпиада", "subject": "Все предметы", "grades": "7–11", "date": "01.11.2026 – 25.12.2026", "level": "Всероссийская", "url": "https://olimpiada.ru"},
    {"name": "ВсОШ — региональный этап", "type": "Олимпиада", "subject": "Все предметы", "grades": "9–11", "date": "10.01.2027 – 28.02.2027", "level": "Всероссийская", "url": "https://olimpiada.ru"},
    {"name": "ВсОШ — заключительный этап", "type": "Олимпиада", "subject": "Все предметы", "grades": "9–11", "date": "15.03.2027 – 30.04.2027", "level": "Всероссийская", "url": "https://olimpiada.ru"},
    {"name": "Олимпиада «Ломоносов» по математике", "type": "Олимпиада", "subject": "Математика", "grades": "5–11", "date": "01.10.2026 – 31.03.2027", "level": "Высший уровень", "url": "https://olymp.msu.ru"},
    {"name": "Турнир городов", "type": "Олимпиада", "subject": "Математика", "grades": "8–11", "date": "11.10.2026, 14.02.2027", "level": "Высший уровень", "url": "https://www.turgor.ru"},
    {"name": "Олимпиада «Высшая проба» по математике", "type": "Олимпиада", "subject": "Математика", "grades": "7–11", "date": "01.11.2026 – 28.02.2027", "level": "Высший уровень", "url": "https://olymp.hse.ru"},
    {"name": "Московская математическая олимпиада", "type": "Олимпиада", "subject": "Математика", "grades": "6–11", "date": "15.02.2027 – 20.03.2027", "level": "Высший уровень", "url": "https://olympiads.mccme.ru"},
    {"name": "Олимпиада «Физтех» по математике", "type": "Олимпиада", "subject": "Математика", "grades": "8–11", "date": "01.10.2026 – 31.03.2027", "level": "Высший уровень", "url": "https://olymp.mipt.ru"},
    {"name": "Олимпиада «Физтех» по физике", "type": "Олимпиада", "subject": "Физика", "grades": "8–11", "date": "01.10.2026 – 31.03.2027", "level": "Высший уровень", "url": "https://olymp.mipt.ru"},
    {"name": "Олимпиада «Ломоносов» по физике", "type": "Олимпиада", "subject": "Физика", "grades": "7–11", "date": "01.10.2026 – 31.03.2027", "level": "Высший уровень", "url": "https://olymp.msu.ru"},
    {"name": "Олимпиада «Росатом» по физике", "type": "Олимпиада", "subject": "Физика", "grades": "7–11", "date": "01.11.2026 – 31.03.2027", "level": "Высший уровень", "url": "https://mephi.ru"},
    {"name": "Московская олимпиада школьников по физике", "type": "Олимпиада", "subject": "Физика", "grades": "7–11", "date": "01.12.2026 – 31.03.2027", "level": "Высший уровень", "url": "https://mos.olimpiada.ru"},
    {"name": "Олимпиада «Высшая проба» по информатике", "type": "Олимпиада", "subject": "Информатика", "grades": "9–11", "date": "01.11.2026 – 28.02.2027", "level": "Высший уровень", "url": "https://olymp.hse.ru"},
    {"name": "Олимпиада «Физтех» по информатике", "type": "Олимпиада", "subject": "Информатика", "grades": "9–11", "date": "01.10.2026 – 31.03.2027", "level": "Высший уровень", "url": "https://olymp.mipt.ru"},
    {"name": "Открытая олимпиада по программированию", "type": "Олимпиада", "subject": "Информатика", "grades": "5–11", "date": "01.10.2026 – 31.03.2027", "level": "Высший уровень", "url": "https://olimpiada.ru"},
    {"name": "Олимпиада «Технокубок»", "type": "Олимпиада", "subject": "Информатика", "grades": "8–11", "date": "01.10.2026 – 31.03.2027", "level": "Повышенный уровень", "url": "https://technocup.mail.ru"},
    {"name": "Олимпиада «Высшая проба» по химии", "type": "Олимпиада", "subject": "Химия", "grades": "9–11", "date": "01.11.2026 – 28.02.2027", "level": "Высший уровень", "url": "https://olymp.hse.ru"},
    {"name": "Московская олимпиада школьников по химии", "type": "Олимпиада", "subject": "Химия", "grades": "8–11", "date": "01.12.2026 – 31.03.2027", "level": "Высший уровень", "url": "https://mos.olimpiada.ru"},
    {"name": "Олимпиада «Ломоносов» по химии", "type": "Олимпиада", "subject": "Химия", "grades": "8–11", "date": "01.10.2026 – 31.03.2027", "level": "Высший уровень", "url": "https://olymp.msu.ru"},
    {"name": "Олимпиада «Ломоносов» по биологии", "type": "Олимпиада", "subject": "Биология", "grades": "7–11", "date": "01.10.2026 – 31.03.2027", "level": "Высший уровень", "url": "https://olymp.msu.ru"},
    {"name": "Олимпиада «Высшая проба» по биологии", "type": "Олимпиада", "subject": "Биология", "grades": "9–11", "date": "01.11.2026 – 28.02.2027", "level": "Высший уровень", "url": "https://olymp.hse.ru"},
    {"name": "Олимпиада «Высшая проба» по русскому языку", "type": "Олимпиада", "subject": "Русский язык", "grades": "7–11", "date": "01.11.2026 – 28.02.2027", "level": "Высший уровень", "url": "https://olymp.hse.ru"},
    {"name": "Олимпиада «Ломоносов» по русскому языку", "type": "Олимпиада", "subject": "Русский язык", "grades": "5–11", "date": "01.10.2026 – 31.03.2027", "level": "Высший уровень", "url": "https://olymp.msu.ru"},
    {"name": "Всероссийский конкурс сочинений", "type": "Конкурс", "subject": "Литература", "grades": "4–11", "date": "01.09.2026 – 31.10.2026", "level": "Всероссийский", "url": "https://olimpiada.ru"},
    {"name": "Олимпиада «Высшая проба» по истории", "type": "Олимпиада", "subject": "История", "grades": "7–11", "date": "01.11.2026 – 28.02.2027", "level": "Высший уровень", "url": "https://olymp.hse.ru"},
    {"name": "Олимпиада «Ломоносов» по истории", "type": "Олимпиада", "subject": "История", "grades": "5–11", "date": "01.10.2026 – 31.03.2027", "level": "Высший уровень", "url": "https://olymp.msu.ru"},
    {"name": "Олимпиада по обществознанию «Высшая проба»", "type": "Олимпиада", "subject": "Обществознание", "grades": "7–11", "date": "01.11.2026 – 28.02.2027", "level": "Высший уровень", "url": "https://olymp.hse.ru"},
    {"name": "Олимпиада «Высшая проба» по английскому языку", "type": "Олимпиада", "subject": "Английский язык", "grades": "7–11", "date": "01.11.2026 – 28.02.2027", "level": "Высший уровень", "url": "https://olymp.hse.ru"},
    {"name": "Олимпиада «Ломоносов» по иностранным языкам", "type": "Олимпиада", "subject": "Иностранные языки", "grades": "5–11", "date": "01.10.2026 – 31.03.2027", "level": "Высший уровень", "url": "https://olymp.msu.ru"},
    {"name": "Олимпиада «Высшая проба» по экономике", "type": "Олимпиада", "subject": "Экономика", "grades": "7–11", "date": "01.11.2026 – 28.02.2027", "level": "Высший уровень", "url": "https://olymp.hse.ru"},
    {"name": "Олимпиада «Высшая проба» по праву", "type": "Олимпиада", "subject": "Право", "grades": "9–11", "date": "01.11.2026 – 28.02.2027", "level": "Высший уровень", "url": "https://olymp.hse.ru"},
    {"name": "Олимпиада «Ломоносов» по географии", "type": "Олимпиада", "subject": "География", "grades": "5–11", "date": "01.10.2026 – 31.03.2027", "level": "Высший уровень", "url": "https://olymp.msu.ru"},
    {"name": "Всероссийский конкурс «Живая классика»", "type": "Конкурс", "subject": "Литература", "grades": "5–11", "date": "01.02.2027 – 31.05.2027", "level": "Всероссийский", "url": "https://youngreaders.ru"},
    {"name": "Международный конкурс «Русский медвежонок»", "type": "Конкурс", "subject": "Русский язык", "grades": "2–11", "date": "15.11.2026", "level": "Международный", "url": "https://russian-kenguru.ru/konkursy/russkij-medvezhonok"},
    {"name": "Международный конкурс «Кенгуру»", "type": "Конкурс", "subject": "Математика", "grades": "2–11", "date": "20.03.2027", "level": "Международный", "url": "https://mathkang.ru"},
    {"name": "Международный конкурс «Британский бульдог»", "type": "Конкурс", "subject": "Английский язык", "grades": "3–11", "date": "15.12.2026", "level": "Международный", "url": "https://runodog.ru"},
    {"name": "Олимпиада «Юный предприниматель»", "type": "Олимпиада", "subject": "Экономика", "grades": "1–11", "date": "01.10.2026 – 31.03.2027", "level": "Всероссийская", "url": "https://olimpiada.ru"},
    {"name": "Олимпиада «Плюс» по математике", "type": "Олимпиада", "subject": "Математика", "grades": "1–4", "date": "01.09.2026 – 31.03.2027", "level": "Всероссийская", "url": "https://olimpiada.ru"},
    {"name": "Олимпиада «Русский с Пушкиным»", "type": "Олимпиада", "subject": "Русский язык", "grades": "1–4", "date": "01.09.2026 – 31.03.2027", "level": "Всероссийская", "url": "https://olimpiada.ru"},
    {"name": "Олимпиада «Заврики»", "type": "Олимпиада", "subject": "Все предметы", "grades": "1–4", "date": "01.09.2026 – 30.04.2027", "level": "Всероссийская", "url": "https://olimpiada.ru"},
    {"name": "Олимпиада «Дино»", "type": "Олимпиада", "subject": "Все предметы", "grades": "1–4", "date": "01.09.2026 – 30.04.2027", "level": "Всероссийская", "url": "https://olimpiada.ru"},
]


# ============ ОБУЧАЮЩИЕ САЙТЫ И КУРСЫ ============
EDUCATION = [
    {"name": "Школково — подготовка к ЕГЭ и олимпиадам", "category": "Математика", "type": "Курсы", "grades": "5–11", "url": "https://shkolkovo.net/"},
    {"name": "Сириус.Курсы — бесплатные онлайн-курсы", "category": "Математика", "type": "Курсы", "grades": "5–11", "url": "https://edu.sirius.online/"},
    {"name": "Фоксфорд — курсы по всем предметам", "category": "Математика", "type": "Курсы", "grades": "1–11", "url": "https://foxford.ru/"},
    {"name": "Учи.ру — интерактивные задания", "category": "Математика", "type": "Тренажёр", "grades": "1–9", "url": "https://uchi.ru/"},
    {"name": "Яндекс.Учебник", "category": "Математика", "type": "Тренажёр", "grades": "1–8", "url": "https://education.yandex.ru/"},
    {"name": "Problems.ru — банк олимпиадных задач", "category": "Математика", "type": "Задачи", "grades": "5–11", "url": "https://problems.ru/"},
    {"name": "Сириус.Курсы по физике", "category": "Физика", "type": "Курсы", "grades": "7–11", "url": "https://edu.sirius.online/"},
    {"name": "Фоксфорд — физика", "category": "Физика", "type": "Курсы", "grades": "7–11", "url": "https://foxford.ru/"},
    {"name": "GetAClass — физика в опытах", "category": "Физика", "type": "Видеокурс", "grades": "7–11", "url": "https://getaclass.ru/"},
    {"name": "Школково — физика", "category": "Физика", "type": "Курсы", "grades": "7–11", "url": "https://shkolkovo.net/"},
    {"name": "Stepik — курсы по программированию", "category": "Информатика", "type": "Курсы", "grades": "5–11", "url": "https://stepik.org/"},
    {"name": "Codeforces — олимпиадное программирование", "category": "Информатика", "type": "Тренажёр", "grades": "7–11", "url": "https://codeforces.com/"},
    {"name": "Академия Яндекса", "category": "Информатика", "type": "Курсы", "grades": "8–11", "url": "https://academy.yandex.ru/"},
    {"name": "Питонтьютор — Python для начинающих", "category": "Информатика", "type": "Курсы", "grades": "5–11", "url": "https://pythontutor.ru/"},
    {"name": "Школково — информатика", "category": "Информатика", "type": "Курсы", "grades": "8–11", "url": "https://shkolkovo.net/"},
    {"name": "Informatics.msk.ru — задачи по информатике", "category": "Информатика", "type": "Задачи", "grades": "7–11", "url": "https://informatics.msk.ru/"},
    {"name": "Сириус.Курсы по химии", "category": "Химия", "type": "Курсы", "grades": "8–11", "url": "https://edu.sirius.online/"},
    {"name": "Фоксфорд — химия", "category": "Химия", "type": "Курсы", "grades": "8–11", "url": "https://foxford.ru/"},
    {"name": "Школково — химия", "category": "Химия", "type": "Курсы", "grades": "8–11", "url": "https://shkolkovo.net/"},
    {"name": "Сириус.Курсы по биологии", "category": "Биология", "type": "Курсы", "grades": "7–11", "url": "https://edu.sirius.online/"},
    {"name": "Фоксфорд — биология", "category": "Биология", "type": "Курсы", "grades": "7–11", "url": "https://foxford.ru/"},
    {"name": "Школково — биология", "category": "Биология", "type": "Курсы", "grades": "7–11", "url": "https://shkolkovo.net/"},
    {"name": "Фоксфорд — русский язык", "category": "Русский язык", "type": "Курсы", "grades": "1–11", "url": "https://foxford.ru/"},
    {"name": "Школково — русский язык", "category": "Русский язык", "type": "Курсы", "grades": "5–11", "url": "https://shkolkovo.net/"},
    {"name": "Учи.ру — русский язык", "category": "Русский язык", "type": "Тренажёр", "grades": "1–9", "url": "https://uchi.ru/"},
    {"name": "Грамота.ру — справочник по русскому языку", "category": "Русский язык", "type": "Справочник", "grades": "1–11", "url": "https://gramota.ru/"},
    {"name": "Arzamas — курсы по литературе и истории", "category": "Литература", "type": "Курсы", "grades": "8–11", "url": "https://arzamas.academy/"},
    {"name": "Фоксфорд — история", "category": "История", "type": "Курсы", "grades": "5–11", "url": "https://foxford.ru/"},
    {"name": "Arzamas — история", "category": "История", "type": "Курсы", "grades": "8–11", "url": "https://arzamas.academy/"},
    {"name": "Школково — обществознание", "category": "Обществознание", "type": "Курсы", "grades": "8–11", "url": "https://shkolkovo.net/"},
    {"name": "Duolingo — бесплатное изучение языков", "category": "Английский язык", "type": "Тренажёр", "grades": "1–11", "url": "https://www.duolingo.com/"},
    {"name": "Skyeng — английский онлайн", "category": "Английский язык", "type": "Курсы", "grades": "1–11", "url": "https://skyeng.ru/"},
    {"name": "Puzzle English — английский по видео", "category": "Английский язык", "type": "Курсы", "grades": "5–11", "url": "https://puzzle-english.com/"},
    {"name": "Сириус.Курсы — все предметы", "category": "Все предметы", "type": "Курсы", "grades": "5–11", "url": "https://edu.sirius.online/"},
    {"name": "Фоксфорд — все предметы", "category": "Все предметы", "type": "Курсы", "grades": "1–11", "url": "https://foxford.ru/"},
    {"name": "Учи.ру — все предметы", "category": "Все предметы", "type": "Тренажёр", "grades": "1–9", "url": "https://uchi.ru/"},
    {"name": "ЯКласс — все предметы", "category": "Все предметы", "type": "Тренажёр", "grades": "1–11", "url": "https://www.yaklass.ru/"},
    {"name": "ИнтернетУрок — видеоуроки по всем предметам", "category": "Все предметы", "type": "Видеокурс", "grades": "1–11", "url": "https://interneturok.ru/"},
    {"name": "Российская электронная школа", "category": "Все предметы", "type": "Видеокурс", "grades": "1–11", "url": "https://resh.edu.ru/"},
    {"name": "Stepik — курсы по всем предметам", "category": "Все предметы", "type": "Курсы", "grades": "5–11", "url": "https://stepik.org/"},
]


# ============ ОБУЧАЮЩИЕ МАТЕРИАЛЫ ============
MATERIALS = [
    # ===== Видеоуроки =====
    {"name": "ИнтернетУрок — видеоуроки по всем предметам (1–11 класс)", "category": "Все предметы", "type": "Видеоуроки", "grades": "1–11", "url": "https://interneturok.ru/"},
    {"name": "Российская электронная школа — уроки от лучших учителей", "category": "Все предметы", "type": "Видеоуроки", "grades": "1–11", "url": "https://resh.edu.ru/"},
    {"name": "GetAClass — физика и математика в опытах", "category": "Физика", "type": "Видеоуроки", "grades": "7–11", "url": "https://getaclass.ru/"},
    {"name": "Академия Хана — видеоуроки на русском", "category": "Все предметы", "type": "Видеоуроки", "grades": "1–11", "url": "https://ru.khanacademy.org/"},
    {"name": "Arzamas — лекции по истории, литературе, искусству", "category": "История", "type": "Лекции", "grades": "8–11", "url": "https://arzamas.academy/"},
    {"name": "ПостНаука — лекции учёных по всем наукам", "category": "Все предметы", "type": "Лекции", "grades": "8–11", "url": "https://postnauka.org/"},

    # ===== Учебники и книги =====
    {"name": "Учебники МЦНМО (математика, физика)", "category": "Математика", "type": "Учебники", "grades": "5–11", "url": "https://mccme.ru/"},
    {"name": "Библиотека «Математическое просвещение»", "category": "Математика", "type": "Книги", "grades": "5–11", "url": "https://mccme.ru/free-books/"},
    {"name": "Лекторий «ПостНаука» — книги и статьи", "category": "Все предметы", "type": "Книги", "grades": "8–11", "url": "https://postnauka.org/"},
    {"name": "Электронная библиотека «Гипермаркет знаний»", "category": "Все предметы", "type": "Учебники", "grades": "1–11", "url": "https://www.grandars.ru/"},
    {"name": "Фоксфорд.Учебник — онлайн-справочник", "category": "Все предметы", "type": "Учебники", "grades": "1–11", "url": "https://foxford.ru/wiki"},

    # ===== Задачи и архивы олимпиад =====
    {"name": "Problems.ru — банк олимпиадных задач с решениями", "category": "Математика", "type": "Задачи", "grades": "5–11", "url": "https://problems.ru/"},
    {"name": "Задачи по математике — архив МЦНМО", "category": "Математика", "type": "Задачи", "grades": "5–11", "url": "https://mccme.ru/"},
    {"name": "Informatics.msk.ru — задачи по информатике", "category": "Информатика", "type": "Задачи", "grades": "7–11", "url": "https://informatics.msk.ru/"},
    {"name": "Codeforces — задачи по программированию", "category": "Информатика", "type": "Задачи", "grades": "7–11", "url": "https://codeforces.com/"},
    {"name": "Архив ВсОШ — задания прошлых лет", "category": "Все предметы", "type": "Задачи", "grades": "4–11", "url": "https://olimpiada.ru/"},
    {"name": "Олимпиадные задачи по физике (МФТИ)", "category": "Физика", "type": "Задачи", "grades": "7–11", "url": "https://olymp.mipt.ru/"},

    # ===== Справочники и шпаргалки =====
    {"name": "Грамота.ру — справочник по русскому языку", "category": "Русский язык", "type": "Справочник", "grades": "1–11", "url": "https://gramota.ru/"},
    {"name": "Культура письменной речи — правила русского языка", "category": "Русский язык", "type": "Справочник", "grades": "5–11", "url": "http://www.gramma.ru/"},
    {"name": "Фоксфорд.Учебник — конспекты по всем предметам", "category": "Все предметы", "type": "Справочник", "grades": "1–11", "url": "https://foxford.ru/wiki"},
    {"name": "Химическая энциклопедия онлайн", "category": "Химия", "type": "Справочник", "grades": "8–11", "url": "https://www.xumuk.ru/"},
    {"name": "Мегаэнциклопедия Кирилла и Мефодия", "category": "Все предметы", "type": "Справочник", "grades": "1–11", "url": "https://megabook.ru/"},

    # ===== Научно-популярное =====
    {"name": "Элементы.ру — научно-популярный портал", "category": "Все предметы", "type": "Статьи", "grades": "8–11", "url": "https://elementy.ru/"},
    {"name": "N+1 — научные новости и статьи", "category": "Все предметы", "type": "Статьи", "grades": "8–11", "url": "https://nplus1.ru/"},
    {"name": "ПостНаука — курсы и лекции учёных", "category": "Все предметы", "type": "Лекции", "grades": "8–11", "url": "https://postnauka.org/"},
    {"name": "Квант — научно-популярный физико-математический журнал", "category": "Математика", "type": "Журнал", "grades": "7–11", "url": "https://kvant.mccme.ru/"},
    {"name": "Химия и жизнь — научно-популярный журнал", "category": "Химия", "type": "Журнал", "grades": "8–11", "url": "https://elementy.ru/nauchno-populyarnaya_biblioteka"},

    # ===== Интерактивные платформы =====
    {"name": "Учи.ру — интерактивные задания по всем предметам", "category": "Все предметы", "type": "Интерактив", "grades": "1–9", "url": "https://uchi.ru/"},
    {"name": "ЯКласс — тренажёры по школьным предметам", "category": "Все предметы", "type": "Интерактив", "grades": "1–11", "url": "https://www.yaklass.ru/"},
    {"name": "Яндекс.Учебник — задания по математике и русскому", "category": "Все предметы", "type": "Интерактив", "grades": "1–8", "url": "https://education.yandex.ru/"},
    {"name": "Skysmart — интерактивная рабочая тетрадь", "category": "Все предметы", "type": "Интерактив", "grades": "1–11", "url": "https://skysmart.ru/"},
]


# ============ HTML ШАБЛОН ============
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Олимпиады, конкурсы, обучение 2026–2027</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            min-height: 100vh;
            padding: 20px;
            color: #1a1a1a;
        }
        .container {
            max-width: 1300px;
            margin: 0 auto;
            background: #fff;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            overflow: hidden;
        }
        header {
            background: #1a1a1a;
            color: #fff;
            padding: 30px 40px;
            text-align: center;
        }
        header h1 { font-size: 1.9em; margin-bottom: 8px; font-weight: 700; }
        header p { opacity: 0.75; font-size: 15px; }
        .tabs {
            display: flex;
            background: #fafafa;
            border-bottom: 1px solid #e0e0e0;
            flex-wrap: wrap;
        }
        .tab {
            padding: 18px 30px;
            cursor: pointer;
            font-size: 15px;
            font-weight: 600;
            color: #666;
            border-bottom: 3px solid transparent;
            transition: all 0.2s;
            user-select: none;
        }
        .tab:hover { background: #f0f0f0; color: #1a1a1a; }
        .tab.active {
            color: #1a1a1a;
            border-bottom-color: #1a1a1a;
            background: #fff;
        }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .filters {
            padding: 20px 40px;
            background: #fafafa;
            border-bottom: 1px solid #e8e8e8;
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            align-items: center;
        }
        .filters select, .filters input {
            padding: 10px 14px;
            border: 1.5px solid #d0d0d0;
            border-radius: 6px;
            font-size: 14px;
            outline: none;
            transition: border-color 0.2s;
            background: #fff;
            color: #1a1a1a;
        }
        .filters select:focus, .filters input:focus { border-color: #1a1a1a; }
        .filters input { flex: 1; min-width: 200px; }
        .stats {
            padding: 12px 40px;
            background: #f0f0f0;
            color: #555;
            font-size: 14px;
            border-bottom: 1px solid #e0e0e0;
        }
        .stats b { color: #1a1a1a; }
        table { width: 100%; border-collapse: collapse; }
        thead { background: #f7f7f7; position: sticky; top: 0; z-index: 5; }
        th {
            padding: 14px 16px;
            text-align: left;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            color: #777;
            border-bottom: 2px solid #e0e0e0;
            font-weight: 700;
        }
        td {
            padding: 14px 16px;
            border-bottom: 1px solid #ededed;
            font-size: 14px;
            vertical-align: top;
        }
        tr:hover td { background: #fafafa; }
        .badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 11.5px;
            font-weight: 600;
            white-space: nowrap;
            border: 1px solid;
        }
        .badge-olymp { background: #1a1a1a; color: #fff; border-color: #1a1a1a; }
        .badge-contest { background: #fff; color: #1a1a1a; border-color: #1a1a1a; }
        .badge-level-1 { background: #1a1a1a; color: #fff; border-color: #1a1a1a; }
        .badge-level-2 { background: #e0e0e0; color: #1a1a1a; border-color: #b0b0b0; }
        .badge-level-other { background: #fff; color: #555; border-color: #b0b0b0; }
        a.link {
            color: #1a1a1a;
            text-decoration: none;
            font-weight: 500;
            word-break: break-all;
            border-bottom: 1px solid #999;
        }
        a.link:hover { border-bottom-color: #1a1a1a; }
        .no-results {
            padding: 60px;
            text-align: center;
            color: #999;
            font-size: 16px;
            display: none;
        }
        footer {
            padding: 20px 40px;
            background: #f7f7f7;
            text-align: center;
            color: #777;
            font-size: 13px;
            border-top: 1px solid #e0e0e0;
        }
        @media (max-width: 800px) {
            header { padding: 20px; }
            header h1 { font-size: 1.3em; }
            .tab { padding: 14px 18px; font-size: 13px; }
            .filters, .stats, footer { padding: 15px 20px; }
            th, td { padding: 10px 8px; font-size: 12px; }
            th:nth-child(5), td:nth-child(5) { display: none; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Олимпиады, конкурсы, обучение 2026–2027</h1>
            <p>Всё для школьников с 1 по 11 класс в одном месте</p>
        </header>

        <div class="tabs">
            <div class="tab active" data-tab="olympiads">🏆 Олимпиады и конкурсы</div>
            <div class="tab" data-tab="education">📚 Курсы и тренажёры</div>
            <div class="tab" data-tab="materials">📖 Обучающие материалы</div>
        </div>

        <!-- ===== ВКЛАДКА: ОЛИМПИАДЫ ===== -->
        <div class="tab-content active" id="tab-olympiads">
            <div class="filters">
                <select id="filterClass"><option value="">Все классы</option>__CLASS_OPTIONS__</select>
                <select id="filterSubject"><option value="">Все предметы</option>__SUBJECT_OPTIONS__</select>
                <select id="filterType">
                    <option value="">Все типы</option>
                    <option value="Олимпиада">Олимпиады</option>
                    <option value="Конкурс">Конкурсы</option>
                </select>
                <input type="text" id="searchInput" placeholder="🔍 Поиск по названию...">
            </div>
            <div class="stats">Показано: <b id="count">__TOTAL__</b> из <b>__TOTAL__</b> мероприятий</div>
            <table>
                <thead><tr>
                    <th>Название</th><th>Тип</th><th>Предмет</th><th>Классы</th>
                    <th>Сроки</th><th>Уровень</th><th>Сайт</th>
                </tr></thead>
                <tbody id="tbody-olympiads">__ROWS_OLYMPIADS__</tbody>
            </table>
            <div class="no-results" id="noResults-olympiads">😔 Ничего не найдено.</div>
        </div>

        <!-- ===== ВКЛАДКА: КУРСЫ ===== -->
        <div class="tab-content" id="tab-education">
            <div class="filters">
                <select id="filterClassEdu"><option value="">Все классы</option>__CLASS_OPTIONS_EDU__</select>
                <select id="filterCategory"><option value="">Все предметы</option>__CATEGORY_OPTIONS__</select>
                <select id="filterTypeEdu">
                    <option value="">Все типы</option>
                    <option value="Курсы">Курсы</option>
                    <option value="Тренажёр">Тренажёры</option>
                    <option value="Видеокурс">Видеокурсы</option>
                    <option value="Задачи">Задачи</option>
                    <option value="Справочник">Справочники</option>
                </select>
                <input type="text" id="searchInputEdu" placeholder="🔍 Поиск по названию...">
            </div>
            <div class="stats">Показано: <b id="countEdu">__TOTAL_EDU__</b> из <b>__TOTAL_EDU__</b> ресурсов</div>
            <table>
                <thead><tr>
                    <th>Название</th><th>Тип</th><th>Предмет</th><th>Классы</th><th>Сайт</th>
                </tr></thead>
                <tbody id="tbody-education">__ROWS_EDUCATION__</tbody>
            </table>
            <div class="no-results" id="noResults-education">😔 Ничего не найдено.</div>
        </div>

        <!-- ===== ВКЛАДКА: МАТЕРИАЛЫ ===== -->
        <div class="tab-content" id="tab-materials">
            <div class="filters">
                <select id="filterClassMat"><option value="">Все классы</option>__CLASS_OPTIONS_MAT__</select>
                <select id="filterCategoryMat"><option value="">Все предметы</option>__CATEGORY_OPTIONS_MAT__</select>
                <select id="filterTypeMat"><option value="">Все типы</option>__TYPE_OPTIONS_MAT__</select>
                <input type="text" id="searchInputMat" placeholder="🔍 Поиск по названию...">
            </div>
            <div class="stats">Показано: <b id="countMat">__TOTAL_MAT__</b> из <b>__TOTAL_MAT__</b> материалов</div>
            <table>
                <thead><tr>
                    <th>Название</th><th>Тип</th><th>Предмет</th><th>Классы</th><th>Сайт</th>
                </tr></thead>
                <tbody id="tbody-materials">__ROWS_MATERIALS__</tbody>
            </table>
            <div class="no-results" id="noResults-materials">😔 Ничего не найдено.</div>
        </div>

        <footer>
            Данные носят справочный характер. Актуальные сроки уточняйте на официальных сайтах организаторов.
        </footer>
    </div>

    <script>
        // Переключение вкладок
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', () => {
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                tab.classList.add('active');
                document.getElementById('tab-' + tab.dataset.tab).classList.add('active');
            });
        });

        // Универсальная фильтрация
        function setupFilter(rowsSelector, countId, noResultsId, filters) {
            const rows = document.querySelectorAll(rowsSelector);
            const countEl = document.getElementById(countId);
            const noResults = document.getElementById(noResultsId);
            function apply() {
                let visible = 0;
                rows.forEach(row => {
                    let ok = true;
                    filters.forEach(f => {
                        const val = f.el.value;
                        if (!val) return;
                        const dataVal = row.dataset[f.key] || '';
                        if (f.type === 'exact') {
                            if (dataVal !== val) ok = false;
                        } else if (f.type === 'grade') {
                            if (!gradeMatches(dataVal, val)) ok = false;
                        } else if (f.type === 'search') {
                            if (!(row.dataset.name || '').toLowerCase().includes(val.toLowerCase().trim())) ok = false;
                        }
                    });
                    row.style.display = ok ? '' : 'none';
                    if (ok) visible++;
                });
                countEl.textContent = visible;
                noResults.style.display = visible === 0 ? 'block' : 'none';
            }
            filters.forEach(f => f.el.addEventListener(f.type === 'search' ? 'input' : 'change', apply));
        }

        function gradeMatches(grades, cls) {
            const parts = grades.split('–');
            if (parts.length !== 2) return true;
            return parseInt(cls) >= parseInt(parts[0]) && parseInt(cls) <= parseInt(parts[1]);
        }

        setupFilter('#tbody-olympiads tr', 'count', 'noResults-olympiads', [
            {el: document.getElementById('filterClass'), key: 'grades', type: 'grade'},
            {el: document.getElementById('filterSubject'), key: 'subject', type: 'exact'},
            {el: document.getElementById('filterType'), key: 'type', type: 'exact'},
            {el: document.getElementById('searchInput'), key: 'name', type: 'search'}
        ]);

        setupFilter('#tbody-education tr', 'countEdu', 'noResults-education', [
            {el: document.getElementById('filterClassEdu'), key: 'grades', type: 'grade'},
            {el: document.getElementById('filterCategory'), key: 'category', type: 'exact'},
            {el: document.getElementById('filterTypeEdu'), key: 'type', type: 'exact'},
            {el: document.getElementById('searchInputEdu'), key: 'name', type: 'search'}
        ]);

        setupFilter('#tbody-materials tr', 'countMat', 'noResults-materials', [
            {el: document.getElementById('filterClassMat'), key: 'grades', type: 'grade'},
            {el: document.getElementById('filterCategoryMat'), key: 'category', type: 'exact'},
            {el: document.getElementById('filterTypeMat'), key: 'type', type: 'exact'},
            {el: document.getElementById('searchInputMat'), key: 'name', type: 'search'}
        ]);
    </script>
</body>
</html>
"""


def build_olympiad_rows():
    rows = ""
    for o in OLYMPIADS:
        bt = "badge-olymp" if o["type"] == "Олимпиада" else "badge-contest"
        if o["level"] == "Высший уровень":
            bl = "badge-level-1"
        elif o["level"] == "Повышенный уровень":
            bl = "badge-level-2"
        else:
            bl = "badge-level-other"
        rows += f'<tr data-name="{o["name"]}" data-grades="{o["grades"]}" data-subject="{o["subject"]}" data-type="{o["type"]}"><td><b>{o["name"]}</b></td><td><span class="badge {bt}">{o["type"]}</span></td><td>{o["subject"]}</td><td>{o["grades"]}</td><td>{o["date"]}</td><td><span class="badge {bl}">{o["level"]}</span></td><td><a class="link" href="{o["url"]}" target="_blank">Перейти →</a></td></tr>'
    return rows


def build_education_rows():
    rows = ""
    for e in EDUCATION:
        bt = "badge-contest" if e["type"] in ("Курсы", "Видеокурс") else "badge-level-2"
        rows += f'<tr data-name="{e["name"]}" data-grades="{e["grades"]}" data-category="{e["category"]}" data-type="{e["type"]}"><td><b>{e["name"]}</b></td><td><span class="badge {bt}">{e["type"]}</span></td><td>{e["category"]}</td><td>{e["grades"]}</td><td><a class="link" href="{e["url"]}" target="_blank">Перейти →</a></td></tr>'
    return rows


def build_material_rows():
    rows = ""
    for m in MATERIALS:
        bt = "badge-contest" if m["type"] in ("Видеоуроки", "Лекции", "Курсы") else "badge-level-2"
        rows += f'<tr data-name="{m["name"]}" data-grades="{m["grades"]}" data-category="{m["category"]}" data-type="{m["type"]}"><td><b>{m["name"]}</b></td><td><span class="badge {bt}">{m["type"]}</span></td><td>{m["category"]}</td><td>{m["grades"]}</td><td><a class="link" href="{m["url"]}" target="_blank">Перейти →</a></td></tr>'
    return rows


def build_options(items):
    return "".join(f'<option value="{i}">{i}</option>' for i in sorted(set(items)))


# ============ FASTAPI ============
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    class_options = "".join(f'<option value="{i}">{i} класс</option>' for i in range(1, 12))

    html = HTML_TEMPLATE
    html = html.replace("__CLASS_OPTIONS__", class_options)
    html = html.replace("__CLASS_OPTIONS_EDU__", class_options)
    html = html.replace("__CLASS_OPTIONS_MAT__", class_options)
    html = html.replace("__SUBJECT_OPTIONS__", build_options([o["subject"] for o in OLYMPIADS]))
    html = html.replace("__CATEGORY_OPTIONS__", build_options([e["category"] for e in EDUCATION]))
    html = html.replace("__CATEGORY_OPTIONS_MAT__", build_options([m["category"] for m in MATERIALS]))
    html = html.replace("__TYPE_OPTIONS_MAT__", build_options([m["type"] for m in MATERIALS]))
    html = html.replace("__ROWS_OLYMPIADS__", build_olympiad_rows())
    html = html.replace("__ROWS_EDUCATION__", build_education_rows())
    html = html.replace("__ROWS_MATERIALS__", build_material_rows())
    html = html.replace("__TOTAL__", str(len(OLYMPIADS)))
    html = html.replace("__TOTAL_EDU__", str(len(EDUCATION)))
    html = html.replace("__TOTAL_MAT__", str(len(MATERIALS)))
    return HTMLResponse(content=html)


# ============ ЗАПУСК ============
if __name__ == "__main__":
    import threading, webbrowser, socket, time

    PORT = 8000

    def get_local_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    def open_browser():
        time.sleep(1.5)
        webbrowser.open(f"http://127.0.0.1:{PORT}")

    local_ip = get_local_ip()

    print("\n" + "=" * 60)
    print("🚀 Сервер запущен!")
    print("=" * 60)
    print(f"Локально:             http://127.0.0.1:{PORT}")
    print(f"С других устройств:   http://{local_ip}:{PORT}")
    print("=" * 60)
    print("Браузер откроется автоматически...")
    print("Для остановки нажми Ctrl+C")
    print("=" * 60 + "\n")

    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run(app, host="0.0.0.0", port=PORT)