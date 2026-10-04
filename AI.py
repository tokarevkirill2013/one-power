import webbrowser
import threading
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

HTML_PAGE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <title>Карта мира</title>
    <style>
        html, body {
            margin: 0;
            padding: 0;
            height: 100%;
            overflow: hidden;
            font-family: Arial, sans-serif;
        }

        #map {
            width: 100%;
            height: 100vh;
        }

        #bottom-panel {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            background: rgba(255, 255, 255, 0.95);
            padding: 12px 16px;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.15);
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        #layers {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }

        #layers button {
            padding: 8px 16px;
            border: none;
            border-radius: 20px;
            background: #f0f0f0;
            cursor: pointer;
            font-size: 14px;
            transition: background 0.2s;
        }

        #layers button:hover {
            background: #e0e0e0;
        }

        #layers button.active {
            background: #4a90d9;
            color: white;
        }

        #search-box {
            display: flex;
            gap: 8px;
        }

        #search-input {
            flex: 1;
            padding: 12px 16px;
            border: 2px solid #ddd;
            border-radius: 24px;
            font-size: 16px;
            outline: none;
            transition: border-color 0.2s;
        }

        #search-input:focus {
            border-color: #4a90d9;
        }

        #search-button {
            padding: 12px 24px;
            border: none;
            border-radius: 24px;
            background: #4a90d9;
            color: white;
            font-size: 16px;
            cursor: pointer;
        }

        #search-button:hover {
            background: #357abd;
        }
    </style>
</head>
<body>

    <div id="map"></div>

    <div id="bottom-panel">
        <div id="layers">
            <button class="active" onclick="setLayer('normal', this)">Обычная карта</button>
            <button onclick="setLayer('temperature', this)">Температура</button>
            <button onclick="setLayer('religion', this)">Религия</button>
            <button onclick="setLayer('languages', this)">Языки</button>
            <button onclick="setLayer('climate', this)">Климатические зоны</button>
        </div>

        <div id="search-box">
            <input type="text" id="search-input" placeholder="Введите место на карте...">
            <button id="search-button" onclick="searchPlace()">Найти</button>
        </div>
    </div>

    <!-- ТВОЙ API-КЛЮЧ УЖЕ ВСТАВЛЕН -->
    <script src="https://api-maps.yandex.ru/2.1/?apikey=abf43157-6a8e-4a02-a1dc-f092002685ce&lang=ru_RU"></script>

    <script>
        var map;

        ymaps.ready(function () {
            map = new ymaps.Map("map", {
                center: [20, 0],
                zoom: 2,
                controls: ['zoomControl', 'typeSelector']
            });
        });

        function setLayer(layerName, btn) {
            document.querySelectorAll('#layers button').forEach(function(b) {
                b.classList.remove('active');
            });
            btn.classList.add('active');

            if (layerName === 'normal') {
                console.log('Обычная карта');
            } else if (layerName === 'temperature') {
                console.log('Слой температуры — данные будут позже');
            } else if (layerName === 'religion') {
                console.log('Слой религии — данные будут позже');
            } else if (layerName === 'languages') {
                console.log('Слой языков — данные будут позже');
            } else if (layerName === 'climate') {
                console.log('Слой климатических зон — данные будут позже');
            }
        }

        function searchPlace() {
            var query = document.getElementById('search-input').value;
            if (!query) return;

            ymaps.geocode(query).then(function (res) {
                var first = res.geoObjects.get(0);
                if (first) {
                    var coords = first.geometry.getCoordinates();
                    map.setCenter(coords, 10);
                    map.geoObjects.removeAll();
                    map.geoObjects.add(new ymaps.Placemark(coords, {
                        balloonContent: first.properties.get('name')
                    }));
                } else {
                    alert('Место не найдено');
                }
            }).catch(function (err) {
                console.error('Ошибка геокодера:', err);
                alert('Ошибка поиска. Проверь API-ключ.');
            });
        }

        document.getElementById('search-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') searchPlace();
        });
    </script>

</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def index():
    return HTML_PAGE


def open_browser():
    webbrowser.open("http://127.0.0.1:8000")


if __name__ == "__main__":
    threading.Timer(1.5, open_browser).start()
    uvicorn.run(app, host="127.0.0.1", port=8000)