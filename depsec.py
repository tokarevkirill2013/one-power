import webbrowser
import os
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Создаем главную страницу с играми
main_html = """
<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🎮 ИГРОВОЙ ПОРТАЛ</title>
<style>
* {
margin: 0;
padding: 0;
box-sizing: border-box;
}
body {
font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
background: linear-gradient(135deg, #0a0a1a 0%, #1a0a2a 100%);
min-height: 100vh;
padding: 20px;
}
.container {
max-width: 1200px;
margin: 0 auto;
}
h1 {
color: #ffd700;
text-align: center;
margin-bottom: 30px;
font-size: 2.5em;
text-shadow: 0 0 20px rgba(255,215,0,0.3);
letter-spacing: 3px;
}
.balance {
font-size: 1.5em;
color: #ffd700;
text-align: center;
padding: 10px;
background: rgba(0,0,0,0.3);
border-radius: 10px;
margin-bottom: 15px;
font-weight: bold;
}
.game-grid {
display: grid;
grid-template-columns: repeat(4, 1fr);
gap: 20px;
margin: 20px 0;
}
.game-card {
background: rgba(30,10,10,0.9);
padding: 30px 20px;
border-radius: 15px;
text-align: center;
border: 2px solid #ffd70033;
cursor: pointer;
transition: all 0.3s;
text-decoration: none;
color: inherit;
}
.game-card:hover {
transform: scale(1.05);
border-color: #ffd700;
background: rgba(255,215,0,0.1);
box-shadow: 0 0 30px rgba(255,215,0,0.2);
}
.game-card .icon {
font-size: 4em;
}
.game-card .name {
color: #ffd700;
font-weight: bold;
font-size: 1.2em;
margin-top: 10px;
}
.game-card .desc {
color: #aa8866;
font-size: 14px;
margin-top: 5px;
}
.nav {
display: flex;
gap: 10px;
flex-wrap: wrap;
justify-content: center;
margin-bottom: 20px;
}
.nav-btn {
padding: 12px 25px;
border: 2px solid #ffd70044;
border-radius: 10px;
background: rgba(30,10,10,0.8);
color: #ffd700;
cursor: pointer;
font-size: 16px;
font-weight: bold;
transition: all 0.3s;
text-decoration: none;
}
.nav-btn:hover {
background: #ffd700;
color: #1a0a0a;
transform: scale(1.05);
}
.nav-btn.active {
background: #ffd700;
color: #1a0a0a;
}
.shop-grid {
display: grid;
grid-template-columns: repeat(3, 1fr);
gap: 15px;
margin: 15px 0;
}
.shop-item {
background: rgba(0,0,0,0.3);
padding: 20px;
border-radius: 10px;
text-align: center;
border: 1px solid #ffd70033;
}
.shop-item .icon {
font-size: 3em;
}
.shop-item .name {
color: #ffd700;
font-weight: bold;
margin-top: 10px;
}
.shop-item .price {
color: #66bbff;
margin: 10px 0;
}
.shop-item .owned {
color: #44ff88;
}
.btn {
padding: 12px 25px;
border: none;
border-radius: 8px;
font-size: 16px;
font-weight: 600;
cursor: pointer;
transition: all 0.3s;
color: #1a0a0a;
text-transform: uppercase;
}
.btn-buy {
background: linear-gradient(135deg, #ff6b6b, #ee5a24);
color: white;
}
.btn-buy:hover {
transform: scale(1.05);
}
.stats {
display: grid;
grid-template-columns: repeat(3, 1fr);
gap: 10px;
margin: 10px 0;
}
.stat-box {
background: rgba(0,0,0,0.3);
padding: 15px;
border-radius: 8px;
text-align: center;
border: 1px solid #ffd70022;
}
.stat-box .number {
font-size: 24px;
font-weight: bold;
color: #ffd700;
}
.stat-box .label {
color: #aa8866;
font-size: 12px;
margin-top: 3px;
}
@media (max-width: 768px) {
.game-grid, .shop-grid {
grid-template-columns: repeat(2, 1fr);
}
.stats {
grid-template-columns: repeat(2, 1fr);
}
}
</style>
</head>
<body>
<div class="container">
<h1>🎮 ИГРОВОЙ ПОРТАЛ</h1>
<div class="balance">💰 Баланс: <span id="balance">1000</span></div>

<div class="nav">
<a href="#games" class="nav-btn active" onclick="switchTab('games')">🎮 Игры</a>
<a href="#shop" class="nav-btn" onclick="switchTab('shop')">🛒 Магазин</a>
<a href="#stats" class="nav-btn" onclick="switchTab('stats')">📊 Статистика</a>
</div>

<!-- Игры -->
<div id="tab-games" class="active" style="display:block;">
<div class="game-grid">
<a href="casino.html" target="_blank" class="game-card">
<div class="icon">🎰</div>
<div class="name">Казино</div>
<div class="desc">Слоты с джекпотом</div>
</a>
<a href="chess.html" target="_blank" class="game-card">
<div class="icon">♟️</div>
<div class="name">Шахматы</div>
<div class="desc">Классические шахматы</div>
</a>
<a href="tictac.html" target="_blank" class="game-card">
<div class="icon">❌⭕</div>
<div class="name">Крестики-нолики</div>
<div class="desc">Игра против компьютера</div>
</a>
<a href="randomizer.html" target="_blank" class="game-card">
<div class="icon">🎲</div>
<div class="name">Рандомайзер</div>
<div class="desc">Генератор случайных чисел</div>
</a>
<a href="clicker.html" target="_blank" class="game-card">
<div class="icon">🖱️</div>
<div class="name">Кликер</div>
<div class="desc">Зарабатывай кликами</div>
</a>
<a href="dino.html" target="_blank" class="game-card">
<div class="icon">🦕</div>
<div class="name">Динозаврик</div>
<div class="desc">Прыгай и беги!</div>
</a>
<a href="war.html" target="_blank" class="game-card">
<div class="icon">⚔️</div>
<div class="name">Мировая война</div>
<div class="desc">Стратегия захвата</div>
</a>
</div>
</div>

<!-- Магазин -->
<div id="tab-shop" style="display:none;">
<h2 style="color:#ffd700; text-align:center;">🛒 МАГАЗИН</h2>
<div class="shop-grid" id="shopGrid"></div>
</div>

<!-- Статистика -->
<div id="tab-stats" style="display:none;">
<h2 style="color:#ffd700; text-align:center;">📊 СТАТИСТИКА</h2>
<div class="stats">
<div class="stat-box">
<div class="number" id="statGames">0</div>
<div class="label">Игр сыграно</div>
</div>
<div class="stat-box">
<div class="number" id="statWins">0</div>
<div class="label">Побед</div>
</div>
<div class="stat-box">
<div class="number" id="statEarnings">0</div>
<div class="label">Заработано</div>
</div>
</div>
</div>
</div>

<script>
const SHOP_ITEMS = [
    {id: 'x2', name: 'x2 Множитель', icon: '⚡', price: 500, desc: 'Удваивает выигрыши в казино'},
    {id: 'x3', name: 'x3 Множитель', icon: '🔥', price: 1000, desc: 'Утраивает выигрыши в казино'},
    {id: 'jackpot_boost', name: 'Бустер джекпота', icon: '💎', price: 1500, desc: 'Увеличивает шанс джекпота'},
    {id: 'extra_life', name: 'Доп. жизнь', icon: '❤️', price: 300, desc: '+1 жизнь в динозаврике'}
];

let gameState = {
    balance: 1000,
    inventory: {},
    stats: { gamesPlayed: 0, wins: 0, earnings: 0 }
};

function saveGame() {
    try {
        localStorage.setItem('game_portal', JSON.stringify(gameState));
    } catch(e) {}
}

function loadGame() {
    try {
        const data = localStorage.getItem('game_portal');
        if (data) {
            const saved = JSON.parse(data);
            Object.assign(gameState, saved);
            return true;
        }
    } catch(e) {}
    return false;
}

function updateBalance() {
    document.getElementById('balance').textContent = Math.round(gameState.balance);
}

function updateStats() {
    document.getElementById('statGames').textContent = gameState.stats.gamesPlayed || 0;
    document.getElementById('statWins').textContent = gameState.stats.wins || 0;
    document.getElementById('statEarnings').textContent = Math.round(gameState.stats.earnings || 0);
}

function renderShop() {
    const grid = document.getElementById('shopGrid');
    grid.innerHTML = SHOP_ITEMS.map(item => `
        <div class="shop-item">
            <div class="icon">${item.icon}</div>
            <div class="name">${item.name}</div>
            <div class="desc">${item.desc}</div>
            <div class="price">💰 ${item.price}₽</div>
            ${gameState.inventory[item.id] ? '<div class="owned">✅ Куплено</div>' : 
            `<button class="btn btn-buy" onclick="buyItem('${item.id}')">Купить</button>`}
        </div>
    `).join('');
}

function buyItem(id) {
    const item = SHOP_ITEMS.find(i => i.id === id);
    if (!item) return;
    if (gameState.inventory[id]) {
        alert('❌ У вас уже есть этот предмет');
        return;
    }
    if (gameState.balance < item.price) {
        alert('❌ Недостаточно средств!');
        return;
    }
    gameState.balance -= item.price;
    gameState.inventory[id] = true;
    saveGame();
    updateBalance();
    renderShop();
    alert(`✅ Куплено: ${item.name}`);
}

function switchTab(tab) {
    document.querySelectorAll('[id^="tab-"]').forEach(el => el.style.display = 'none');
    document.getElementById(`tab-${tab}`).style.display = 'block';
    document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active'));
    document.querySelector(`.nav-btn[onclick="switchTab('${tab}')"]`).classList.add('active');

    if (tab === 'shop') renderShop();
    if (tab === 'stats') updateStats();
}

loadGame();
updateBalance();
updateStats();
</script>
</body>
</html>
"""


