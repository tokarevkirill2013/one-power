from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
import uvicorn
import os
import webbrowser
import threading
import time
import requests
import random
import math
import socket
import subprocess
import json
import sys

app = FastAPI(title="Городской гид")

# Создаём папку для шаблонов
os.makedirs("templates", exist_ok=True)

templates = Jinja2Templates(directory="templates")

# ============================================
# РЕКЛАМА
# ============================================
ads = [
    {"id": 1, "title": "Пятёрочка", "desc": "Скидки до 50% на товары!", "link": "https://5ka.ru", "image": "🛒",
     "color": "linear-gradient(135deg, #ed1c24, #d4141a)", "brand": "Пятёрочка"},
    {"id": 2, "title": "Магнит", "desc": "Выгодные цены на продукты!", "link": "https://magnit.ru", "image": "🛍️",
     "color": "linear-gradient(135deg, #0033a0, #002266)", "brand": "Магнит"},
    {"id": 3, "title": "Перекрёсток", "desc": "Доставка на дом за 1 час!", "link": "https://perekrestok.ru",
     "image": "🛒", "color": "linear-gradient(135deg, #00a651, #007a3d)", "brand": "Перекрёсток"},
    {"id": 4, "title": "Яндекс.Маркет", "desc": "Миллионы товаров по лучшим ценам!", "link": "https://market.yandex.ru",
     "image": "📦", "color": "linear-gradient(135deg, #ffcc00, #ff9900)", "brand": "Яндекс.Маркет"},
    {"id": 5, "title": "Ozon", "desc": "Скидки до 70% на тысячи товаров!", "link": "https://www.ozon.ru", "image": "📦",
     "color": "linear-gradient(135deg, #005bff, #0044cc)", "brand": "Ozon"},
    {"id": 6, "title": "Wildberries", "desc": "Мода, техника, товары для дома!", "link": "https://www.wildberries.ru",
     "image": "👗", "color": "linear-gradient(135deg, #e6007e, #cc0066)", "brand": "Wildberries"},
    {"id": 7, "title": "Avito", "desc": "Покупайте и продавайте рядом с вами!", "link": "https://www.avito.ru",
     "image": "🔍", "color": "linear-gradient(135deg, #00b81f, #008f16)", "brand": "Avito"},
    {"id": 8, "title": "AliExpress", "desc": "Товары со всего мира с бесплатной доставкой!",
     "link": "https://aliexpress.ru", "image": "🌏", "color": "linear-gradient(135deg, #ff6a00, #ee2d2d)",
     "brand": "AliExpress"},
    {"id": 9, "title": "Кинопоиск", "desc": "Тысячи фильмов. 30 дней бесплатно!", "link": "https://www.kinopoisk.ru",
     "image": "🎬", "color": "linear-gradient(135deg, #ffde17, #ffb800)", "brand": "Кинопоиск"},
    {"id": 10, "title": "VK Музыка", "desc": "Миллионы треков без рекламы!", "link": "https://music.vk.com",
     "image": "🎵", "color": "linear-gradient(135deg, #4a76a8, #2b5a8a)", "brand": "VK Музыка"}
]
random.shuffle(ads)

# ============================================
# ПОГОДА
# ============================================

weather_cache = {}
CACHE_TIME = 600

weather_codes = {
    0: {"text": "Ясно", "icon": "☀️"},
    1: {"text": "Преимущественно ясно", "icon": "🌤️"},
    2: {"text": "Переменная облачность", "icon": "⛅"},
    3: {"text": "Пасмурно", "icon": "☁️"},
    45: {"text": "Туман", "icon": "🌫️"},
    48: {"text": "Туман", "icon": "🌫️"},
    51: {"text": "Морось", "icon": "🌦️"},
    53: {"text": "Морось", "icon": "🌦️"},
    55: {"text": "Морось", "icon": "🌦️"},
    61: {"text": "Дождь", "icon": "🌧️"},
    63: {"text": "Дождь", "icon": "🌧️"},
    65: {"text": "Дождь", "icon": "🌧️"},
    71: {"text": "Снег", "icon": "❄️"},
    73: {"text": "Снег", "icon": "❄️"},
    75: {"text": "Снег", "icon": "❄️"},
    80: {"text": "Ливень", "icon": "🌧️"},
    81: {"text": "Ливень", "icon": "🌧️"},
    82: {"text": "Ливень", "icon": "🌧️"},
    95: {"text": "Гроза", "icon": "⛈️"},
    96: {"text": "Гроза", "icon": "⛈️"},
    99: {"text": "Гроза", "icon": "⛈️"},
}


def get_weather_openmeteo(city_name, lat, lng):
    cache_key = f"{city_name}_{lat}_{lng}"
    if cache_key in weather_cache:
        cache_data = weather_cache[cache_key]
        if time.time() - cache_data["time"] < CACHE_TIME:
            return cache_data["data"]

    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lng}&current_weather=true&hourly=temperature_2m,relative_humidity_2m,weathercode&daily=weathercode,sunrise,sunset,temperature_2m_max,temperature_2m_min&timezone=auto"
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            raise Exception(f"Ошибка API: {response.status_code}")

        data = response.json()
        current = data.get("current_weather", {})
        current_temp = current.get("temperature", 0)
        current_code = current.get("weathercode", 0)

        hourly = data.get("hourly", {})
        humidity = 50
        if hourly and "relative_humidity_2m" in hourly:
            humidity = hourly["relative_humidity_2m"][0] if hourly["relative_humidity_2m"] else 50

        daily = data.get("daily", {})
        week = []
        days = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]

        if daily and "temperature_2m_max" in daily and "weathercode" in daily:
            max_temps = daily["temperature_2m_max"][:7]
            min_temps = daily["temperature_2m_min"][:7] if "temperature_2m_min" in daily else max_temps
            codes = daily["weathercode"][:7]

            for i in range(len(max_temps)):
                code = codes[i] if i < len(codes) else 0
                weather_info = weather_codes.get(code, {"text": "Неизвестно", "icon": "🌤️"})
                week.append({
                    "day": days[i] if i < len(days) else f"Д{i + 1}",
                    "temp": round((max_temps[i] + min_temps[i]) / 2) if i < len(min_temps) else round(max_temps[i]),
                    "icon": weather_info["icon"]
                })

        if not week:
            for i in range(7):
                week.append({
                    "day": days[i] if i < len(days) else f"Д{i + 1}",
                    "temp": round(current_temp + i * 0.5),
                    "icon": "🌤️"
                })

        weather_info = weather_codes.get(current_code, {"text": "Неизвестно", "icon": "🌤️"})

        sunrise = "06:30"
        sunset = "20:45"
        if daily and "sunrise" in daily and daily["sunrise"]:
            sunrise = daily["sunrise"][0].split("T")[1][:5] if "T" in daily["sunrise"][0] else daily["sunrise"][0]
        if daily and "sunset" in daily and daily["sunset"]:
            sunset = daily["sunset"][0].split("T")[1][:5] if "T" in daily["sunset"][0] else daily["sunset"][0]

        weather_data = {
            "temp": round(current_temp),
            "feels_like": round(current_temp - 2 + (humidity > 70) * 1),
            "condition": weather_info["text"],
            "icon": weather_info["icon"],
            "humidity": humidity,
            "wind": round(current.get("windspeed", 3)),
            "pressure": 1013,
            "uv": 3,
            "sunrise": sunrise,
            "sunset": sunset,
            "week": week
        }

        weather_cache[cache_key] = {"time": time.time(), "data": weather_data}
        return weather_data

    except Exception as e:
        print(f"⚠️ Ошибка получения погоды для {city_name}: {e}")
        return get_fallback_weather(city_name)


def get_fallback_weather(city_name):
    import random
    conditions = ["Солнечно", "Облачно", "Дождь", "Снег", "Туман", "Ветрено"]
    icons = ["☀️", "⛅", "🌧️", "❄️", "🌫️", "💨"]
    days = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]
    return {
        "temp": random.randint(15, 25),
        "feels_like": random.randint(12, 22),
        "condition": random.choice(conditions),
        "icon": random.choice(icons),
        "humidity": random.randint(45, 85),
        "wind": random.randint(1, 8),
        "pressure": random.randint(1005, 1025),
        "uv": random.randint(2, 7),
        "sunrise": "06:30",
        "sunset": "20:45",
        "week": [{"day": days[i], "temp": random.randint(12, 25), "icon": random.choice(icons)} for i in range(7)]
    }


# ============================================
# ДАННЫЕ ПО ГОРОДАМ
# ============================================

