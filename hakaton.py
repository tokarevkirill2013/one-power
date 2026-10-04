from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Smart Booking API")

templates = Jinja2Templates(directory="templates")

bookings_db = []

def generate_id():
    import time
    return str(int(time.time() * 1000)) + str(len(bookings_db))

def is_time_slot_available(room_id, date, time):
    for booking in bookings_db:
        if booking.get('room_id') == room_id and booking.get('date') == date and booking.get('time') == time:
            return False
    return True

def is_date_valid(date_str):
    try:
        from datetime import datetime
        parts = date_str.split('-')
        if len(parts) != 3:
            return False
        year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
        datetime(year, month, day)
        today = datetime.now().date()
        date_obj = datetime(year, month, day).date()
        delta = (date_obj - today).days
        return 0 <= delta <= 14
    except:
        return False

def validate_booking_data(data):
    errors = []
    required_fields = ['room_id', 'date', 'time', 'name']
    for field in required_fields:
        if field not in data:
            errors.append(f"Поле '{field}' обязательно")
    if errors:
        return False, errors
    if not isinstance(data['room_id'], int):
        errors.append("room_id должен быть числом")
    if not is_date_valid(data['date']):
        errors.append("Дата должна быть в формате YYYY-MM-DD и в пределах от сегодня до +14 дней")
    time_parts = data['time'].split(':')
    if len(time_parts) != 2:
        errors.append("Время должно быть в формате HH:MM")
    else:
        try:
            hour, minute = int(time_parts[0]), int(time_parts[1])
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                errors.append("Некорректное время")
        except:
            errors.append("Некорректное время")
    if not data['name'] or len(data['name'].strip()) == 0:
        errors.append("Имя не может быть пустым")
    return len(errors) == 0, errors

def format_response(data, status_code=200):
    if data is None:
        return HTMLResponse(status_code=status_code)
    if isinstance(data, dict):
        items = []
        for key, value in data.items():
            if isinstance(value, str):
                items.append(f'"{key}": "{value}"')
            elif isinstance(value, (int, float)):
                items.append(f'"{key}": {value}')
            elif isinstance(value, bool):
                items.append(f'"{key}": {str(value).lower()}')
            elif value is None:
                items.append(f'"{key}": null')
            else:
                items.append(f'"{key}": "{value}"')
        content = "{" + ", ".join(items) + "}"
        return HTMLResponse(content=content, status_code=status_code)
    elif isinstance(data, list):
        items = []
        for item in data:
            if isinstance(item, dict):
                dict_items = []
                for key, value in item.items():
                    if isinstance(value, str):
                        dict_items.append(f'"{key}": "{value}"')
                    elif isinstance(value, (int, float)):
                        dict_items.append(f'"{key}": {value}')
                    elif isinstance(value, bool):
                        dict_items.append(f'"{key}": {str(value).lower()}')
                    elif value is None:
                        dict_items.append(f'"{key}": null')
                    else:
                        dict_items.append(f'"{key}": "{value}"')
                items.append("{" + ", ".join(dict_items) + "}")
            else:
                items.append(f'"{item}"')
        content = "[" + ", ".join(items) + "]"
        return HTMLResponse(content=content, status_code=status_code)
    else:
        return HTMLResponse(content=str(data), status_code=status_code)

def format_error_response(message, status_code=400):
    content = f'{{"detail": "{message}"}}'
    return HTMLResponse(content=content, status_code=status_code)

@app.get("/", response_class=HTMLResponse)
async def get_html(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/bookings")
async def get_all_bookings():
    return format_response(bookings_db)

@app.post("/api/bookings")
async def create_booking(request: Request):
    try:
        data = await request.json()
    except:
        return format_error_response("Неверный формат JSON", 400)
    is_valid, errors = validate_booking_data(data)
    if not is_valid:
        return format_error_response("; ".join(errors), 400)
    if not is_time_slot_available(data['room_id'], data['date'], data['time']):
        return format_error_response("Это время уже забронировано", 409)
    new_booking = {
        "id": generate_id(),
        "room_id": data['room_id'],
        "date": data['date'],
        "time": data['time'],
        "name": data['name'],
        "email": data.get('email', '')
    }
    bookings_db.append(new_booking)
    return format_response(new_booking, 201)

@app.delete("/api/bookings/{booking_id}")
async def delete_booking(booking_id: str):
    for i, booking in enumerate(bookings_db):
        if booking.get('id') == booking_id:
            del bookings_db[i]
            return HTMLResponse(status_code=204)
    return format_error_response("Бронирование не найдено", 404)

@app.get("/api/rooms/{room_id}/bookings")
async def get_room_bookings(room_id: int, date: str = None):
    filtered = [b for b in bookings_db if b.get('room_id') == room_id]
    if date:
        filtered = [b for b in filtered if b.get('date') == date]
    return format_response(filtered)

@app.get("/api/health")
async def health_check():
    return format_response({"status": "ok", "bookings_count": len(bookings_db)})