# Создаем страницу для каждой игры
def create_game_page(title, content):
    return f"""
<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
* {{
margin: 0;
padding: 0;
box-sizing: border-box;
}}
body {{
font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
background: linear-gradient(135deg, #0a0a1a 0%, #1a0a2a 100%);
min-height: 100vh;
padding: 20px;
}}
.container {{
max-width: 800px;
margin: 0 auto;
}}
h1 {{
color: #ffd700;
text-align: center;
margin-bottom: 20px;
}}
.back-btn {{
display: inline-block;
padding: 10px 20px;
background: #ffd700;
color: #1a0a0a;
text-decoration: none;
border-radius: 8px;
font-weight: bold;
margin-bottom: 20px;
}}
.back-btn:hover {{
transform: scale(1.05);
}}
.card {{
background: rgba(30,10,10,0.9);
border-radius: 15px;
padding: 25px;
margin-bottom: 20px;
box-shadow: 0 10px 30px rgba(0,0,0,0.5);
border: 1px solid #ffd70033;
}}
.btn {{
padding: 12px 25px;
border: none;
border-radius: 8px;
font-size: 16px;
font-weight: 600;
cursor: pointer;
transition: all 0.3s;
color: #1a0a0a;
text-transform: uppercase;
}}
.btn-spin {{
background: linear-gradient(135deg, #ffd700, #f0a500);
}}
.btn-spin:hover {{
transform: scale(1.05);
}}
.btn-reset {{
background: linear-gradient(135deg, #ff4444, #cc0000);
color: white;
}}
.btn-reset:hover {{
transform: scale(1.05);
}}
.btn-game {{
background: linear-gradient(135deg, #aa66ff, #7733cc);
color: white;
}}
.btn-game:hover {{
transform: scale(1.05);
}}
.message-box {{
padding: 15px;
border-radius: 8px;
margin: 10px 0;
text-align: center;
font-weight: bold;
}}
.message-box.win {{
background: rgba(255,215,0,0.2);
color: #ffd700;
border: 1px solid #ffd70044;
}}
.message-box.lose {{
background: rgba(255,0,0,0.2);
color: #ff6666;
border: 1px solid #ff000044;
}}
.message-box.info {{
background: rgba(68,170,255,0.2);
color: #66bbff;
border: 1px solid #44aaff44;
}}
{content}
</style>
</head>
<body>
<div class="container">
<a href="index.html" class="back-btn">← Назад к играм</a>
{content}
</div>
</body>
</html>
"""


# Страница казино (только здесь есть баланс)
casino_page = create_game_page("🎰 Казино", """
<h1>🎰 КАЗИНО</h1>
<div class="balance" style="color:#ffd700;text-align:center;font-size:2em;margin-bottom:15px;">💰 Баланс: <span id="balance">1000</span></div>
<div style="display:flex; justify-content:center; gap:15px; font-size:4em; padding:20px; background:rgba(0,0,0,0.3); border-radius:15px; margin:20px 0;">
    <div class="slot" id="s1">🍒</div>
    <div class="slot" id="s2">🍒</div>
    <div class="slot" id="s3">🍒</div>
</div>
<div style="text-align:center; margin:10px 0;">
    <input type="number" id="betAmount" value="50" min="10" step="10" style="padding:10px; border-radius:8px; border:2px solid #ffd70044; background:rgba(0,0,0,0.3); color:#ffd700; width:150px;">
    <button class="btn btn-spin" onclick="spinSlots()">🎰 КРУТИТЬ</button>
</div>
<div id="slotMessage" class="message-box info" style="text-align:center;">Нажми "КРУТИТЬ"</div>
<script>
const SYMBOLS = ['🍒', '🍋', '🍊', '🍇', '💎', '⭐', '🎰', '🎯', '🏆'];
const PAYOUTS = {0: 2, 1: 2, 2: 2, 3: 2, 4: 10, 5: 5, 6: 20, 7: 3, 8: 8};

let balance = 1000;
let inventory = {};

function loadData() {
    try {
        const data = localStorage.getItem('game_portal');
        if (data) {
            const saved = JSON.parse(data);
            balance = saved.balance || 1000;
            inventory = saved.inventory || {};
            document.getElementById('balance').textContent = balance;
        }
    } catch(e) {}
}

function saveData() {
    try {
        const data = localStorage.getItem('game_portal');
        const saved = data ? JSON.parse(data) : {};
        saved.balance = balance;
        saved.inventory = inventory;
        localStorage.setItem('game_portal', JSON.stringify(saved));
    } catch(e) {}
}

function spinSlots() {
    const bet = parseInt(document.getElementById('betAmount').value);
    if (isNaN(bet) || bet <= 0 || bet > balance) {
        document.getElementById('slotMessage').textContent = '❌ Недостаточно средств!';
        document.getElementById('slotMessage').className = 'message-box lose';
        return;
    }

    balance -= bet;
    document.getElementById('balance').textContent = balance;

    const results = [
        Math.floor(Math.random() * SYMBOLS.length),
        Math.floor(Math.random() * SYMBOLS.length),
        Math.floor(Math.random() * SYMBOLS.length)
    ];

    document.getElementById('s1').textContent = SYMBOLS[results[0]];
    document.getElementById('s2').textContent = SYMBOLS[results[1]];
    document.getElementById('s3').textContent = SYMBOLS[results[2]];

    let winAmount = 0;
    let msg = '';
    let type = 'lose';

    const isJackpot = results[0] === 6 && results[1] === 6 && results[2] === 6;
    const isWin = results[0] === results[1] && results[1] === results[2];

    if (isJackpot) {
        const boost = inventory.jackpot_boost ? 2 : 1;
        winAmount = bet * 50 * boost;
        msg = `🎰 ДЖЕКПОТ! +${winAmount}₽`;
        type = 'win';
    } else if (isWin) {
        let multiplier = PAYOUTS[results[0]] || 2;
        if (inventory.x2) multiplier *= 2;
        if (inventory.x3) multiplier *= 3;
        winAmount = bet * multiplier;
        msg = `🎉 ВЫИГРЫШ! x${multiplier} = +${winAmount}₽`;
        type = 'win';
    } else {
        msg = `😢 Проигрыш -${bet}₽`;
        type = 'lose';
    }

    balance += winAmount;
    document.getElementById('balance').textContent = balance;
    saveData();

    document.getElementById('slotMessage').textContent = msg;
    document.getElementById('slotMessage').className = 'message-box ' + type;
}

loadData();
</script>
""")