russia_cities = [
    {"name": "Москва", "population": 13100000, "founded": "1147", "region": "Центральный", "lat": 55.7558,
     "lng": 37.6173, "description": "Столица России", "famous": "Кремль, Красная площадь, метро"},
    {"name": "Санкт-Петербург", "population": 5600000, "founded": "1703", "region": "Северо-Западный", "lat": 59.9343,
     "lng": 30.3351, "description": "Северная столица", "famous": "Эрмитаж, Дворцовая площадь, каналы"},
    {"name": "Новосибирск", "population": 1600000, "founded": "1893", "region": "Сибирский", "lat": 55.0084,
     "lng": 82.9357, "description": "Столица Сибири", "famous": "Академгородок, театр, Обь"},
    {"name": "Екатеринбург", "population": 1500000, "founded": "1723", "region": "Уральский", "lat": 56.8389,
     "lng": 60.6057, "description": "Столица Урала", "famous": "Граница Европа-Азия, Уралмаш"},
    {"name": "Казань", "population": 1300000, "founded": "1005", "region": "Приволжский", "lat": 55.7887,
     "lng": 49.1221, "description": "Столица Татарстана", "famous": "Кремль, мечеть Кул-Шариф"},
    {"name": "Нижний Новгород", "population": 1250000, "founded": "1221", "region": "Приволжский", "lat": 56.2965,
     "lng": 43.9361, "description": "Крупный промышленный центр", "famous": "Кремль, Волга, ярмарка"},
    {"name": "Челябинск", "population": 1200000, "founded": "1736", "region": "Уральский", "lat": 55.1644,
     "lng": 61.4368, "description": "Крупный промышленный центр Урала", "famous": "Южный Урал, металлургия"},
    {"name": "Самара", "population": 1150000, "founded": "1586", "region": "Приволжский", "lat": 53.1959,
     "lng": 50.1008, "description": "Крупный город на Волге", "famous": "Волга, ракеты, площадь"},
    {"name": "Омск", "population": 1150000, "founded": "1716", "region": "Сибирский", "lat": 54.9885, "lng": 73.3242,
     "description": "Крупный город в Западной Сибири", "famous": "Омская крепость, Иртыш"},
    {"name": "Ростов-на-Дону", "population": 1130000, "founded": "1749", "region": "Южный", "lat": 47.2221,
     "lng": 39.7203, "description": "Столица Юга России", "famous": "Дон, казачество"},
    {"name": "Уфа", "population": 1120000, "founded": "1574", "region": "Приволжский", "lat": 54.7348, "lng": 55.9579,
     "description": "Столица Башкортостана", "famous": "Башкирский мёд, Салават Юлаев"},
    {"name": "Красноярск", "population": 1090000, "founded": "1628", "region": "Сибирский", "lat": 56.0106,
     "lng": 92.8526, "description": "Крупнейший город Восточной Сибири", "famous": "Столбы, Енисей"},
    {"name": "Воронеж", "population": 1050000, "founded": "1586", "region": "Центральный", "lat": 51.6606,
     "lng": 39.2003, "description": "Крупный город Черноземья", "famous": "Петровский корабль, Терновка"},
    {"name": "Пермь", "population": 1050000, "founded": "1723", "region": "Приволжский", "lat": 58.0104, "lng": 56.2502,
     "description": "Крупный промышленный центр на Урале", "famous": "Пермский звериный стиль, Кама"},
    {"name": "Волгоград", "population": 1000000, "founded": "1589", "region": "Южный", "lat": 48.7080, "lng": 44.5133,
     "description": "Город-герой на Волге", "famous": "Мамаев курган, Родина-мать"},
    {"name": "Краснодар", "population": 950000, "founded": "1793", "region": "Южный", "lat": 45.0355, "lng": 38.9753,
     "description": "Столица Кубани", "famous": "Казачья культура, парки"},
    {"name": "Саратов", "population": 900000, "founded": "1590", "region": "Приволжский", "lat": 51.5336,
     "lng": 46.0342, "description": "Крупный город на Волге", "famous": "Волга, музеи"},
    {"name": "Тюмень", "population": 850000, "founded": "1586", "region": "Уральский", "lat": 57.1522, "lng": 65.5272,
     "description": "Столица Западной Сибири", "famous": "Нефть, горячие источники"},
    {"name": "Ижевск", "population": 650000, "founded": "1760", "region": "Приволжский", "lat": 56.8528, "lng": 53.2118,
     "description": "Столица Удмуртии", "famous": "Оружие, Калашников"},
    {"name": "Барнаул", "population": 630000, "founded": "1730", "region": "Сибирский", "lat": 53.3561, "lng": 83.7636,
     "description": "Крупный город на Алтае", "famous": "Горный Алтай, музеи"},
    {"name": "Ярославль", "population": 600000, "founded": "1010", "region": "Центральный", "lat": 57.6263,
     "lng": 39.8845, "description": "Жемчужина Золотого кольца", "famous": "Спасо-Преображенский монастырь, Волга"},
    {"name": "Владивосток", "population": 600000, "founded": "1860", "region": "Дальневосточный", "lat": 43.1155,
     "lng": 131.8855, "description": "Главный город Дальнего Востока", "famous": "Золотой мост, океан, порт"},
    {"name": "Иркутск", "population": 600000, "founded": "1661", "region": "Сибирский", "lat": 52.2864, "lng": 104.2807,
     "description": "Город на Байкале", "famous": "Озеро Байкал, исторический центр"},
    {"name": "Калининград", "population": 440000, "founded": "1255", "region": "Северо-Западный", "lat": 54.7104,
     "lng": 20.4522, "description": "Самый западный город России", "famous": "Янтарь, собор, море"},
    {"name": "Сочи", "population": 380000, "founded": "1838", "region": "Южный", "lat": 43.6028, "lng": 39.7341,
     "description": "Город-курорт, столица Олимпиады 2014", "famous": "Чёрное море, Кавказские горы"},
    {"name": "Тула", "population": 450000, "founded": "1146", "region": "Центральный", "lat": 54.1961, "lng": 37.6182,
     "description": "Город оружейников", "famous": "Пряники, оружие, Левша"},
    {"name": "Архангельск", "population": 320000, "founded": "1584", "region": "Северо-Западный", "lat": 64.5398,
     "lng": 40.5186, "description": "Город на Севере", "famous": "Морской порт, Северное сияние"},
    {"name": "Мурманск", "population": 230000, "founded": "1916", "region": "Северо-Западный", "lat": 68.9706,
     "lng": 33.0747, "description": "Самый крупный город за Полярным кругом", "famous": "Северное сияние, порт"},
    {"name": "Якутск", "population": 270000, "founded": "1632", "region": "Дальневосточный", "lat": 62.0281,
     "lng": 129.7325, "description": "Самый холодный крупный город в мире", "famous": "Вечная мерзлота, Лена"},
    {"name": "Владимир", "population": 310000, "founded": "1108", "region": "Центральный", "lat": 56.1290,
     "lng": 40.4070, "description": "Жемчужина Золотого кольца", "famous": "Успенский собор, Золотые ворота"},
    {"name": "Анапа", "population": 140000, "founded": "1781", "region": "Южный", "lat": 44.8951, "lng": 37.3163,
     "description": "Город-курорт на Черном море", "famous": "Санатории, пляжи, море"},
    {"name": "Армавир", "population": 210000, "founded": "1839", "region": "Южный", "lat": 44.9979, "lng": 41.1321,
     "description": "Город в Краснодарском крае", "famous": "Музеи, парки"},
    {"name": "Белгород", "population": 340000, "founded": "1596", "region": "Центральный", "lat": 50.5975,
     "lng": 36.5858, "description": "Город на границе с Украиной", "famous": "Белгородская черта, парки"},
    {"name": "Брянск", "population": 400000, "founded": "985", "region": "Центральный", "lat": 53.2433, "lng": 34.3632,
     "description": "Древний город на Десне", "famous": "Парк-музей, храмы"},
    {"name": "Великий Новгород", "population": 80000, "founded": "859", "region": "Северо-Западный", "lat": 58.5214,
     "lng": 31.2755, "description": "Древний город, колыбель российской государственности",
     "famous": "Софийский собор, Кремль"},
    {"name": "Владикавказ", "population": 240000, "founded": "1784", "region": "Южный", "lat": 43.0207, "lng": 44.6820,
     "description": "Столица Северной Осетии", "famous": "Горы, осетинские пироги"},
    {"name": "Вологда", "population": 280000, "founded": "1147", "region": "Северо-Западный", "lat": 59.2203,
     "lng": 39.8915, "description": "Город на Севере", "famous": "Вологодское кружево, масло"},
    {"name": "Грозный", "population": 230000, "founded": "1818", "region": "Южный", "lat": 43.3180, "lng": 45.6980,
     "description": "Столица Чечни", "famous": "Мечеть, современный город"},
    {"name": "Иваново", "population": 400000, "founded": "1871", "region": "Центральный", "lat": 57.0003,
     "lng": 40.9739, "description": "Текстильная столица России", "famous": "Текстиль, музеи"},
    {"name": "Калуга", "population": 300000, "founded": "1371", "region": "Центральный", "lat": 54.5138, "lng": 36.2614,
     "description": "Колыбель космонавтики", "famous": "Музей космонавтики, Циолковский"},
    {"name": "Кемерово", "population": 550000, "founded": "1721", "region": "Сибирский", "lat": 55.3549, "lng": 86.0873,
     "description": "Столица Кузбасса", "famous": "Уголь, промышленность"},
    {"name": "Киров", "population": 480000, "founded": "1374", "region": "Приволжский", "lat": 58.6035, "lng": 49.6680,
     "description": "Древний город на Вятке", "famous": "Вятская игрушка, дымковская"},
    {"name": "Курган", "population": 220000, "founded": "1679", "region": "Уральский", "lat": 55.4409, "lng": 65.3411,
     "description": "Город в Зауралье", "famous": "Машиностроение"},
    {"name": "Курск", "population": 400000, "founded": "1032", "region": "Центральный", "lat": 51.7304, "lng": 36.1926,
     "description": "Город воинской славы", "famous": "Курская дуга, музеи"},
    {"name": "Липецк", "population": 500000, "founded": "1703", "region": "Центральный", "lat": 52.6080, "lng": 39.5965,
     "description": "Крупный промышленный центр", "famous": "Металлургия, парки"},
    {"name": "Махачкала", "population": 460000, "founded": "1844", "region": "Южный", "lat": 42.9849, "lng": 47.5046,
     "description": "Столица Дагестана", "famous": "Каспийское море, горы"},
    {"name": "Нальчик", "population": 250000, "founded": "1818", "region": "Южный", "lat": 43.4855, "lng": 43.6080,
     "description": "Столица Кабардино-Балкарии", "famous": "Курорт, горы"},
    {"name": "Новокузнецк", "population": 510000, "founded": "1618", "region": "Сибирский", "lat": 53.7592,
     "lng": 87.1216, "description": "Город металлургов", "famous": "Металлургия, шахты"},
    {"name": "Новороссийск", "population": 130000, "founded": "1838", "region": "Южный", "lat": 44.7166, "lng": 37.7746,
     "description": "Город-герой, порт", "famous": "Порт, море"},
    {"name": "Оренбург", "population": 530000, "founded": "1743", "region": "Приволжский", "lat": 51.7682,
     "lng": 55.0970, "description": "Город на границе Европы и Азии", "famous": "Пуховый платок, граница"},
    {"name": "Орел", "population": 290000, "founded": "1566", "region": "Центральный", "lat": 52.9700, "lng": 36.0629,
     "description": "Город на Оке", "famous": "Литературная столица, Тургенев"},
    {"name": "Пенза", "population": 510000, "founded": "1663", "region": "Приволжский", "lat": 53.1955, "lng": 45.0183,
     "description": "Культурный центр Поволжья", "famous": "Музеи, театры"},
    {"name": "Петрозаводск", "population": 260000, "founded": "1703", "region": "Северо-Западный", "lat": 61.7891,
     "lng": 34.3598, "description": "Столица Карелии", "famous": "Онежское озеро, Кижи"},
    {"name": "Псков", "population": 150000, "founded": "903", "region": "Северо-Западный", "lat": 57.8194,
     "lng": 28.3318, "description": "Древний город, один из старейших", "famous": "Кремль, древние храмы"},
    {"name": "Рязань", "population": 530000, "founded": "1095", "region": "Центральный", "lat": 54.6199, "lng": 39.7449,
     "description": "Древний город, столица Рязанского княжества", "famous": "Кремль, древние храмы"},
    {"name": "Севастополь", "population": 340000, "founded": "1783", "region": "Южный", "lat": 44.6166, "lng": 33.5254,
     "description": "Город-герой, база Черноморского флота", "famous": "Черное море, Херсонес"},
    {"name": "Симферополь", "population": 330000, "founded": "1784", "region": "Южный", "lat": 44.9521, "lng": 34.1023,
     "description": "Столица Крыма", "famous": "Горы, парки, история"},
    {"name": "Смоленск", "population": 290000, "founded": "863", "region": "Центральный", "lat": 54.7865,
     "lng": 31.8215, "description": "Город-щит России", "famous": "Кремль, храмы"},
    {"name": "Ставрополь", "population": 390000, "founded": "1777", "region": "Южный", "lat": 45.0448, "lng": 41.9691,
     "description": "Город на Ставропольской возвышенности", "famous": "Парки, горы"},
    {"name": "Сургут", "population": 300000, "founded": "1594", "region": "Уральский", "lat": 61.2543, "lng": 73.3973,
     "description": "Нефтяная столица России", "famous": "Нефть, холод, мосты"},
    {"name": "Тверь", "population": 370000, "founded": "1135", "region": "Центральный", "lat": 56.8587, "lng": 35.9176,
     "description": "Город на Волге, древняя столица Тверского княжества", "famous": "Волга, храмы"},
    {"name": "Тольятти", "population": 700000, "founded": "1737", "region": "Приволжский", "lat": 53.5078,
     "lng": 49.4204, "description": "Крупный город на Волге", "famous": "Автопром, Волга"},
    {"name": "Томск", "population": 520000, "founded": "1604", "region": "Сибирский", "lat": 56.4887, "lng": 84.9523,
     "description": "Старейший город Сибири", "famous": "Университеты, деревянное зодчество"},
    {"name": "Улан-Удэ", "population": 240000, "founded": "1666", "region": "Сибирский", "lat": 51.8335,
     "lng": 107.5841, "description": "Столица Бурятии", "famous": "Байкал, буддийские храмы"},
    {"name": "Ульяновск", "population": 620000, "founded": "1648", "region": "Приволжский", "lat": 54.3174,
     "lng": 48.4034, "description": "Родина Ленина", "famous": "Музеи, Волга"},
    {"name": "Чебоксары", "population": 450000, "founded": "1469", "region": "Приволжский", "lat": 56.1440,
     "lng": 47.2489, "description": "Столица Чувашии", "famous": "Волга, древняя культура"},
    {"name": "Чита", "population": 310000, "founded": "1653", "region": "Сибирский", "lat": 52.0330, "lng": 113.4990,
     "description": "Город в Забайкалье", "famous": "Забайкалье, история"},
    {"name": "Ялта", "population": 80000, "founded": "1837", "region": "Южный", "lat": 44.4958, "lng": 34.1663,
     "description": "Город-курорт в Крыму", "famous": "Южный берег Крыма, море"},
    {"name": "Нижний Тагил", "population": 350000, "founded": "1722", "region": "Уральский", "lat": 57.9190,
     "lng": 59.9651, "description": "Город на Урале", "famous": "Металлургия, танки"},
    {"name": "Назрань", "population": 150000, "founded": "1810", "region": "Южный", "lat": 43.2267, "lng": 44.7591,
     "description": "Столица Ингушетии", "famous": "Горы, традиции"},
    {"name": "Евпатория", "population": 100000, "founded": "1784", "region": "Южный", "lat": 45.1936, "lng": 33.3626,
     "description": "Город-курорт в Крыму", "famous": "Море, санатории"},
    {"name": "Геленджик", "population": 100000, "founded": "1831", "region": "Южный", "lat": 44.5607, "lng": 38.0803,
     "description": "Город-курорт на Черном море", "famous": "Пляжи, набережная"},
    {"name": "Суздаль", "population": 50000, "founded": "1024", "region": "Центральный", "lat": 56.4221, "lng": 40.4489,
     "description": "Жемчужина Золотого кольца", "famous": "Древние храмы, музеи"}
]

