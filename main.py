from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn
import os
import uuid
from datetime import datetime

app = FastAPI(title="Олимпиады и задания 2026-2027")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ============ ОЛИМПИАДЫ ============
OLYMPIADS = [
    {"name": "ВсОШ — школьный этап", "type": "Олимпиада", "subject": "Все предметы", "grades": "4–11", "date": "01.09.2026 – 31.10.2026", "level": "Всероссийская", "url": "https://olimpiada.ru"},
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
    {"name": "Олимпиада «Высшая проба» по информатике", "type": "Олимпиада", "subject": "Информатика", "grades": "9–11", "date": "01.11.2026 – 28.02.2027", "level": "Высший уровень", "url": "https://olymp.hse.ru"},
    {"name": "Открытая олимпиада по программированию", "type": "Олимпиада", "subject": "Информатика", "grades": "5–11", "date": "01.10.2026 – 31.03.2027", "level": "Высший уровень", "url": "https://info.olimpiada.ru"},
    {"name": "Олимпиада «Технокубок»", "type": "Олимпиада", "subject": "Информатика", "grades": "8–11", "date": "01.10.2026 – 31.03.2027", "level": "Повышенный уровень", "url": "https://technocup.mail.ru"},
    {"name": "Олимпиада «Высшая проба» по химии", "type": "Олимпиада", "subject": "Химия", "grades": "9–11", "date": "01.11.2026 – 28.02.2027", "level": "Высший уровень", "url": "https://olymp.hse.ru"},
    {"name": "Олимпиада «Ломоносов» по химии", "type": "Олимпиада", "subject": "Химия", "grades": "8–11", "date": "01.10.2026 – 31.03.2027", "level": "Высший уровень", "url": "https://olymp.msu.ru"},
    {"name": "Олимпиада «Ломоносов» по биологии", "type": "Олимпиада", "subject": "Биология", "grades": "7–11", "date": "01.10.2026 – 31.03.2027", "level": "Высший уровень", "url": "https://olymp.msu.ru"},
    {"name": "Олимпиада «Высшая проба» по русскому языку", "type": "Олимпиада", "subject": "Русский язык", "grades": "7–11", "date": "01.11.2026 – 28.02.2027", "level": "Высший уровень", "url": "https://olymp.hse.ru"},
    {"name": "Олимпиада «Ломоносов» по русскому языку", "type": "Олимпиада", "subject": "Русский язык", "grades": "5–11", "date": "01.10.2026 – 31.03.2027", "level": "Высший уровень", "url": "https://olymp.msu.ru"},
    {"name": "Олимпиада «Высшая проба» по истории", "type": "Олимпиада", "subject": "История", "grades": "7–11", "date": "01.11.2026 – 28.02.2027", "level": "Высший уровень", "url": "https://olymp.hse.ru"},
    {"name": "Олимпиада «Высшая проба» по английскому языку", "type": "Олимпиада", "subject": "Английский язык", "grades": "7–11", "date": "01.11.2026 – 28.02.2027", "level": "Высший уровень", "url": "https://olymp.hse.ru"},
    {"name": "Олимпиада «Высшая проба» по экономике", "type": "Олимпиада", "subject": "Экономика", "grades": "7–11", "date": "01.11.2026 – 28.02.2027", "level": "Высший уровень", "url": "https://olymp.hse.ru"},
    {"name": "Олимпиада «Высшая проба» по праву", "type": "Олимпиада", "subject": "Право", "grades": "9–11", "date": "01.11.2026 – 28.02.2027", "level": "Высший уровень", "url": "https://olymp.hse.ru"},
    {"name": "Олимпиада «Ломоносов» по географии", "type": "Олимпиада", "subject": "География", "grades": "5–11", "date": "01.10.2026 – 31.03.2027", "level": "Высший уровень", "url": "https://olymp.msu.ru"},
    {"name": "Международный конкурс «Русский медвежонок»", "type": "Конкурс", "subject": "Русский язык", "grades": "2–11", "date": "15.11.2026", "level": "Международный", "url": "https://rm.ckp-rf.ru"},
    {"name": "Международный конкурс «Кенгуру»", "type": "Конкурс", "subject": "Математика", "grades": "2–11", "date": "20.03.2027", "level": "Международный", "url": "https://mathkang.ru"},
    {"name": "Международный конкурс «Британский бульдог»", "type": "Конкурс", "subject": "Английский язык", "grades": "3–11", "date": "15.12.2026", "level": "Международный", "url": "https://runodog.ru"},
    {"name": "Олимпиада «Плюс» по математике", "type": "Олимпиада", "subject": "Математика", "grades": "1–4", "date": "01.09.2026 – 31.03.2027", "level": "Всероссийская", "url": "https://plus.olimpiada.ru"},
    {"name": "Олимпиада «Русский с Пушкиным»", "type": "Олимпиада", "subject": "Русский язык", "grades": "1–4", "date": "01.09.2026 – 31.03.2027", "level": "Всероссийская", "url": "https://pushkin.olimpiada.ru"},
    {"name": "Олимпиада «Заврики»", "type": "Олимпиада", "subject": "Все предметы", "grades": "1–4", "date": "01.09.2026 – 30.04.2027", "level": "Всероссийская", "url": "https://zavriki.olimpiada.ru"},
]