chess_page = create_game_page("♟️ Шахматы с ИИ", """
<h1>♟️ ШАХМАТЫ С ИИ</h1>
<div style="color:#aa8866; text-align:center; margin-bottom:15px;">
    <p><strong style="color:#ffd700;">Правила:</strong> Вы играете белыми, ИИ играет черными.</p>
    <p>🟦 Полные шахматные правила: шах, мат, рокировка, взятие на проходе</p>
    <p style="color:#44ff88;">💡 ИИ просчитывает на 3 хода вперед</p>
</div>
<div id="chessStatus" style="text-align:center; color:#ffd700; margin-bottom:10px;">Ваш ход (Белые)</div>
<div id="chessBoard" style="display:grid; grid-template-columns:repeat(8,1fr); max-width:400px; margin:20px auto; gap:0;"></div>
<div style="text-align:center;">
    <button class="btn btn-reset" onclick="initChess()">🔄 Новая игра</button>
    <button class="btn btn-game" onclick="undoMove()">↩️ Отмена хода</button>
</div>
<div id="chessMessage" class="message-box info" style="text-align:center;">Начинайте игру</div>
<script>
const CHESS_PIECES = {
    'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
    'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙'
};

const PIECE_VALUES = {
    'p': 1, 'P': 1,
    'n': 3, 'N': 3,
    'b': 3, 'B': 3,
    'r': 5, 'R': 5,
    'q': 9, 'Q': 9,
    'k': 1000, 'K': 1000
};

const PROMOTION_PIECES = {
    'white': ['Q', 'R', 'B', 'N'],
    'black': ['q', 'r', 'b', 'n']
};

const PROMOTION_SYMBOLS = {
    'white': ['♕', '♖', '♗', '♘'],
    'black': ['♛', '♜', '♝', '♞']
};

let board = [];
let selected = null;
let turn = 'white';
let gameOver = false;
let moveHistory = [];
let isAIThinking = false;
let enPassantTarget = null;
let enPassantColor = null;
let castlingRights = { K: true, Q: true, k: true, q: true };

function getColor(piece) {
    if (!piece) return null;
    return piece === piece.toUpperCase() ? 'white' : 'black';
}

function initChess() {
    board = [
        ['r','n','b','q','k','b','n','r'],
        ['p','p','p','p','p','p','p','p'],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['P','P','P','P','P','P','P','P'],
        ['R','N','B','Q','K','B','N','R']
    ];
    selected = null;
    turn = 'white';
    gameOver = false;
    moveHistory = [];
    isAIThinking = false;
    enPassantTarget = null;
    enPassantColor = null;
    castlingRights = { K: true, Q: true, k: true, q: true };
    renderChess();
    document.getElementById('chessStatus').textContent = 'Ваш ход (Белые)';
    document.getElementById('chessMessage').textContent = 'Начинайте игру';
    document.getElementById('chessMessage').className = 'message-box info';
}

function renderChess() {
    const boardEl = document.getElementById('chessBoard');
    boardEl.innerHTML = '';
    for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
            const cell = document.createElement('div');
            const isLight = (i + j) % 2 === 0;
            cell.style.cssText = `
                aspect-ratio: 1;
                background: ${isLight ? '#f0d9b5' : '#b58863'};
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 2em;
                cursor: ${!gameOver && turn === 'white' && !isAIThinking ? 'pointer' : 'default'};
                transition: all 0.2s;
                ${selected && selected[0] === i && selected[1] === j ? 'background: #7fc97f !important;' : ''}
                position: relative;
            `;
            const piece = board[i][j];
            if (piece) cell.textContent = CHESS_PIECES[piece];
            cell.dataset.row = i;
            cell.dataset.col = j;
            cell.onclick = () => chessClick(i, j);
            boardEl.appendChild(cell);
        }
    }
}

function copyBoard(b) {
    return b.map(row => [...row]);
}

function findKing(color, boardState) {
    const b = boardState || board;
    const king = color === 'white' ? 'K' : 'k';
    for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
            if (b[i][j] === king) {
                return [i, j];
            }
        }
    }
    return null;
}

function isKingInCheck(color, boardState) {
    const b = boardState || board;
    const kingPos = findKing(color, b);
    if (!kingPos) return true;

    const [kr, kc] = kingPos;
    const enemy = color === 'white' ? 'black' : 'white';

    for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
            const piece = b[i][j];
            if (piece) {
                const pieceColor = getColor(piece);
                if (pieceColor === enemy) {
                    if (canPieceAttack(i, j, kr, kc, b)) {
                        return true;
                    }
                }
            }
        }
    }
    return false;
}

function canPieceAttack(row, col, targetRow, targetCol, boardState) {
    const b = boardState || board;
    const piece = b[row][col];
    if (!piece) return false;
    const color = getColor(piece);
    const type = piece.toLowerCase();
    const dr = targetRow - row;
    const dc = targetCol - col;

    // Пешка
    if (type === 'p') {
        const dir = color === 'white' ? -1 : 1;
        return dr === dir && Math.abs(dc) === 1;
    }

    // Конь
    if (type === 'n') {
        return (Math.abs(dr) === 2 && Math.abs(dc) === 1) || (Math.abs(dr) === 1 && Math.abs(dc) === 2);
    }

    // Слон
    if (type === 'b') {
        if (Math.abs(dr) !== Math.abs(dc)) return false;
        if (dr === 0 && dc === 0) return false;
        const stepR = dr > 0 ? 1 : -1;
        const stepC = dc > 0 ? 1 : -1;
        let r = row + stepR, c = col + stepC;
        while (r !== targetRow || c !== targetCol) {
            if (r < 0 || r >= 8 || c < 0 || c >= 8) return false;
            if (b[r][c]) return false;
            r += stepR;
            c += stepC;
        }
        return true;
    }

    // Ладья
    if (type === 'r') {
        if (dr === 0 && dc === 0) return false;
        if (dr !== 0 && dc !== 0) return false;
        if (dr === 0) {
            const step = dc > 0 ? 1 : -1;
            let c = col + step;
            while (c !== targetCol) {
                if (c < 0 || c >= 8) return false;
                if (b[row][c]) return false;
                c += step;
            }
        } else {
            const step = dr > 0 ? 1 : -1;
            let r = row + step;
            while (r !== targetRow) {
                if (r < 0 || r >= 8) return false;
                if (b[r][col]) return false;
                r += step;
            }
        }
        return true;
    }

    // Ферзь
    if (type === 'q') {
        if (dr === 0 && dc === 0) return false;
        if (dr === 0 || dc === 0 || Math.abs(dr) === Math.abs(dc)) {
            if (dr === 0) {
                const step = dc > 0 ? 1 : -1;
                let c = col + step;
                while (c !== targetCol) {
                    if (c < 0 || c >= 8) return false;
                    if (b[row][c]) return false;
                    c += step;
                }
            } else if (dc === 0) {
                const step = dr > 0 ? 1 : -1;
                let r = row + step;
                while (r !== targetRow) {
                    if (r < 0 || r >= 8) return false;
                    if (b[r][col]) return false;
                    r += step;
                }
            } else {
                const stepR = dr > 0 ? 1 : -1;
                const stepC = dc > 0 ? 1 : -1;
                let r = row + stepR, c = col + stepC;
                while (r !== targetRow || c !== targetCol) {
                    if (r < 0 || r >= 8 || c < 0 || c >= 8) return false;
                    if (b[r][c]) return false;
                    r += stepR;
                    c += stepC;
                }
            }
            return true;
        }
        return false;
    }

    // Король
    if (type === 'k') {
        return Math.abs(dr) <= 1 && Math.abs(dc) <= 1 && (dr !== 0 || dc !== 0);
    }

    return false;
}

function getRawMoves(row, col, boardState) {
    const b = boardState || board;
    const piece = b[row][col];
    if (!piece) return [];
    const color = getColor(piece);
    const moves = [];
    const type = piece.toLowerCase();

    // Пешка
    if (type === 'p') {
        const dir = color === 'white' ? -1 : 1;
        const startRow = color === 'white' ? 6 : 1;
        if (row + dir >= 0 && row + dir < 8 && !b[row + dir][col]) {
            moves.push([row + dir, col]);
            if (row === startRow && !b[row + 2 * dir][col]) {
                moves.push([row + 2 * dir, col]);
            }
        }
        for (let dc of [-1, 1]) {
            const nc = col + dc;
            if (nc >= 0 && nc < 8) {
                const nr = row + dir;
                if (nr >= 0 && nr < 8) {
                    const target = b[nr][nc];
                    if (target && getColor(target) !== color) {
                        moves.push([nr, nc]);
                    }
                    if (enPassantTarget && enPassantTarget[0] === nr && enPassantTarget[1] === nc && enPassantColor === color) {
                        moves.push([nr, nc]);
                    }
                }
            }
        }
    }

    // Ладья
    if (type === 'r') {
        for (let d of [[-1,0],[1,0],[0,-1],[0,1]]) {
            for (let i = 1; i < 8; i++) {
                const nr = row + d[0] * i;
                const nc = col + d[1] * i;
                if (nr < 0 || nr >= 8 || nc < 0 || nc >= 8) break;
                const target = b[nr][nc];
                if (target) {
                    if (getColor(target) !== color) {
                        moves.push([nr, nc]);
                    }
                    break;
                }
                moves.push([nr, nc]);
            }
        }
    }

    // Слон
    if (type === 'b') {
        for (let d of [[-1,-1],[-1,1],[1,-1],[1,1]]) {
            for (let i = 1; i < 8; i++) {
                const nr = row + d[0] * i;
                const nc = col + d[1] * i;
                if (nr < 0 || nr >= 8 || nc < 0 || nc >= 8) break;
                const target = b[nr][nc];
                if (target) {
                    if (getColor(target) !== color) {
                        moves.push([nr, nc]);
                    }
                    break;
                }
                moves.push([nr, nc]);
            }
        }
    }

    // Ферзь
    if (type === 'q') {
        for (let d of [[-1,0],[1,0],[0,-1],[0,1],[-1,-1],[-1,1],[1,-1],[1,1]]) {
            for (let i = 1; i < 8; i++) {
                const nr = row + d[0] * i;
                const nc = col + d[1] * i;
                if (nr < 0 || nr >= 8 || nc < 0 || nc >= 8) break;
                const target = b[nr][nc];
                if (target) {
                    if (getColor(target) !== color) {
                        moves.push([nr, nc]);
                    }
                    break;
                }
                moves.push([nr, nc]);
            }
        }
    }

    // Конь
    if (type === 'n') {
        for (let d of [[-2,-1],[-2,1],[-1,-2],[-1,2],[1,-2],[1,2],[2,-1],[2,1]]) {
            const nr = row + d[0];
            const nc = col + d[1];
            if (nr < 0 || nr >= 8 || nc < 0 || nc >= 8) continue;
            const target = b[nr][nc];
            if (!target || getColor(target) !== color) {
                moves.push([nr, nc]);
            }
        }
    }

    // Король
    if (type === 'k') {
        for (let d of [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]) {
            const nr = row + d[0];
            const nc = col + d[1];
            if (nr < 0 || nr >= 8 || nc < 0 || nc >= 8) continue;
            const target = b[nr][nc];
            if (!target || getColor(target) !== color) {
                moves.push([nr, nc]);
            }
        }
        // Рокировка
        if (color === 'white' && !isKingInCheck('white', b)) {
            if (castlingRights.K && !b[7][5] && !b[7][6] && b[7][7] === 'R') {
                if (!isSquareAttacked(7, 5, 'black', b) && !isSquareAttacked(7, 6, 'black', b)) {
                    moves.push([7, 6]);
                }
            }
            if (castlingRights.Q && !b[7][1] && !b[7][2] && !b[7][3] && b[7][0] === 'R') {
                if (!isSquareAttacked(7, 3, 'black', b) && !isSquareAttacked(7, 2, 'black', b)) {
                    moves.push([7, 2]);
                }
            }
        } else if (color === 'black' && !isKingInCheck('black', b)) {
            if (castlingRights.k && !b[0][5] && !b[0][6] && b[0][7] === 'r') {
                if (!isSquareAttacked(0, 5, 'white', b) && !isSquareAttacked(0, 6, 'white', b)) {
                    moves.push([0, 6]);
                }
            }
            if (castlingRights.q && !b[0][1] && !b[0][2] && !b[0][3] && b[0][0] === 'r') {
                if (!isSquareAttacked(0, 3, 'white', b) && !isSquareAttacked(0, 2, 'white', b)) {
                    moves.push([0, 2]);
                }
            }
        }
    }

    return moves;
}

function isSquareAttacked(row, col, attackerColor, boardState) {
    const b = boardState || board;
    for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
            const piece = b[i][j];
            if (piece) {
                const pieceColor = getColor(piece);
                if (pieceColor === attackerColor) {
                    if (canPieceAttack(i, j, row, col, b)) {
                        return true;
                    }
                }
            }
        }
    }
    return false;
}

function getLegalMoves(row, col) {
    const piece = board[row][col];
    if (!piece) return [];
    const color = getColor(piece);
    const rawMoves = getRawMoves(row, col);
    const legalMoves = [];

    for (let move of rawMoves) {
        const [toRow, toCol] = move;
        const boardCopy = copyBoard(board);
        const enPassantCopy = enPassantTarget;
        const enPassantColorCopy = enPassantColor;
        const castlingCopy = {...castlingRights};

        const pieceCopy = boardCopy[row][col];
        boardCopy[toRow][toCol] = pieceCopy;
        boardCopy[row][col] = '';

        if (pieceCopy.toLowerCase() === 'p' && enPassantCopy && enPassantCopy[0] === toRow && enPassantCopy[1] === toCol) {
            boardCopy[row][toCol] = '';
        }

        if (pieceCopy.toLowerCase() === 'k' && Math.abs(toCol - col) === 2) {
            if (toCol === 6) {
                boardCopy[row][5] = boardCopy[row][7];
                boardCopy[row][7] = '';
            } else if (toCol === 2) {
                boardCopy[row][3] = boardCopy[row][0];
                boardCopy[row][0] = '';
            }
        }

        const inCheck = isKingInCheck(color, boardCopy);

        if (!inCheck) {
            legalMoves.push(move);
        }
    }

    return legalMoves;
}

function makeMoveWithRules(from, to, promotionPiece) {
    const [fr, fc] = from;
    const [tr, tc] = to;
    const piece = board[fr][fc];
    const color = getColor(piece);
    const captured = board[tr][tc];
    const type = piece.toLowerCase();

    const oldEnPassant = enPassantTarget;
    const oldEnPassantColor = enPassantColor;
    const oldCastling = {...castlingRights};
    let promoted = false;
    let enPassantCaptured = false;
    let enPassantRow = null;
    let enPassantCol = null;
    let enPassantPiece = null;

    if (type === 'p' && enPassantTarget && enPassantTarget[0] === tr && enPassantTarget[1] === tc) {
        enPassantCaptured = true;
        enPassantRow = fr;
        enPassantCol = tc;
        enPassantPiece = board[fr][tc];
        board[fr][tc] = '';
    }

    if (type === 'k' && Math.abs(tc - fc) === 2) {
        if (tc === 6) {
            board[fr][5] = board[fr][7];
            board[fr][7] = '';
        } else if (tc === 2) {
            board[fr][3] = board[fr][0];
            board[fr][0] = '';
        }
    }

    if (type === 'k') {
        if (color === 'white') {
            castlingRights.K = false;
            castlingRights.Q = false;
        } else {
            castlingRights.k = false;
            castlingRights.q = false;
        }
    }
    if (type === 'r') {
        if (fr === 7 && fc === 7) castlingRights.K = false;
        if (fr === 7 && fc === 0) castlingRights.Q = false;
        if (fr === 0 && fc === 7) castlingRights.k = false;
        if (fr === 0 && fc === 0) castlingRights.q = false;
    }
    if (captured === 'R') {
        if (tr === 7 && tc === 7) castlingRights.K = false;
        if (tr === 7 && tc === 0) castlingRights.Q = false;
    }
    if (captured === 'r') {
        if (tr === 0 && tc === 7) castlingRights.k = false;
        if (tr === 0 && tc === 0) castlingRights.q = false;
    }

    if (type === 'p' && Math.abs(tr - fr) === 2) {
        enPassantTarget = [(fr + tr) / 2, fc];
        enPassantColor = color;
    } else {
        enPassantTarget = null;
        enPassantColor = null;
    }

    let promotedPiece = piece;
    if (type === 'p' && (tr === 0 || tr === 7)) {
        if (promotionPiece) {
            promotedPiece = promotionPiece;
        } else {
            // По умолчанию ферзь
            promotedPiece = color === 'white' ? 'Q' : 'q';
        }
        promoted = true;
    }

    board[tr][tc] = promotedPiece;
    board[fr][fc] = '';

    return { 
        captured, 
        oldEnPassant, 
        oldEnPassantColor, 
        oldCastling, 
        promoted,
        promotedPiece,
        enPassantCaptured,
        enPassantRow,
        enPassantCol,
        enPassantPiece
    };
}

function undoMoveWithRules(from, to, data) {
    const [fr, fc] = from;
    const [tr, tc] = to;
    const piece = board[tr][tc];
    const color = getColor(piece);
    const type = piece.toLowerCase();

    if (data.promoted) {
        board[tr][tc] = color === 'white' ? 'P' : 'p';
    }

    board[fr][fc] = piece;
    board[tr][tc] = data.captured;

    if (data.enPassantCaptured) {
        board[data.enPassantRow][data.enPassantCol] = data.enPassantPiece;
    }

    if (type === 'k' && Math.abs(tc - fc) === 2) {
        if (tc === 6) {
            board[fr][7] = board[fr][5];
            board[fr][5] = '';
        } else if (tc === 2) {
            board[fr][0] = board[fr][3];
            board[fr][3] = '';
        }
    }

    enPassantTarget = data.oldEnPassant;
    enPassantColor = data.oldEnPassantColor;
    castlingRights = data.oldCastling;
}

function evaluateBoard() {
    let score = 0;
    for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
            const piece = board[i][j];
            if (piece) {
                const value = PIECE_VALUES[piece] || 0;
                const isWhite = getColor(piece) === 'white';
                score += isWhite ? value : -value;
            }
        }
    }
    return score;
}

function getAllLegalMoves(color) {
    const moves = [];
    for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
            const piece = board[i][j];
            if (piece) {
                const pieceColor = getColor(piece);
                if (pieceColor === color) {
                    const legalMoves = getLegalMoves(i, j);
                    for (let move of legalMoves) {
                        moves.push({from: [i, j], to: move, piece: piece});
                    }
                }
            }
        }
    }
    return moves;
}

function minimax(depth, isMaximizing, alpha, beta) {
    if (depth === 0) {
        return {score: evaluateBoard(), move: null};
    }

    const color = isMaximizing ? 'white' : 'black';
    const moves = getAllLegalMoves(color);

    if (moves.length === 0) {
        if (isKingInCheck(color)) {
            return {score: isMaximizing ? -9999 + (10 - depth) : 9999 - (10 - depth), move: null};
        }
        return {score: 0, move: null};
    }

    let bestMove = moves[0];

    if (isMaximizing) {
        let maxEval = -Infinity;
        for (let move of moves) {
            const data = makeMoveWithRules(move.from, move.to);
            const result = minimax(depth - 1, false, alpha, beta);
            undoMoveWithRules(move.from, move.to, data);

            if (result.score > maxEval) {
                maxEval = result.score;
                bestMove = move;
            }
            alpha = Math.max(alpha, maxEval);
            if (beta <= alpha) break;
        }
        return {score: maxEval, move: bestMove};
    } else {
        let minEval = Infinity;
        for (let move of moves) {
            const data = makeMoveWithRules(move.from, move.to);
            const result = minimax(depth - 1, true, alpha, beta);
            undoMoveWithRules(move.from, move.to, data);

            if (result.score < minEval) {
                minEval = result.score;
                bestMove = move;
            }
            beta = Math.min(beta, minEval);
            if (beta <= alpha) break;
        }
        return {score: minEval, move: bestMove};
    }
}

function aiMove() {
    if (gameOver || isAIThinking) return;
    isAIThinking = true;
    document.getElementById('chessStatus').textContent = '🤔 ИИ думает...';

    setTimeout(() => {
        const result = minimax(3, false, -Infinity, Infinity);
        const move = result.move;

        if (move) {
            const data = makeMoveWithRules(move.from, move.to);
            moveHistory.push({from: move.from, to: move.to, data: data});
            turn = 'white';
            renderChess();

            const whiteMoves = getAllLegalMoves('white');
            if (whiteMoves.length === 0) {
                gameOver = true;
                if (isKingInCheck('white')) {
                    document.getElementById('chessMessage').textContent = '🤖 Мат! ИИ победил!';
                    document.getElementById('chessMessage').className = 'message-box lose';
                } else {
                    document.getElementById('chessMessage').textContent = '🤝 Пат! Ничья!';
                    document.getElementById('chessMessage').className = 'message-box info';
                }
                document.getElementById('chessStatus').textContent = 'Игра окончена';
            } else {
                document.getElementById('chessStatus').textContent = 'Ваш ход (Белые)';
                document.getElementById('chessMessage').textContent = 'Ваш ход';
                document.getElementById('chessMessage').className = 'message-box info';
            }
        }
        isAIThinking = false;
    }, 500);
}

function chessClick(row, col) {
    if (gameOver || turn !== 'white' || isAIThinking) return;

    const piece = board[row][col];
    const color = piece ? getColor(piece) : null;

    if (selected) {
        const [sRow, sCol] = selected;
        const legalMoves = getLegalMoves(sRow, sCol);
        const isValid = legalMoves.some(m => m[0] === row && m[1] === col);

        if (isValid) {
            const selectedPiece = board[sRow][sCol];
            if (selectedPiece && selectedPiece.toLowerCase() === 'p' && (row === 0 || row === 7)) {
                showPromotionDialog([sRow, sCol], [row, col]);
                return;
            }

            const data = makeMoveWithRules([sRow, sCol], [row, col]);
            moveHistory.push({from: [sRow, sCol], to: [row, col], data: data});
            selected = null;
            turn = 'black';
            renderChess();

            const blackMoves = getAllLegalMoves('black');
            if (blackMoves.length === 0) {
                gameOver = true;
                if (isKingInCheck('black')) {
                    document.getElementById('chessMessage').textContent = '🏆 Мат! Вы победили!';
                    document.getElementById('chessMessage').className = 'message-box win';
                } else {
                    document.getElementById('chessMessage').textContent = '🤝 Пат! Ничья!';
                    document.getElementById('chessMessage').className = 'message-box info';
                }
                document.getElementById('chessStatus').textContent = 'Игра окончена';
                return;
            }

            document.getElementById('chessStatus').textContent = '🤖 Ход ИИ...';
            document.getElementById('chessMessage').textContent = 'ИИ думает...';
            document.getElementById('chessMessage').className = 'message-box info';

            setTimeout(() => {
                aiMove();
            }, 500);
            return;
        } else {
            selected = null;
            renderChess();
            return;
        }
    }

    if (color === 'white') {
        const moves = getLegalMoves(row, col);
        if (moves.length > 0) {
            selected = [row, col];
            renderChess();
        }
    }
}

function showPromotionDialog(from, to) {
    const color = getColor(board[from[0]][from[1]]);
    const pieces = PROMOTION_PIECES[color];
    const symbols = PROMOTION_SYMBOLS[color];

    const dialog = document.createElement('div');
    dialog.id = 'promotionDialog';
    dialog.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: rgba(0,0,0,0.95);
        padding: 25px;
        border-radius: 15px;
        border: 3px solid #ffd700;
        z-index: 1000;
        text-align: center;
        box-shadow: 0 0 50px rgba(255,215,0,0.3);
    `;
    dialog.innerHTML = `
        <h3 style="color:#ffd700; margin-bottom:20px;">Выберите фигуру:</h3>
        <div style="display:flex; gap:20px; justify-content:center;">
            ${pieces.map((p, i) => `
                <div style="font-size:4em; cursor:pointer; padding:15px; border:2px solid #ffd70044; border-radius:15px; background:rgba(0,0,0,0.5); transition:all 0.3s; min-width:80px;" 
                     onmouseover="this.style.borderColor='#ffd700'; this.style.transform='scale(1.1)'; this.style.background='rgba(255,215,0,0.1)'" 
                     onmouseout="this.style.borderColor='#ffd70044'; this.style.transform='scale(1)'; this.style.background='rgba(0,0,0,0.5)'"
                     onclick="promotePawn([${from}], [${to}], '${p}')">
                    ${symbols[i]}
                </div>
            `).join('')}
        </div>
    `;
    document.body.appendChild(dialog);
}

function promotePawn(from, to, piece) {
    const dialog = document.getElementById('promotionDialog');
    if (dialog) dialog.remove();

    const data = makeMoveWithRules(from, to, piece);
    moveHistory.push({from: from, to: to, data: data});
    selected = null;
    turn = 'black';
    renderChess();

    const blackMoves = getAllLegalMoves('black');
    if (blackMoves.length === 0) {
        gameOver = true;
        if (isKingInCheck('black')) {
            document.getElementById('chessMessage').textContent = '🏆 Мат! Вы победили!';
            document.getElementById('chessMessage').className = 'message-box win';
        } else {
            document.getElementById('chessMessage').textContent = '🤝 Пат! Ничья!';
            document.getElementById('chessMessage').className = 'message-box info';
        }
        document.getElementById('chessStatus').textContent = 'Игра окончена';
        return;
    }

    document.getElementById('chessStatus').textContent = '🤖 Ход ИИ...';
    document.getElementById('chessMessage').textContent = 'ИИ думает...';
    document.getElementById('chessMessage').className = 'message-box info';

    setTimeout(() => {
        aiMove();
    }, 500);
}

function undoMove() {
    if (moveHistory.length === 0 || isAIThinking) return;

    for (let i = 0; i < 2 && moveHistory.length > 0; i++) {
        const last = moveHistory.pop();
        undoMoveWithRules(last.from, last.to, last.data);
    }

    turn = 'white';
    selected = null;
    gameOver = false;
    renderChess();
    document.getElementById('chessStatus').textContent = 'Ваш ход (Белые)';
    document.getElementById('chessMessage').textContent = 'Ход отменен';
    document.getElementById('chessMessage').className = 'message-box info';
}

initChess();
</script>
""")