russia_cities.sort(key=lambda x: x["name"])

default_city = "Москва"

# ============================================
# ССЫЛКИ ДЛЯ ЭКСКУРСИЙ
# ============================================

tour_links = {
    "Москва": "https://www.mos.ru/afisha/excursions/",
    "Санкт-Петербург": "https://www.spb.ru/afisha/excursions/",
    "Новосибирск": "https://novosibirsk.ru/afisha/excursions/",
    "Екатеринбург": "https://ekaterinburg.ru/afisha/excursions/",
    "Казань": "https://www.kazan.ru/afisha/excursions/",
    "Нижний Новгород": "https://nn.ru/afisha/excursions/",
    "Челябинск": "https://chelyabinsk.ru/afisha/excursions/",
    "Самара": "https://samara.ru/afisha/excursions/",
    "Омск": "https://omsk.ru/afisha/excursions/",
    "Ростов-на-Дону": "https://rostov.ru/afisha/excursions/",
    "Уфа": "https://ufa.ru/afisha/excursions/",
    "Красноярск": "https://krasnoyarsk.ru/afisha/excursions/",
    "Воронеж": "https://voronezh.ru/afisha/excursions/",
    "Пермь": "https://perm.ru/afisha/excursions/",
    "Волгоград": "https://volgograd.ru/afisha/excursions/",
    "Краснодар": "https://krasnodar.ru/afisha/excursions/",
    "Саратов": "https://saratov.ru/afisha/excursions/",
    "Тюмень": "https://tyumen.ru/afisha/excursions/",
    "Ижевск": "https://izhevsk.ru/afisha/excursions/",
    "Барнаул": "https://barnaul.ru/afisha/excursions/",
    "Ярославль": "https://yaroslavl.ru/afisha/excursions/",
    "Владивосток": "https://vladivostok.ru/afisha/excursions/",
    "Иркутск": "https://irkutsk.ru/afisha/excursions/",
    "Калининград": "https://kaliningrad.ru/afisha/excursions/",
    "Сочи": "https://sochi.ru/afisha/excursions/",
    "Тула": "https://tula.ru/afisha/excursions/",
    "Архангельск": "https://arhangelsk.ru/afisha/excursions/",
    "Мурманск": "https://murmanck.ru/afisha/excursions/",
    "Якутск": "https://yakutsk.ru/afisha/excursions/",
    "Владимир": "https://vladimir.ru/afisha/excursions/",
    "Анапа": "https://anapa.ru/afisha/excursions/",
    "Армавир": "https://armavir.ru/afisha/excursions/",
    "Белгород": "https://belgorod.ru/afisha/excursions/",
    "Брянск": "https://bryansk.ru/afisha/excursions/",
    "Великий Новгород": "https://novgorod.ru/afisha/excursions/",
    "Владикавказ": "https://vladikavkaz.ru/afisha/excursions/",
    "Вологда": "https://vologda.ru/afisha/excursions/",
    "Грозный": "https://grozny.ru/afisha/excursions/",
    "Иваново": "https://ivanovo.ru/afisha/excursions/",
    "Калуга": "https://kaluga.ru/afisha/excursions/",
    "Кемерово": "https://kemerovo.ru/afisha/excursions/",
    "Киров": "https://kirov.ru/afisha/excursions/",
    "Курган": "https://kurgan.ru/afisha/excursions/",
    "Курск": "https://kursk.ru/afisha/excursions/",
    "Липецк": "https://lipetsk.ru/afisha/excursions/",
    "Махачкала": "https://makhachkala.ru/afisha/excursions/",
    "Нальчик": "https://nalchik.ru/afisha/excursions/",
    "Новокузнецк": "https://novokuznetsk.ru/afisha/excursions/",
    "Новороссийск": "https://novorossiysk.ru/afisha/excursions/",
    "Оренбург": "https://orenburg.ru/afisha/excursions/",
    "Орел": "https://orel.ru/afisha/excursions/",
    "Пенза": "https://penza.ru/afisha/excursions/",
    "Петрозаводск": "https://petrozavodsk.ru/afisha/excursions/",
    "Псков": "https://pskov.ru/afisha/excursions/",
    "Рязань": "https://ryazan.ru/afisha/excursions/",
    "Севастополь": "https://sevastopol.ru/afisha/excursions/",
    "Симферополь": "https://simferopol.ru/afisha/excursions/",
    "Смоленск": "https://smolensk.ru/afisha/excursions/",
    "Ставрополь": "https://stavropol.ru/afisha/excursions/",
    "Сургут": "https://surgut.ru/afisha/excursions/",
    "Тверь": "https://tver.ru/afisha/excursions/",
    "Тольятти": "https://tolyatti.ru/afisha/excursions/",
    "Томск": "https://tomsk.ru/afisha/excursions/",
    "Улан-Удэ": "https://ulan-ude.ru/afisha/excursions/",
    "Ульяновск": "https://ulyanovsk.ru/afisha/excursions/",
    "Чебоксары": "https://cheboksary.ru/afisha/excursions/",
    "Чита": "https://chita.ru/afisha/excursions/",
    "Ялта": "https://yalta.ru/afisha/excursions/",
    "Нижний Тагил": "https://n-tagil.ru/afisha/excursions/",
    "Назрань": "https://nazran.ru/afisha/excursions/",
    "Евпатория": "https://evpatoria.ru/afisha/excursions/",
    "Геленджик": "https://gelendzhik.ru/afisha/excursions/",
    "Суздаль": "https://suzdal.ru/afisha/excursions/"
}


# ============================================
# ФУНКЦИЯ ДЛЯ ЗАПУСКА NGROK
# ============================================

