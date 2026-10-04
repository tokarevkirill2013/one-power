from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, Response, RedirectResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import os
import webbrowser
import threading
import time
from datetime import datetime

app = FastAPI(title="Навигатор")

# Создаём папку для шаблонов
os.makedirs("templates", exist_ok=True)

templates = Jinja2Templates(directory="templates")

# Данные о погоде
weather_data = {
    "Санкт-Петербург": {"temp": "+18°C", "condition": "Облачно", "icon": "☁️", "humidity": "72%", "wind": "5 м/с"},
    "Москва": {"temp": "+22°C", "condition": "Солнечно", "icon": "☀️", "humidity": "55%", "wind": "3 м/с"},
    "Новосибирск": {"temp": "+15°C", "condition": "Дождь", "icon": "🌧️", "humidity": "85%", "wind": "7 м/с"},
    "Владивосток": {"temp": "+20°C", "condition": "Туман", "icon": "🌫️", "humidity": "78%", "wind": "4 м/с"}
}

# Все доступные валюты
all_currencies = {
    "USD": {"name": "Доллар США", "rate": "91.50", "change": "+0.5%", "flag": "🇺🇸"},
    "EUR": {"name": "Евро", "rate": "98.20", "change": "-0.3%", "flag": "🇪🇺"},
    "CNY": {"name": "Юань", "rate": "12.80", "change": "+0.8%", "flag": "🇨🇳"},
    "GBP": {"name": "Фунт стерлингов", "rate": "115.40", "change": "-0.2%", "flag": "🇬🇧"},
    "JPY": {"name": "Иена", "rate": "0.62", "change": "+0.1%", "flag": "🇯🇵"},
    "CHF": {"name": "Швейцарский франк", "rate": "103.20", "change": "-0.1%", "flag": "🇨🇭"},
    "CAD": {"name": "Канадский доллар", "rate": "67.30", "change": "+0.3%", "flag": "🇨🇦"},
    "AUD": {"name": "Австралийский доллар", "rate": "60.80", "change": "-0.4%", "flag": "🇦🇺"},
    "TRY": {"name": "Турецкая лира", "rate": "2.85", "change": "+1.2%", "flag": "🇹🇷"},
    "KZT": {"name": "Тенге", "rate": "0.19", "change": "+0.2%", "flag": "🇰🇿"}
}

default_currencies = ["USD", "EUR", "CNY", "GBP"]

# Новости
news_data = [
    {"id": 1, "title": "Открытие нового парка", "date": "2026-08-13",
     "summary": "В Санкт-Петербурге открылся новый парк на набережной Невы.", "category": "Город"},
    {"id": 2, "title": "Запуск новой линии метро", "date": "2026-08-12",
     "summary": "Началось тестирование новой линии метро в Санкт-Петербурге.", "category": "Транспорт"},
    {"id": 3, "title": "Культурный фестиваль", "date": "2026-08-11",
     "summary": "С 15 по 25 августа пройдет фестиваль «Петербургские сезоны».", "category": "Культура"},
]