# Мировая война с картой и правилами
war_page = create_game_page("⚔️ Мировая война", """
<h1>⚔️ МИРОВАЯ ВОЙНА</h1>
<div style="color:#aa8866; text-align:center; margin-bottom:15px;">
    <p><strong style="color:#ffd700;">Правила:</strong> Захватывайте территории врага. Игрок (🛡️) атакует врага (⚔️).</p>
    <p>💰 Ставка: 100₽ за ход. Захватите всю карту чтобы победить!</p>
</div>
<div id="warStatus" style="text-align:center; color:#ffd700; margin-bottom:10px;">Ход: Игрок</div>
<div id="warGrid" style="display:grid; grid-template-columns:repeat(6,1fr); gap:10px; max-width:500px; margin:20px auto;"></div>
<div style="text-align:center;">
    <button class="btn btn-reset" onclick="initWar()">🔄 Новая игра</button>
</div>
<div id="warMessage" class="message-box info" style="text-align:center;">Начинайте игру</div>
<script>
let warBoard = [];
let warTurn = 'player';
let warGameOver = false;

const countries = [
    '🇺🇸', '🇬🇧', '🇫🇷', '🇩🇪', '🇷🇺', '🇨🇳',
    '🇯🇵', '🇮🇳', '🇧🇷', '🇦🇺', '🇨🇦', '🇮🇹'
];

function initWar() {
    warBoard = [];
    for (let i = 0; i < 6; i++) {
        warBoard[i] = [];
        for (let j = 0; j < 6; j++) {
            const idx = i * 6 + j;
            warBoard[i][j] = {
                country: countries[idx % countries.length],
                owner: Math.random() < 0.5 ? 'player' : 'enemy',
                troops: 1 + Math.floor(Math.random() * 3)
            };
        }
    }
    warTurn = 'player';
    warGameOver = false;
    renderWar();
    document.getElementById('warStatus').textContent = 'Ход: Игрок';
    document.getElementById('warMessage').textContent = 'Начинайте игру';
    document.getElementById('warMessage').className = 'message-box info';
}

function renderWar() {
    const grid = document.getElementById('warGrid');
    grid.innerHTML = '';
    for (let i = 0; i < 6; i++) {
        for (let j = 0; j < 6; j++) {
            const cell = document.createElement('div');
            const data = warBoard[i][j];
            const isPlayer = data.owner === 'player';
            cell.style.cssText = `
                padding: 15px;
                background: ${isPlayer ? 'rgba(68,170,255,0.2)' : 'rgba(255,68,68,0.2)'};
                border: 2px solid ${isPlayer ? '#44aaff44' : '#ff444444'};
                border-radius: 8px;
                text-align: center;
                cursor: ${isPlayer && warTurn === 'player' && !warGameOver ? 'pointer' : 'default'};
                transition: all 0.3s;
                min-height: 80px;
            `;
            cell.innerHTML = `
                <div style="font-size:2em;">${data.country}</div>
                <div style="color:${isPlayer ? '#44aaff' : '#ff4444'}; font-weight:bold;">
                    🪖 ${data.troops}
                </div>
            `;
            if (isPlayer && warTurn === 'player' && !warGameOver) {
                cell.onclick = () => warAttack(i, j);
                cell.onmouseover = () => cell.style.transform = 'scale(1.05)';
                cell.onmouseout = () => cell.style.transform = 'scale(1)';
            }
            grid.appendChild(cell);
        }
    }
}

function warAttack(row, col) {
    if (warGameOver || warTurn !== 'player') return;

    const source = warBoard[row][col];
    if (source.owner !== 'player') return;
    if (source.troops < 2) {
        document.getElementById('warMessage').textContent = '❌ Недостаточно войск! Нужно минимум 2';
        document.getElementById('warMessage').className = 'message-box lose';
        return;
    }

    // Находим вражеские территории рядом
    const targets = [];
    const dirs = [[-1,0],[1,0],[0,-1],[0,1]];
    for (let [dr, dc] of dirs) {
        const nr = row + dr;
        const nc = col + dc;
        if (nr >= 0 && nr < 6 && nc >= 0 && nc < 6) {
            if (warBoard[nr][nc].owner === 'enemy') {
                targets.push([nr, nc]);
            }
        }
    }

    if (targets.length === 0) {
        document.getElementById('warMessage').textContent = '❌ Нет вражеских территорий рядом!';
        document.getElementById('warMessage').className = 'message-box lose';
        return;
    }

    // Атака
    const target = targets[Math.floor(Math.random() * targets.length)];
    const [tr, tc] = target;
    const enemy = warBoard[tr][tc];

    const attackPower = source.troops;
    const defensePower = enemy.troops;

    if (attackPower > defensePower) {
        // Победа
        enemy.owner = 'player';
        enemy.troops = attackPower - defensePower;
        source.troops = 1;
        document.getElementById('warMessage').textContent = `⚔️ Победа! Захвачена ${enemy.country}`;
        document.getElementById('warMessage').className = 'message-box win';
    } else {
        // Поражение
        source.troops = 1;
        document.getElementById('warMessage').textContent = `😢 Поражение! Потеряно ${attackPower} войск`;
        document.getElementById('warMessage').className = 'message-box lose';
    }

    warTurn = 'enemy';
    renderWar();
    document.getElementById('warStatus').textContent = 'Ход: Враг';

    // Проверка победы
    let playerCount = 0;
    let enemyCount = 0;
    for (let i = 0; i < 6; i++) {
        for (let j = 0; j < 6; j++) {
            if (warBoard[i][j].owner === 'player') playerCount++;
            else enemyCount++;
        }
    }

    if (enemyCount === 0) {
        warGameOver = true;
        document.getElementById('warMessage').textContent = '🏆 ПОБЕДА! Вся карта захвачена!';
        document.getElementById('warMessage').className = 'message-box win';
        return;
    }

    // Ход врага
    setTimeout(() => {
        enemyTurn();
    }, 800);
}

function enemyTurn() {
    if (warGameOver) return;

    // Находим вражеские территории
    const enemies = [];
    for (let i = 0; i < 6; i++) {
        for (let j = 0; j < 6; j++) {
            if (warBoard[i][j].owner === 'enemy' && warBoard[i][j].troops >= 2) {
                enemies.push([i, j]);
            }
        }
    }

    if (enemies.length === 0) {
        warGameOver = true;
        document.getElementById('warMessage').textContent = '🏆 ПОБЕДА! Вся карта захвачена!';
        document.getElementById('warMessage').className = 'message-box win';
        return;
    }

    // Враг атакует
    const enemy = enemies[Math.floor(Math.random() * enemies.length)];
    const [er, ec] = enemy;
    const source = warBoard[er][ec];

    const targets = [];
    const dirs = [[-1,0],[1,0],[0,-1],[0,1]];
    for (let [dr, dc] of dirs) {
        const nr = er + dr;
        const nc = ec + dc;
        if (nr >= 0 && nr < 6 && nc >= 0 && nc < 6) {
            if (warBoard[nr][nc].owner === 'player') {
                targets.push([nr, nc]);
            }
        }
    }

    if (targets.length > 0) {
        const target = targets[Math.floor(Math.random() * targets.length)];
        const [tr, tc] = target;
        const enemyTarget = warBoard[tr][tc];

        if (source.troops > enemyTarget.troops) {
            enemyTarget.owner = 'enemy';
            enemyTarget.troops = source.troops - enemyTarget.troops;
            source.troops = 1;
            document.getElementById('warMessage').textContent = `⚔️ Враг захватил ${enemyTarget.country}`;
            document.getElementById('warMessage').className = 'message-box lose';
        } else {
            source.troops = 1;
        }
    }

    warTurn = 'player';
    renderWar();
    document.getElementById('warStatus').textContent = 'Ход: Игрок';

    // Проверка победы врага
    let playerCount = 0;
    for (let i = 0; i < 6; i++) {
        for (let j = 0; j < 6; j++) {
            if (warBoard[i][j].owner === 'player') playerCount++;
        }
    }

    if (playerCount === 0) {
        warGameOver = true;
        document.getElementById('warMessage').textContent = '💀 ПОРАЖЕНИЕ! Все территории захвачены врагом';
        document.getElementById('warMessage').className = 'message-box lose';
    }
}

initWar();
</script>
""")