def start_ngrok(port=8000):
    """Запускает ngrok и возвращает публичный URL"""
    try:
        # Проверяем, установлен ли ngrok
        result = subprocess.run(['ngrok', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ ngrok не установлен!")
            print("📌 Установите ngrok:")
            print("   1. Скачайте с https://ngrok.com/download")
            print("   2. Распакуйте в папку с проектом")
            print("   3. Или добавьте в PATH")
            return None

        # Запускаем ngrok в фоновом режиме
        print("🔄 Запуск ngrok...")
        subprocess.Popen(['ngrok', 'http', str(port)],
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)

        # Ждём, пока ngrok запустится
        time.sleep(3)

        # Получаем публичный URL через API ngrok
        try:
            response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
            if response.status_code == 200:
                data = response.json()
                for tunnel in data.get('tunnels', []):
                    if tunnel.get('proto') == 'https':
                        public_url = tunnel.get('public_url')
                        if public_url:
                            return public_url
        except:
            pass

        # Если не удалось получить через API, пробуем через веб-интерфейс
        try:
            response = requests.get('http://localhost:4040/status', timeout=5)
            if response.status_code == 200:
                # Парсим HTML (простой способ)
                import re
                match = re.search(r'https://[a-f0-9]+\.ngrok\.io', response.text)
                if match:
                    return match.group(0)
        except:
            pass

        return None

    except Exception as e:
        print(f"❌ Ошибка запуска ngrok: {e}")
        return None


def get_local_ip():
    """Получает локальный IP-адрес компьютера в сети"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


# ============================================
# БАЗОВЫЙ HTML
# ============================================

BASE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Городской гид</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background: #1a1a1a; min-height: 100vh; }

        .app-wrapper { display: flex; min-height: 100vh; }

        .sidebar {
            width: 320px;
            background: #222;
            padding: 20px 15px;
            position: fixed;
            top: 0;
            left: 0;
            height: 100vh;
            overflow-y: auto;
            transition: all 0.3s ease;
            z-index: 1000;
            border-right: 1px solid #333;
        }
        .sidebar::-webkit-scrollbar { width: 4px; }
        .sidebar::-webkit-scrollbar-track { background: #2a2a2a; }
        .sidebar::-webkit-scrollbar-thumb { background: #555; border-radius: 2px; }

        .sidebar-brand { text-align: center; padding: 10px 0 20px 0; border-bottom: 2px solid #333; margin-bottom: 20px; }
        .sidebar-brand h2 { font-size: 1.3em; color: #fff; }
        .sidebar-brand h2 span { color: #888; }
        .sidebar-brand .subtitle { font-size: 0.75em; color: #666; margin-top: 2px; }

        .sidebar-search { margin-bottom: 15px; position: relative; }
        .sidebar-search input {
            width: 100%;
            padding: 10px 14px 10px 40px;
            border-radius: 10px;
            border: 2px solid #444;
            background: #2a2a2a;
            color: #fff;
            font-size: 0.9em;
            outline: none;
        }
        .sidebar-search input:focus { border-color: #888; background: #333; }
        .sidebar-search input::placeholder { color: #666; }
        .sidebar-search .search-icon {
            position: absolute;
            left: 12px;
            top: 50%;
            transform: translateY(-50%);
            color: #666;
            font-size: 1.1em;
        }
        .sidebar-search .clear-btn {
            position: absolute;
            right: 12px;
            top: 50%;
            transform: translateY(-50%);
            color: #666;
            font-size: 1.1em;
            cursor: pointer;
            display: none;
            background: none;
            border: none;
            color: #888;
        }
        .sidebar-search .clear-btn:hover { color: #fff; }
        .sidebar-search .clear-btn.visible { display: block; }

        .sidebar-city-list { max-height: calc(100vh - 350px); overflow-y: auto; margin-bottom: 15px; }
        .sidebar-city-list::-webkit-scrollbar { width: 4px; }
        .sidebar-city-list::-webkit-scrollbar-track { background: #2a2a2a; }
        .sidebar-city-list::-webkit-scrollbar-thumb { background: #555; border-radius: 2px; }

        .sidebar-city-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 12px;
            border-radius: 8px;
            color: #aaa;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.85em;
        }
        .sidebar-city-item:hover { background: #333; color: #fff; }
        .sidebar-city-item.active { background: #fff; color: #222; }
        .sidebar-city-item .pop { font-size: 0.7em; color: #666; }
        .sidebar-city-item.active .pop { color: #444; }

        .no-results { text-align: center; padding: 30px 20px; color: #666; font-size: 0.9em; }
        .no-results .big-icon { font-size: 2.5em; display: block; margin-bottom: 10px; }

        .sidebar-section-title {
            font-size: 0.7em;
            text-transform: uppercase;
            color: #555;
            font-weight: 700;
            letter-spacing: 1px;
            padding: 8px 12px;
            margin-top: 10px;
        }

        .sidebar-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 14px;
            border-radius: 10px;
            color: #aaa;
            text-decoration: none;
            transition: all 0.3s ease;
            cursor: pointer;
            font-weight: 500;
            font-size: 0.9em;
            margin: 2px 0;
        }
        .sidebar-item:hover { background: #333; color: #fff; transform: translateX(5px); }
        .sidebar-item.active { background: #fff; color: #222; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
        .sidebar-item .icon { font-size: 1.2em; width: 28px; text-align: center; }
        .sidebar-item .label { flex: 1; }
        .sidebar-item .badge { background: #666; color: #fff; font-size: 0.65em; padding: 2px 8px; border-radius: 12px; font-weight: 600; }

        .sidebar-footer {
            padding: 10px 14px;
            margin-top: 10px;
            border-top: 1px solid #333;
            font-size: 0.7em;
            color: #555;
            text-align: center;
        }

        .main-content {
            margin-left: 320px;
            flex: 1;
            padding: 25px 35px;
            min-height: 100vh;
            background: #f5f5f5;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: #fff;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
        }

        .page-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 2px solid #eee;
            flex-wrap: wrap;
            gap: 10px;
        }
        .page-header-left {
            display: flex;
            align-items: center;
            gap: 15px;
            flex-wrap: wrap;
        }
        .page-header h1 { font-size: 1.8em; color: #222; }
        .page-header .breadcrumb { font-size: 0.85em; color: #888; }
        .page-header .breadcrumb a { color: #222; text-decoration: none; }
        .page-header .breadcrumb a:hover { text-decoration: underline; }
        .page-header .breadcrumb span { color: #999; }

        .city-name-clickable {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: #f0f0f5;
            padding: 6px 16px 6px 18px;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 2px solid #ddd;
            font-weight: 600;
            font-size: 1em;
            color: #222;
            position: relative;
        }
        .city-name-clickable:hover {
            background: #e9ecef;
            border-color: #667eea;
            transform: scale(1.02);
        }
        .city-name-clickable .arrow {
            font-size: 0.7em;
            color: #888;
            transition: transform 0.3s ease;
            margin-left: 4px;
        }
        .city-name-clickable .arrow.open {
            transform: rotate(180deg);
        }

        .city-dropdown-left {
            display: none;
            position: absolute;
            top: calc(100% + 8px);
            left: 0;
            background: white;
            border-radius: 12px;
            box-shadow: 0 15px 50px rgba(0,0,0,0.15);
            border: 1px solid #eee;
            min-width: 220px;
            max-height: 350px;
            overflow-y: auto;
            z-index: 100;
            padding: 8px 0;
        }
        .city-dropdown-left.show { display: block; }
        .city-dropdown-left::-webkit-scrollbar { width: 4px; }
        .city-dropdown-left::-webkit-scrollbar-track { background: #f5f5f5; }
        .city-dropdown-left::-webkit-scrollbar-thumb { background: #ccc; border-radius: 2px; }

        .city-dropdown-left-item {
            padding: 10px 18px;
            color: #333;
            cursor: pointer;
            transition: all 0.2s ease;
            font-size: 0.9em;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .city-dropdown-left-item:hover { background: #f0f0f5; }
        .city-dropdown-left-item.active { background: #667eea; color: white; }
        .city-dropdown-left-item .pop-small { font-size: 0.7em; color: #888; }
        .city-dropdown-left-item.active .pop-small { color: rgba(255,255,255,0.7); }

        .city-select-wrapper-left {
            position: relative;
            display: inline-block;
        }

        .city-count { font-size: 0.8em; color: #888; margin-top: 5px; }

        .city-indicator {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 3px 15px;
            border-radius: 20px;
            font-size: 0.7em;
            font-weight: 600;
            margin-left: 10px;
        }

        .info-card {
            background: #f8f8f8;
            padding: 20px;
            border-radius: 15px;
            margin: 15px 0;
            border: 1px solid #eee;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .info-card:hover { transform: translateY(-2px); box-shadow: 0 5px 20px rgba(0,0,0,0.05); }
        .info-card h3 { color: #222; margin-bottom: 8px; font-size: 1.1em; }
        .info-card p { color: #555; line-height: 1.6; font-size: 0.95em; }
        .info-card ul { margin: 8px 15px; color: #555; }
        .info-card ul li { margin: 3px 0; }

        .city-highlight {
            background: linear-gradient(135deg, #f0f0f0, #e8e8e8);
            padding: 25px;
            border-radius: 15px;
            margin: 15px 0;
            border: 1px solid #ddd;
        }
        .city-highlight h2 { color: #222; margin-bottom: 10px; }
        .famous { display: flex; gap: 10px; flex-wrap: wrap; margin: 10px 0; }
        .famous-tag { background: #222; color: #fff; padding: 4px 15px; border-radius: 20px; font-size: 0.8em; }

        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 12px;
            margin: 15px 0;
        }
        .info-grid .info-item {
            background: #f8f8f8;
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            border: 1px solid #eee;
        }
        .info-grid .info-item .label { font-size: 0.7em; color: #888; text-transform: uppercase; letter-spacing: 0.5px; }
        .info-grid .info-item .value { font-size: 1.1em; font-weight: 600; color: #222; margin-top: 3px; }

        .weather-main {
            display: flex;
            align-items: center;
            gap: 25px;
            flex-wrap: wrap;
            padding: 15px 20px;
            background: #f8f8f8;
            border-radius: 15px;
            margin: 10px 0;
            border: 1px solid #eee;
        }
        .weather-main .icon { font-size: 3.5em; }
        .weather-main .temp { font-size: 2.5em; font-weight: 700; color: #222; }
        .weather-main .condition { font-size: 1.1em; color: #555; }
        .weather-main .details { font-size: 0.85em; color: #888; margin-top: 3px; }

        .weather-week {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 8px;
            margin: 10px 0;
        }
        .weather-day {
            background: #f8f8f8;
            padding: 12px 8px;
            border-radius: 10px;
            text-align: center;
            transition: all 0.3s ease;
            border: 1px solid #eee;
        }
        .weather-day:hover { transform: scale(1.05); background: #eee; }
        .weather-day .icon { font-size: 1.8em; }
        .weather-day .day { font-weight: 600; margin-bottom: 3px; font-size: 0.8em; color: #222; }
        .weather-day .temp { font-size: 1em; font-weight: 700; color: #222; }

        .city-weather-details {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 8px;
            padding: 12px;
            background: #f8f8f8;
            border-radius: 15px;
            margin: 10px 0;
            border: 1px solid #eee;
        }
        .city-weather-details .detail-item { text-align: center; padding: 5px; }
        .city-weather-details .detail-item .label { font-size: 0.7em; color: #888; }
        .city-weather-details .detail-item .value { font-size: 0.95em; font-weight: 600; color: #222; }

        .places-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 12px;
            margin: 10px 0;
        }
        .place-item {
            background: #f8f8f8;
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
            text-decoration: none;
            color: inherit;
            display: block;
            border: 1px solid #eee;
        }
        .place-item:hover { transform: translateY(-3px); box-shadow: 0 10px 30px rgba(0,0,0,0.1); background: #eee; }
        .place-item .icon { font-size: 2.2em; display: block; margin-bottom: 5px; }
        .place-item .name { font-weight: 600; font-size: 1em; color: #222; }
        .place-item .desc { font-size: 0.8em; color: #888; margin-top: 3px; }

        .place-detail {
            background: #f8f8f8;
            padding: 20px;
            border-radius: 15px;
            margin: 15px 0;
            border: 1px solid #eee;
        }
        .place-detail h2 { color: #222; margin-bottom: 10px; }
        .place-detail p { color: #555; line-height: 1.6; margin: 5px 0; }
        .place-detail .tour-btn {
            display: inline-block;
            padding: 10px 25px;
            background: #222;
            color: #fff;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
            font-size: 0.95em;
            margin-top: 10px;
            text-decoration: none;
        }
        .place-detail .tour-btn:hover { opacity: 0.8; transform: scale(1.05); }

        .map-container {
            width: 100%;
            height: 400px;
            border-radius: 15px;
            overflow: hidden;
            border: 2px solid #eee;
            margin: 10px 0;
        }
        .map-container iframe { width: 100%; height: 100%; border: none; }

        .map-controls {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin: 10px 0;
            padding: 12px 15px;
            background: #f8f8f8;
            border-radius: 12px;
            align-items: center;
            border: 1px solid #eee;
        }
        .map-controls label { font-weight: 600; font-size: 0.9em; color: #222; }
        .map-controls input {
            flex: 1;
            padding: 8px 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 0.9em;
            min-width: 150px;
            background: #fff;
        }
        .map-controls button {
            padding: 8px 20px;
            background: #222;
            color: #fff;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        .map-controls button:hover { opacity: 0.8; transform: scale(1.02); }
        .map-controls .location-btn { background: #444; }

        .history-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin: 15px 0;
        }
        .history-item {
            background: #f8f8f8;
            padding: 18px;
            border-radius: 15px;
            border: 1px solid #eee;
        }
        .history-item h3 { color: #222; margin-bottom: 8px; border-bottom: 2px solid #222; padding-bottom: 5px; }
        .history-item ul { list-style: none; padding: 0; }
        .history-item li { padding: 4px 0; color: #555; border-bottom: 1px solid #eee; font-size: 0.9em; }
        .history-item li:last-child { border-bottom: none; }

        .history-selector {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin: 10px 0;
            padding: 12px;
            background: #f8f8f8;
            border-radius: 12px;
            border: 1px solid #eee;
        }
        .history-selector .history-btn {
            padding: 8px 20px;
            border: 2px solid #ddd;
            border-radius: 20px;
            background: #fff;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
            font-size: 13px;
            color: #222;
        }
        .history-selector .history-btn:hover { transform: scale(1.05); border-color: #222; }
        .history-selector .history-btn.active { border-color: #222; background: #222; color: #fff; }

        .resources-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 12px;
            margin: 10px 0;
        }
        .resource-item {
            background: #f8f8f8;
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            transition: all 0.3s ease;
            border: 1px solid #eee;
        }
        .resource-item:hover { transform: translateY(-3px); box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
        .resource-item .name { font-weight: 600; font-size: 0.95em; color: #222; }
        .resource-item .desc { font-size: 0.8em; color: #888; margin: 5px 0; }
        .resource-item a { color: #222; text-decoration: none; font-weight: 500; }
        .resource-item a:hover { text-decoration: underline; }

        .back-link {
            display: inline-block;
            margin-top: 20px;
            padding: 10px 25px;
            background: #222;
            color: #fff;
            text-decoration: none;
            border-radius: 10px;
            transition: all 0.3s ease;
            border: none;
            cursor: pointer;
            font-size: 0.95em;
        }
        .back-link:hover { transform: scale(1.05); opacity: 0.8; }

        .ad-section {
            margin-top: 25px;
            padding-top: 15px;
            border-top: 2px solid #eee;
        }
        .ad-section-title {
            font-size: 0.8em;
            color: #888;
            text-align: center;
            margin-bottom: 10px;
            letter-spacing: 1px;
        }
        .ad-banner {
            position: relative;
            padding: 18px 20px;
            border-radius: 15px;
            color: #fff;
            text-align: center;
            min-height: 70px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            transition: all 0.8s ease;
            overflow: hidden;
            cursor: pointer;
        }
        .ad-banner:hover { transform: scale(1.01); }
        .ad-banner .ad-emoji { font-size: 2em; margin-bottom: 3px; }
        .ad-banner .ad-brand { 
            position: absolute;
            top: 6px;
            left: 12px;
            font-size: 0.6em;
            opacity: 0.7;
            background: rgba(0,0,0,0.2);
            padding: 2px 10px;
            border-radius: 10px;
            font-weight: 600;
            letter-spacing: 0.5px;
        }
        .ad-banner h3 { font-size: 1.1em; margin-bottom: 2px; color: #fff; }
        .ad-banner p { font-size: 0.85em; margin-bottom: 5px; opacity: 0.9; color: #ddd; }
        .ad-banner .ad-btn {
            display: inline-block;
            padding: 5px 20px;
            background: rgba(255,255,255,0.15);
            color: #fff;
            text-decoration: none;
            border-radius: 20px;
            font-weight: 600;
            transition: all 0.3s ease;
            border: 2px solid rgba(255,255,255,0.2);
            font-size: 0.8em;
        }
        .ad-banner .ad-btn:hover { background: rgba(255,255,255,0.3); transform: scale(1.05); }
        .ad-timer {
            position: absolute;
            top: 6px;
            right: 12px;
            font-size: 0.6em;
            opacity: 0.6;
            background: rgba(0,0,0,0.2);
            padding: 2px 8px;
            border-radius: 10px;
            color: #ddd;
        }
        .ad-dots {
            display: flex;
            gap: 5px;
            justify-content: center;
            margin-top: 5px;
        }
        .ad-dots .dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: rgba(255,255,255,0.3);
            cursor: pointer;
            transition: all 0.3s ease;
            border: none;
        }
        .ad-dots .dot:hover { transform: scale(1.2); }
        .ad-dots .dot.active { background: #fff; transform: scale(1.1); }

        .found-count {
            padding: 5px 12px;
            font-size: 0.75em;
            color: #666;
            text-align: center;
            margin-top: 5px;
        }

        .menu-toggle {
            display: none;
            position: fixed;
            top: 15px;
            left: 15px;
            z-index: 1001;
            background: #222;
            color: #fff;
            border: none;
            font-size: 1.5em;
            padding: 10px 14px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .menu-toggle:hover { transform: scale(1.05); }

        .sidebar-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.6);
            z-index: 999;
        }

        @media (max-width: 768px) {
            .menu-toggle { display: block; }
            .sidebar {
                transform: translateX(-100%);
                width: 300px;
            }
            .sidebar.open { transform: translateX(0); }
            .sidebar-overlay.active { display: block; }
            .main-content {
                margin-left: 0;
                padding: 60px 15px 15px 15px;
            }
            .container { padding: 20px; }
            .weather-week { grid-template-columns: repeat(4, 1fr); }
            .weather-main { flex-direction: column; text-align: center; gap: 5px; }
            .page-header { flex-direction: column; gap: 10px; align-items: flex-start; }
            .page-header h1 { font-size: 1.4em; }
            .history-selector { flex-direction: column; align-items: stretch; }
            .map-controls { flex-direction: column; align-items: stretch; }
            .places-grid { grid-template-columns: 1fr 1fr; }
            .sidebar-city-list { max-height: 200px; }
            .info-grid { grid-template-columns: 1fr 1fr; }
            .city-dropdown-left { min-width: 180px; }
            .ad-banner .ad-brand { display: none; }
            .city-name-clickable { font-size: 0.9em; padding: 4px 12px; }
        }

        @media (max-width: 480px) {
            .places-grid { grid-template-columns: 1fr; }
            .weather-week { grid-template-columns: repeat(3, 1fr); }
            .sidebar { width: 280px; }
            .info-grid { grid-template-columns: 1fr; }
            .ad-timer { display: none; }
            .city-dropdown-left { min-width: 160px; }
        }
    </style>
</head>
<body>
    <button class="menu-toggle" onclick="toggleSidebar()">☰</button>
    <div class="sidebar-overlay" id="sidebarOverlay" onclick="toggleSidebar()"></div>

    <div class="app-wrapper">
        <nav class="sidebar" id="sidebar">
            <div class="sidebar-brand">
                <h2>🏙️ <span>Городской гид</span></h2>
                <div class="subtitle">Все города России</div>
            </div>

            <div class="sidebar-search">
                <span class="search-icon">🔍</span>
                <input type="text" id="citySearch" placeholder="Поиск города..." oninput="filterCities()">
                <button class="clear-btn" id="clearBtn" onclick="clearSearch()">✕</button>
            </div>

            <div id="foundCount" class="found-count">Найдено: {{ cities|length }}</div>

            <div class="sidebar-city-list" id="cityList">
                {% for city in cities %}
                    <div class="sidebar-city-item {% if city == current_city %}active{% endif %}" 
                         data-city="{{ city }}" onclick="changeCity('{{ city }}')">
                        <span>{{ city }}</span>
                        <span class="pop">{{ city_data[city].population if city in city_data else '' }}</span>
                    </div>
                {% endfor %}
            </div>

            <div class="sidebar-section">
                <div class="sidebar-section-title">📋 Навигация</div>
                <a href="/" class="sidebar-item {% if current_path == '/' %}active{% endif %}">
                    <span class="icon">🏠</span>
                    <span class="label">О городе</span>
                </a>
                <a href="/weather" class="sidebar-item {% if current_path == '/weather' %}active{% endif %}">
                    <span class="icon">🌤️</span>
                    <span class="label">Погода</span>
                </a>
                <a href="/places" class="sidebar-item {% if current_path == '/places' %}active{% endif %}">
                    <span class="icon">📍</span>
                    <span class="label">Достопримечательности</span>
                </a>
                <a href="/map" class="sidebar-item {% if current_path == '/map' %}active{% endif %}">
                    <span class="icon">🗺️</span>
                    <span class="label">Карта города</span>
                </a>
                <a href="/history" class="sidebar-item {% if current_path == '/history' %}active{% endif %}">
                    <span class="icon">📜</span>
                    <span class="label">История</span>
                    <span class="badge">Новое</span>
                </a>
            </div>

            <div class="sidebar-footer">
                © 2026 Городской гид<br>
                {{ cities|length }} городов России
            </div>
        </nav>

        <main class="main-content">
            <div class="container">
                <div class="page-header">
                    <div class="page-header-left">
                        <h1>
                            {{ page_title|default('О городе') }}
                            <span class="city-indicator">📍</span>
                        </h1>
                        <div class="city-select-wrapper-left">
                            <span class="city-name-clickable" onclick="toggleCityDropdownLeft()">
                                <span>{{ current_city }}</span>
                                <span class="arrow" id="cityArrowLeft">▼</span>
                            </span>
                            <div class="city-dropdown-left" id="cityDropdownLeft">
                                {% for city in cities %}
                                    <div class="city-dropdown-left-item {% if city == current_city %}active{% endif %}" 
                                         onclick="selectCityFromLeft('{{ city }}')">
                                        <span>{{ city }}</span>
                                        <span class="pop-small">{{ city_data[city].population if city in city_data else '' }}</span>
                                    </div>
                                {% endfor %}
                            </div>
                        </div>
                        <div class="city-count">🏙️ Всего городов: {{ cities|length }}</div>
                    </div>
                    <div class="breadcrumb">
                        <a href="/">О городе</a>
                        {% if current_path != "/" %}
                            <span> → </span>
                            <span>{{ page_title|default(current_path) }}</span>
                        {% endif %}
                    </div>
                </div>

                {{ content|safe }}

                <div class="ad-section">
                    <div class="ad-section-title">— 🛍️ Рекламные предложения —</div>
                    <div class="ad-banner" id="adBanner" onclick="window.open(document.getElementById('adBtn').href, '_blank')">
                        <span class="ad-brand" id="adBrand">🏷️ Бренд</span>
                        <span class="ad-timer" id="adTimer">⏱️ 5 сек</span>
                        <div class="ad-emoji" id="adEmoji">🏙️</div>
                        <h3 id="adTitle">Добро пожаловать!</h3>
                        <p id="adDesc">Лучшие предложения в вашем городе</p>
                        <a href="#" class="ad-btn" id="adBtn" target="_blank">Узнать больше</a>
                        <div class="ad-dots" id="adDots"></div>
                    </div>
                </div>
            </div>
        </main>
    </div>

    <script>
        function getSavedCity() {
            try {
                var saved = localStorage.getItem('selectedCity');
                if (saved) return saved;
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = cookies[i].trim();
                    if (cookie.indexOf('selectedCity=') === 0) {
                        return cookie.substring('selectedCity='.length, cookie.length);
                    }
                }
                return null;
            } catch(e) { return null; }
        }

        function saveCity(city) {
            try {
                localStorage.setItem('selectedCity', city);
                var d = new Date();
                d.setTime(d.getTime() + (30 * 24 * 60 * 60 * 1000));
                document.cookie = 'selectedCity=' + city + '; expires=' + d.toUTCString() + '; path=/';
            } catch(e) {}
        }

        function toggleSidebar() {
            document.getElementById('sidebar').classList.toggle('open');
            document.getElementById('sidebarOverlay').classList.toggle('active');
        }

        function toggleCityDropdownLeft() {
            var dropdown = document.getElementById('cityDropdownLeft');
            var arrow = document.getElementById('cityArrowLeft');
            dropdown.classList.toggle('show');
            arrow.classList.toggle('open');
        }

        function selectCityFromLeft(city) {
            document.getElementById('cityDropdownLeft').classList.remove('show');
            document.getElementById('cityArrowLeft').classList.remove('open');
            saveCity(city);
            var currentPath = window.location.pathname;
            var currentQuery = window.location.search;
            if (currentQuery.includes('city=')) {
                window.location.href = currentPath + '?city=' + encodeURIComponent(city);
            } else if (currentPath === '/' || currentPath.startsWith('/city/')) {
                window.location.href = '/city/' + encodeURIComponent(city);
            } else {
                window.location.href = currentPath + '?city=' + encodeURIComponent(city);
            }
        }

        function changeCity(city) {
            saveCity(city);
            var currentPath = window.location.pathname;
            var currentQuery = window.location.search;
            if (currentQuery.includes('city=')) {
                window.location.href = currentPath + '?city=' + encodeURIComponent(city);
            } else if (currentPath === '/' || currentPath.startsWith('/city/')) {
                window.location.href = '/city/' + encodeURIComponent(city);
            } else {
                window.location.href = currentPath + '?city=' + encodeURIComponent(city);
            }
        }

        function filterCities() {
            var search = document.getElementById('citySearch').value.toLowerCase().trim();
            var items = document.querySelectorAll('.sidebar-city-item');
            var count = 0;
            var clearBtn = document.getElementById('clearBtn');

            if (search.length > 0) {
                clearBtn.classList.add('visible');
            } else {
                clearBtn.classList.remove('visible');
            }

            items.forEach(function(item) {
                var city = item.getAttribute('data-city').toLowerCase();
                if (city.includes(search) || search === '') {
                    item.style.display = 'flex';
                    count++;
                } else {
                    item.style.display = 'none';
                }
            });

            document.getElementById('foundCount').textContent = 'Найдено: ' + count;

            var list = document.getElementById('cityList');
            var oldNoResults = list.querySelector('.no-results');
            if (oldNoResults) oldNoResults.remove();

            if (count === 0) {
                var div = document.createElement('div');
                div.className = 'no-results';
                div.innerHTML = '<span class="big-icon">🔍</span>Город не найден<br><span style="font-size:0.8em;color:#555;">Попробуйте изменить запрос</span>';
                list.appendChild(div);
            }
        }

        function clearSearch() {
            document.getElementById('citySearch').value = '';
            document.getElementById('clearBtn').classList.remove('visible');
            filterCities();
            document.getElementById('citySearch').focus();
        }

        function getLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function(pos) {
                    alert('📍 Ваше местоположение:\\nШирота: ' + pos.coords.latitude.toFixed(4) + '\\nДолгота: ' + pos.coords.longitude.toFixed(4));
                }, function() {
                    alert('❌ Не удалось определить ваше местоположение.');
                });
            } else {
                alert('❌ Ваш браузер не поддерживает геолокацию.');
            }
        }

        function routeToPlace() {
            var address = document.getElementById('userAddress');
            if (address && address.value) {
                window.open('https://yandex.ru/maps/?rtext=~' + encodeURIComponent(address.value) + '&rtt=auto', '_blank');
            } else {
                alert('❌ Введите адрес для построения маршрута');
            }
        }

        document.addEventListener('click', function(event) {
            var wrapper = document.querySelector('.city-select-wrapper-left');
            if (wrapper && !wrapper.contains(event.target)) {
                document.getElementById('cityDropdownLeft').classList.remove('show');
                document.getElementById('cityArrowLeft').classList.remove('open');
            }
        });

        document.addEventListener('DOMContentLoaded', function() {
            var savedCity = getSavedCity();
            var cities = {{ cities|tojson }};

            if (savedCity && cities.indexOf(savedCity) !== -1) {
                var currentPath = window.location.pathname;
                var currentQuery = window.location.search;
                var currentCity = '{{ current_city }}';

                if (currentCity !== savedCity && !currentQuery.includes('city=')) {
                    if (currentPath === '/') {
                        window.location.href = '/?city=' + encodeURIComponent(savedCity);
                    } else if (!currentQuery.includes('city=')) {
                        window.location.href = currentPath + '?city=' + encodeURIComponent(savedCity);
                    }
                }
            }

            initAdBanner();
        });

        var ads = {{ ads|tojson }};
        var currentAdIndex = 0;
        var adInterval = null;
        var adTimer = 5;

        function initAdBanner() {
            var dotsContainer = document.getElementById('adDots');
            if (!dotsContainer) return;
            dotsContainer.innerHTML = '';
            if (ads.length === 0) {
                document.getElementById('adBanner').style.display = 'none';
                return;
            }
            ads.forEach(function(ad, index) {
                var dot = document.createElement('button');
                dot.className = 'dot' + (index === 0 ? ' active' : '');
                dot.setAttribute('data-index', index);
                dot.onclick = function() { goToAd(index); };
                dotsContainer.appendChild(dot);
            });
            showAd(0);
            startAdRotation();
        }

        function showAd(index) {
            var ad = ads[index];
            document.getElementById('adBrand').textContent = '🏷️ ' + ad.brand;
            document.getElementById('adEmoji').textContent = ad.image || ad.emoji || '🏙️';
            document.getElementById('adTitle').textContent = ad.title;
            document.getElementById('adDesc').textContent = ad.desc;
            document.getElementById('adBtn').textContent = 'Перейти';
            document.getElementById('adBtn').href = ad.link || '#';
            document.getElementById('adBanner').style.background = ad.color || 'linear-gradient(135deg, #333, #555)';

            document.querySelectorAll('.ad-dots .dot').forEach(function(dot, i) {
                dot.classList.toggle('active', i === index);
            });
            adTimer = 5;
            document.getElementById('adTimer').textContent = '⏱️ ' + adTimer + ' сек';
        }

        function goToAd(index) {
            clearInterval(adInterval);
            currentAdIndex = index;
            showAd(index);
            startAdRotation();
        }

        function startAdRotation() {
            clearInterval(adInterval);
            adInterval = setInterval(function() {
                adTimer--;
                document.getElementById('adTimer').textContent = '⏱️ ' + adTimer + ' сек';
                if (adTimer <= 0) {
                    currentAdIndex = (currentAdIndex + 1) % ads.length;
                    showAd(currentAdIndex);
                }
            }, 1000);
        }
    </script>
</body>
</html>
"""

# СОХРАНЯЕМ ШАБЛОН
with open("templates/base.html", "w", encoding="utf-8") as f:
    f.write(BASE_HTML)


# ==================== МАРШРУТЫ ====================

def get_city_data(city_name):
    for city in russia_cities:
        if city["name"].lower() == city_name.lower():
            return city
    for city in russia_cities:
        if city["name"] == default_city:
            return city
    return russia_cities[0]


def get_all_city_names():
    return [city["name"] for city in russia_cities]


def render_page(request, city_name, content, current_path, page_title=None, extra=None):
    city = get_city_data(city_name)
    city_dict = {}
    for c in russia_cities:
        city_dict[c["name"]] = {"population": f"{c['population']:,}"}

    shuffled_ads = ads.copy()
    random.shuffle(shuffled_ads)

    context = {
        "request": request,
        "current_path": current_path,
        "content": content,
        "cities": get_all_city_names(),
        "current_city": city["name"],
        "ads": shuffled_ads,
        "page_title": page_title or "О городе",
        "city_data": city_dict
    }
    if extra:
        context.update(extra)
    return templates.TemplateResponse("base.html", context)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    city_name = request.query_params.get("city", default_city)
    city = get_city_data(city_name)
    famous_list = [f.strip() for f in city["famous"].split(",")] if "famous" in city else []

    content = f'''
        <div class="city-highlight">
            <h2>🏙️ {city["name"]}</h2>
            <p style="font-size:1.05em;color:#444;">{city["description"]}</p>
            <div style="margin:15px 0;">
                <strong style="color:#222;">⭐ Что известно:</strong>
                <div class="famous">
                    {''.join([f'<span class="famous-tag">{item.strip()}</span>' for item in famous_list])}
                </div>
            </div>
        </div>
        <div class="info-grid">
            <div class="info-item"><div class="label">👨‍👩‍👧‍👦 Население</div><div class="value">{city["population"]:,} чел.</div></div>
            <div class="info-item"><div class="label">📅 Год основания</div><div class="value">{city["founded"]}</div></div>
            <div class="info-item"><div class="label">📍 Регион</div><div class="value">{city["region"]}</div></div>
            <div class="info-item"><div class="label">🗺️ Координаты</div><div class="value">{city["lat"]}, {city["lng"]}</div></div>
        </div>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin:15px 0;">
            <div class="info-card" onclick="window.location.href='/weather?city={city["name"]}'">
                <h3>🌤️ Погода</h3>
                <p>Узнать прогноз в {city["name"]}</p>
            </div>
            <div class="info-card" onclick="window.location.href='/places?city={city["name"]}'">
                <h3>📍 Достопримечательности</h3>
                <p>Что посмотреть в {city["name"]}</p>
            </div>
            <div class="info-card" onclick="window.location.href='/map?city={city["name"]}'">
                <h3>🗺️ Карта</h3>
                <p>Посмотреть {city["name"]} на карте</p>
            </div>
            <div class="info-card" onclick="window.location.href='/history?city={city["name"]}'">
                <h3>📜 История</h3>
                <p>Узнать историю {city["name"]}</p>
            </div>
        </div>
    '''
    return render_page(request, city_name, content, "/", f"{city['name']} — О городе")


@app.get("/city/{city_name}", response_class=HTMLResponse)
async def city_page(request: Request, city_name: str):
    city = get_city_data(city_name)
    famous_list = [f.strip() for f in city["famous"].split(",")] if "famous" in city else []

    content = f'''
        <div class="city-highlight">
            <h2>🏙️ {city["name"]}</h2>
            <p style="font-size:1.05em;color:#444;">{city["description"]}</p>
            <div style="margin:15px 0;">
                <strong style="color:#222;">⭐ Что известно:</strong>
                <div class="famous">
                    {''.join([f'<span class="famous-tag">{item.strip()}</span>' for item in famous_list])}
                </div>
            </div>
        </div>
        <div class="info-grid">
            <div class="info-item"><div class="label">👨‍👩‍👧‍👦 Население</div><div class="value">{city["population"]:,} чел.</div></div>
            <div class="info-item"><div class="label">📅 Год основания</div><div class="value">{city["founded"]}</div></div>
            <div class="info-item"><div class="label">📍 Регион</div><div class="value">{city["region"]}</div></div>
            <div class="info-item"><div class="label">🗺️ Координаты</div><div class="value">{city["lat"]}, {city["lng"]}</div></div>
        </div>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin:15px 0;">
            <div class="info-card" onclick="window.location.href='/weather?city={city["name"]}'">
                <h3>🌤️ Погода</h3>
                <p>Узнать прогноз в {city["name"]}</p>
            </div>
            <div class="info-card" onclick="window.location.href='/places?city={city["name"]}'">
                <h3>📍 Достопримечательности</h3>
                <p>Что посмотреть в {city["name"]}</p>
            </div>
            <div class="info-card" onclick="window.location.href='/map?city={city["name"]}'">
                <h3>🗺️ Карта</h3>
                <p>Посмотреть {city["name"]} на карте</p>
            </div>
            <div class="info-card" onclick="window.location.href='/history?city={city["name"]}'">
                <h3>📜 История</h3>
                <p>Узнать историю {city["name"]}</p>
            </div>
        </div>
    '''
    return render_page(request, city_name, content, f"/{city['name']}", city["name"])


@app.get("/weather", response_class=HTMLResponse)
async def weather_page(request: Request):
    city_name = request.query_params.get("city", default_city)
    city = get_city_data(city_name)

    weather = get_weather_openmeteo(city["name"], city["lat"], city["lng"])

    content = f'''
        <h2 style="margin:12px 0 5px 0;">🌤️ Погода в {city["name"]}</h2>
        <div class="weather-main">
            <div><div class="icon">{weather["icon"]}</div></div>
            <div>
                <div class="temp">{weather["temp"]}°C</div>
                <div class="condition">{weather["condition"]}</div>
                <div class="details">Ощущается как {weather["feels_like"]}°C</div>
            </div>
            <div style="margin-left:auto;">
                <div class="details">💧 Влажность: {weather["humidity"]}%</div>
                <div class="details">💨 Ветер: {weather["wind"]} м/с</div>
                <div class="details">📊 Давление: {weather["pressure"]} гПа</div>
                <div class="details">☀️ УФ-индекс: {weather["uv"]}</div>
            </div>
        </div>
        <div class="city-weather-details">
            <div class="detail-item"><div class="label">🌅 Рассвет</div><div class="value">{weather["sunrise"]}</div></div>
            <div class="detail-item"><div class="label">🌇 Закат</div><div class="value">{weather["sunset"]}</div></div>
            <div class="detail-item"><div class="label">📈 Атмосфера</div><div class="value">Хорошая</div></div>
            <div class="detail-item"><div class="label">🌡️ Комфорт</div><div class="value">Комфортно</div></div>
        </div>
        <h2 style="margin:12px 0 5px 0;">📅 Прогноз на неделю</h2>
        <div class="weather-week">
    '''
    for day in weather["week"]:
        content += f'''
            <div class="weather-day">
                <div class="day">{day["day"]}</div>
                <div class="icon">{day["icon"]}</div>
                <div class="temp">{day["temp"]}°C</div>
            </div>
        '''
    content += '</div>'
    return render_page(request, city_name, content, "/weather", f"Погода в {city['name']}")


@app.get("/places", response_class=HTMLResponse)
async def places_page(request: Request):
    city_name = request.query_params.get("city", default_city)
    city = get_city_data(city_name)

    tour_link = tour_links.get(city["name"], "https://www.tripadvisor.ru/Attractions")

    places = [
        {"id": 1, "name": f"Главная площадь {city['name']}", "icon": "🏛️", "desc": "Центральная площадь",
         "history": f"Сформировалась в {city['founded']} году", "tours": "Экскурсия: 1 час, 500 ₽"},
        {"id": 2, "name": f"Исторический центр", "icon": "🏰", "desc": "Старая часть города",
         "history": "Старейший район", "tours": "Пешеходная экскурсия: 1.5 часа, 700 ₽"},
        {"id": 3, "name": f"Главный храм", "icon": "⛪", "desc": "Главный собор города",
         "history": "Построен в XIX веке", "tours": "Экскурсия: 1 час, 400 ₽"},
        {"id": 4, "name": f"Набережная", "icon": "🌉", "desc": "Любимое место горожан", "history": "Построена в XX веке",
         "tours": "Прогулка: 1 час, бесплатно"}
    ]

    content = f'''
        <h2 style="margin:12px 0 5px 0;">📍 Достопримечательности {city["name"]}</h2>
        <div class="places-grid">
    '''
    for place in places:
        content += f'''
            <a href="/place/{place["id"]}?city={city["name"]}" class="place-item">
                <span class="icon">{place["icon"]}</span>
                <div class="name">{place["name"]}</div>
                <div class="desc">{place["desc"]}</div>
            </a>
        '''
    content += '''
        </div>
        <div class="info-card" style="cursor:default;">
            <h3>🎫 Запись на экскурсии</h3>
            <p>Для записи на экскурсии перейдите по ссылке ниже:</p>
            <br>
            <a href="''' + tour_link + '''" target="_blank" style="display:inline-block;padding:10px 30px;background:#222;color:#fff;border-radius:10px;text-decoration:none;font-weight:600;transition:all 0.3s ease;">
                📝 Записаться на экскурсию в ''' + city["name"] + '''
            </a>
        </div>
    '''
    return render_page(request, city_name, content, "/places", f"Достопримечательности {city['name']}")


@app.get("/place/{place_id}", response_class=HTMLResponse)
async def place_detail(request: Request, place_id: int):
    city_name = request.query_params.get("city", default_city)
    city = get_city_data(city_name)

    tour_link = tour_links.get(city["name"], "https://www.tripadvisor.ru/Attractions")

    places = [
        {"id": 1, "name": f"Главная площадь {city['name']}", "icon": "🏛️", "desc": "Центральная площадь",
         "history": f"Сформировалась в {city['founded']} году", "tours": "Экскурсия: 1 час, 500 ₽"},
        {"id": 2, "name": f"Исторический центр", "icon": "🏰", "desc": "Старая часть города",
         "history": "Старейший район", "tours": "Пешеходная экскурсия: 1.5 часа, 700 ₽"},
        {"id": 3, "name": f"Главный храм", "icon": "⛪", "desc": "Главный собор города",
         "history": "Построен в XIX веке", "tours": "Экскурсия: 1 час, 400 ₽"},
        {"id": 4, "name": f"Набережная", "icon": "🌉", "desc": "Любимое место горожан", "history": "Построена в XX веке",
         "tours": "Прогулка: 1 час, бесплатно"}
    ]
    place = next((p for p in places if p["id"] == place_id), None)
    if not place:
        return render_page(request, city_name,
                           '<div class="info-card"><h3>❌ Достопримечательность не найдена</h3></div>', "/places",
                           "Не найдено")

    content = f'''
        <div class="place-detail">
            <div style="font-size:3em;text-align:center;margin-bottom:10px;">{place["icon"]}</div>
            <h2>{place["name"]}</h2>
            <p><strong>📖 История:</strong> {place["history"]}</p>
            <p><strong>🎫 Экскурсии:</strong> {place["tours"]}</p>
            <a href="{tour_link}" target="_blank" class="tour-btn" style="display:inline-block;text-decoration:none;text-align:center;">
                📝 Записаться на экскурсию
            </a>
            <br>
            <a href="/places?city={city["name"]}" class="back-link" style="margin-top:15px;display:inline-block;">← Назад к достопримечательностям</a>
        </div>
    '''
    return render_page(request, city_name, content, f"/place/{place_id}", place["name"])


@app.get("/map", response_class=HTMLResponse)
async def map_page(request: Request):
    city_name = request.query_params.get("city", default_city)
    city = get_city_data(city_name)

    map_html = f'''
        <h2 style="margin:12px 0 5px 0;">🗺️ Карта {city["name"]}</h2>
        <div class="map-controls">
            <label>📍 Мой адрес:</label>
            <input type="text" id="userAddress" placeholder="Введите ваш адрес..." onkeyup="if(event.key==='Enter') routeToPlace()">
            <button onclick="routeToPlace()">🚗 Маршрут</button>
            <button class="location-btn" onclick="getLocation()">📍 Моё местоположение</button>
        </div>
        <div class="map-container">
            <iframe 
                src="https://yandex.ru/map-widget/v1/?ll={city["lng"]},{city["lat"]}&z=12&pt={city["lng"]},{city["lat"]},flag"
                loading="lazy"
                allowfullscreen>
            </iframe>
        </div>
        <div class="info-card">
            <h3>📍 Координаты {city["name"]}</h3>
            <p><strong>Широта:</strong> {city["lat"]}</p>
            <p><strong>Долгота:</strong> {city["lng"]}</p>
            <p><strong>Население:</strong> {city["population"]:,} человек</p>
        </div>
        <script>
            function routeToPlace() {{
                var address = document.getElementById('userAddress');
                if (address && address.value) {{
                    window.open('https://yandex.ru/maps/?rtext=~' + encodeURIComponent(address.value) + '&rtt=auto', '_blank');
                }} else {{
                    alert('❌ Введите адрес для построения маршрута');
                }}
            }}
        </script>
    '''
    return render_page(request, city_name, map_html, "/map", f"Карта {city['name']}")


@app.get("/history", response_class=HTMLResponse)
async def history_page(request: Request):
    city_name = request.query_params.get("city", default_city)
    city = get_city_data(city_name)
    history_type = request.query_params.get("type", "city")

    selector = f'''
        <div class="history-selector">
            <button class="history-btn {'active' if history_type == 'city' else ''}" onclick="window.location.href='/history?city={city["name"]}&type=city'">
                🏙️ История {city["name"]}
            </button>
            <button class="history-btn {'active' if history_type == 'russia' else ''}" onclick="window.location.href='/history?city={city["name"]}&type=russia'">
                🇷🇺 История России
            </button>
        </div>
    '''

    if history_type == "russia":
        content = f'''
            <h2 style="margin:12px 0 5px 0;">📜 История России</h2>
            {selector}
            <div class="history-grid">
                <div class="history-item">
                    <h3>Древняя Русь (IX-XIII вв.)</h3>
                    <ul><li><strong>882</strong> — Образование Древнерусского государства</li><li><strong>988</strong> — Крещение Руси</li></ul>
                </div>
                <div class="history-item">
                    <h3>Московское царство (XIV-XVII вв.)</h3>
                    <ul><li><strong>1380</strong> — Куликовская битва</li><li><strong>1480</strong> — Стояние на Угре</li></ul>
                </div>
                <div class="history-item">
                    <h3>Российская империя (XVIII-XIX вв.)</h3>
                    <ul><li><strong>1812</strong> — Отечественная война</li><li><strong>1861</strong> — Отмена крепостного права</li></ul>
                </div>
                <div class="history-item">
                    <h3>XX век</h3>
                    <ul><li><strong>1917</strong> — Революция</li><li><strong>1941-1945</strong> — Великая Отечественная война</li></ul>
                </div>
                <div class="history-item">
                    <h3>Современная Россия</h3>
                    <ul><li><strong>1991</strong> — Распад СССР</li><li><strong>2014</strong> — Олимпиада в Сочи</li></ul>
                </div>
            </div>
            <div class="info-card">
                <h3>📚 Образовательные ресурсы</h3>
                <div class="resources-grid">
                    <div class="resource-item"><div class="name">Культура.РФ</div><div class="desc">Портал о культуре России</div><a href="https://www.culture.ru" target="_blank">🌐 Перейти</a></div>
                    <div class="resource-item"><div class="name">История.РФ</div><div class="desc">История России</div><a href="https://www.historyrussia.org" target="_blank">🌐 Перейти</a></div>
                </div>
            </div>
        '''
    else:
        content = f'''
            <h2 style="margin:12px 0 5px 0;">📜 История {city["name"]}</h2>
            {selector}
            <div class="history-grid">
                <div class="history-item">
                    <h3>Основание города</h3>
                    <ul><li>• Город основан в {city["founded"]} году</li><li>• Историческое значение города</li></ul>
                </div>
                <div class="history-item">
                    <h3>XIX век</h3>
                    <ul><li>• Развитие промышленности</li><li>• Строительство железной дороги</li></ul>
                </div>
                <div class="history-item">
                    <h3>XX век</h3>
                    <ul><li>• Революционные события</li><li>• Современное развитие</li></ul>
                </div>
                <div class="history-item">
                    <h3>Современность</h3>
                    <ul><li>• Экономический рост</li><li>• Развитие инфраструктуры</li></ul>
                </div>
            </div>
            <div class="info-card">
                <h3>📚 Образовательные ресурсы</h3>
                <div class="resources-grid">
                    <div class="resource-item"><div class="name">Культура.РФ</div><div class="desc">Портал о культуре России</div><a href="https://www.culture.ru" target="_blank">🌐 Перейти</a></div>
                    <div class="resource-item"><div class="name">История.РФ</div><div class="desc">История России</div><a href="https://www.historyrussia.org" target="_blank">🌐 Перейти</a></div>
                </div>
            </div>
        '''

    return render_page(request, city_name, content, "/history", f"История {city['name']}")


@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)


# ============================================
# ЗАПУСК
# ============================================

def open_browser_local():
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:8000")


if __name__ == "__main__":
    local_ip = get_local_ip()

    print("=" * 70)
    print("🏙️ ЗАПУСК ГОРОДСКОГО ГИДА")
    print("=" * 70)
    print(f"📂 Всего городов в базе: {len(russia_cities)}")
    print("✅ ПОГОДА: Open-Meteo (БЕСПЛАТНО, БЕЗ КЛЮЧА)")
    print(f"📢 РЕКЛАМА: {len(ads)} баннеров")
    print("=" * 70)
    print("🌐 ДОСТУП К САЙТУ:")
    print(f"   • На этом устройстве: http://127.0.0.1:8000")
    print(f"   • На этом устройстве: http://localhost:8000")
    print(f"   • В локальной сети: http://{local_ip}:8000")
    print("=" * 70)

    # Пытаемся запустить ngrok для доступа из интернета
    print("🔄 Пытаемся запустить ngrok для доступа из интернета...")
    public_url = start_ngrok(8000)

    if public_url:
        print("=" * 70)
        print("🌍 ДОСТУП ИЗ ИНТЕРНЕТА (ЧЕРЕЗ NGROK):")
        print(f"   🔗 {public_url}")
        print("   📱 Отправьте эту ссылку кому угодно!")
        print("   ⚠️  Ссылка работает пока запущен ngrok")
        print("=" * 70)
    else:
        print("=" * 70)
        print("⚠️ NGROK НЕ ЗАПУЩЕН")
        print("📌 Чтобы открыть сайт из интернета:")
        print("   1. Скачайте ngrok с https://ngrok.com/download")
        print("   2. Распакуйте в папку с проектом")
        print("   3. Запустите командную строку в папке с ngrok")
        print("   4. Выполните: ngrok http 8000")
        print("   5. Скопируйте ссылку из терминала")
        print("=" * 70)

    print("⏹️ Для остановки нажмите Ctrl+C")
    print("=" * 70)

    # Открываем браузер на локальном компьютере
    threading.Thread(target=open_browser_local, daemon=True).start()

    # Запускаем сервер на ВСЕХ интерфейсах
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        access_log=True
    )