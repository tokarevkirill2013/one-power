from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

app = FastAPI(title="Smart Booking API", description="API для управления бронированием переговорных")


# --- Модели данных ---
class BookingCreate(BaseModel):
    room_id: int
    date: str  # YYYY-MM-DD
    time: str  # HH:MM
    name: str
    email: Optional[str] = ""


class Booking(BookingCreate):
    id: str


# --- Хранилище в памяти ---
bookings_db: List[Booking] = []


# --- Вспомогательные функции ---
def is_time_slot_available(room_id: int, date: str, time: str) -> bool:
    """Проверяет, свободно ли время"""
    for booking in bookings_db:
        if booking.room_id == room_id and booking.date == date and booking.time == time:
            return False
    return True


def is_date_valid(date_str: str) -> bool:
    """Проверяет, что дата не старше текущей и не дальше 14 дней"""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        today = datetime.now().date()
        delta = (date_obj - today).days
        return 0 <= delta <= 14
    except:
        return False


# --- HTML интерфейс ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Booking</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: Arial, sans-serif;
            background: #f0f0f0;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            color: #333;
            margin-bottom: 20px;
        }
        .dates {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-bottom: 20px;
            background: #fff;
            padding: 20px;
            border-radius: 10px;
        }
        .date-btn {
            padding: 10px 20px;
            border: 2px solid #667eea;
            border-radius: 8px;
            background: #fff;
            color: #333;
            cursor: pointer;
            font-weight: bold;
            min-width: 70px;
            text-align: center;
            border-color: #333;
        }
        .date-btn:hover {
            background: #CCCCCC;
            color: #fff;
        }
        .date-btn.active {
            background: #333;
            color: #fff;
        }
        .date-btn.booked {
            border-color: #e53e3e;
            color: #e53e3e;
            opacity: 0.6;
        }
        .time-slots {
            background: #fff;
            padding: 20px;
            border-radius: 10px;
            display: none;
        }
        .time-slots.active {
            display: block;
        }
        .time-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
            gap: 10px;
            margin-top: 15px;
        }
        .time-btn {
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 8px;
            background: #fff;
            cursor: pointer;
            text-align: center;
            border-color: #333;
        }
        .time-btn:hover:not(.booked) {
            background: #CCCCCC;
            color: #fff;
            border-color: #333;
        }
        .time-btn.booked {
            background: #fed7d7;
            border-color: #333;
            color: #e53e3e;
            cursor: not-allowed;
        }
        .time-btn.selected {
            background: #333;
            border-color: #333;
            color: #fff;
        }
        .rooms {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        .room-card {
            background: #fff;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #333;
            cursor: pointer;
        }
        .room-card:hover {
            transform: scale(1.02);
        }
        .room-card.active {
            border-left-color: #margin;
            background: #FFFFFF;
        }
        .message {
            padding: 15px;
            border-radius: 8px;
            margin-top: 10px;
            display: none;
        }
        .message.show {
            display: block;
        }
        .success {
            background: #c6f6d5;
            color: #22543d;
            border: 1px solid #48bb78;
        }
        .error {
            background: #fed7d7;
            color: #742a2a;
            border: 1px solid #e53e3e;
        }
        .info {
            background: #bee3f8;
            color: #2a4365;
            border: 1px solid #63b3ed;
        }
        #textBlock {
            margin-top: 10px;
            padding: 15px;
            background: #f7fafc;
            border-radius: 8px;
            border-left: 4px solid #333;
            display: none;
        }
        .booking-card {
            background: #f7fafc;
            padding: 10px;
            border-radius: 5px;
            margin: 5px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-left: 4px solid #333;
        }
        .booking-card button {
            padding: 5px 15px;
            background: #fc8181;
            color: #fff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .desc-btn {
            padding: 10px 20px;
            background: #667eea;
            color: #fff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin-bottom: 15px;
            font-weight: bold;
        }
        .desc-btn:hover {
            background: #5a67d8;
        }
        .booking-btn {
            padding: 10px 25px;
            background: #48bb78;
            color: #fff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            margin-top: 5px;
        }
        .booking-btn:hover {
            background: #38a169;
        }
        .cancel-btn {
            padding: 10px 25px;
            background: #e53e3e;
            color: #fff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            margin-top: 5px;
            margin-left: 5px;
        }
        .cancel-btn:hover {
            background: #c53030;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Распланируй своё время</h1>

        <div class="rooms" id="rooms">
            <div class="room-card active" data-room="1" onclick="selectRoom(1)">Добро пожаловать! <br><small>Комната 1</small></div>
            <div class="room-card" data-room="2" onclick="selectRoom(2)">Конференц-зал <br><small>Комната 2</small></div>
            <div class="room-card" data-room="3" onclick="selectRoom(3)">Переговорная <br><small>Комната 3</small></div>
        </div>

        <button class="desc-btn" onclick="toggleText()">Показать описание</button>
        <div id="textBlock">
            <b>Как работает Smart Booking:</b><br>
            1. Выберите переговорную комнату<br>
            2. Выберите дату (доступно на 14 дней вперед)<br>
            3. Нажмите на свободное время для бронирования<br>
            4. Подтвердите бронирование<br>
            5. Управляйте бронированиями
        </div>

        <div class="dates" id="dates"></div>

        <div class="time-slots" id="timeSlots">
            <h3>Доступное время</h3>
            <div class="time-grid" id="timeGrid"></div>
            <div id="bookingInfo" style="margin-top:15px;"></div>
        </div>

        <div id="myBookings" style="background:#fff;padding:20px;border-radius:10px;margin-top:20px;">
            <h3>Мои бронирования</h3>
            <div id="bookingsList"><p style="color:#999;">Нет бронирований</p></div>
        </div>

        <div class="message" id="message"></div>
    </div>

    <script>
        const API_BASE = '/api';

        let bookings = [];
        let selectedRoom = 1;
        let selectedDate = null;
        let selectedTime = null;

        async function init() {
            await loadBookings();
            generateDates();
            const today = new Date();
            const dateStr = formatDate(today);
            document.querySelectorAll('.date-btn').forEach(b => {
                if (b.dataset.date === dateStr) {
                    b.classList.add('active');
                    showTimeSlots(dateStr);
                }
            });
            updateBookings();
        }

        async function loadBookings() {
            try {
                const response = await fetch(`${API_BASE}/bookings`);
                if (response.ok) {
                    bookings = await response.json();
                } else {
                    console.error('Ошибка загрузки бронирований');
                }
            } catch (error) {
                console.error('Ошибка сети:', error);
            }
        }

        async function saveBooking(booking) {
            try {
                const response = await fetch(`${API_BASE}/bookings`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(booking)
                });
                if (response.ok) {
                    const newBooking = await response.json();
                    bookings.push(newBooking);
                    updateBookings();
                    return true;
                } else {
                    const error = await response.json();
                    showMessage(error.detail || 'Ошибка бронирования', 'error');
                    return false;
                }
            } catch (error) {
                showMessage('Ошибка сети', 'error');
                return false;
            }
        }

        async function deleteBooking(id) {
            try {
                const response = await fetch(`${API_BASE}/bookings/${id}`, {
                    method: 'DELETE'
                });
                if (response.ok) {
                    bookings = bookings.filter(b => b.id !== id);
                    updateBookings();
                    if (selectedDate) showTimeSlots(selectedDate);
                    showMessage('Бронирование отменено', 'info');
                    return true;
                } else {
                    showMessage('Ошибка отмены', 'error');
                    return false;
                }
            } catch (error) {
                showMessage('Ошибка сети', 'error');
                return false;
            }
        }

        function formatDate(d) {
            return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2,
            '0');
        }

        function generateDates() {
            const container = document.getElementById('dates');
            container.innerHTML = '';
            const today = new Date();
            for (let i = 0; i < 14; i++) {
                const d = new Date(today);
                d.setDate(d.getDate() + i);
                const dateStr = formatDate(d);
                const btn = document.createElement('button');
                btn.className = 'date-btn';
                btn.dataset.date = dateStr;
                btn.innerHTML = d.getDate() + '<br><small>' + ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'][d.getDay()] + '</small>';
                const dayBookings = bookings.filter(b => b.date === dateStr && b.room_id === selectedRoom);
                if (dayBookings.length > 0) btn.classList.add('booked');
                btn.onclick = function() {
                    document.querySelectorAll('.date-btn').forEach(b => b.classList.remove('active'));
                    this.classList.add('active');
                    selectedDate = dateStr;
                    selectedTime = null;
                    showTimeSlots(dateStr);
                };
                container.appendChild(btn);
            }
        }

        function selectRoom(room) {
            document.querySelectorAll('.room-card').forEach(c => c.classList.remove('active'));
            document.querySelector(`.room-card[data-room="${room}"]`).classList.add('active');
            selectedRoom = room;
            selectedTime = null;
            if (selectedDate) showTimeSlots(selectedDate);
            generateDates();
            updateBookings();
        }

        function showTimeSlots(date) {
            const container = document.getElementById('timeSlots');
            container.classList.add('active');
            const booked = bookings.filter(b => b.date === date && b.room_id === selectedRoom).map(b => b.time);
            const grid = document.getElementById('timeGrid');
            grid.innerHTML = '';
            const now = new Date();
            const currentTime = String(now.getHours()).padStart(2, '0') + ':' + String(now.getMinutes()).padStart(2, '0');
            const isToday = date === formatDate(new Date());
            const TIME_SLOTS = ['09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00',
                '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00'
            ];
            TIME_SLOTS.forEach(time => {
                const btn = document.createElement('button');
                btn.className = 'time-btn';
                btn.textContent = time;
                if (booked.includes(time)) btn.classList.add('booked');
                if (isToday && time < currentTime) btn.classList.add('booked');
                if (selectedTime === time) btn.classList.add('selected');
                btn.onclick = function() {
                    if (this.classList.contains('booked')) return;
                    document.querySelectorAll('.time-btn').forEach(b => b.classList.remove('selected'));
                    this.classList.add('selected');
                    selectedTime = time;
                    showBookingForm();
                };
                grid.appendChild(btn);
            });
        }

        function showBookingForm() {
            const info = document.getElementById('bookingInfo');
            info.innerHTML = `
            <div style="background:#f7fafc;padding:15px;border-radius:8px;margin-top:10px;">
              <p><strong>${document.querySelector(`.room-card[data-room="${selectedRoom}"]`).textContent.trim().split('\\n')[0]}</strong></p>
              <p>${selectedDate} | ${selectedTime}</p>
              <input type="text" id="userName" placeholder="Ваше имя" style="padding:8px;border:2px solid #ddd;border-radius:5px;margin:5px 0;width:100%;max-width:300px;">
              <input type="email" id="userEmail" placeholder="Email" style="padding:8px;border:2px solid #ddd;border-radius:5px;margin:5px 0;width:100%;max-width:300px;">
              <button onclick="confirmBooking()" class="booking-btn">Забронировать</button>
              <button onclick="cancelBooking()" class="cancel-btn">Отмена</button>
            </div>
          `;
        }

        async function confirmBooking() {
            const name = document.getElementById('userName')?.value || 'Гость';
            const email = document.getElementById('userEmail')?.value || '';
            if (!selectedTime || !selectedDate) {
                showMessage('Выберите время', 'error');
                return;
            }
            const booking = {
                room_id: selectedRoom,
                date: selectedDate,
                time: selectedTime,
                name: name,
                email: email
            };
            const success = await saveBooking(booking);
            if (success) {
                showMessage('Бронирование подтверждено!', 'success');
                document.getElementById('bookingInfo').innerHTML = '';
                selectedTime = null;
                showTimeSlots(selectedDate);
                updateBookings();
            }
        }

        function cancelBooking() {
            document.getElementById('bookingInfo').innerHTML = '';
            selectedTime = null;
            document.querySelectorAll('.time-btn').forEach(b => b.classList.remove('selected'));
            showMessage('Бронирование отменено', 'info');
        }

        function updateBookings() {
            const list = document.getElementById('bookingsList');
            const myBookings = bookings.filter(b => b.room_id === selectedRoom);
            if (myBookings.length === 0) {
                list.innerHTML = '<p style="color:#999;">Нет бронирований</p>';
                return;
            }
            list.innerHTML = myBookings.map(b => `
            <div class="booking-card">
              <div><strong>${b.date}</strong> ${b.time} | ${b.name}</div>
              <button onclick="removeBooking('${b.id}')">X</button>
            </div>
          `).join('');
        }

        async function removeBooking(id) {
            if (!confirm('Отменить бронирование?')) return;
            await deleteBooking(id);
        }

        function showMessage(text, type) {
            const msg = document.getElementById('message');
            msg.textContent = text;
            msg.className = 'message show ' + type;
            setTimeout(() => {
                msg.className = 'message';
            }, 3000);
        }

        function toggleText() {
            const block = document.getElementById('textBlock');
            const btn = document.querySelector('.desc-btn');
            if (block.style.display === 'none' || block.style.display === '') {
                block.style.display = 'block';
                btn.textContent = 'Скрыть описание';
            } else {
                block.style.display = 'none';
                btn.textContent = 'Показать описание';
            }
        }

        init();
    </script>