# Остальные игры (упрощенные)
tictac_page = create_game_page("❌ Крестики-нолики", """
<h1>❌ КРЕСТИКИ-НОЛИКИ</h1>
<div id="tictacStatus" style="text-align:center; color:#ffd700; margin-bottom:10px;">Ход: X</div>
<div id="tictacGrid" style="display:grid; grid-template-columns:repeat(3,1fr); gap:5px; max-width:300px; margin:20px auto;"></div>
<div style="text-align:center;">
    <button class="btn btn-reset" onclick="initTicTac()">🔄 Новая игра</button>
</div>
<div id="tictacMessage" class="message-box info" style="text-align:center;">Начинайте игру</div>
<script>
let ticBoard = [];
let ticTurn = 'X';
let ticGameOver = false;

function initTicTac() {
    ticBoard = ['', '', '', '', '', '', '', '', ''];
    ticTurn = 'X';
    ticGameOver = false;
    renderTicTac();
    document.getElementById('tictacStatus').textContent = 'Ход: X';
    document.getElementById('tictacMessage').textContent = 'Начинайте игру';
    document.getElementById('tictacMessage').className = 'message-box info';
}

function renderTicTac() {
    const grid = document.getElementById('tictacGrid');
    grid.innerHTML = '';
    ticBoard.forEach((cell, i) => {
        const div = document.createElement('div');
        div.style.cssText = `
            aspect-ratio: 1;
            font-size: 3em;
            background: rgba(0,0,0,0.3);
            border: 2px solid #ffd70044;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 5px;
            color: ${cell === 'X' ? '#44aaff' : '#ff6b6b'};
        `;
        div.textContent = cell;
        if (!cell && !ticGameOver) {
            div.onclick = () => ticMove(i);
        }
        grid.appendChild(div);
    });
}

function ticMove(index) {
    if (ticGameOver || ticBoard[index]) return;

    ticBoard[index] = ticTurn;
    renderTicTac();

    const winner = checkWinner();
    if (winner) {
        ticGameOver = true;
        document.getElementById('tictacMessage').textContent = `🏆 Победил ${winner}!`;
        document.getElementById('tictacMessage').className = 'message-box win';
        return;
    }

    if (!ticBoard.includes('')) {
        ticGameOver = true;
        document.getElementById('tictacMessage').textContent = '🤝 Ничья!';
        document.getElementById('tictacMessage').className = 'message-box info';
        return;
    }

    ticTurn = ticTurn === 'X' ? 'O' : 'X';
    document.getElementById('tictacStatus').textContent = `Ход: ${ticTurn}`;

    // Ход компьютера
    if (ticTurn === 'O' && !ticGameOver) {
        setTimeout(() => {
            const empty = ticBoard.map((c,i) => c === '' ? i : null).filter(i => i !== null);
            if (empty.length > 0) {
                const move = empty[Math.floor(Math.random() * empty.length)];
                ticBoard[move] = 'O';
                renderTicTac();
                const w = checkWinner();
                if (w) {
                    ticGameOver = true;
                    document.getElementById('tictacMessage').textContent = `🏆 Победил ${w}!`;
                    document.getElementById('tictacMessage').className = 'message-box win';
                } else if (!ticBoard.includes('')) {
                    ticGameOver = true;
                    document.getElementById('tictacMessage').textContent = '🤝 Ничья!';
                    document.getElementById('tictacMessage').className = 'message-box info';
                } else {
                    ticTurn = 'X';
                    document.getElementById('tictacStatus').textContent = 'Ход: X';
                }
            }
        }, 300);
    }
}

function checkWinner() {
    const lines = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ];
    for (let line of lines) {
        const [a,b,c] = line;
        if (ticBoard[a] && ticBoard[a] === ticBoard[b] && ticBoard[a] === ticBoard[c]) {
            return ticBoard[a];
        }
    }
    return null;
}

initTicTac();
</script>
""")