# ============ ОБУЧАЮЩИЕ САЙТЫ ============
EDUCATION = [
    {"name": "Школково — подготовка к ЕГЭ и олимпиадам", "category": "Математика", "type": "Курсы", "grades": "5–11", "url": "https://3.shkolkovo.online/"},
    {"name": "Сириус.Курсы", "category": "Математика", "type": "Курсы", "grades": "5–11", "url": "https://edu.sirius.online/"},
    {"name": "Фоксфорд", "category": "Математика", "type": "Курсы", "grades": "1–11", "url": "https://foxford.ru/"},
    {"name": "Учи.ру", "category": "Математика", "type": "Тренажёр", "grades": "1–9", "url": "https://uchi.ru/"},
    {"name": "Яндекс.Учебник", "category": "Математика", "type": "Тренажёр", "grades": "1–8", "url": "https://education.yandex.ru/"},
    {"name": "Problems.ru", "category": "Математика", "type": "Задачи", "grades": "5–11", "url": "https://problems.ru/"},
    {"name": "GetAClass — физика в опытах", "category": "Физика", "type": "Видеокурс", "grades": "7–11", "url": "https://getaclass.ru/"},
    {"name": "Stepik", "category": "Информатика", "type": "Курсы", "grades": "5–11", "url": "https://stepik.org/"},
    {"name": "Codeforces", "category": "Информатика", "type": "Тренажёр", "grades": "7–11", "url": "https://codeforces.com/"},
    {"name": "Академия Яндекса", "category": "Информатика", "type": "Курсы", "grades": "8–11", "url": "https://academy.yandex.ru/"},
    {"name": "Питонтьютор", "category": "Информатика", "type": "Курсы", "grades": "5–11", "url": "https://pythontutor.ru/"},
    {"name": "Informatics.msk.ru", "category": "Информатика", "type": "Задачи", "grades": "7–11", "url": "https://informatics.msk.ru/"},
    {"name": "Arzamas — литература и история", "category": "Литература", "type": "Курсы", "grades": "8–11", "url": "https://arzamas.academy/"},
    {"name": "Грамота.ру", "category": "Русский язык", "type": "Справочник", "grades": "1–11", "url": "https://gramota.ru/"},
    {"name": "Duolingo", "category": "Английский язык", "type": "Тренажёр", "grades": "1–11", "url": "https://www.duolingo.com/"},
    {"name": "Puzzle English", "category": "Английский язык", "type": "Курсы", "grades": "5–11", "url": "https://puzzle-english.com/"},
    {"name": "ЯКласс — все предметы", "category": "Все предметы", "type": "Тренажёр", "grades": "1–11", "url": "https://www.yaklass.ru/"},
    {"name": "ИнтернетУрок", "category": "Все предметы", "type": "Видеокурс", "grades": "1–11", "url": "https://interneturok.ru/"},
    {"name": "Российская электронная школа", "category": "Все предметы", "type": "Видеокурс", "grades": "1–11", "url": "https://resh.edu.ru/"},
]