</body>
</html>
"""


# --- Эндпоинты API ---

@app.get("/", response_class=HTMLResponse)
async def get_html():
    """Отдает HTML интерфейс"""
    return HTML_TEMPLATE


@app.get("/api/bookings", response_model=List[Booking])
async def get_all_bookings():
    """Получить все бронирования"""
    return bookings_db


@app.post("/api/bookings", response_model=Booking, status_code=201)
async def create_booking(booking: BookingCreate):
    """Создать новое бронирование"""
    # Проверка валидности даты
    if not is_date_valid(booking.date):
        raise HTTPException(status_code=400, detail="Дата должна быть в пределах от сегодня до +14 дней")

    # Проверка доступности
    if not is_time_slot_available(booking.room_id, booking.date, booking.time):
        raise HTTPException(status_code=409, detail="Это время уже забронировано")

    # Создание бронирования
    new_booking = Booking(
        id=str(uuid.uuid4())[:8],
        room_id=booking.room_id,
        date=booking.date,
        time=booking.time,
        name=booking.name,
        email=booking.email
    )
    bookings_db.append(new_booking)
    return new_booking


@app.delete("/api/bookings/{booking_id}", status_code=204)
async def delete_booking(booking_id: str):
    """Отменить бронирование по ID"""
    for i, booking in enumerate(bookings_db):
        if booking.id == booking_id:
            del bookings_db[i]
            return
    raise HTTPException(status_code=404, detail="Бронирование не найдено")


@app.get("/api/rooms/{room_id}/bookings")
async def get_room_bookings(room_id: int, date: Optional[str] = None):
    """Получить бронирования для конкретной комнаты (опционально по дате)"""
    filtered = [b for b in bookings_db if b.room_id == room_id]
    if date:
        filtered = [b for b in filtered if b.date == date]
    return filtered


@app.get("/api/health")
async def health_check():
    """Проверка статуса сервера"""
    return {"status": "ok", "bookings_count": len(bookings_db)}


# --- Запуск сервера ---
if __name__ == "__main__":
    import uvicorn

    print("Сервер запущен на http://localhost:8000")
    print("Документация API доступна на http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