# Базовый HTML шаблон
BASE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Навигатор</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            transition: all 0.5s ease;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            transition: all 0.5s ease;
        }
        
        h1 { text-align: center; color: #333; margin-bottom: 30px; font-size: 2.5em; }
        h1 span { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        
        /* ТЕМЫ - через data атрибут */
        body[data-theme="dark"] { background: linear-gradient(135deg, #2d3436, #1a1a2e); }
        body[data-theme="dark"] .container { background: #2d3436; }
        body[data-theme="dark"] h1 { color: #fff; }
        body[data-theme="dark"] .nav-card { background: #3d3d3d; color: #fff; }
        body[data-theme="dark"] .nav-card .title { color: #fff; }
        body[data-theme="dark"] .breadcrumb { background: #3d3d3d; color: #fff; }
        body[data-theme="dark"] .breadcrumb a { color: #74b9ff; }
        body[data-theme="dark"] .info-card { background: #3d3d3d; color: #fff; }
        body[data-theme="dark"] .info-card h3 { color: #fff; }
        body[data-theme="dark"] .info-card p { color: #ccc; }
        body[data-theme="dark"] .weather-item { background: #3d3d3d; color: #fff; }
        body[data-theme="dark"] .weather-item .city { color: #fff; }
        body[data-theme="dark"] .currency-item { background: #3d3d3d; color: #fff; }
        body[data-theme="dark"] .news-item { background: #3d3d3d; color: #fff; }
        body[data-theme="dark"] .news-item h3 { color: #fff; }
        body[data-theme="dark"] .child-item { background: #3d3d3d; }
        body[data-theme="dark"] .child-item a { color: #fff; }
        body[data-theme="dark"] .calculator { background: #3d3d3d; }
        body[data-theme="dark"] .calculator input { background: #2d3436; color: #fff; border-color: #555; }
        body[data-theme="dark"] .calculator .btn-group button { background: #2d3436; color: #fff; border-color: #555; }
        body[data-theme="dark"] .calculator .result { background: #2d3436; color: #fff; }
        body[data-theme="dark"] .currency-controls { background: #3d3d3d; color: #fff; }
        body[data-theme="dark"] .currency-controls label { color: #fff; }
        body[data-theme="dark"] .currency-checkbox label { background: #2d3436; color: #fff; border-color: #555; }
        body[data-theme="dark"] .theme-selector { background: #3d3d3d; }
        body[data-theme="dark"] .theme-btn { background: #2d3436; color: #fff; border-color: #555; }
        
        body[data-theme="ocean"] { background: linear-gradient(135deg, #0077b6, #00b4d8); }
        body[data-theme="ocean"] .container { background: #caf0f8; }
        body[data-theme="ocean"] h1 { color: #023e8a; }
        body[data-theme="ocean"] .nav-card { background: #fff; color: #023e8a; }
        body[data-theme="ocean"] .nav-card .title { color: #023e8a; }
        body[data-theme="ocean"] .breadcrumb { background: #fff; }
        body[data-theme="ocean"] .info-card { background: #fff; }
        body[data-theme="ocean"] .weather-item { background: #fff; }
        body[data-theme="ocean"] .currency-item { background: #fff; }
        body[data-theme="ocean"] .news-item { background: #fff; }
        body[data-theme="ocean"] .child-item { background: #fff; }
        body[data-theme="ocean"] .calculator { background: #fff; }
        body[data-theme="ocean"] .currency-controls { background: #fff; }
        body[data-theme="ocean"] .theme-selector { background: #fff; }
        body[data-theme="ocean"] .theme-btn { background: #fff; }
        
        body[data-theme="nature"] { background: linear-gradient(135deg, #2d6a4f, #52b788); }
        body[data-theme="nature"] .container { background: #d8f3dc; }
        body[data-theme="nature"] h1 { color: #1b4332; }
        body[data-theme="nature"] .nav-card { background: #fff; color: #1b4332; }
        body[data-theme="nature"] .nav-card .title { color: #1b4332; }
        body[data-theme="nature"] .breadcrumb { background: #fff; }
        body[data-theme="nature"] .info-card { background: #fff; }
        body[data-theme="nature"] .weather-item { background: #fff; }
        body[data-theme="nature"] .currency-item { background: #fff; }
        body[data-theme="nature"] .news-item { background: #fff; }
        body[data-theme="nature"] .child-item { background: #fff; }
        body[data-theme="nature"] .calculator { background: #fff; }
        body[data-theme="nature"] .currency-controls { background: #fff; }
        body[data-theme="nature"] .theme-selector { background: #fff; }
        body[data-theme="nature"] .theme-btn { background: #fff; }
        
        body[data-theme="sunset"] { background: linear-gradient(135deg, #e76f51, #f4a261); }
        body[data-theme="sunset"] .container { background: #fef0e9; }
        body[data-theme="sunset"] h1 { color: #6b3a2a; }
        body[data-theme="sunset"] .nav-card { background: #fff; color: #6b3a2a; }
        body[data-theme="sunset"] .nav-card .title { color: #6b3a2a; }
        body[data-theme="sunset"] .breadcrumb { background: #fff; }
        body[data-theme="sunset"] .info-card { background: #fff; }
        body[data-theme="sunset"] .weather-item { background: #fff; }
        body[data-theme="sunset"] .currency-item { background: #fff; }
        body[data-theme="sunset"] .news-item { background: #fff; }
        body[data-theme="sunset"] .child-item { background: #fff; }
        body[data-theme="sunset"] .calculator { background: #fff; }
        body[data-theme="sunset"] .currency-controls { background: #fff; }
        body[data-theme="sunset"] .theme-selector { background: #fff; }
        body[data-theme="sunset"] .theme-btn { background: #fff; }

        .theme-selector {
            display: flex;
            gap: 10px;
            justify-content: center;
            flex-wrap: wrap;
            margin-bottom: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 15px;
        }
        
        .theme-btn {
            padding: 8px 20px;
            border: 2px solid #ddd;
            border-radius: 25px;
            background: white;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
        }
        
        .theme-btn:hover { transform: scale(1.05); border-color: #667eea; }
        .theme-btn.active { border-color: #667eea; background: #667eea; color: white; }
        
        .nav-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 12px;
            margin-bottom: 30px;
        }
        
        .nav-card {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 15px;
            transition: all 0.3s ease;
            border: 2px solid transparent;
            text-decoration: none;
            display: block;
            color: #333;
            text-align: center;
        }
        
        .nav-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            border-color: #667eea;
        }
        
        .nav-card .icon { font-size: 2.2em; display: block; margin-bottom: 5px; }
        .nav-card .title { font-size: 0.9em; font-weight: 600; }
        
        .breadcrumb {
            background: #f8f9fa;
            padding: 10px 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        
        .breadcrumb a { color: #667eea; text-decoration: none; }
        .breadcrumb span { color: #666; }
        
        .current-page {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            display: inline-block;
        }
        
        .back-link {
            display: inline-block;
            margin-top: 20px;
            padding: 10px 25px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 10px;
            transition: all 0.3s ease;
            border: none;
            cursor: pointer;
            font-size: 1em;
        }
        
        .back-link:hover { transform: scale(1.05); opacity: 0.9; }
        
        .children-section {
            margin-top: 30px;
            border-top: 2px solid #e9ecef;
            padding-top: 20px;
        }
        
        .children-section h2 { color: #555; margin-bottom: 15px; font-size: 1.3em; }
        
        .children-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
            gap: 10px;
        }
        
        .child-item {
            background: #f1f3f5;
            padding: 12px;
            border-radius: 10px;
            transition: all 0.3s ease;
            text-align: center;
        }
        
        .child-item:hover { background: #e9ecef; transform: scale(1.02); }
        .child-item .icon { font-size: 1.5em; display: block; margin-bottom: 3px; }
        .child-item a { text-decoration: none; color: #333; font-weight: 500; font-size: 0.9em; }
        
        .info-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
        }
        
        .info-card h3 { color: #333; margin-bottom: 10px; }
        .info-card p { color: #666; line-height: 1.6; }
        .info-card ul { margin: 10px 20px; color: #555; }
        .info-card ul li { margin: 5px 0; }
        
        .weather-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .weather-item {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .weather-item:hover { transform: scale(1.02); }
        .weather-item .icon { font-size: 3em; }
        .weather-item .city { font-weight: 600; margin: 10px 0 5px; }
        .weather-item .temp { font-size: 1.8em; font-weight: 700; }
        .weather-item .condition { color: #666; }
        .weather-item .details { font-size: 0.9em; color: #888; margin-top: 5px; }
        
        .map-container {
            width: 100%;
            height: 450px;
            border-radius: 15px;
            overflow: hidden;
            border: 2px solid #e9ecef;
            margin: 20px 0;
        }
        
        .map-container iframe { width: 100%; height: 100%; border: none; }
        
        .currency-controls {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin: 15px 0;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 15px;
            align-items: center;
        }
        
        .currency-controls label { font-weight: 600; color: #333; margin-right: 10px; }
        
        .currency-checkbox {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }
        
        .currency-checkbox label {
            display: flex;
            align-items: center;
            gap: 5px;
            background: white;
            padding: 5px 12px;
            border-radius: 20px;
            border: 2px solid #ddd;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: normal;
            font-size: 0.85em;
        }
        
        .currency-checkbox label:hover { border-color: #667eea; }
        .currency-checkbox label.selected { border-color: #667eea; background: #667eea; color: white; }
        .currency-checkbox input[type="checkbox"] { display: none; }
        
        .currency-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 12px;
            margin: 20px 0;
        }
        
        .currency-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 15px;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .currency-item:hover { transform: scale(1.02); }
        .currency-item .flag { font-size: 2em; }
        .currency-item .code { font-weight: 700; margin: 5px 0; }
        .currency-item .name { font-size: 0.75em; color: #888; }
        .currency-item .rate { font-size: 1.3em; font-weight: 700; }
        .currency-item .change { font-size: 0.85em; }
        .currency-item .change.positive { color: #27ae60; }
        .currency-item .change.negative { color: #e74c3c; }
        
        .news-container { margin: 20px 0; }
        
        .news-item {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 18px;
            margin-bottom: 15px;
            transition: all 0.3s ease;
            border-left: 4px solid #667eea;
        }
        
        .news-item:hover { transform: translateX(5px); }
        .news-item h3 { margin-bottom: 5px; font-size: 1.1em; }
        .news-meta { color: #888; font-size: 0.85em; margin-bottom: 8px; }
        .news-meta .category {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            display: inline-block;
        }
        .news-item p { color: #555; line-height: 1.5; font-size: 0.95em; }
        
        .calculator {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 15px;
            margin: 20px auto;
            max-width: 380px;
        }
        
        .calculator input {
            width: 100%;
            padding: 10px;
            margin: 8px 0;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 1.1em;
        }
        
        .calculator .btn-group {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 6px;
            margin: 8px 0;
        }
        
        .calculator .btn-group button {
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 1.1em;
            cursor: pointer;
            transition: all 0.2s ease;
            background: white;
        }
        
        .calculator .btn-group button:hover {
            background: #667eea;
            color: white;
            transform: scale(1.05);
        }
        
        .calculator .btn-group button.operator {
            background: #667eea;
            color: white;
            border-color: #667eea;
        }
        
        .calculator .result {
            font-size: 1.8em;
            font-weight: 700;
            text-align: right;
            padding: 10px;
            background: white;
            border-radius: 10px;
            margin-top: 10px;
            min-height: 50px;
        }
        
        @media (max-width: 600px) {
            .container { padding: 15px; }
            .nav-grid { grid-template-columns: 1fr 1fr; }
            .map-container { height: 300px; }
            .currency-controls { flex-direction: column; align-items: stretch; }
        }
    </style>
</head>
<body data-theme="default">
    <div class="container">
        <h1>🧭 <span>Навигатор</span></h1>
        
        <div class="theme-selector">
            <button class="theme-btn active" onclick="changeTheme('default')">🌞 Светлая</button>
            <button class="theme-btn" onclick="changeTheme('dark')">🌙 Тёмная</button>
            <button class="theme-btn" onclick="changeTheme('ocean')">🌊 Океан</button>
            <button class="theme-btn" onclick="changeTheme('nature')">🌿 Природа</button>
            <button class="theme-btn" onclick="changeTheme('sunset')">🌅 Закат</button>
        </div>
        
        <div class="breadcrumb">
            <a href="/">Главная</a>
            {% if current_path != "/" %}
                <span> → </span>
                <span class="current-page">{{ current_path }}</span>
            {% endif %}
        </div>
        
        <div class="nav-grid">
            <a href="/" class="nav-card"><span class="icon">🏠</span><div class="title">Главная</div></a>
            <a href="/weather" class="nav-card"><span class="icon">🌤️</span><div class="title">Погода</div></a>
            <a href="/currency" class="nav-card"><span class="icon">💱</span><div class="title">Курсы валют</div></a>
            <a href="/map" class="nav-card"><span class="icon">🗺️</span><div class="title">Карта</div></a>
            <a href="/services" class="nav-card"><span class="icon">💼</span><div class="title">Услуги</div></a>
            <a href="/blog" class="nav-card"><span class="icon">📝</span><div class="title">Блог</div></a>
        </div>
        
        {% if children and children|length > 0 %}
            <div class="children-section">
                <h2>📂 Подразделы</h2>
                <div class="children-grid">
                    {% for child_key, child_value in children.items() %}
                        <div class="child-item">
                            <span class="icon">{{ child_value.icon }}</span>
                            <a href="{{ child_value.url }}">{{ child_key }}</a>
                        </div>
                    {% endfor %}
                </div>
            </div>
        {% endif %}
        
        <!-- Содержимое страниц -->
        {{ content|safe }}
        
        {% if current_path != "/" %}
            <a href="/" class="back-link">← На главную</a>
        {% endif %}
    </div>
    
    <script>
        function changeTheme(theme) {
            document.body.setAttribute('data-theme', theme);
            document.querySelectorAll('.theme-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.theme-btn').forEach(btn => {
                if (btn.textContent.toLowerCase().includes(theme) || 
                    (theme === 'default' && btn.textContent.includes('Светлая'))) {
                    btn.classList.add('active');
                }
            });
            localStorage.setItem('theme', theme);
        }
        
        document.addEventListener('DOMContentLoaded', function() {
            const savedTheme = localStorage.getItem('theme');
            if (savedTheme) {
                changeTheme(savedTheme);
            }
        });
    </script>
</body>
</html>
"""

# Создаём страницы

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    content = """
        <div class="info-card">
            <h3>🏠 Добро пожаловать в Навигатор!</h3>
            <p>Выберите нужный раздел в меню выше.</p>
            <ul>
                <li>🌤️ Погода - актуальная погода в городах России</li>
                <li>💱 Курсы валют - курсы с возможностью выбора</li>
                <li>🗺️ Карта - карта Санкт-Петербурга</li>
                <li>💼 Услуги - наши услуги</li>
                <li>📝 Блог - новости и статьи</li>
            </ul>
        </div>
    """
    return templates.TemplateResponse(
        "base.html",
        {
            "request": request,
            "current_path": "/",
            "children": None,
            "content": content
        }
    )

@app.get("/weather", response_class=HTMLResponse)
async def weather(request: Request):
    weather_html = '<h2 style="margin: 20px 0 10px 0;">🌤️ Погода в городах России</h2><div class="weather-grid">'
    for city, data in weather_data.items():
        weather_html += f'''
            <div class="weather-item">
                <div class="icon">{data["icon"]}</div>
                <div class="city">{city}</div>
                <div class="temp">{data["temp"]}</div>
                <div class="condition">{data["condition"]}</div>
                <div class="details">💧 {data["humidity"]} | 💨 {data["wind"]}</div>
            </div>
        '''
    weather_html += '</div>'
    weather_html += f'''
        <div class="info-card">
            <h3>📊 Прогноз на сегодня</h3>
            <p>В Санкт-Петербурге ожидается {weather_data["Санкт-Петербург"]["condition"].lower()}, температура {weather_data["Санкт-Петербург"]["temp"]}.</p>
        </div>
    '''
    return templates.TemplateResponse(
        "base.html",
        {
            "request": request,
            "current_path": "/weather",
            "children": None,
            "content": weather_html
        }
    )

@app.get("/currency", response_class=HTMLResponse)
async def currency(request: Request):
    currency_html = '<h2 style="margin: 20px 0 10px 0;">💱 Курсы валют</h2>'
    currency_html += '<div class="currency-grid">'
    for code, data in default_currencies:
        if code in all_currencies:
            d = all_currencies[code]
            change_class = 'positive' if d['change'].startswith('+') else 'negative'
            currency_html += f'''
                <div class="currency-item">
                    <div class="flag">{d["flag"]}</div>
                    <div class="code">{code}</div>
                    <div class="name">{d["name"]}</div>
                    <div class="rate">{d["rate"]} ₽</div>
                    <div class="change {change_class}">{d["change"]}</div>
                </div>
            '''
    currency_html += '</div>'
    currency_html += f'''
        <div class="info-card">
            <h3>📊 Аналитика</h3>
            <p>Курс доллара: {all_currencies["USD"]["rate"]} ₽ ({all_currencies["USD"]["change"]})<br>
            Курс евро: {all_currencies["EUR"]["rate"]} ₽ ({all_currencies["EUR"]["change"]})</p>
        </div>
    '''
    return templates.TemplateResponse(
        "base.html",
        {
            "request": request,
            "current_path": "/currency",
            "children": None,
            "content": currency_html
        }
    )

@app.get("/map", response_class=HTMLResponse)
async def map_page(request: Request):
    map_html = '''
        <h2 style="margin: 20px 0 10px 0;">🗺️ Карта Санкт-Петербурга</h2>
        <div class="map-container">
            <iframe 
                src="https://yandex.ru/map-widget/v1/?um=constructor%3A6df9a9c323f4ca77ce47a32c6d7c53a336ea01cd2fca3628b9ad0e09e2db2d73&amp;source=constructor"
                loading="lazy"
                allowfullscreen>
            </iframe>
        </div>
        <div class="info-card">
            <h3>📌 Санкт-Петербург</h3>
            <p><strong>Население:</strong> ~5.6 млн человек</p>
            <p><strong>Год основания:</strong> 1703</p>
        </div>
    '''
    return templates.TemplateResponse(
        "base.html",
        {
            "request": request,
            "current_path": "/map",
            "children": None,
            "content": map_html
        }
    )

@app.get("/services", response_class=HTMLResponse)
async def services(request: Request):
    content = '''
        <div class="info-card">
            <h3>💼 Наши услуги</h3>
            <p>Выберите нужную услугу в подразделах:</p>
            <ul>
                <li>💻 Разработка - создание сайтов и приложений</li>
                <li>🎨 Дизайн - разработка дизайна и интерфейсов</li>
                <li>📈 Маркетинг - продвижение и реклама</li>
            </ul>
        </div>
    '''
    return templates.TemplateResponse(
        "base.html",
        {
            "request": request,
            "current_path": "/services",
            "children": {
                "Разработка": {"url": "/services/dev", "icon": "💻"},
                "Дизайн": {"url": "/services/design", "icon": "🎨"},
                "Маркетинг": {"url": "/services/marketing", "icon": "📈"}
            },
            "content": content
        }
    )

@app.get("/services/dev", response_class=HTMLResponse)
async def services_dev(request: Request):
    content = '''
        <h2 style="margin: 20px 0 10px 0;">💻 Разработка</h2>
        <div class="info-card">
            <h3>Создание сайтов и приложений</h3>
            <p>Мы занимаемся разработкой веб-сайтов, мобильных приложений и программного обеспечения.</p>
            <p><strong>Технологии:</strong> Python, FastAPI, JavaScript, React, HTML, CSS</p>
        </div>
        <div class="calculator">
            <h3 style="margin-bottom: 10px;">🧮 Калькулятор</h3>
            <input type="text" id="calcDisplay" readonly placeholder="0">
            <div class="btn-group">
                <button onclick="calcInput('7')">7</button>
                <button onclick="calcInput('8')">8</button>
                <button onclick="calcInput('9')">9</button>
                <button class="operator" onclick="calcInput('/')">÷</button>
                <button onclick="calcInput('4')">4</button>
                <button onclick="calcInput('5')">5</button>
                <button onclick="calcInput('6')">6</button>
                <button class="operator" onclick="calcInput('*')">×</button>
                <button onclick="calcInput('1')">1</button>
                <button onclick="calcInput('2')">2</button>
                <button onclick="calcInput('3')">3</button>
                <button class="operator" onclick="calcInput('-')">−</button>
                <button onclick="calcInput('0')">0</button>
                <button onclick="calcInput('.')">.</button>
                <button onclick="calcClear()">C</button>
                <button class="operator" onclick="calcResult()">=</button>
            </div>
            <div class="result" id="calcResult">0</div>
        </div>
        <script>
            let calcDisplay = document.getElementById('calcDisplay');
            let calcResult = document.getElementById('calcResult');
            let calcExpression = '';
            function calcInput(value) { calcExpression += value; calcDisplay.value = calcExpression; }
            function calcClear() { calcExpression = ''; calcDisplay.value = ''; calcResult.textContent = '0'; }
            function calcResult() {
                try {
                    let result = eval(calcExpression.replace(/×/g, '*').replace(/÷/g, '/'));
                    calcResult.textContent = result;
                    calcExpression = result.toString();
                    calcDisplay.value = calcExpression;
                } catch(e) { calcResult.textContent = 'Ошибка'; }
            }
        </script>
    '''
    return templates.TemplateResponse(
        "base.html",
        {
            "request": request,
            "current_path": "/services/dev",
            "children": None,
            "content": content
        }
    )

@app.get("/services/design", response_class=HTMLResponse)
async def services_design(request: Request):
    content = '''
        <h2 style="margin: 20px 0 10px 0;">🎨 Дизайн</h2>
        <div class="info-card">
            <h3>Разработка дизайна и интерфейсов</h3>
            <p>Мы создаём современные и удобные дизайны для сайтов, приложений и брендов.</p>
            <p><strong>Направления:</strong> UI/UX дизайн, веб-дизайн, графический дизайн</p>
            <br>
            <h4>🎨 Выберите тему оформления сайта:</h4>
            <p>Нажмите на кнопки вверху страницы (Светлая, Тёмная, Океан, Природа, Закат)</p>
            <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 10px;">
                <span style="padding: 10px 20px; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 10px; color: white;">Светлая</span>
                <span style="padding: 10px 20px; background: linear-gradient(135deg, #2d3436, #1a1a2e); border-radius: 10px; color: white;">Тёмная</span>
                <span style="padding: 10px 20px; background: linear-gradient(135deg, #0077b6, #00b4d8); border-radius: 10px; color: white;">Океан</span>
                <span style="padding: 10px 20px; background: linear-gradient(135deg, #2d6a4f, #52b788); border-radius: 10px; color: white;">Природа</span>
                <span style="padding: 10px 20px; background: linear-gradient(135deg, #e76f51, #f4a261); border-radius: 10px; color: white;">Закат</span>
            </div>
        </div>
    '''
    return templates.TemplateResponse(
        "base.html",
        {
            "request": request,
            "current_path": "/services/design",
            "children": None,
            "content": content
        }
    )

@app.get("/services/marketing", response_class=HTMLResponse)
async def services_marketing(request: Request):
    content = '''
        <h2 style="margin: 20px 0 10px 0;">📈 Маркетинг</h2>
        <div class="info-card">
            <h3>Продвижение и реклама</h3>
            <p>Мы помогаем бизнесу расти через эффективные маркетинговые стратегии.</p>
            <p><strong>Услуги:</strong> SEO, контекстная реклама, SMM, email-маркетинг</p>
            <p><strong>Результат:</strong> увеличение продаж и узнаваемости бренда</p>
        </div>
    '''
    return templates.TemplateResponse(
        "base.html",
        {
            "request": request,
            "current_path": "/services/marketing",
            "children": None,
            "content": content
        }
    )

@app.get("/blog", response_class=HTMLResponse)
async def blog(request: Request):
    content = '''
        <div class="info-card">
            <h3>📝 Блог</h3>
            <p>Читайте наши новости и статьи в подразделах:</p>
            <ul>
                <li>📰 Новости - свежие новости</li>
                <li>📄 Статьи - полезные статьи</li>
            </ul>
        </div>
    '''
    return templates.TemplateResponse(
        "base.html",
        {
            "request": request,
            "current_path": "/blog",
            "children": {
                "Новости": {"url": "/blog/news", "icon": "📰"},
                "Статьи": {"url": "/blog/articles", "icon": "📄"}
            },
            "content": content
        }
    )

@app.get("/blog/news", response_class=HTMLResponse)
async def blog_news(request: Request):
    news_html = '<div class="news-container"><h2>📰 Последние новости</h2><br>'
    for news in news_data:
        news_html += f'''
            <div class="news-item">
                <h3>{news["title"]}</h3>
                <div class="news-meta">
                    <span>{news["date"]}</span>
                    <span class="category">{news["category"]}</span>
                </div>
                <p>{news["summary"]}</p>
            </div>
        '''
    news_html += '</div>'
    return templates.TemplateResponse(
        "base.html",
        {
            "request": request,
            "current_path": "/blog/news",
            "children": None,
            "content": news_html
        }
    )

@app.get("/blog/articles", response_class=HTMLResponse)
async def blog_articles(request: Request):
    content = '''
        <div class="info-card">
            <h3>📄 Статьи</h3>
            <p>Здесь будут публиковаться полезные статьи.</p>
            <p><strong>Скоро:</strong> статьи по веб-разработке, дизайну и маркетингу</p>
        </div>
    '''
    return templates.TemplateResponse(
        "base.html",
        {
            "request": request,
            "current_path": "/blog/articles",
            "children": None,
            "content": content
        }
    )

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    content = '''
        <div class="info-card">
            <h3>ℹ️ О нас</h3>
            <p>Мы создали этот навигатор, чтобы упростить вашу работу с информацией.</p>
            <p><strong>Версия:</strong> 2.0</p>
            <p><strong>Обновлено:</strong> 2026-08-13</p>
        </div>
    '''
    return templates.TemplateResponse(
        "base.html",
        {
            "request": request,
            "current_path": "/about",
            "children": None,
            "content": content
        }
    )

@app.get("/contacts", response_class=HTMLResponse)
async def contacts(request: Request):
    content = '''
        <div class="info-card">
            <h3>📞 Контакты</h3>
            <p><strong>📧 Email:</strong> support@navigator.ru</p>
            <p><strong>📱 Телефон:</strong> +7 (800) 555-01-01</p>
            <p><strong>📍 Адрес:</strong> г. Санкт-Петербург, Невский пр., д. 1</p>
        </div>
    '''
    return templates.TemplateResponse(
        "base.html",
        {
            "request": request,
            "current_path": "/contacts",
            "children": None,
            "content": content
        }
    )

@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)

def open_browser():
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 ЗАПУСК НАВИГАТОРА")
    print("=" * 50)
    print("📂 Доступные разделы:")
    print("  • / - Главная")
    print("  • /weather - Погода")
    print("  • /currency - Курсы валют")
    print("  • /map - Карта")
    print("  • /services - Услуги")
    print("    ↳ /services/dev - Разработка (калькулятор)")
    print("    ↳ /services/design - Дизайн (настройка тем)")
    print("    ↳ /services/marketing - Маркетинг")
    print("  • /blog - Блог")
    print("    ↳ /blog/news - Новости")
    print("    ↳ /blog/articles - Статьи")
    print("=" * 50)
    print("🌐 Сервер запускается на http://127.0.0.1:8000")
    print("⏳ Браузер откроется автоматически через 1.5 секунды...")
    print("⏹️ Для остановки нажмите Ctrl+C")
    print("=" * 50)

    threading.Thread(target=open_browser, daemon=True).start()

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info",
        access_log=True
    )