# ============ БАЗА ЗАДАНИЙ ИЗ УЧЕБНИКОВ ============
# Каждое задание: предмет, класс, тип (ДЗ/Классная), вопрос, ответ, решение
TASKS = [
    # ===== МАТЕМАТИКА 1-4 =====
    {"id": "m1", "title": "Сложение в пределах 20", "subject": "Математика", "grade": "1", "type": "Классная", "question": "Сколько будет 7 + 8?", "correct": "15", "answer": "15", "solution": "7 + 8 = 15."},
    {"id": "m2", "title": "Вычитание в пределах 20", "subject": "Математика", "grade": "1", "type": "ДЗ", "question": "Сколько будет 15 − 9?", "correct": "6", "answer": "6", "solution": "15 − 9 = 6."},
    {"id": "m3", "title": "Таблица умножения", "subject": "Математика", "grade": "2", "type": "Классная", "question": "Сколько будет 7 × 6?", "correct": "42", "answer": "42", "solution": "7 × 6 = 42."},
    {"id": "m4", "title": "Деление", "subject": "Математика", "grade": "2", "type": "ДЗ", "question": "Сколько будет 48 ÷ 6?", "correct": "8", "answer": "8", "solution": "48 ÷ 6 = 8."},
    {"id": "m5", "title": "Периметр прямоугольника", "subject": "Математика", "grade": "3", "type": "Классная", "question": "Периметр прямоугольника со сторонами 5 см и 3 см.", "correct": "16", "answer": "16 см", "solution": "P = 2 × (5 + 3) = 16 см."},
    {"id": "m6", "title": "Площадь прямоугольника", "subject": "Математика", "grade": "3", "type": "ДЗ", "question": "Площадь прямоугольника 6 см × 4 см.", "correct": "24", "answer": "24 см²", "solution": "S = 6 × 4 = 24 см²."},
    {"id": "m7", "title": "Порядок действий", "subject": "Математика", "grade": "4", "type": "Классная", "question": "Вычислите: 20 + 5 × 3", "correct": "35", "answer": "35", "solution": "Сначала умножение: 5 × 3 = 15. Потом сложение: 20 + 15 = 35."},
    {"id": "m8", "title": "Дроби", "subject": "Математика", "grade": "4", "type": "ДЗ", "question": "Сколько будет 1/2 + 1/4?", "correct": "3/4", "answer": "3/4", "solution": "1/2 = 2/4. 2/4 + 1/4 = 3/4."},

    # ===== МАТЕМАТИКА 5-6 =====
    {"id": "m9", "title": "Сложение дробей", "subject": "Математика", "grade": "5", "type": "ДЗ", "question": "Вычислите: 1/2 + 1/3", "correct": "5/6", "answer": "5/6", "solution": "Приводим к знаменателю 6: 3/6 + 2/6 = 5/6."},
    {"id": "m10", "title": "Умножение дробей", "subject": "Математика", "grade": "5", "type": "Классная", "question": "Вычислите: 2/3 × 3/4", "correct": "1/2", "answer": "1/2", "solution": "2/3 × 3/4 = 6/12 = 1/2."},
    {"id": "m11", "title": "Проценты", "subject": "Математика", "grade": "5", "type": "ДЗ", "question": "Найдите 20% от 150.", "correct": "30", "answer": "30", "solution": "150 × 0.2 = 30."},
    {"id": "m12", "title": "Линейное уравнение", "subject": "Математика", "grade": "6", "type": "Классная", "question": "Решите: 2x + 5 = 13", "correct": "4", "answer": "x = 4", "solution": "2x = 8, x = 4."},
    {"id": "m13", "title": "Отрицательные числа", "subject": "Математика", "grade": "6", "type": "ДЗ", "question": "Вычислите: −7 + 12", "correct": "5", "answer": "5", "solution": "−7 + 12 = 5."},
    {"id": "m14", "title": "Пропорция", "subject": "Математика", "grade": "6", "type": "Классная", "question": "Найдите x: 3/5 = x/15", "correct": "9", "answer": "x = 9", "solution": "x = 3 × 15 / 5 = 9."},

    # ===== МАТЕМАТИКА 7-9 =====
    {"id": "m15", "title": "Линейная функция", "subject": "Математика", "grade": "7", "type": "ДЗ", "question": "Найдите y, если y = 3x + 1, x = 4.", "correct": "13", "answer": "y = 13", "solution": "y = 3 × 4 + 1 = 13."},
    {"id": "m16", "title": "Формулы сокращённого умножения", "subject": "Математика", "grade": "7", "type": "Классная", "question": "Разложите: x² − 9", "correct": "(x-3)(x+3)", "answer": "(x − 3)(x + 3)", "solution": "Разность квадратов: a² − b² = (a − b)(a + b)."},
    {"id": "m17", "title": "Квадратное уравнение", "subject": "Математика", "grade": "8", "type": "ДЗ", "question": "Решите: x² − 5x + 6 = 0", "correct": "2;3", "answer": "x₁ = 2, x₂ = 3", "solution": "D = 25 − 24 = 1. x = (5 ± 1) / 2 = 3 или 2."},
    {"id": "m18", "title": "Теорема Пифагора", "subject": "Математика", "grade": "8", "type": "Классная", "question": "Катеты 3 и 4. Найдите гипотенузу.", "correct": "5", "answer": "5", "solution": "c² = 3² + 4² = 9 + 16 = 25, c = 5."},
    {"id": "m19", "title": "Арифметическая прогрессия", "subject": "Математика", "grade": "9", "type": "ДЗ", "question": "a₁ = 2, d = 3. Найдите a₅.", "correct": "14", "answer": "a₅ = 14", "solution": "a₅ = 2 + 4 × 3 = 14."},
    {"id": "m20", "title": "Геометрическая прогрессия", "subject": "Математика", "grade": "9", "type": "Классная", "question": "b₁ = 1, q = 2. Найдите b₆.", "correct": "32", "answer": "b₆ = 32", "solution": "b₆ = 1 × 2⁵ = 32."},

    # ===== МАТЕМАТИКА 10-11 =====
    {"id": "m21", "title": "Производная", "subject": "Математика", "grade": "10", "type": "ДЗ", "question": "Найдите производную: f(x) = x³ + 2x", "correct": "3x^2+2", "answer": "f'(x) = 3x² + 2", "solution": "(x³)' = 3x², (2x)' = 2. Итого: 3x² + 2."},
    {"id": "m22", "title": "Тригонометрия", "subject": "Математика", "grade": "10", "type": "Классная", "question": "Чему равен sin(30°)?", "correct": "0.5", "answer": "0.5", "solution": "sin(30°) = 1/2 = 0.5."},
    {"id": "m23", "title": "Логарифмы", "subject": "Математика", "grade": "11", "type": "ДЗ", "question": "Вычислите: log₂(8)", "correct": "3", "answer": "3", "solution": "2³ = 8, значит log₂(8) = 3."},
    {"id": "m24", "title": "Интеграл", "subject": "Математика", "grade": "11", "type": "Классная", "question": "Найдите ∫2x dx", "correct": "x^2", "answer": "x² + C", "solution": "∫2x dx = x² + C."},

    # ===== РУССКИЙ ЯЗЫК =====
    {"id": "r1", "title": "Безударная гласная", "subject": "Русский язык", "grade": "2", "type": "Классная", "question": "Вставьте букву: в_да (проверочное — воды)", "correct": "вода", "answer": "вода", "solution": "Проверяем: вОды → вода."},
    {"id": "r2", "title": "Парные согласные", "subject": "Русский язык", "grade": "2", "type": "ДЗ", "question": "Вставьте букву: зу_ (проверочное — зубы)", "correct": "зуб", "answer": "зуб", "solution": "Проверяем: зубы → зуб."},
    {"id": "r3", "title": "Словарное слово", "subject": "Русский язык", "grade": "3", "type": "Классная", "question": "Как пишется: к_рова или карова?", "correct": "корова", "answer": "корова", "solution": "Словарное слово — корова."},
    {"id": "r4", "title": "Части речи", "subject": "Русский язык", "grade": "3", "type": "ДЗ", "question": "Какая часть речи слово «бежит»?", "correct": "глагол", "answer": "глагол", "solution": "Отвечает на вопрос «что делает?» — глагол."},
    {"id": "r5", "title": "Приставки и предлоги", "subject": "Русский язык", "grade": "4", "type": "Классная", "question": "Как пишется: (на)столе?", "correct": "на столе", "answer": "на столе", "solution": "Предлог с существительным — раздельно."},
    {"id": "r6", "title": "Спряжение глаголов", "subject": "Русский язык", "grade": "5", "type": "ДЗ", "question": "Какое спряжение у глагола «смотреть»?", "correct": "2", "answer": "2-е спряжение", "solution": "Смотреть — исключение, 2-е спряжение."},
    {"id": "r7", "title": "Н и НН", "subject": "Русский язык", "grade": "7", "type": "Классная", "question": "Сколько Н: «кожа_ый»?", "correct": "1", "answer": "кожаный (одна Н)", "solution": "В отымённых прилагательных с суффиксом -ан-/-ян- пишется одна Н."},
    {"id": "r8", "title": "Причастие", "subject": "Русский язык", "grade": "7", "type": "ДЗ", "question": "Какое слово — причастие: «читающий» или «читать»?", "correct": "читающий", "answer": "читающий", "solution": "Причастие отвечает на «какой?» — читающий."},

    # ===== ФИЗИКА =====
    {"id": "f1", "title": "Скорость", "subject": "Физика", "grade": "7", "type": "Классная", "question": "Тело прошло 300 м за 20 с. Найдите скорость.", "correct": "15", "answer": "15 м/с", "solution": "v = S/t = 300/20 = 15 м/с."},
    {"id": "f2", "title": "Плотность", "subject": "Физика", "grade": "7", "type": "ДЗ", "question": "Масса 2 кг, объём 0.001 м³. Найдите плотность.", "correct": "2000", "answer": "2000 кг/м³", "solution": "ρ = m/V = 2 / 0.001 = 2000 кг/м³."},
    {"id": "f3", "title": "Сила тяжести", "subject": "Физика", "grade": "7", "type": "Классная", "question": "Масса 5 кг. Найдите силу тяжести (g = 10).", "correct": "50", "answer": "50 Н", "solution": "F = mg = 5 × 10 = 50 Н."},
    {"id": "f4", "title": "Давление", "subject": "Физика", "grade": "7", "type": "ДЗ", "question": "Сила 100 Н на площадь 0.5 м². Найдите давление.", "correct": "200", "answer": "200 Па", "solution": "p = F/S = 100 / 0.5 = 200 Па."},
    {"id": "f5", "title": "Закон Ома", "subject": "Физика", "grade": "8", "type": "Классная", "question": "U = 12 В, R = 4 Ом. Найдите силу тока.", "correct": "3", "answer": "3 А", "solution": "I = U/R = 12/4 = 3 А."},
    {"id": "f6", "title": "Мощность тока", "subject": "Физика", "grade": "8", "type": "ДЗ", "question": "U = 220 В, I = 0.5 А. Найдите мощность.", "correct": "110", "answer": "110 Вт", "solution": "P = U × I = 220 × 0.5 = 110 Вт."},
    {"id": "f7", "title": "Кинетическая энергия", "subject": "Физика", "grade": "9", "type": "Классная", "question": "m = 2 кг, v = 3 м/с. Найдите Ek.", "correct": "9", "answer": "9 Дж", "solution": "Ek = mv²/2 = 2 × 9 / 2 = 9 Дж."},
    {"id": "f8", "title": "Закон сохранения импульса", "subject": "Физика", "grade": "9", "type": "ДЗ", "question": "m = 2 кг, v = 5 м/с. Найдите импульс.", "correct": "10", "answer": "10 кг·м/с", "solution": "p = mv = 2 × 5 = 10 кг·м/с."},
    {"id": "f9", "title": "Уравнение состояния газа", "subject": "Физика", "grade": "10", "type": "Классная", "question": "p = 100 кПа, V = 2 м³, T = 300 К. Найдите ν (R = 8.31).", "correct": "80.2", "answer": "≈ 80.2 моль", "solution": "ν = pV / (RT) = 100000 × 2 / (8.31 × 300) ≈ 80.2 моль."},
    {"id": "f10", "title": "Электростатика", "subject": "Физика", "grade": "10", "type": "ДЗ", "question": "q = 2 × 10⁻⁶ Кл, U = 100 В. Найдите работу.", "correct": "0.0002", "answer": "2 × 10⁻⁴ Дж", "solution": "A = qU = 2 × 10⁻⁶ × 100 = 2 × 10⁻⁴ Дж."},

    # ===== ХИМИЯ =====
    {"id": "c1", "title": "Молярная масса", "subject": "Химия", "grade": "8", "type": "Классная", "question": "Молярная масса H₂O?", "correct": "18", "answer": "18 г/моль", "solution": "M(H₂O) = 2×1 + 16 = 18 г/моль."},
    {"id": "c2", "title": "Количество вещества", "subject": "Химия", "grade": "8", "type": "ДЗ", "question": "Масса 36 г воды. Сколько это моль?", "correct": "2", "answer": "2 моль", "solution": "n = m/M = 36/18 = 2 моль."},
    {"id": "c3", "title": "Валентность", "subject": "Химия", "grade": "8", "type": "Классная", "question": "Валентность кислорода в H₂O?", "correct": "2", "answer": "II", "solution": "Кислород двухвалентен."},
    {"id": "c4", "title": "Уравнение реакции", "subject": "Химия", "grade": "9", "type": "ДЗ", "question": "Расставьте коэффициенты: H₂ + O₂ → H₂O", "correct": "2h2+o2=2h2o", "answer": "2H₂ + O₂ = 2H₂O", "solution": "2H₂ + O₂ = 2H₂O."},
    {"id": "c5", "title": "Молярный объём газа", "subject": "Химия", "grade": "9", "type": "Классная", "question": "Какой объём занимают 2 моль газа (н.у.)?", "correct": "44.8", "answer": "44.8 л", "solution": "V = n × 22.4 = 2 × 22.4 = 44.8 л."},

    # ===== БИОЛОГИЯ =====
    {"id": "b1", "title": "Строение клетки", "subject": "Биология", "grade": "5", "type": "Классная", "question": "Какой органоид отвечает за фотосинтез?", "correct": "хлоропласт", "answer": "хлоропласт", "solution": "Фотосинтез идёт в хлоропластах (содержат хлорофилл)."},
    {"id": "b2", "title": "Царства природы", "subject": "Биология", "grade": "5", "type": "ДЗ", "question": "К какому царству относится гриб?", "correct": "грибы", "answer": "Царство Грибы", "solution": "Грибы — отдельное царство."},
    {"id": "b3", "title": "Кровообращение", "subject": "Биология", "grade": "8", "type": "Классная", "question": "Сколько камер в сердце человека?", "correct": "4", "answer": "4 камеры", "solution": "Два предсердия и два желудочка."},
    {"id": "b4", "title": "Фотосинтез", "subject": "Биология", "grade": "6", "type": "ДЗ", "question": "Какой газ выделяется при фотосинтезе?", "correct": "кислород", "answer": "Кислород (O₂)", "solution": "6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂."},

    # ===== ИНФОРМАТИКА =====
    {"id": "i1", "title": "Системы счисления", "subject": "Информатика", "grade": "8", "type": "Классная", "question": "Переведите 5 из 10-й в 2-ю систему.", "correct": "101", "answer": "101", "solution": "5 = 4 + 1 = 101₂."},
    {"id": "i2", "title": "Биты и байты", "subject": "Информатика", "grade": "7", "type": "ДЗ", "question": "Сколько бит в 1 байте?", "correct": "8", "answer": "8 бит", "solution": "1 байт = 8 бит."},
    {"id": "i3", "title": "Алгоритмы", "subject": "Информатика", "grade": "8", "type": "Классная", "question": "Сколько раз выполнится цикл: for i in range(5)?", "correct": "5", "answer": "5 раз", "solution": "range(5) даёт 0,1,2,3,4 — 5 итераций."},
    {"id": "i4", "title": "Python", "subject": "Информатика", "grade": "9", "type": "ДЗ", "question": "Что выведет: print(2 ** 3)?", "correct": "8", "answer": "8", "solution": "** — возведение в степень. 2³ = 8."},

    # ===== АНГЛИЙСКИЙ =====
    {"id": "e1", "title": "To be", "subject": "Английский язык", "grade": "3", "type": "Классная", "question": "Вставьте: I ___ a student.", "correct": "am", "answer": "am", "solution": "I + am."},
    {"id": "e2", "title": "Present Simple", "subject": "Английский язык", "grade": "4", "type": "ДЗ", "question": "Вставьте: She ___ (go) to school.", "correct": "goes", "answer": "goes", "solution": "3-е лицо ед. ч. — добавляем -es."},
    {"id": "e3", "title": "Past Simple", "subject": "Английский язык", "grade": "5", "type": "Классная", "question": "Вставьте: Yesterday I ___ (watch) TV.", "correct": "watched", "answer": "watched", "solution": "Правильный глагол → +ed."},
    {"id": "e4", "title": "Артикли", "subject": "Английский язык", "grade": "5", "type": "ДЗ", "question": "Вставьте: This is ___ apple.", "correct": "an", "answer": "an", "solution": "Перед гласной — an."},

    # ===== ИСТОРИЯ =====
    {"id": "h1", "title": "Древняя Русь", "subject": "История", "grade": "6", "type": "Классная", "question": "В каком году произошло Крещение Руси?", "correct": "988", "answer": "988 год", "solution": "Крещение Руси — 988 г., князь Владимир."},
    {"id": "h2", "title": "Куликовская битва", "subject": "История", "grade": "6", "type": "ДЗ", "question": "В каком году была Куликовская битва?", "correct": "1380", "answer": "1380 год", "solution": "8 сентября 1380 г."},
    {"id": "h3", "title": "Отечественная война", "subject": "История", "grade": "8", "type": "Классная", "question": "В каком году началась Отечественная война с Наполеоном?", "correct": "1812", "answer": "1812 год", "solution": "12 июня 1812 г."},
]


