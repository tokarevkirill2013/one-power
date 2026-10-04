import webbrowser
import http.server
import socketserver
import os
import threading
import time

# Создаем HTML-файл с игрой
html_content = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚔️ Derivative Duel - Математическая дуэль</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0a0e27 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
        }
        .game-container {
            background: rgba(20, 25, 55, 0.95);
            border-radius: 30px;
            padding: 30px;
            border: 2px solid rgba(100, 150, 255, 0.3);
            box-shadow: 0 0 60px rgba(50, 100, 255, 0.2);
            max-width: 900px;
            width: 95%;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            color: #8ab4ff;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        .health-bar {
            flex: 1;
            margin: 0 20px;
            height: 8px;
            background: #1a1f3a;
            border-radius: 4px;
            overflow: hidden;
        }
        .health-fill {
            height: 100%;
            background: linear-gradient(90deg, #00ff88, #00ccff);
            transition: width 0.3s ease;
            border-radius: 4px;
        }
        .health-fill.enemy {
            background: linear-gradient(90deg, #ff6b6b, #ff3366);
        }
        .arena {
            background: rgba(0, 0, 0, 0.5);
            border-radius: 20px;
            padding: 20px;
            margin: 15px 0;
            border: 1px solid rgba(100, 150, 255, 0.15);
        }
        canvas {
            display: block;
            width: 100%;
            height: auto;
            border-radius: 10px;
            background: #0a0e1f;
            cursor: crosshair;
        }
        .battle-log {
            background: rgba(0, 0, 0, 0.4);
            border-radius: 10px;
            padding: 15px;
            margin: 15px 0;
            min-height: 60px;
            max-height: 80px;
            overflow-y: auto;
            color: #88bbff;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            border: 1px solid rgba(100, 150, 255, 0.1);
        }
        .battle-log::-webkit-scrollbar {
            width: 4px;
        }
        .battle-log::-webkit-scrollbar-thumb {
            background: #3366ff;
            border-radius: 2px;
        }
        .controls {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin: 15px 0;
        }
        .player-panel {
            background: rgba(0, 50, 150, 0.2);
            border-radius: 15px;
            padding: 15px;
            border: 1px solid rgba(50, 150, 255, 0.2);
        }
        .player-panel.enemy-panel {
            background: rgba(150, 0, 50, 0.2);
            border-color: rgba(255, 50, 100, 0.2);
        }
        .player-panel h4 {
            color: #8ab4ff;
            margin-bottom: 10px;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .player-panel.enemy-panel h4 {
            color: #ff6b8a;
        }
        .function-display {
            background: rgba(0, 0, 0, 0.5);
            border-radius: 8px;
            padding: 12px;
            text-align: center;
            font-family: 'Courier New', monospace;
            font-size: 22px;
            color: #ffffff;
            margin-bottom: 10px;
            min-height: 50px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        .btn-group {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 8px;
        }
        .btn {
            padding: 10px 8px;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.2s;
            font-family: 'Courier New', monospace;
            background: rgba(50, 100, 200, 0.3);
            color: #8ab4ff;
            border: 1px solid rgba(50, 100, 200, 0.3);
        }
        .btn:hover {
            transform: scale(1.05);
            background: rgba(50, 100, 200, 0.5);
            box-shadow: 0 0 20px rgba(50, 100, 255, 0.2);
        }
        .btn:active {
            transform: scale(0.95);
        }
        .btn.enemy-btn {
            background: rgba(200, 50, 50, 0.3);
            border-color: rgba(200, 50, 50, 0.3);
            color: #ff6b8a;
        }
        .btn.enemy-btn:hover {
            background: rgba(200, 50, 50, 0.5);
        }
        .btn.primary {
            background: linear-gradient(135deg, #3366ff, #00ccff);
            color: white;
            border: none;
        }
        .btn.primary:hover {
            box-shadow: 0 0 30px rgba(50, 150, 255, 0.4);
        }
        .btn.danger {
            background: linear-gradient(135deg, #ff3366, #ff6b6b);
            color: white;
            border: none;
        }
        .btn.danger:hover {
            box-shadow: 0 0 30px rgba(255, 50, 100, 0.4);
        }
        .btn.success {
            background: linear-gradient(135deg, #00cc88, #00ff88);
            color: #0a0e27;
            border: none;
        }
        .btn.success:hover {
            box-shadow: 0 0 30px rgba(0, 255, 136, 0.3);
        }
        .btn:disabled {
            opacity: 0.4;
            cursor: not-allowed;
            transform: none !important;
        }
        .status-text {
            text-align: center;
            color: #88bbff;
            font-size: 16px;
            margin: 10px 0;
            min-height: 24px;
            font-weight: bold;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .waiting {
            animation: pulse 1s infinite;
        }
        .footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 15px;
            color: #446688;
            font-size: 12px;
        }
        .score {
            color: #ffd700;
            font-weight: bold;
            font-size: 16px;
        }
    </style>
</head>
<body>

<div class="game-container">
    <div class="header">
        <span>⚔️ DUEL</span>
        <div class="health-bar">
            <div class="health-fill" id="playerHealth" style="width: 100%"></div>
        </div>
        <span id="playerHealthText">100 HP</span>
        <span style="margin: 0 10px;">VS</span>
        <span id="enemyHealthText">100 HP</span>
        <div class="health-bar">
            <div class="health-fill enemy" id="enemyHealth" style="width: 100%"></div>
        </div>
        <span>🎯</span>
    </div>

    <div class="arena">
        <canvas id="gameCanvas" width="800" height="300"></canvas>
    </div>

    <div class="battle-log" id="battleLog">
        <span style="color: #446688;">Добро пожаловать в Derivative Duel! Выберите функцию для атаки...</span>
    </div>

    <div class="status-text" id="statusText">🎯 Ваш ход! Выберите функцию для атаки</div>

    <div class="controls">
        <div class="player-panel">
            <h4>👤 Игрок</h4>
            <div class="function-display" id="playerFunction">f(x) = ?</div>
            <div class="btn-group">
                <button class="btn" onclick="selectPlayerFunction('x')">x</button>
                <button class="btn" onclick="selectPlayerFunction('x^2')">x²</button>
                <button class="btn" onclick="selectPlayerFunction('x^3')">x³</button>
                <button class="btn" onclick="selectPlayerFunction('sin(x)')">sin(x)</button>
                <button class="btn" onclick="selectPlayerFunction('cos(x)')">cos(x)</button>
                <button class="btn" onclick="selectPlayerFunction('e^x')">eˣ</button>
            </div>
            <button class="btn primary" id="attackBtn" onclick="playerAttack()" style="width:100%;margin-top:10px;padding:12px;">
                ⚡ АТАКА
            </button>
        </div>

        <div class="player-panel enemy-panel">
            <h4>🤖 Противник</h4>
            <div class="function-display" id="enemyFunction">f(x) = ?</div>
            <div class="btn-group">
                <button class="btn enemy-btn" disabled>Защита</button>
                <button class="btn enemy-btn" disabled>Контратака</button>
                <button class="btn enemy-btn" disabled>Блок</button>
            </div>
            <button class="btn danger" id="defendBtn" onclick="playerDefend()" style="width:100%;margin-top:10px;padding:12px;" disabled>
                🛡️ ЗАЩИТА (Интеграл)
            </button>
        </div>
    </div>

    <div class="footer">
        <span>🏆 Побед: <span class="score" id="playerScore">0</span></span>
        <span>📐 Математическая дуэль v1.0</span>
        <span>💀 Поражений: <span class="score" id="enemyScore">0</span></span>
    </div>
</div>

<script>
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    const log = document.getElementById('battleLog');
    const statusText = document.getElementById('statusText');

    // Состояние игры
    let gameState = {
        playerHP: 100,
        enemyHP: 100,
        maxHP: 100,
        playerFunc: null,
        enemyFunc: null,
        playerFuncName: '?',
        enemyFuncName: '?',
        isPlayerTurn: true,
        isWaiting: false,
        playerScore: 0,
        enemyScore: 0,
        battleHistory: [],
        defending: false,
        defenseResult: null,
        projectile: null,
        particles: [],
        turnPhase: 'idle' // idle, attacking, defending, resolving
    };

    // Функции и их значения
    const functions = {
        'x': { f: (x) => x, integral: 'x²/2', derivative: '1' },
        'x^2': { f: (x) => x*x, integral: 'x³/3', derivative: '2x' },
        'x^3': { f: (x) => x*x*x, integral: 'x⁴/4', derivative: '3x²' },
        'sin(x)': { f: (x) => Math.sin(x), integral: '-cos(x)', derivative: 'cos(x)' },
        'cos(x)': { f: (x) => Math.cos(x), integral: 'sin(x)', derivative: '-sin(x)' },
        'e^x': { f: (x) => Math.exp(x), integral: 'eˣ', derivative: 'eˣ' }
    };

    // Выбор функции игроком
    window.selectPlayerFunction = function(funcName) {
        if (gameState.isWaiting || !gameState.isPlayerTurn) return;
        gameState.playerFunc = functions[funcName];
        gameState.playerFuncName = funcName;
        document.getElementById('playerFunction').textContent = `f(x) = ${funcName}`;
        document.getElementById('playerFunction').style.color = '#00ff88';
        addLog(`Вы выбрали: f(x) = ${funcName}`);
    };

    // Атака игрока
    window.playerAttack = function() {
        if (gameState.isWaiting || !gameState.isPlayerTurn || !gameState.playerFunc) {
            addLog('⚠️ Сначала выберите функцию!');
            return;
        }
        if (gameState.enemyHP <= 0 || gameState.playerHP <= 0) {
            resetGame();
            return;
        }

        gameState.isWaiting = true;
        gameState.isPlayerTurn = false;
        document.getElementById('attackBtn').disabled = true;
        document.getElementById('defendBtn').disabled = true;
        statusText.textContent = '⚡ Атака!';

        // Анимация выстрела
        const attackX = 100;
        const targetX = 700;
        let progress = 0;
        const attackValue = gameState.playerFunc.f(3);

        addLog(`🎯 Вы атакуете f(x) = ${gameState.playerFuncName} → значение ${attackValue.toFixed(2)}`);

        // Анимация снаряда
        const projectile = { x: attackX, y: 150, progress: 0, targetX: targetX, speed: 0.02 };

        function animateShot() {
            if (progress >= 1) {
                // Попадание
                resolvePlayerAttack(attackValue);
                return;
            }
            progress += 0.025;
            const px = attackX + (targetX - attackX) * progress;
            const py = 150 + Math.sin(progress * 20) * 30;

            ctx.clearRect(0, 0, canvas.width, canvas.height);
            drawArena();
            drawProjectile(px, py, '#00ff88');

            // Частицы следа
            for (let i = 0; i < 3; i++) {
                gameState.particles.push({
                    x: px + Math.random() * 10 - 5,
                    y: py + Math.random() * 10 - 5,
                    life: 1,
                    vx: Math.random() * 2 - 1,
                    vy: Math.random() * 2 - 1,
                    color: '#00ff88'
                });
            }
            drawParticles();

            requestAnimationFrame(animateShot);
        }
        animateShot();
    };

    function resolvePlayerAttack(attackValue) {
        // Враг защищается (автоматически)
        const enemyDefense = Math.random();
        let defenseMultiplier = 0;
        let defenseText = '';

        if (enemyDefense < 0.4) {
            // Плохая защита
            defenseMultiplier = 1.5;
            defenseText = '❌ Плохая защита!';
        } else if (enemyDefense < 0.7) {
            // Средняя защита
            defenseMultiplier = 0.8;
            defenseText = '🛡️ Частичная защита';
        } else {
            // Хорошая защита
            defenseMultiplier = 0.3;
            defenseText = '✨ Отличная защита!';
        }

        const damage = attackValue * defenseMultiplier * 0.5 + 5;
        const actualDamage = Math.min(damage, gameState.enemyHP);
        gameState.enemyHP -= actualDamage;

        if (gameState.enemyHP < 0) gameState.enemyHP = 0;

        updateHealthBars();
        addLog(`${defenseText} Урон: ${actualDamage.toFixed(1)} HP`);

        // Визуализация попадания
        for (let i = 0; i < 30; i++) {
            gameState.particles.push({
                x: 700 + Math.random() * 60 - 30,
                y: 150 + Math.random() * 60 - 30,
                life: 1,
                vx: Math.random() * 8 - 4,
                vy: Math.random() * 8 - 4,
                color: '#ff6b6b'
            });
        }

        drawParticles();

        if (gameState.enemyHP <= 0) {
            gameState.playerScore++;
            document.getElementById('playerScore').textContent = gameState.playerScore;
            addLog('🎉 ПОБЕДА! Вы уничтожили противника!');
            statusText.textContent = '🏆 ПОБЕДА! Нажмите атаку для нового раунда';
            resetGame();
            return;
        }

        // Ход противника
        setTimeout(() => {
            gameState.isWaiting = false;
            enemyTurn();
        }, 1000);
    }

    // Ход противника
    function enemyTurn() {
        if (gameState.playerHP <= 0) {
            resetGame();
            return;
        }

        statusText.textContent = '🤖 Ход противника...';
        addLog('🤖 Противник готовится к атаке...');

        const enemyFuncs = ['x', 'x^2', 'sin(x)', 'cos(x)', 'e^x'];
        const choice = enemyFuncs[Math.floor(Math.random() * enemyFuncs.length)];
        gameState.enemyFunc = functions[choice];
        gameState.enemyFuncName = choice;
        document.getElementById('enemyFunction').textContent = `f(x) = ${choice}`;
        document.getElementById('enemyFunction').style.color = '#ff6b6b';

        const attackValue = gameState.enemyFunc.f(3);
        addLog(`🤖 Противник атакует f(x) = ${choice} → значение ${attackValue.toFixed(2)}`);

        // Анимация атаки противника
        const attackX = 700;
        const targetX = 100;
        let progress = 0;

        function animateEnemyShot() {
            if (progress >= 1) {
                // Игрок должен защищаться
                document.getElementById('defendBtn').disabled = false;
                document.getElementById('defendBtn').textContent = `🛡️ ЗАЩИТА (Интеграл от ${choice})`;
                document.getElementById('defendBtn').style.background = 'linear-gradient(135deg, #ff6b6b, #ff3366)';
                gameState.defending = true;
                gameState.defenseResult = null;
                statusText.textContent = `⚠️ АТАКА! Защититесь интегралом от ${choice}!`;
                addLog(`⚠️ Быстро! Выберите интеграл от ${choice}!`);
                gameState.isWaiting = false;
                return;
            }
            progress += 0.025;
            const px = attackX - (attackX - targetX) * progress;
            const py = 150 + Math.sin(progress * 20 + 1) * 30;

            ctx.clearRect(0, 0, canvas.width, canvas.height);
            drawArena();
            drawProjectile(px, py, '#ff3366');

            for (let i = 0; i < 3; i++) {
                gameState.particles.push({
                    x: px + Math.random() * 10 - 5,
                    y: py + Math.random() * 10 - 5,
                    life: 1,
                    vx: Math.random() * 2 - 1,
                    vy: Math.random() * 2 - 1,
                    color: '#ff3366'
                });
            }
            drawParticles();

            requestAnimationFrame(animateEnemyShot);
        }
        animateEnemyShot();
    }

    // Защита игрока
    window.playerDefend = function() {
        if (!gameState.defending || gameState.isWaiting) return;

        // Варианты интегралов для выбора (3 неправильных, 1 правильный)
        const funcName = gameState.enemyFuncName;
        const correctIntegral = gameState.enemyFunc.integral;

        // Создаем варианты
        const options = [
            correctIntegral,
            'x²/2 + x',
            'x³/3 + 1',
            'sin(x) + x'
        ];

        // Перемешиваем
        for (let i = options.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [options[i], options[j]] = [options[j], options[i]];
        }

        // Показываем варианты кнопками
        const btnGroup = document.querySelector('.player-panel .btn-group');
        btnGroup.innerHTML = '';
        options.forEach(opt => {
            const btn = document.createElement('button');
            btn.className = 'btn';
            btn.textContent = opt;
            btn.onclick = function() {
                checkDefense(opt, correctIntegral);
            };
            btnGroup.appendChild(btn);
        });

        document.getElementById('defendBtn').disabled = true;
        statusText.textContent = '🔍 Выберите правильный интеграл!';
        addLog('🔍 Выберите правильный интеграл из предложенных...');
    };

    function checkDefense(selected, correct) {
        gameState.isWaiting = true;
        const isCorrect = selected === correct;

        if (isCorrect) {
            addLog('✅ Правильно! Контратака!');
            statusText.textContent = '✨ Отличная защита! Контратака!';
            // Контратака - урон врагу
            const counterDamage = 15 + Math.random() * 10;
            gameState.enemyHP -= counterDamage;
            if (gameState.enemyHP < 0) gameState.enemyHP = 0;
            updateHealthBars();

            // Эффект контратаки
            for (let i = 0; i < 40; i++) {
                gameState.particles.push({
                    x: 400 + Math.random() * 200 - 100,
                    y: 150 + Math.random() * 200 - 100,
                    life: 1,
                    vx: Math.random() * 10 - 5,
                    vy: Math.random() * 10 - 5,
                    color: '#ffd700'
                });
            }
            drawParticles();

            if (gameState.enemyHP <= 0) {
                gameState.playerScore++;
                document.getElementById('playerScore').textContent = gameState.playerScore;
                addLog('🎉 ПОБЕДА! Контратака уничтожила врага!');
                statusText.textContent = '🏆 ПОБЕДА!';
                resetGame();
                return;
            }
        } else {
            addLog(`❌ Неправильно! Правильный ответ: ${correct}`);
            statusText.textContent = '💥 Вы получили урон!';
            const damage = 20 + Math.random() * 15;
            gameState.playerHP -= damage;
            if (gameState.playerHP < 0) gameState.playerHP = 0;
            updateHealthBars();

            if (gameState.playerHP <= 0) {
                gameState.enemyScore++;
                document.getElementById('enemyScore').textContent = gameState.enemyScore;
                addLog('💀 Вы проиграли!');
                statusText.textContent = '💀 ПОРАЖЕНИЕ!';
                resetGame();
                return;
            }
        }

        // Восстанавливаем кнопки
        setTimeout(() => {
            document.getElementById('attackBtn').disabled = false;
            document.getElementById('defendBtn').disabled = true;
            gameState.isWaiting = false;
            gameState.isPlayerTurn = true;
            gameState.defending = false;
            statusText.textContent = '🎯 Ваш ход! Выберите функцию для атаки';
            document.getElementById('defendBtn').textContent = '🛡️ ЗАЩИТА (Интеграл)';

            // Восстанавливаем кнопки выбора функции
            const btnGroup = document.querySelector('.player-panel .btn-group');
            btnGroup.innerHTML = `
                <button class="btn" onclick="selectPlayerFunction('x')">x</button>
                <button class="btn" onclick="selectPlayerFunction('x^2')">x²</button>
                <button class="btn" onclick="selectPlayerFunction('x^3')">x³</button>
                <button class="btn" onclick="selectPlayerFunction('sin(x)')">sin(x)</button>
                <button class="btn" onclick="selectPlayerFunction('cos(x)')">cos(x)</button>
                <button class="btn" onclick="selectPlayerFunction('e^x')">eˣ</button>
            `;

            if (gameState.enemyHP > 0 && gameState.playerHP > 0) {
                enemyTurn();
            }
        }, 1500);
    }

    // Функции отрисовки
    function drawArena() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Сетка
        ctx.strokeStyle = 'rgba(50, 100, 200, 0.1)';
        ctx.lineWidth = 1;
        for (let x = 0; x < canvas.width; x += 40) {
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, canvas.height);
            ctx.stroke();
        }
        for (let y = 0; y < canvas.height; y += 40) {
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(canvas.width, y);
            ctx.stroke();
        }

        // Игроки
        drawPlayer(100, 150, '#00ff88', '👤', gameState.playerHP);
        drawPlayer(700, 150, '#ff6b6b', '🤖', gameState.enemyHP);

        // Подписи функций
        ctx.fillStyle = '#446688';
        ctx.font = '12px monospace';
        ctx.fillText(`Ваша функция: ${gameState.playerFuncName}`, 20, 280);
        ctx.fillText(`Функция врага: ${gameState.enemyFuncName}`, 620, 280);
    }

    function drawPlayer(x, y, color, emoji, hp) {
        // Круг с пульсирующим эффектом
        const gradient = ctx.createRadialGradient(x, y, 5, x, y, 30);
        gradient.addColorStop(0, color);
        gradient.addColorStop(1, 'rgba(0,0,0,0)');
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(x, y, 30, 0, Math.PI * 2);
        ctx.fill();

        // Основной круг
        ctx.strokeStyle = color;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(x, y, 20, 0, Math.PI * 2);
        ctx.stroke();

        ctx.fillStyle = '#ffffff';
        ctx.font = '24px sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(emoji, x, y);

        // HP bar
        const hpPercent = hp / 100;
        ctx.fillStyle = 'rgba(0,0,0,0.5)';
        ctx.fillRect(x - 25, y + 25, 50, 4);
        ctx.fillStyle = hpPercent > 0.5 ? '#00ff88' : hpPercent > 0.25 ? '#ffaa00' : '#ff3333';
        ctx.fillRect(x - 25, y + 25, 50 * hpPercent, 4);
    }

    function drawProjectile(x, y, color) {
        ctx.shadowColor = color;
        ctx.shadowBlur = 20;
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.arc(x, y, 8, 0, Math.PI * 2);
        ctx.fill();
        ctx.shadowBlur = 0;

        // Свечение
        const gradient = ctx.createRadialGradient(x, y, 2, x, y, 25);
        gradient.addColorStop(0, color);
        gradient.addColorStop(1, 'rgba(0,0,0,0)');
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(x, y, 25, 0, Math.PI * 2);
        ctx.fill();
    }

    function drawParticles() {
        gameState.particles = gameState.particles.filter(p => p.life > 0);
        gameState.particles.forEach(p => {
            p.x += p.vx;
            p.y += p.vy;
            p.life -= 0.02;
            p.vy += 0.1;

            ctx.globalAlpha = p.life;
            ctx.fillStyle = p.color;
            ctx.beginPath();
            ctx.arc(p.x, p.y, 3 * p.life, 0, Math.PI * 2);
            ctx.fill();
        });
        ctx.globalAlpha = 1;
    }

    function updateHealthBars() {
        const playerPercent = (gameState.playerHP / gameState.maxHP) * 100;
        const enemyPercent = (gameState.enemyHP / gameState.maxHP) * 100;

        document.getElementById('playerHealth').style.width = playerPercent + '%';
        document.getElementById('enemyHealth').style.width = enemyPercent + '%';
        document.getElementById('playerHealthText').textContent = `${Math.round(gameState.playerHP)} HP`;
        document.getElementById('enemyHealthText').textContent = `${Math.round(gameState.enemyHP)} HP`;
    }

    function addLog(message) {
        const logDiv = document.getElementById('battleLog');
        const time = new Date().toLocaleTimeString();
        logDiv.innerHTML += `<div style="color: #88bbff; opacity: 0.8; font-size: 12px;">[${time}] ${message}</div>`;
        logDiv.scrollTop = logDiv.scrollHeight;
        if (logDiv.children.length > 20) {
            logDiv.removeChild(logDiv.children[0]);
        }
    }

    function resetGame() {
        gameState.playerHP = 100;
        gameState.enemyHP = 100;
        gameState.isPlayerTurn = true;
        gameState.isWaiting = false;
        gameState.defending = false;
        gameState.playerFunc = null;
        gameState.enemyFunc = null;
        gameState.playerFuncName = '?';
        gameState.enemyFuncName = '?';

        document.getElementById('playerFunction').textContent = 'f(x) = ?';
        document.getElementById('playerFunction').style.color = '#ffffff';
        document.getElementById('enemyFunction').textContent = 'f(x) = ?';
        document.getElementById('enemyFunction').style.color = '#ffffff';
        document.getElementById('attackBtn').disabled = false;
        document.getElementById('defendBtn').disabled = true;
        document.getElementById('defendBtn').textContent = '🛡️ ЗАЩИТА (Интеграл)';
        document.getElementById('defendBtn').style.background = 'linear-gradient(135deg, #ff3366, #ff6b6b)';

        updateHealthBars();

        if (gameState.playerHP <= 0) {
            statusText.textContent = '💀 Поражение! Нажмите атаку чтобы начать заново';
        } else if (gameState.enemyHP <= 0) {
            statusText.textContent = '🏆 Победа! Нажмите атаку для нового раунда';
        } else {
            statusText.textContent = '🎯 Новый раунд! Выберите функцию для атаки';
        }

        // Восстанавливаем кнопки выбора функции
        const btnGroup = document.querySelector('.player-panel .btn-group');
        btnGroup.innerHTML = `
            <button class="btn" onclick="selectPlayerFunction('x')">x</button>
            <button class="btn" onclick="selectPlayerFunction('x^2')">x²</button>
            <button class="btn" onclick="selectPlayerFunction('x^3')">x³</button>
            <button class="btn" onclick="selectPlayerFunction('sin(x)')">sin(x)</button>
            <button class="btn" onclick="selectPlayerFunction('cos(x)')">cos(x)</button>
            <button class="btn" onclick="selectPlayerFunction('e^x')">eˣ</button>
        `;
    }

    // Основной цикл анимации
    function gameLoop() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawArena();
        drawParticles();

        // Автоматическая анимация врага, если его очередь
        if (!gameState.isPlayerTurn && !gameState.isWaiting && gameState.enemyHP > 0 && gameState.playerHP > 0) {
            // Небольшая задержка перед ходом врага
        }

        requestAnimationFrame(gameLoop);
    }

    // Запуск
    document.getElementById('attackBtn').addEventListener('click', function() {
        if (gameState.enemyHP <= 0 || gameState.playerHP <= 0) {
            resetGame();
        }
    });

    // Инициализация
    gameState.playerFunc = functions['x'];
    gameState.playerFuncName = 'x';
    document.getElementById('playerFunction').textContent = 'f(x) = x';

    updateHealthBars();
    gameLoop();

    // Стили для скроллбара лога
    const style = document.createElement('style');
    style.textContent = `
        .battle-log::-webkit-scrollbar {
            width: 4px;
        }
        .battle-log::-webkit-scrollbar-thumb {
            background: #3366ff;
            border-radius: 2px;
        }
    `;
    document.head.appendChild(style);

    addLog('🎮 Игра загружена! Выберите функцию и атакуйте!');
</script>

</body>
</html>
'''

# Сохраняем HTML файл
html_file = "derivative_duel.html"
with open(html_file, "w", encoding="utf-8") as f:
    f.write(html_content)

# Запускаем сервер и открываем браузер
PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

def open_browser():
    time.sleep(1)
    webbrowser.open(f'http://localhost:{PORT}/{html_file}')

# Запускаем сервер в отдельном потоке
threading.Thread(target=open_browser, daemon=True).start()

try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Сервер запущен на http://localhost:{PORT}")
        print(f"Игра доступна по адресу: http://localhost:{PORT}/{html_file}")
        print("Нажмите Ctrl+C для остановки сервера")
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\nСервер остановлен")
finally:
    # Удаляем HTML файл после завершения
    if os.path.exists(html_file):
        try:
            os.remove(html_file)
        except:
            pass