randomizer_page = create_game_page("🎲 Рандомайзер", """
<h1>🎲 РАНДОМАЙЗЕР</h1>
<div style="text-align:center; padding:20px;">
    <div style="display:flex; gap:15px; justify-content:center; flex-wrap:wrap; margin:15px 0;">
        <div>
            <label style="color:#aa8866;">От:</label>
            <input type="number" id="randomMin" value="1" style="padding:10px; border-radius:8px; border:2px solid #ffd70044; background:rgba(0,0,0,0.3); color:#ffd700; width:100px;">
        </div>
        <div>
            <label style="color:#aa8866;">До:</label>
            <input type="number" id="randomMax" value="100" style="padding:10px; border-radius:8px; border:2px solid #ffd70044; background:rgba(0,0,0,0.3); color:#ffd700; width:100px;">
        </div>
    </div>
    <div style="font-size:5em; color:#ffd700; margin:20px 0; padding:20px; background:rgba(0,0,0,0.3); border-radius:15px;" id="randomNumber">?</div>
    <button class="btn btn-spin" onclick="generateRandom()">🎲 Сгенерировать</button>
    <div id="randomMessage" class="message-box info" style="text-align:center; margin-top:15px;">Нажмите "Сгенерировать"</div>
</div>
<script>
function generateRandom() {
    const min = parseInt(document.getElementById('randomMin').value) || 1;
    const max = parseInt(document.getElementById('randomMax').value) || 100;

    if (min >= max) {
        document.getElementById('randomMessage').textContent = '❌ Минимум должен быть меньше максимума!';
        document.getElementById('randomMessage').className = 'message-box lose';
        return;
    }

    const result = Math.floor(Math.random() * (max - min + 1)) + min;
    document.getElementById('randomNumber').textContent = result;
    document.getElementById('randomMessage').textContent = `🎲 Случайное число от ${min} до ${max}: ${result}`;
    document.getElementById('randomMessage').className = 'message-box win';
}
</script>
""")