# ============ HTML ============
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Олимпиады, конкурсы и задания 2026–2027</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5; min-height: 100vh; padding: 20px; color: #1a1a1a;
        }
        .container {
            max-width: 1300px; margin: 0 auto; background: #fff;
            border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); overflow: hidden;
        }
        header { background: #1a1a1a; color: #fff; padding: 30px 40px; text-align: center; }
        header h1 { font-size: 1.9em; margin-bottom: 8px; }
        header p { opacity: 0.75; font-size: 15px; }
        .tabs { display: flex; background: #fafafa; border-bottom: 1px solid #e0e0e0; flex-wrap: wrap; }
        .tab {
            padding: 18px 30px; cursor: pointer; font-size: 15px; font-weight: 600;
            color: #666; border-bottom: 3px solid transparent; transition: all 0.2s; user-select: none;
        }
        .tab:hover { background: #f0f0f0; color: #1a1a1a; }
        .tab.active { color: #1a1a1a; border-bottom-color: #1a1a1a; background: #fff; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .filters {
            padding: 20px 40px; background: #fafafa; border-bottom: 1px solid #e8e8e8;
            display: flex; flex-wrap: wrap; gap: 12px; align-items: center;
        }
        .filters select, .filters input {
            padding: 10px 14px; border: 1.5px solid #d0d0d0; border-radius: 6px;
            font-size: 14px; outline: none; background: #fff; color: #1a1a1a;
        }
        .filters select:focus, .filters input:focus { border-color: #1a1a1a; }
        .filters input { flex: 1; min-width: 200px; }
        .stats {
            padding: 12px 40px; background: #f0f0f0; color: #555;
            font-size: 14px; border-bottom: 1px solid #e0e0e0;
        }
        .stats b { color: #1a1a1a; }
        table { width: 100%; border-collapse: collapse; }
        thead { background: #f7f7f7; }
        th {
            padding: 14px 16px; text-align: left; font-size: 12px;
            text-transform: uppercase; letter-spacing: 0.6px; color: #777;
            border-bottom: 2px solid #e0e0e0; font-weight: 700;
        }
        td { padding: 14px 16px; border-bottom: 1px solid #ededed; font-size: 14px; vertical-align: top; }
        tr:hover td { background: #fafafa; }
        .badge {
            display: inline-block; padding: 4px 10px; border-radius: 4px;
            font-size: 11.5px; font-weight: 600; white-space: nowrap; border: 1px solid;
        }
        .badge-olymp { background: #1a1a1a; color: #fff; border-color: #1a1a1a; }
        .badge-contest { background: #fff; color: #1a1a1a; border-color: #1a1a1a; }
        .badge-level-1 { background: #1a1a1a; color: #fff; border-color: #1a1a1a; }
        .badge-level-2 { background: #e0e0e0; color: #1a1a1a; border-color: #b0b0b0; }
        .badge-level-other { background: #fff; color: #555; border-color: #b0b0b0; }
        a.link {
            color: #1a1a1a; text-decoration: none; font-weight: 500;
            border-bottom: 1px solid #999;
        }
        a.link:hover { border-bottom-color: #1a1a1a; }
        .no-results { padding: 60px; text-align: center; color: #999; font-size: 16px; display: none; }

        /* ===== ЗАДАНИЯ ===== */
        .task-card {
            border: 1.5px solid #e0e0e0; border-radius: 10px;
            padding: 20px; margin: 16px 40px; background: #fafafa;
        }
        .task-card h3 { font-size: 17px; margin-bottom: 10px; }
        .task-meta { font-size: 13px; color: #666; margin-bottom: 12px; }
        .task-question { font-size: 15px; margin-bottom: 14px; line-height: 1.5; }
        .task-answer-input {
            padding: 10px 14px; border: 1.5px solid #d0d0d0; border-radius: 6px;
            font-size: 14px; width: 200px; margin-right: 10px;
        }
        .task-answer-input:focus { border-color: #1a1a1a; outline: none; }
        .btn {
            padding: 10px 20px; border: 1.5px solid #1a1a1a; background: #1a1a1a;
            color: #fff; border-radius: 6px; font-size: 14px; cursor: pointer;
            font-weight: 600; transition: all 0.2s;
        }
        .btn:hover { background: #fff; color: #1a1a1a; }
        .btn-outline { background: #fff; color: #1a1a1a; }
        .btn-outline:hover { background: #1a1a1a; color: #fff; }
        .result { margin-top: 14px; padding: 12px 16px; border-radius: 6px; font-size: 14px; display: none; }
        .result.ok { background: #e8f5e9; border: 1.5px solid #4caf50; color: #1b5e20; display: block; }
        .result.bad { background: #ffebee; border: 1.5px solid #f44336; color: #b71c1c; display: block; }
        .solution {
            margin-top: 12px; padding: 12px 16px; background: #f0f0f0;
            border-radius: 6px; font-size: 14px; line-height: 1.5; display: none;
        }
        .solution.show { display: block; }

        .upload-block {
            padding: 30px 40px; background: #fafafa;
            border-bottom: 1px solid #e8e8e8;
        }
        .upload-block h3 { font-size: 17px; margin-bottom: 14px; }
        .upload-block input[type="text"], .upload-block select, .upload-block textarea {
            padding: 10px 14px; border: 1.5px solid #d0d0d0; border-radius: 6px;
            font-size: 14px; width: 100%; margin-bottom: 10px; font-family: inherit;
        }
        .upload-block textarea { min-height: 70px; resize: vertical; }
        .upload-block input[type="file"] { margin-bottom: 10px; }

        footer {
            padding: 20px 40px; background: #f7f7f7; text-align: center;
            color: #777; font-size: 13px; border-top: 1px solid #e0e0e0;
        }

        @media (max-width: 800px) {
            header { padding: 20px; }
            header h1 { font-size: 1.3em; }
            .tab { padding: 14px 18px; font-size: 14px; }
            .filters, .stats, footer, .task-card, .upload-block { padding: 15px 20px; margin: 10px 15px; }
            th, td { padding: 10px 8px; font-size: 12px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Олимпиады, конкурсы и задания 2026–2027</h1>
            <p>Всё для школьников с 1 по 11 класс</p>
        </header>

        <div class="tabs">
            <div class="tab active" data-tab="olympiads">🏆 Олимпиады</div>
            <div class="tab" data-tab="education">📚 Обучение</div>
            <div class="tab" data-tab="tasks">📝 Задания и ответы</div>
        </div>

        <!-- ===== ОЛИМПИАДЫ ===== -->
        <div class="tab-content active" id="tab-olympiads">
            <div class="filters">
                <select id="filterClass">
                    <option value="">Все классы</option>
                    __CLASS_OPTIONS__
                </select>
                <select id="filterSubject">
                    <option value="">Все предметы</option>
                    __SUBJECT_OPTIONS__
                </select>
                <select id="filterType">
                    <option value="">Все типы</option>
                    <option value="Олимпиада">Олимпиады</option>
                    <option value="Конкурс">Конкурсы</option>
                </select>
                <input type="text" id="searchInput" placeholder="🔍 Поиск по названию...">
            </div>
            <div class="stats">Показано: <b id="count">__TOTAL__</b> из <b>__TOTAL__</b> мероприятий</div>
            <table>
                <thead>
                    <tr><th>Название</th><th>Тип</th><th>Предмет</th><th>Классы</th><th>Сроки</th><th>Уровень</th><th>Сайт</th></tr>
                </thead>
                <tbody id="tbody-olympiads">__ROWS_OLYMPIADS__</tbody>
            </table>
            <div class="no-results" id="noResults-olympiads">😔 Ничего не найдено.</div>
        </div>

        <!-- ===== ОБУЧЕНИЕ ===== -->
        <div class="tab-content" id="tab-education">
            <div class="filters">
                <select id="filterClassEdu">
                    <option value="">Все классы</option>
                    __CLASS_OPTIONS_EDU__
                </select>
                <select id="filterCategory">
                    <option value="">Все предметы</option>
                    __CATEGORY_OPTIONS__
                </select>
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
                <thead>
                    <tr><th>Название</th><th>Тип</th><th>Предмет</th><th>Классы</th><th>Сайт</th></tr>
                </thead>
                <tbody id="tbody-education">__ROWS_EDUCATION__</tbody>
            </table>
            <div class="no-results" id="noResults-education">😔 Ничего не найдено.</div>
        </div>

        <!-- ===== ЗАДАНИЯ ===== -->
        <div class="tab-content" id="tab-tasks">
            <div class="filters">
                <select id="filterTaskClass">
                    <option value="">Все классы</option>
                    __CLASS_OPTIONS_TASK__
                </select>
                <select id="filterTaskSubject">
                    <option value="">Все предметы</option>
                    __TASK_SUBJECT_OPTIONS__
                </select>
                <select id="filterTaskType">
                    <option value="">Все типы</option>
                    <option value="ДЗ">ДЗ</option>
                    <option value="Классная">Классная работа</option>
                </select>
                <input type="text" id="searchInputTask" placeholder="🔍 Поиск по заданию...">
            </div>
            <div class="stats">Показано: <b id="countTask">__TOTAL_TASKS__</b> из <b>__TOTAL_TASKS__</b> заданий</div>

            <div id="tasks-list">__ROWS_TASKS__</div>
            <div class="no-results" id="noResults-tasks">😔 Ничего не найдено.</div>

            <!-- Форма загрузки своего задания -->
            <div class="upload-block">
                <h3>📤 Загрузить своё задание</h3>
                <p style="font-size:13px; color:#666; margin-bottom:12px;">
                    Если вы не нашли своё задание — отправьте его фото или текст, и оно появится в базе после проверки.
                </p>
                <form id="uploadForm" enctype="multipart/form-data">
                    <select name="subject" required>
                        <option value="">— Предмет —</option>
                        __TASK_SUBJECT_OPTIONS__
                    </select>
                    <select name="grade" required>
                        <option value="">— Класс —</option>
                        __CLASS_OPTIONS_TASK__
                    </select>
                    <select name="type" required>
                        <option value="">— Тип —</option>
                        <option value="ДЗ">ДЗ</option>
                        <option value="Классная">Классная работа</option>
                    </select>
                    <input type="text" name="title" placeholder="Название задания (например, ДЗ: Уравнения)" required>
                    <textarea name="question" placeholder="Текст задания (необязательно, если есть фото)" rows="3"></textarea>
                    <input type="file" name="photo" accept="image/*">
                    <button type="submit" class="btn">Отправить</button>
                </form>
                <div id="uploadResult" style="margin-top:14px;"></div>
            </div>
        </div>

        <footer>
            Данные носят справочный характер. Актуальные сроки уточняйте на официальных сайтах.
        </footer>
    </div>

    <script>
        // ===== ПЕРЕКЛЮЧЕНИЕ ВКЛАДОК =====
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', () => {
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                tab.classList.add('active');
                document.getElementById('tab-' + tab.dataset.tab).classList.add('active');
            });
        });

        // ===== ПРОВЕРКА ОТВЕТА =====
        function checkAnswer(taskId, correct, inputId, resultId, solutionId) {
            const input = document.getElementById(inputId);
            const result = document.getElementById(resultId);
            const solution = document.getElementById(solutionId);
            const userAnswer = (input.value || '').trim().toLowerCase().replace(/\\s+/g, '');
            const correctNorm = correct.toLowerCase().replace(/\\s+/g, '');
            const answerEl = document.getElementById('answer-' + taskId);
            const correctAnswer = answerEl ? answerEl.dataset.answer : '';

            if (!userAnswer) {
                result.className = 'result bad';
                result.textContent = '✏️ Введите ответ.';
                result.style.display = 'block';
                return;
            }

            if (userAnswer === correctNorm) {
                result.className = 'result ok';
                result.textContent = '✅ Правильно!';
            } else {
                result.className = 'result bad';
                result.textContent = '❌ Неправильно. Правильный ответ: ' + correctAnswer;
            }
            result.style.display = 'block';
            solution.classList.add('show');
        }

        function toggleSolution(id) {
            const el = document.getElementById(id);
            el.classList.toggle('show');
        }

        // ===== ФИЛЬТРЫ ОЛИМПИАД =====
        function gradeMatches(grades, cls) {
            const parts = grades.split('–');
            if (parts.length !== 2) return true;
            return parseInt(cls) >= parseInt(parts[0]) && parseInt(cls) <= parseInt(parts[1]);
        }

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
                        if (f.type === 'exact') { if (row.dataset[f.key] !== val) ok = false; }
                        else if (f.type === 'grade') { if (!gradeMatches(row.dataset[f.key], val)) ok = false; }
                        else if (f.type === 'search') {
                            if (!row.dataset.name.toLowerCase().includes(val.toLowerCase().trim())) ok = false;
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

        setupFilter('#tasks-list .task-card', 'countTask', 'noResults-tasks', [
            {el: document.getElementById('filterTaskClass'), key: 'grade', type: 'exact'},
            {el: document.getElementById('filterTaskSubject'), key: 'subject', type: 'exact'},
            {el: document.getElementById('filterTaskType'), key: 'type', type: 'exact'},
            {el: document.getElementById('searchInputTask'), key: 'name', type: 'search'}
        ]);

        // ===== ЗАГРУЗКА СВОЕГО ЗАДАНИЯ =====
        document.getElementById('uploadForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const form = e.target;
            const formData = new FormData(form);
            const resultDiv = document.getElementById('uploadResult');
            resultDiv.innerHTML = '<p>⏳ Отправка...</p>';
            try {
                const resp = await fetch('/upload-task', { method: 'POST', body: formData });
                const data = await resp.json();
                if (data.ok) {
                    resultDiv.innerHTML = '<p style="color:#1b5e20;">✅ Задание отправлено! Оно появится в базе после проверки.</p>';
                    form.reset();
                } else {
                    resultDiv.innerHTML = '<p style="color:#b71c1c;">❌ ' + (data.error || 'Ошибка') + '</p>';
                }
            } catch (err) {
                resultDiv.innerHTML = '<p style="color:#b71c1c;">❌ Ошибка соединения</p>';
            }
        });
    </script>
</body>
</html>
"""


def build_olympiad_rows():
    rows = ""
    for o in OLYMPIADS:
        bt = "badge-olymp" if o["type"] == "Олимпиада" else "badge-contest"
        bl = "badge-level-1" if o["level"] == "Высший уровень" else ("badge-level-2" if o["level"] == "Повышенный уровень" else "badge-level-other")
        rows += f"""
        <tr data-name="{o['name']}" data-grades="{o['grades']}" data-subject="{o['subject']}" data-type="{o['type']}">
            <td><b>{o['name']}</b></td>
            <td><span class="badge {bt}">{o['type']}</span></td>
            <td>{o['subject']}</td>
            <td>{o['grades']}</td>
            <td>{o['date']}</td>
            <td><span class="badge {bl}">{o['level']}</span></td>
            <td><a class="link" href="{o['url']}" target="_blank">Перейти →</a></td>
        </tr>"""
    return rows


def build_education_rows():
    rows = ""
    for e in EDUCATION:
        bt = "badge-contest" if e["type"] in ("Курсы", "Видеокурс") else "badge-level-2"
        rows += f"""
        <tr data-name="{e['name']}" data-grades="{e['grades']}" data-category="{e['category']}" data-type="{e['type']}">
            <td><b>{e['name']}</b></td>
            <td><span class="badge {bt}">{e['type']}</span></td>
            <td>{e['category']}</td>
            <td>{e['grades']}</td>
            <td><a class="link" href="{e['url']}" target="_blank">Перейти →</a></td>
        </tr>"""
    return rows


def build_task_cards():
    cards = ""
    for t in TASKS:
        bt = "badge-olymp" if t["type"] == "ДЗ" else "badge-contest"
        input_id = f"input-{t['id']}"
        result_id = f"result-{t['id']}"
        solution_id = f"solution-{t['id']}"
        correct_safe = t["correct"].replace("'", "\\'")
        cards += f"""
        <div class="task-card" data-name="{t['title']} {t['question']}" data-grade="{t['grade']}" data-subject="{t['subject']}" data-type="{t['type']}">
            <h3>{t['title']}</h3>
            <div class="task-meta">
                <span class="badge {bt}">{t['type']}</span>
                &nbsp; {t['subject']} · {t['grade']} класс
            </div>
            <div class="task-question">{t['question']}</div>
            <input type="text" class="task-answer-input" id="{input_id}" placeholder="Ваш ответ...">
            <button class="btn" onclick="checkAnswer('{t['id']}', '{correct_safe}', '{input_id}', '{result_id}', '{solution_id}')">Проверить</button>
            <button class="btn btn-outline" onclick="toggleSolution('{solution_id}')">Показать решение</button>
            <div class="result" id="{result_id}"></div>
            <div class="solution" id="{solution_id}">
                <b>Правильный ответ:</b> <span id="answer-{t['id']}" data-answer="{t['answer']}">{t['answer']}</span><br><br>
                <b>Решение:</b> {t['solution']}
            </div>
        </div>"""
    return cards


def build_options(items):
    return "".join(f'<option value="{i}">{i}</option>' for i in sorted(set(items)))


# ============ FASTAPI ============
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    class_opts = "".join(f'<option value="{i}">{i} класс</option>' for i in range(1, 12))
    html = HTML_TEMPLATE
    html = html.replace("__CLASS_OPTIONS__", class_opts)
    html = html.replace("__CLASS_OPTIONS_EDU__", class_opts)
    html = html.replace("__CLASS_OPTIONS_TASK__", class_opts)
    html = html.replace("__SUBJECT_OPTIONS__", build_options([o["subject"] for o in OLYMPIADS]))
    html = html.replace("__CATEGORY_OPTIONS__", build_options([e["category"] for e in EDUCATION]))
    html = html.replace("__TASK_SUBJECT_OPTIONS__", build_options([t["subject"] for t in TASKS]))
    html = html.replace("__ROWS_OLYMPIADS__", build_olympiad_rows())
    html = html.replace("__ROWS_EDUCATION__", build_education_rows())
    html = html.replace("__ROWS_TASKS__", build_task_cards())
    html = html.replace("__TOTAL__", str(len(OLYMPIADS)))
    html = html.replace("__TOTAL_EDU__", str(len(EDUCATION)))
    html = html.replace("__TOTAL_TASKS__", str(len(TASKS)))
    return HTMLResponse(content=html)


@app.post("/upload-task")
async def upload_task(
    subject: str = Form(...),
    grade: str = Form(...),
    type: str = Form(...),
    title: str = Form(...),
    question: str = Form(""),
    photo: UploadFile = File(None),
):
    try:
        photo_name = ""
        if photo and photo.filename:
            ext = os.path.splitext(photo.filename)[1] or ".jpg"
            photo_name = f"{uuid.uuid4().hex}{ext}"
            with open(os.path.join(UPLOAD_DIR, photo_name), "wb") as f:
                f.write(await photo.read())

        # Сохраняем в текстовый файл как заявку
        with open("pending_tasks.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()} | {subject} | {grade} | {type} | {title} | {photo_name} | {question}\n")

        return JSONResponse({"ok": True})
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)})


# ============ ЗАПУСК ============
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)