import webbrowser
import os
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Создаем HTML файл
html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🍽️ Ассистент по питанию</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            color: white;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .card h2 {
            color: #333;
            margin-bottom: 15px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        .grid-3 {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 20px;
        }
        .form-group {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        .form-group input, .form-group select {
            flex: 1;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            min-width: 150px;
        }
        .btn {
            padding: 12px 25px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            color: white;
        }
        .btn-primary {
            background: #667eea;
        }
        .btn-primary:hover {
            background: #5a67d8;
            transform: translateY(-2px);
        }
        .btn-danger {
            background: #e53e3e;
        }
        .btn-danger:hover {
            background: #c53030;
        }
        .btn-success {
            background: #48bb78;
        }
        .btn-success:hover {
            background: #38a169;
        }
        .btn-warning {
            background: #ed8936;
        }
        .btn-warning:hover {
            background: #dd6b20;
        }
        .btn-purple {
            background: #9f7aea;
        }
        .btn-purple:hover {
            background: #805ad5;
        }
        .btn-secondary {
            background: #a0aec0;
        }
        .btn-secondary:hover {
            background: #718096;
        }
        .product-list {
            list-style: none;
            padding: 0;
        }
        .product-list li {
            padding: 12px;
            background: #f7fafc;
            margin-bottom: 8px;
            border-radius: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-left: 4px solid #667eea;
        }
        .product-list li .remove-btn {
            background: #fc8181;
            color: white;
            border: none;
            padding: 5px 15px;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .product-list li .remove-btn:hover {
            background: #e53e3e;
        }
        .plan-item {
            background: #f0fff4;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 10px;
            border-left: 4px solid #48bb78;
        }
        .plan-item.recommended {
            background: #fff5f5;
            border-left-color: #e53e3e;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
        }
        .stat-box {
            background: #f7fafc;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        .stat-box .number {
            font-size: 28px;
            font-weight: bold;
            color: #667eea;
        }
        .stat-box .label {
            color: #718096;
            font-size: 14px;
            margin-top: 5px;
        }
        .shopping-item {
            background: #ebf8ff;
            padding: 10px 15px;
            border-radius: 8px;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            border-left: 4px solid #4299e1;
        }
        .message {
            padding: 12px;
            border-radius: 8px;
            margin-top: 10px;
            display: none;
        }
        .message.success {
            display: block;
            background: #c6f6d5;
            color: #22543d;
        }
        .message.error {
            display: block;
            background: #fed7d7;
            color: #742a2a;
        }
        .hidden {
            display: none;
        }
        .tab-btn {
            padding: 10px 20px;
            border: none;
            border-radius: 8px 8px 0 0;
            cursor: pointer;
            background: #e2e8f0;
            font-weight: 600;
            transition: all 0.3s;
        }
        .tab-btn.active {
            background: #667eea;
            color: white;
        }
        .tab-content {
            display: none;
            padding-top: 20px;
        }
        .tab-content.active {
            display: block;
        }
        .category-tag {
            display: inline-block;
            padding: 2px 10px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            background: #e2e8f0;
            color: #4a5568;
        }
        @media (max-width: 768px) {
            .grid-2, .grid-3, .stats-grid {
                grid-template-columns: 1fr;
            }
            .form-group {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🍽️ Ассистент по питанию</h1>

        <div id="message" class="message"></div>

        <div class="grid-2">
            <div class="card">
                <h2>📦 Добавить продукты</h2>
                <div class="form-group">
                    <input type="text" id="productInput" placeholder="Название продукта" list="productList">
                    <datalist id="productList"></datalist>
                    <input type="number" id="quantityInput" placeholder="Кол-во" value="1" min="1" style="max-width: 100px;">
                    <button class="btn btn-primary" onclick="addProduct()">Добавить</button>
                </div>
                <div style="margin-top: 15px; display: flex; gap: 10px; flex-wrap: wrap;">
                    <button class="btn btn-danger" onclick="resetAll()">🗑️ Сбросить всё</button>
                    <button class="btn btn-secondary" onclick="addExampleProducts()">📋 Пример</button>
                </div>
            </div>

            <div class="card">
                <h2>📊 Статистика</h2>
                <div class="stats-grid" id="statsGrid">
                    <div class="stat-box">
                        <div class="number" id="statProducts">0</div>
                        <div class="label">Продуктов</div>
                    </div>
                    <div class="stat-box">
                        <div class="number" id="statCalories">0</div>
                        <div class="label">Ккал</div>
                    </div>
                    <div class="stat-box">
                        <div class="number" id="statProtein">0</div>
                        <div class="label">Белки (г)</div>
                    </div>
                    <div class="stat-box">
                        <div class="number" id="statCarbs">0</div>
                        <div class="label">Углеводы (г)</div>
                    </div>
                </div>
            </div>
        </div>

        <div class="card">
            <div style="display: flex; gap: 10px; flex-wrap: wrap; border-bottom: 2px solid #e2e8f0; margin-bottom: 15px;">
                <button class="tab-btn active" onclick="switchTab('products')">🛒 Мои продукты</button>
                <button class="tab-btn" onclick="switchTab('plan')">📋 План питания</button>
                <button class="tab-btn" onclick="switchTab('shopping')">🛍️ Список покупок</button>
            </div>

            <div id="tab-products" class="tab-content active">
                <ul class="product-list" id="productListUI">
                    <li style="color: #718096; text-align: center; border-left: none;">Нет добавленных продуктов</li>
                </ul>
            </div>

            <div id="tab-plan" class="tab-content">
                <div class="form-group" style="margin-bottom: 15px;">
                    <input type="number" id="caloriesTarget" placeholder="Целевая калорийность" value="2000" min="500" max="5000">
                    <button class="btn btn-success" onclick="generatePlan()">🔄 Сгенерировать план</button>
                </div>
                <div id="planUI">
                    <p style="color: #718096; text-align: center;">Добавьте продукты и сгенерируйте план</p>
                </div>
            </div>

            <div id="tab-shopping" class="tab-content">
                <button class="btn btn-purple" onclick="generateShoppingList()" style="margin-bottom: 15px;">🔄 Обновить список</button>
                <div id="shoppingListUI">
                    <p style="color: #718096; text-align: center;">Сгенерируйте список покупок</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        // База данных продуктов
        const PRODUCTS_DB = {
            'курица': {calories: 165, protein: 31, carbs: 0, fat: 3.6, category: 'мясо '},
            'рис': {calories: 130, protein: 2.7, carbs: 28, fat: 0.3, category: 'крупы'},
            'гречка': {calories: 110, protein: 3.8, carbs: 23, fat: 0.8, category: 'крупы'},
            'овсянка': {calories: 88, protein: 3.4, carbs: 16, fat: 1.8, category: 'крупы'},
            'яблоко': {calories: 52, protein: 0.3, carbs: 14, fat: 0.2, category: 'фрукты'},
            'банан': {calories: 89, protein: 1.1, carbs: 23, fat: 0.3, category: 'фрукты'},
            'молоко': {calories: 60, protein: 3.2, carbs: 4.8, fat: 3.3, category: 'молочное'},
            'яйцо': {calories: 155, protein: 12.6, carbs: 1.2, fat: 10.6, category: 'яйца'},
            'хлеб': {calories: 265, protein: 9, carbs: 49, fat: 3.2, category: 'хлебобулочные'},
            'сыр': {calories: 350, protein: 25, carbs: 1.3, fat: 27, category: 'молочное'},
            'творог': {calories: 121, protein: 16.7, carbs: 2.6, fat: 5, category: 'молочное'},
            'картофель': {calories: 77, protein: 2, carbs: 17, fat: 0.1, category: 'овощи'},
            'морковь': {calories: 41, protein: 0.9, carbs: 9.6, fat: 0.1, category: 'овощи'},
            'лук': {calories: 40, protein: 1.1, carbs: 9.3, fat: 0.1, category: 'овощи'},
            'томат': {calories: 18, protein: 0.9, carbs: 3.9, fat: 0.2, category: 'овощи'},
            'макароны': {calories: 131, protein: 5, carbs: 27, fat: 1.1, category: 'крупы'},
            'рыба': {calories: 120, protein: 22, carbs: 0, fat: 3.5, category: 'рыба'},
            'оливковое масло': {calories: 884, protein: 0, carbs: 0, fat: 100, category: 'масла'},
            'кефир': {calories: 53, protein: 3.4, carbs: 4.7, fat: 2.5, category: 'молочное'},
            'творог': {calories: 121, protein: 16.7, carbs: 2.6, fat: 5, category: 'молочное'},
            'огурец': {calories: 15, protein: 0.6, carbs: 3.6, fat: 0.1, category: 'овощи'},
            'капуста': {calories: 25, protein: 1.3, carbs: 5.8, fat: 0.1, category: 'овощи'},
            'свекла': {calories: 42, protein: 1.6, carbs: 9.6, fat: 0.1, category: 'овощи'},
            'грецкий орех': {calories: 654, protein: 15, carbs: 14, fat: 65, category: 'орехи'},
            'миндаль': {calories: 579, protein: 21, carbs: 22, fat: 49, category: 'орехи'},
            'авокадо': {calories: 160, protein: 2, carbs: 9, fat: 15, category: 'фрукты'}
        };

        // Состояние приложения
        let userProducts = {};
        let mealPlan = [];
        let shoppingList = [];

        // Заполняем автодополнение
        function initProductList() {
            const datalist = document.getElementById('productList');
            Object.keys(PRODUCTS_DB).forEach(p => {
                const option = document.createElement('option');
                option.value = p;
                datalist.appendChild(option);
            });
        }

        function showMessage(text, type) {
            const msg = document.getElementById('message');
            msg.textContent = text;
            msg.className = 'message ' + type;
            setTimeout(() => {
                msg.className = 'message';
            }, 3000);
        }

        function addProduct() {
            const product = document.getElementById('productInput').value.trim().toLowerCase();
            const quantity = parseInt(document.getElementById('quantityInput').value) || 1;

            if (!product) {
                showMessage('Введите название продукта', 'error');
                return;
            }

            if (!(product in PRODUCTS_DB)) {
                showMessage(`Продукт "${product}" не найден в базе`, 'error');
                return;
            }

            if (product in userProducts) {
                userProducts[product] += quantity;
            } else {
                userProducts[product] = quantity;
            }

            showMessage(`✅ Продукт "${product}" добавлен (${quantity} шт)`, 'success');
            document.getElementById('productInput').value = '';
            loadData();
        }

        function removeProduct(product) {
            if (!confirm(`Удалить "${product}"?`)) return;
            delete userProducts[product];
            showMessage(`✅ "${product}" удален`, 'success');
            loadData();
        }

        function resetAll() {
            if (!confirm('Сбросить все продукты?')) return;
            userProducts = {};
            mealPlan = [];
            shoppingList = [];
            showMessage('✅ Всё сброшено', 'success');
            loadData();
        }

        function addExampleProducts() {
            const examples = {'курица': 2, 'рис': 1, 'овсянка': 1, 'яблоко': 3, 'молоко': 1};
            Object.entries(examples).forEach(([product, quantity]) => {
                if (product in userProducts) {
                    userProducts[product] += quantity;
                } else {
                    userProducts[product] = quantity;
                }
            });
            showMessage('✅ Добавлены примеры продуктов', 'success');
            loadData();
        }

        function generatePlan() {
            const caloriesTarget = parseInt(document.getElementById('caloriesTarget').value) || 2000;
            mealPlan = [];
            let totalCalories = 0;

            // Сортируем продукты по категориям для разнообразия
            const categories = {};
            Object.keys(userProducts).forEach(p => {
                const cat = PRODUCTS_DB[p].category;
                if (!categories[cat]) categories[cat] = [];
                categories[cat].push(p);
            });

            // Добавляем по 1-2 продукта из каждой категории
            let selectedProducts = [];
            Object.values(categories).forEach(catProducts => {
                const shuffled = catProducts.sort(() => 0.5 - Math.random());
                const count = Math.min(2, shuffled.length);
                for (let i = 0; i < count; i++) {
                    selectedProducts.push(shuffled[i]);
                }
            });

            // Если продуктов мало, добавляем все
            if (selectedProducts.length < 3) {
                selectedProducts = Object.keys(userProducts);
            }

            // Создаем план
            for (const product of selectedProducts) {
                if (product in PRODUCTS_DB) {
                    const info = PRODUCTS_DB[product];
                    const quantity = userProducts[product] || 1;
                    const calories = info.calories * quantity;

                    if (totalCalories + calories <= caloriesTarget * 1.3) {
                        mealPlan.push({
                            product: product,
                            quantity: quantity,
                            calories: Math.round(calories * 10) / 10,
                            protein: Math.round(info.protein * quantity * 10) / 10,
                            carbs: Math.round(info.carbs * quantity * 10) / 10,
                            fat: Math.round(info.fat * quantity * 10) / 10,
                            category: info.category,
                            recommended: false
                        });
                        totalCalories += calories;
                    }
                }
            }

            // Добавляем рекомендации, если мало калорий
            if (totalCalories < caloriesTarget * 0.5) {
                const recommendations = [
                    {product: 'курица', calories: 165, category: 'мясо'},
                    {product: 'рис', calories: 130, category: 'крупы'},
                    {product: 'овсянка', calories: 88, category: 'крупы'},
                    {product: 'творог', calories: 121, category: 'молочное'},
                    {product: 'яйцо', calories: 155, category: 'яйца'},
                    {product: 'банан', calories: 89, category: 'фрукты'}
                ];

                let remaining = caloriesTarget - totalCalories;
                for (const rec of recommendations) {
                    if (remaining > 50 && !(rec.product in userProducts)) {
                        const quantity = Math.max(1, Math.round(remaining / rec.calories / 2));
                        const info = PRODUCTS_DB[rec.product];
                        mealPlan.push({
                            product: rec.product + ' (рекомендовано)',
                            quantity: quantity,
                            calories: Math.round(info.calories * quantity * 10) / 10,
                            protein: Math.round(info.protein * quantity * 10) / 10,
                            carbs: Math.round(info.carbs * quantity * 10) / 10,
                            fat: Math.round(info.fat * quantity * 10) / 10,
                            category: info.category,
                            recommended: true
                        });
                        remaining -= info.calories * quantity;
                        totalCalories += info.calories * quantity;
                    }
                }
            }

            renderPlan();
            showMessage('✅ План питания сгенерирован', 'success');
        }

        function renderPlan() {
            const ui = document.getElementById('planUI');

            if (mealPlan.length === 0) {
                ui.innerHTML = '<p style="color: #718096; text-align: center;">Добавьте продукты и сгенерируйте план</p>';
                return;
            }

            let html = '';
            let totalCal = 0;
            mealPlan.forEach(item => {
                totalCal += item.calories;
                const recClass = item.recommended ? 'plan-item recommended' : 'plan-item';
                html += `
                    <div class="${recClass}">
                        <strong>${item.product}</strong> - ${item.quantity} шт
                        <span class="category-tag">${item.category}</span>
                        <br>
                        <small>${item.calories} ккал | ${item.protein}г белка | ${item.carbs}г углеводов | ${item.fat}г жиров</small>
                        ${item.recommended ? ' <span style="color: #e53e3e; font-weight: bold;">⭐ рекомендовано</span>' : ''}
                    </div>
                `;
            });

            const percent = Math.round((totalCal / parseFloat(document.getElementById('caloriesTarget').value || 2000)) * 100);
            html += `
                <div style="margin-top: 15px; padding: 15px; background: #f7fafc; border-radius: 8px;">
                    <div style="font-weight: bold; text-align: center; font-size: 18px;">
                        Итого: ${Math.round(totalCal)} ккал (${percent}% от цели)
                    </div>
                    <div style="width: 100%; height: 8px; background: #e2e8f0; border-radius: 4px; margin-top: 10px; overflow: hidden;">
                        <div style="height: 100%; width: ${Math.min(100, percent)}%; background: ${percent > 100 ? '#e53e3e' : '#48bb78'}; transition: width 0.5s;"></div>
                    </div>
                </div>
            `;
            ui.innerHTML = html;
        }

        function generateShoppingList() {
            shoppingList = [];

            // Добавляем продукты из плана
            for (const item of mealPlan) {
                const productName = item.product.replace(' (рекомендовано)', '');
                if (!shoppingList.find(p => p.product === productName)) {
                    shoppingList.push({
                        product: productName,
                        quantity: item.quantity,
                        category: PRODUCTS_DB[productName]?.category || 'другое'
                    });
                }
            }

            // Добавляем недостающие продукты из запасов
            for (const [product, quantity] of Object.entries(userProducts)) {
                if (!shoppingList.find(p => p.product === product)) {
                    shoppingList.push({
                        product: product,
                        quantity: quantity,
                        category: PRODUCTS_DB[product]?.category || 'другое'
                    });
                }
            }

            renderShoppingList();
            showMessage('✅ Список покупок обновлен', 'success');
            switchTab('shopping');
        }

        function renderShoppingList() {
            const ui = document.getElementById('shoppingListUI');

            if (shoppingList.length === 0) {
                ui.innerHTML = '<p style="color: #718096; text-align: center;">Сгенерируйте список покупок</p>';
                return;
            }

            let html = '';
            // Группируем по категориям
            const categories = {};
            shoppingList.forEach(item => {
                if (!categories[item.category]) categories[item.category] = [];
                categories[item.category].push(item);
            });

            Object.entries(categories).forEach(([category, items]) => {
                html += `<div style="margin-bottom: 15px;">
                    <h4 style="color: #4a5568; margin-bottom: 8px;">📁 ${category}</h4>`;
                items.forEach(item => {
                    html += `
                        <div class="shopping-item">
                            <span><strong>${item.product}</strong> - ${item.quantity} шт</span>
                            <span style="color: #718096; font-size: 14px;">
                                ${Math.round(PRODUCTS_DB[item.product]?.calories * item.quantity || 0)} ккал
                            </span>
                        </div>
                    `;
                });
                html += `</div>`;
            });

            ui.innerHTML = html;
        }

        function loadData() {
            // Обновляем список продуктов
            const list = document.getElementById('productListUI');
            const keys = Object.keys(userProducts);

            if (keys.length === 0) {
                list.innerHTML = '<li style="color: #718096; text-align: center; border-left: none;">Нет добавленных продуктов</li>';
            } else {
                let html = '';
                keys.forEach(key => {
                    const info = PRODUCTS_DB[key];
                    html += `
                        <li>
                            <div>
                                <strong>${key}</strong> - ${userProducts[key]} шт
                                <span class="category-tag">${info?.category || 'другое'}</span>
                                <span style="margin-left: 10px; color: #718096; font-size: 14px;">
                                    ${info ? Math.round(info.calories * userProducts[key]) : '?'} ккал
                                </span>
                            </div>
                            <button class="remove-btn" onclick="removeProduct('${key}')">✕</button>
                        </li>
                    `;
                });
                list.innerHTML = html;
            }

            // Обновляем статистику
            let totalCal = 0, totalProtein = 0, totalCarbs = 0, totalFat = 0;
            Object.entries(userProducts).forEach(([product, quantity]) => {
                if (product in PRODUCTS_DB) {
                    const info = PRODUCTS_DB[product];
                    totalCal += info.calories * quantity;
                    totalProtein += info.protein * quantity;
                    totalCarbs += info.carbs * quantity;
                    totalFat += info.fat * quantity;
                }
            });

            document.getElementById('statProducts').textContent = Object.keys(userProducts).length;
            document.getElementById('statCalories').textContent = Math.round(totalCal);
            document.getElementById('statProtein').textContent = Math.round(totalProtein * 10) / 10;
            document.getElementById('statCarbs').textContent = Math.round(totalCarbs * 10) / 10;
        }

        function switchTab(tab) {
            // Обновляем кнопки
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));

            // Показываем выбранную вкладку
            document.querySelector(`.tab-btn:nth-child(${tab === 'products' ? 1 : tab === 'plan' ? 2 : 3})`).classList.add('active');
            document.getElementById(`tab-${tab}`).classList.add('active');
        }

        // Инициализация
        initProductList();
        loadData();

        // Enter для добавления
        document.getElementById('productInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') addProduct();
        });
    </script>
</body>
</html>
"""

# Сохраняем HTML файл
with open('nutrition_assistant.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✅ Файл nutrition_assistant.html создан")
print("🚀 Открываю в браузере...")

# Открываем в браузере
webbrowser.open('nutrition_assistant.html')

# Запускаем простой сервер для корректной работы
PORT = 8000
os.chdir(os.path.dirname(os.path.abspath(__file__)))

try:
    print(f"🌐 Сервер запущен на http://localhost:{PORT}")
    print("Нажмите Ctrl+C для остановки")
    handler = SimpleHTTPRequestHandler
    httpd = HTTPServer(("", PORT), handler)
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\n👋 Сервер остановлен")
except OSError:
    print(f"⚠️ Порт {PORT} занят. Попробуйте открыть файл вручную: nutrition_assistant.html")
    webbrowser.open('nutrition_assistant.html')