clicker_page = create_game_page("🖱️ Кликер", """
<h1>🖱️ КЛИКЕР</h1>
<div style="text-align:center; padding:30px;">
    <div style="display:flex; gap:20px; justify-content:center; margin:20px 0;">
        <div style="background:rgba(0,0,0,0.3); padding:15px; border-radius:8px; border:1px solid #ffd70022; text-align:center;">
            <div style="font-size:24px; font-weight:bold; color:#ffd700;" id="clickCount">0</div>
            <div style="color:#aa8866;">Кликов</div>
        </div>
    </div>
    <button class="clicker-btn" onclick="doClick()" style="font-size:5em; padding:20px 40px; background:linear-gradient(135deg,#ffd700,#f0a500); border:none; border-radius:20px; cursor:pointer; transition:all 0.1s;">🖱️</button>
    <button class="btn btn-reset" onclick="resetClicker()" style="display:block; margin:20px auto;">🔄 Сброс</button>
    <div id="clickerMessage" class="message-box info" style="text-align:center;">Кликайте чтобы зарабатывать</div>
</div>
<script>
let clicks = 0;

function doClick() {
    clicks++;
    document.getElementById('clickCount').textContent = clicks;
    document.getElementById('clickerMessage').textContent = `🖱️ Клик! Всего: ${clicks}`;
    document.getElementById('clickerMessage').className = 'message-box win';
}

function resetClicker() {
    clicks = 0;
    document.getElementById('clickCount').textContent = 0;
    document.getElementById('clickerMessage').textContent = '🔄 Сброшено';
    document.getElementById('clickerMessage').className = 'message-box info';
}
</script>
""")

dino_page = create_game_page("🦕 Динозаврик", """
<h1>🦕 ДИНОЗАВРИК</h1>
<div style="text-align:center; background:#1a1a2e; padding:20px; border-radius:10px; position:relative; min-height:300px;">
    <div style="color:#ffd700; font-size:1.5em; margin-bottom:10px;">Счет: <span id="dinoScore">0</span></div>
    <div style="width:100%; height:4px; background:#666; position:absolute; bottom:60px;"></div>
    <div id="dino" style="font-size:3em; position:absolute; bottom:65px; left:50px; transition:bottom 0.1s;">🦕</div>
    <div id="dinoObstacle" style="font-size:2.5em; position:absolute; bottom:65px; right:50px;"></div>
    <div style="margin-top:100px;">
        <button class="btn btn-spin" onclick="startDino()">▶️ СТАРТ</button>
        <button class="btn btn-reset" onclick="resetDino()">🔄 Сброс</button>
    </div>
    <div id="dinoMessage" class="message-box info" style="text-align:center; margin-top:20px;">Нажмите "СТАРТ" чтобы начать</div>
</div>
<script>
let dinoRunning = false;
let dinoScore = 0;
let dinoInterval = null;
let dinoCheck = null;

function startDino() {
    if (dinoRunning) return;
    dinoRunning = true;
    dinoScore = 0;
    document.getElementById('dinoScore').textContent = dinoScore;
    document.getElementById('dinoMessage').textContent = '🦕 Игра началась! Нажмите пробел';
    document.getElementById('dinoMessage').className = 'message-box info';

    const obstacle = document.getElementById('dinoObstacle');
    obstacle.textContent = '🌵';
    obstacle.style.animation = 'moveObstacle 2s linear infinite';

    document.addEventListener('keydown', dinoJump);
    document.addEventListener('click', dinoJump);

    dinoInterval = setInterval(() => {
        dinoScore++;
        document.getElementById('dinoScore').textContent = dinoScore;
    }, 100);

    dinoCheck = setInterval(() => {
        const dino = document.getElementById('dino');
        const obs = document.getElementById('dinoObstacle');
        const dinoRect = dino.getBoundingClientRect();
        const obsRect = obs.getBoundingClientRect();

        if (dinoRect.right > obsRect.left + 20 && 
            dinoRect.left < obsRect.right - 20 &&
            dinoRect.bottom > obsRect.top + 20) {
            gameOverDino();
        }
    }, 50);
}

function dinoJump(e) {
    if (e.type === 'keydown' && e.code !== 'Space') return;
    e.preventDefault();
    const dino = document.getElementById('dino');
    if (dino.classList.contains('jumping')) return;

    dino.classList.add('jumping');
    setTimeout(() => {
        dino.classList.remove('jumping');
    }, 400);
}

function gameOverDino() {
    dinoRunning = false;
    document.removeEventListener('keydown', dinoJump);
    document.removeEventListener('click', dinoJump);
    clearInterval(dinoInterval);
    clearInterval(dinoCheck);
    document.getElementById('dinoMessage').textContent = `💀 Игра окончена! Счет: ${dinoScore}`;
    document.getElementById('dinoMessage').className = 'message-box lose';
    document.getElementById('dinoObstacle').style.animation = 'none';
}

function resetDino() {
    dinoRunning = false;
    document.removeEventListener('keydown', dinoJump);
    document.removeEventListener('click', dinoJump);
    clearInterval(dinoInterval);
    clearInterval(dinoCheck);
    document.getElementById('dinoScore').textContent = 0;
    document.getElementById('dinoObstacle').textContent = '';
    document.getElementById('dinoObstacle').style.animation = 'none';
    document.getElementById('dinoMessage').textContent = '🔄 Сброшено';
    document.getElementById('dinoMessage').className = 'message-box info';
}
</script>
<style>
@keyframes moveObstacle {
0% { right: 50px; }
100% { right: calc(100% + 50px); }
}
.jumping {
animation: jump 0.4s ease;
}
@keyframes jump {
0% { bottom: 65px; }
50% { bottom: 200px; }
100% { bottom: 65px; }
}
</style>
""")

# Сохраняем все страницы
pages = {
    'index.html': main_html,
    'casino.html': casino_page,
    'chess.html': chess_page,
    'tictac.html': tictac_page,
    'randomizer.html': randomizer_page,
    'clicker.html': clicker_page,
    'dino.html': dino_page,
    'war.html': war_page
}

for filename, content in pages.items():
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

print("✅ Созданы все страницы:")
for filename in pages.keys():
    print(f"   - {filename}")

print("\n🚀 Открываю главную страницу...")
webbrowser.open('index.html')

# Запускаем сервер
PORT = 8000
try:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
except:
    pass

try:
    print(f"\n🌐 Сервер запущен на http://localhost:{PORT}")
    print("Нажмите Ctrl+C для остановки")
    handler = SimpleHTTPRequestHandler
    httpd = HTTPServer(("", PORT), handler)
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\n👋 Сервер остановлен")
except OSError:
    print(f"\n⚠️ Порт {PORT} занят. Попробуйте открыть файл вручную: index.html")
    webbrowser.open('index.html')
