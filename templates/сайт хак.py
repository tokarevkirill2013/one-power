from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from datetime import datetime
import uvicorn
import webbrowser
import threading
import time
import sys

app = FastAPI(title="Хаб Багхантера")


# База данных
class Database:
    def __init__(self):
        self.users = {
            "hacker1": {
                "username": "hacker1",
                "password": "pass123",
                "role": "hacker",
                "rating": 1250,
                "earnings": 45000,
                "bugs_found": 12
            },
            "company1": {
                "username": "company1",
                "password": "pass123",
                "role": "company",
                "company_name": "TechCorp",
                "programs_active": 3,
                "bugs_reported": 45
            }
        }
        self.bugs = [
            {
                "id": 1,
                "title": "SQL Injection в форме авторизации",
                "company": "TechCorp",
                "severity": "Critical",
                "status": "Open",
                "reward": 50000,
                "date": "2026-08-10",
                "author": "hacker1",
                "description": "Обнаружена возможность внедрения SQL-кода"
            },
            {
                "id": 2,
                "title": "XSS уязвимость в комментариях",
                "company": "TechCorp",
                "severity": "High",
                "status": "In Review",
                "reward": 15000,
                "date": "2026-08-11",
                "author": "hacker1",
                "description": "Возможно выполнение JavaScript через комментарии"
            },
            {
                "id": 3,
                "title": "Незащищенный эндпоинт API",
                "company": "DataSafe Inc",
                "severity": "Medium",
                "status": "Closed",
                "reward": 7000,
                "date": "2026-08-09",
                "author": "hacker1",
                "description": "API эндпоинт доступен без аутентификации"
            }
        ]
        self.programs = [
            {
                "id": 1,
                "name": "TechCorp Security Program",
                "company": "TechCorp",
                "status": "Active",
                "max_reward": 100000,
                "min_reward": 5000,
                "participants": 23
            },
            {
                "id": 2,
                "name": "DataSafe Initiative",
                "company": "DataSafe Inc",
                "status": "Active",
                "max_reward": 75000,
                "min_reward": 3000,
                "participants": 15
            },
            {
                "id": 3,
                "name": "FinSecure Bug Hunt",
                "company": "FinSecure",
                "status": "Upcoming",
                "max_reward": 150000,
                "min_reward": 10000,
                "participants": 0
            }
        ]
        self.current_user = None


db = Database()

# HTML шаблоны
BASE_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Хаб Багхантера</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        .navbar {
            background: rgba(255,255,255,0.95);
            backdrop-filter: blur(10px);
            box-shadow: 0 2px 20px rgba(0,0,0,0.1);
            padding: 0 2rem;
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        .nav-container {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            height: 70px;
        }
        .nav-brand {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 1.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .brand-icon { font-size: 2rem; }
        .nav-links {
            display: flex;
            align-items: center;
            gap: 1.5rem;
            flex-wrap: wrap;
        }
        .nav-link {
            text-decoration: none;
            color: #555;
            font-weight: 500;
            transition: all 0.3s;
            padding: 0.5rem 1rem;
            border-radius: 8px;
        }
        .nav-link:hover { background: #f0f0f0; color: #667eea; }
        .login-btn {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white !important;
            padding: 0.5rem 1.5rem;
            border-radius: 20px;
        }
        .login-btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(102,126,234,0.4); }
        .logout { color: #e74c3c; }
        .user-info {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            background: #f8f9fa;
            padding: 0.3rem 1rem;
            border-radius: 20px;
        }
        .user-badge {
            background: #667eea;
            color: white;
            padding: 0.2rem 0.8rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }
        .main-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            min-height: calc(100vh - 140px);
        }
        .footer {
            background: rgba(255,255,255,0.95);
            padding: 1.5rem 2rem;
            margin-top: 2rem;
        }
        .footer-content {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: #666;
        }
        .footer-links { display: flex; gap: 2rem; }
        .footer-links a { color: #666; text-decoration: none; }
        .footer-links a:hover { color: #667eea; }
        .hero-section {
            background: rgba(255,255,255,0.95);
            border-radius: 24px;
            padding: 4rem 3rem;
            text-align: center;
            margin-bottom: 3rem;
            box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        }
        .hero-title { font-size: 3.5rem; font-weight: 800; margin-bottom: 1rem; }
        .highlight {
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero-subtitle { font-size: 1.2rem; color: #666; max-width: 600px; margin: 0 auto 2rem; }
        .hero-stats {
            display: flex;
            justify-content: center;
            gap: 3rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
        }
        .stat-card {
            text-align: center;
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 16px;
            min-width: 120px;
        }
        .stat-number {
            display: block;
            font-size: 2.5rem;
            font-weight: 800;
            color: #667eea;
        }
        .stat-label { color: #888; font-size: 0.9rem; }
        .cta-button {
            display: inline-block;
            padding: 1rem 3rem;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            text-decoration: none;
            border-radius: 30px;
            font-weight: 600;
            font-size: 1.1rem;
            transition: all 0.3s;
            border: none;
            cursor: pointer;
        }
        .cta-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(102,126,234,0.4);
        }
        .section-title {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 2rem;
            color: white;
            text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }
        .programs-section, .features-section { margin-bottom: 3rem; }
        .programs-grid, .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
        }
        .program-card, .feature-card {
            background: rgba(255,255,255,0.95);
            border-radius: 16px;
            padding: 1.5rem;
            transition: all 0.3s;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
        .program-card:hover, .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.2);
        }
        .program-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 0.5rem;
        }
        .program-name { font-size: 1.1rem; font-weight: 600; color: #333; }
        .program-status {
            padding: 0.2rem 0.8rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }
        .program-status.active { background: #27ae60; color: white; }
        .program-status.upcoming { background: #f39c12; color: white; }
        .program-status.closed { background: #e74c3c; color: white; }
        .program-company { color: #888; font-size: 0.9rem; margin-bottom: 0.5rem; }
        .program-details {
            display: flex;
            justify-content: space-between;
            font-size: 0.9rem;
            color: #555;
        }
        .feature-card { text-align: center; }
        .feature-icon { font-size: 3rem; margin-bottom: 1rem; }
        .feature-card h3 { margin-bottom: 0.5rem; color: #333; }
        .feature-card p { color: #666; line-height: 1.6; }
        .login-container {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 70vh;
        }
        .login-card {
            background: white;
            padding: 3rem;
            border-radius: 24px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.2);
            width: 100%;
            max-width: 420px;
        }
        .login-title { text-align: center; margin-bottom: 2rem; font-size: 2rem; }
        .login-form { display: flex; flex-direction: column; gap: 1.5rem; }
        .form-group { display: flex; flex-direction: column; gap: 0.5rem; }
        .form-group label { font-weight: 500; color: #555; }
        .form-group input, .form-group select, .form-group textarea {
            padding: 0.75rem;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 1rem;
            transition: all 0.3s;
            font-family: 'Inter', sans-serif;
        }
        .form-group input:focus, .form-group select:focus, .form-group textarea:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102,126,234,0.1);
        }
        .login-button {
            padding: 1rem;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        .login-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102,126,234,0.4);
        }
        .login-hint {
            margin-top: 2rem;
            padding: 1rem;
            background: #f8f9fa;
            border-radius: 12px;
            text-align: center;
        }
        .test-accounts {
            display: flex;
            flex-direction: column;
            gap: 0.3rem;
            margin-top: 0.5rem;
            font-size: 0.9rem;
            color: #666;
        }
        .alert {
            padding: 0.75rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        .alert-error { background: #fee; color: #c0392b; border: 1px solid #f5c6cb; }
        .dashboard-container {
            background: rgba(255,255,255,0.95);
            border-radius: 24px;
            padding: 2rem;
            box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        }
        .dashboard-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
            flex-wrap: wrap;
            gap: 1rem;
        }
        .user-greeting {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 1.1rem;
        }
        .role-badge {
            padding: 0.2rem 0.8rem;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
        }
        .role-badge.hacker { background: #3498db; color: white; }
        .role-badge.company { background: #2ecc71; color: white; }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        .stats-grid .stat-card {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 16px;
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        .stat-icon { font-size: 2.5rem; }
        .stat-info { display: flex; flex-direction: column; }
        .stat-value { font-size: 1.8rem; font-weight: 800; color: #667eea; }
        .dashboard-grid {
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 2rem;
        }
        .dashboard-card {
            background: #f8f9fa;
            border-radius: 16px;
            padding: 1.5rem;
        }
        .dashboard-card h3 { margin-bottom: 1rem; color: #333; }
        .status-list { display: flex; flex-direction: column; gap: 0.8rem; }
        .status-item {
            display: flex;
            justify-content: space-between;
            padding: 0.5rem;
            background: white;
            border-radius: 8px;
        }
        .status-count { font-weight: 600; color: #667eea; }
        .bug-list { display: flex; flex-direction: column; gap: 0.8rem; }
        .bug-item {
            background: white;
            padding: 1rem;
            border-radius: 10px;
        }
        .bug-info {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
            flex-wrap: wrap;
            gap: 0.5rem;
        }
        .bug-title { font-weight: 500; color: #333; }
        .bug-severity {
            padding: 0.2rem 0.8rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        .bug-severity.critical { background: #e74c3c; color: white; }
        .bug-severity.high { background: #e67e22; color: white; }
        .bug-severity.medium { background: #f39c12; color: white; }
        .bug-severity.low { background: #27ae60; color: white; }
        .bug-meta {
            display: flex;
            justify-content: space-between;
            font-size: 0.9rem;
            color: #888;
            flex-wrap: wrap;
            gap: 0.5rem;
        }
        .bug-status {
            padding: 0.2rem 0.8rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        .bug-status.open { background: #3498db; color: white; }
        .bug-status.in-review { background: #f39c12; color: white; }
        .bug-status.closed { background: #2ecc71; color: white; }
        .no-bugs { color: #999; text-align: center; padding: 2rem 0; }
        .reports-container {
            background: rgba(255,255,255,0.95);
            border-radius: 24px;
            padding: 2rem;
            box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        }
        .reports-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
            flex-wrap: wrap;
            gap: 1rem;
        }
        .new-report-btn {
            padding: 0.8rem 2rem;
            background: linear-gradient(135deg, #27ae60, #2ecc71);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        .new-report-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(39,174,96,0.4);
        }
        .filters {
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
        }
        .filter-input, .filter-select {
            padding: 0.6rem 1rem;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 0.95rem;
            transition: all 0.3s;
        }
        .filter-input:focus, .filter-select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102,126,234,0.1);
        }
        .filter-input { flex: 1; min-width: 200px; }
        .filter-select { min-width: 150px; }
        .reports-table-container { overflow-x: auto; }
        .reports-table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 12px;
            overflow: hidden;
        }
        .reports-table thead { background: #f8f9fa; }
        .reports-table th {
            padding: 1rem;
            text-align: left;
            font-weight: 600;
            color: #555;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .reports-table td { padding: 1rem; border-top: 1px solid #f0f0f0; }
        .reports-table tbody tr:hover { background: #f8f9fa; }
        .severity-badge, .status-badge {
            padding: 0.2rem 0.8rem;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        .severity-badge.critical { background: #e74c3c; color: white; }
        .severity-badge.high { background: #e67e22; color: white; }
        .severity-badge.medium { background: #f39c12; color: white; }
        .severity-badge.low { background: #27ae60; color: white; }
        .status-badge.open { background: #3498db; color: white; }
        .status-badge.in-review { background: #f39c12; color: white; }
        .status-badge.closed { background: #2ecc71; color: white; }
        .modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 2000;
        }
        .modal-content {
            background: white;
            padding: 2rem;
            border-radius: 24px;
            max-width: 500px;
            width: 90%;
            max-height: 90vh;
            overflow-y: auto;
            position: relative;
        }
        .modal-close {
            position: absolute;
            top: 1rem;
            right: 1.5rem;
            font-size: 2rem;
            cursor: pointer;
            color: #999;
            transition: all 0.3s;
        }
        .modal-close:hover { color: #333; transform: rotate(90deg); }
        .submit-btn {
            width: 100%;
            padding: 1rem;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            margin-top: 1rem;
        }
        .submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102,126,234,0.4);
        }
        .programs-container {
            background: rgba(255,255,255,0.95);
            border-radius: 24px;
            padding: 2rem;
            box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        }
        .page-title {
            font-size: 2.5rem;
            font-weight: 800;
            color: #333;
            margin-bottom: 0.5rem;
        }
        .page-subtitle { color: #888; font-size: 1.1rem; margin-bottom: 2rem; }
        .programs-filters {
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
        }
        .programs-grid-full {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 2rem;
        }
        .program-card-full {
            background: #f8f9fa;
            border-radius: 16px;
            padding: 1.5rem;
            transition: all 0.3s;
        }
        .program-card-full:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.1);
        }
        .program-card-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 1rem;
        }
        .program-name-full {
            font-size: 1.2rem;
            font-weight: 600;
            color: #333;
        }
        .program-company-full { color: #888; font-size: 0.95rem; }
        .program-card-body { margin: 1rem 0; }
        .program-details-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
        }
        .detail-item { text-align: center; }
        .detail-label {
            display: block;
            font-size: 0.8rem;
            color: #999;
            margin-bottom: 0.3rem;
        }
        .detail-value { font-weight: 600; color: #333; }
        .program-card-footer { margin-top: 1rem; }
        .join-btn {
            width: 100%;
            padding: 0.8rem;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            text-align: center;
            text-decoration: none;
            display: inline-block;
        }
        .join-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102,126,234,0.4);
        }
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem 2rem;
            border-radius: 12px;
            color: white;
            font-weight: 500;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            z-index: 3000;
            animation: slideIn 0.3s ease;
        }
        .notification-success { background: #27ae60; }
        .notification-error { background: #e74c3c; }
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slideOut {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
        @media (max-width: 768px) {
            .hero-title { font-size: 2.5rem; }
            .hero-stats { flex-direction: column; gap: 1rem; }
            .dashboard-grid { grid-template-columns: 1fr; }
            .programs-grid-full { grid-template-columns: 1fr; }
            .program-details-grid { grid-template-columns: 1fr; }
            .nav-links { flex-wrap: wrap; gap: 0.5rem; }
            .main-content { padding: 1rem; }
            .filters { flex-direction: column; }
            .filter-input, .filter-select { width: 100%; }
            .reports-header { flex-direction: column; align-items: stretch; }
            .footer-content { flex-direction: column; gap: 1rem; text-align: center; }
        }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-brand">
                <span class="brand-icon">🛡️</span>
                <span class="brand-text">Хаб Багхантера</span>
            </div>
            <div class="nav-links">
                <a href="/" class="nav-link">Главная</a>
                <a href="/programs" class="nav-link">Программы</a>
                {USER_NAV}
            </div>
        </div>
    </nav>
    <main class="main-content">
        {CONTENT}
    </main>
    <footer class="footer">
        <div class="footer-content">
            <p>© 2026 Хаб Багхантера. Все права защищены.</p>
            <div class="footer-links">
                <a href="#">О нас</a>
                <a href="#">Правила</a>
                <a href="#">Поддержка</a>
            </div>
        </div>
    </footer>
    <script>
        function showNotification(message, type) {
            var notification = document.createElement('div');
            notification.className = 'notification notification-' + (type || 'success');
            notification.textContent = message;
            document.body.appendChild(notification);
            setTimeout(function() {
                notification.style.animation = 'slideOut 0.3s ease';
                setTimeout(function() { notification.remove(); }, 300);
            }, 3000);
        }
        function showNewBugForm() {
            document.getElementById('newBugModal').style.display = 'block';
        }
        function closeModal() {
            document.getElementById('newBugModal').style.display = 'none';
        }
        window.onclick = function(event) {
            var modal = document.getElementById('newBugModal');
            if (event.target == modal) modal.style.display = 'none';
        }
        function filterTable() {
            var search = document.getElementById('searchInput').value.toLowerCase();
            var severity = document.getElementById('severityFilter').value;
            var status = document.getElementById('statusFilter').value;
            var rows = document.querySelectorAll('#reportsBody tr');
            rows.forEach(function(row) {
                var title = row.querySelector('td:nth-child(2)')?.textContent.toLowerCase() || '';
                var rowSeverity = row.querySelector('.severity-badge')?.textContent || '';
                var rowStatus = row.querySelector('.status-badge')?.textContent || '';
                var matchSearch = title.includes(search);
                var matchSeverity = !severity || rowSeverity === severity;
                var matchStatus = !status || rowStatus === status;
                row.style.display = (matchSearch && matchSeverity && matchStatus) ? '' : 'none';
            });
        }
        function exportData() {
            var bugs = [];
            document.querySelectorAll('#reportsBody tr').forEach(function(row) {
                var cells = row.querySelectorAll('td');
                if (cells.length > 0) {
                    bugs.push({
                        id: cells[0].textContent,
                        title: cells[1].textContent,
                        company: cells[2].textContent,
                        severity: cells[3].textContent,
                        status: cells[4].textContent,
                        reward: cells[5].textContent,
                        date: cells[6].textContent
                    });
                }
            });
            if (bugs.length === 0) {
                showNotification('Нет данных для экспорта', 'error');
                return;
            }
            var csv = 'ID,Название,Компания,Уровень,Статус,Награда,Дата\\n';
            bugs.forEach(function(bug) {
                csv += bug.id + ',"' + bug.title + '",' + bug.company + ',' + bug.severity + ',' + bug.status + ',' + bug.reward + ',' + bug.date + '\\n';
            });
            var blob = new Blob([csv], { type: 'text/csv' });
            var url = window.URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = 'bugs_' + new Date().toISOString().split('T')[0] + '.csv';
            a.click();
            window.URL.revokeObjectURL(url);
            showNotification('Данные успешно экспортированы!', 'success');
        }
        document.addEventListener('DOMContentLoaded', function() {
            if (document.getElementById('newBugForm')) {
                document.getElementById('newBugForm').addEventListener('submit', async function(e) {
                    e.preventDefault();
                    var formData = new FormData(this);
                    try {
                        var response = await fetch('/api/bugs/new', { method: 'POST', body: formData });
                        var result = await response.json();
                        if (result.success) {
                            showNotification('✅ Отчет успешно создан!');
                            setTimeout(function() { location.reload(); }, 1000);
                        } else {
                            showNotification('❌ Ошибка при создании отчета', 'error');
                        }
                    } catch (error) {
                        showNotification('❌ Ошибка соединения', 'error');
                    }
                });
            }
            if (document.getElementById('searchInput')) {
                document.getElementById('searchInput').addEventListener('input', filterTable);
                document.getElementById('severityFilter')?.addEventListener('change', filterTable);
                document.getElementById('statusFilter')?.addEventListener('change', filterTable);
            }
            if (document.querySelector('.reports-table')) {
                var header = document.querySelector('.reports-header');
                if (header) {
                    var exportBtn = document.createElement('button');
                    exportBtn.className = 'new-report-btn';
                    exportBtn.style.background = 'linear-gradient(135deg, #3498db, #2980b9)';
                    exportBtn.textContent = '📥 Экспорт CSV';
                    exportBtn.onclick = exportData;
                    header.appendChild(exportBtn);
                }
            }
            var cards = document.querySelectorAll('.program-card, .feature-card, .stat-card');
            cards.forEach(function(card, index) {
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                setTimeout(function() {
                    card.style.transition = 'all 0.5s ease';
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }, 100 * index);
            });
        });
    </script>
</body>
</html>
'''


def render_page(content, user=None):
    """Рендеринг страницы с подстановкой контента"""
    if user:
        nav = '''
                    <a href="/dashboard" class="nav-link">Дашборд</a>
                    <a href="/reports" class="nav-link">Отчеты</a>
                    <div class="user-info">
                        <span class="user-role">👤 {username}</span>
                        <span class="user-badge">{role}</span>
                    </div>
                    <a href="/logout" class="nav-link logout">Выйти</a>
        '''.format(username=user.get('username', ''), role=user.get('role', ''))
    else:
        nav = '<a href="/login" class="nav-link login-btn">Войти</a>'

    return BASE_TEMPLATE.replace('{USER_NAV}', nav).replace('{CONTENT}', content)


# Маршруты
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    stats = {
        "total_bugs": len(db.bugs),
        "total_earnings": sum(b.get("reward", 0) for b in db.bugs),
        "active_programs": len([p for p in db.programs if p["status"] == "Active"])
    }

    programs_html = ''
    for program in db.programs[:3]:
        programs_html += f'''
        <div class="program-card">
            <div class="program-header">
                <h3 class="program-name">{program["name"]}</h3>
                <span class="program-status {program["status"].lower()}">{program["status"]}</span>
            </div>
            <p class="program-company">{program["company"]}</p>
            <div class="program-details">
                <span>💰 {program["min_reward"]} - {program["max_reward"]} ₽</span>
                <span>👥 {program["participants"]} участников</span>
            </div>
        </div>
        '''

    content = f'''
    <div class="hero-section">
        <div class="hero-content">
            <h1 class="hero-title">🛡️ Платформа для <span class="highlight">белых хакеров</span></h1>
            <p class="hero-subtitle">Находите уязвимости, получайте вознаграждения и делайте интернет безопаснее</p>
            <div class="hero-stats">
                <div class="stat-card">
                    <span class="stat-number">{stats["total_bugs"]}</span>
                    <span class="stat-label">Найдено багов</span>
                </div>
                <div class="stat-card">
                    <span class="stat-number">{stats["total_earnings"] // 1000}к</span>
                    <span class="stat-label">Всего выплачено</span>
                </div>
                <div class="stat-card">
                    <span class="stat-number">{stats["active_programs"]}</span>
                    <span class="stat-label">Активных программ</span>
                </div>
            </div>
            <a href="/login" class="cta-button">Начать охоту →</a>
        </div>
    </div>
    <div class="programs-section">
        <h2 class="section-title">🔥 Активные программы</h2>
        <div class="programs-grid">
            {programs_html}
        </div>
    </div>
    <div class="features-section">
        <h2 class="section-title">✨ Почему мы?</h2>
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <h3>Единое окно</h3>
                <p>Все баги и программы в одном месте с интеграцией с популярными платформами</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <h3>Аналитика</h3>
                <p>Подробная статистика по вашим багам, рейтингу и заработанным суммам</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🚀</div>
                <h3>Быстрые выплаты</h3>
                <p>Прозрачная система оценки и моментальные выплаты за найденные уязвимости</p>
            </div>
        </div>
    </div>
    '''
    return HTMLResponse(render_page(content, db.current_user))


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    content = '''
    <div class="login-container">
        <div class="login-card">
            <h2 class="login-title">🔐 Вход в систему</h2>
            <form method="POST" action="/login" class="login-form">
                <div class="form-group">
                    <label for="username">Имя пользователя</label>
                    <input type="text" id="username" name="username" placeholder="Введите логин" required>
                </div>
                <div class="form-group">
                    <label for="password">Пароль</label>
                    <input type="password" id="password" name="password" placeholder="Введите пароль" required>
                </div>
                <button type="submit" class="login-button">Войти</button>
            </form>
            <div class="login-hint">
                <p>Тестовые аккаунты:</p>
                <div class="test-accounts">
                    <span>👨‍💻 Хакер: hacker1 / pass123</span>
                    <span>🏢 Компания: company1 / pass123</span>
                </div>
            </div>
        </div>
    </div>
    '''
    return HTMLResponse(render_page(content))


@app.post("/login", response_class=HTMLResponse)
async def login(
        request: Request,
        username: str = Form(...),
        password: str = Form(...)
):
    if username in db.users and db.users[username]["password"] == password:
        db.current_user = db.users[username]
        db.current_user["username"] = username
        return RedirectResponse(url="/dashboard", status_code=303)

    content = '''
    <div class="login-container">
        <div class="login-card">
            <h2 class="login-title">🔐 Вход в систему</h2>
            <div class="alert alert-error">Неверный логин или пароль</div>
            <form method="POST" action="/login" class="login-form">
                <div class="form-group">
                    <label for="username">Имя пользователя</label>
                    <input type="text" id="username" name="username" placeholder="Введите логин" required>
                </div>
                <div class="form-group">
                    <label for="password">Пароль</label>
                    <input type="password" id="password" name="password" placeholder="Введите пароль" required>
                </div>
                <button type="submit" class="login-button">Войти</button>
            </form>
            <div class="login-hint">
                <p>Тестовые аккаунты:</p>
                <div class="test-accounts">
                    <span>👨‍💻 Хакер: hacker1 / pass123</span>
                    <span>🏢 Компания: company1 / pass123</span>
                </div>
            </div>
        </div>
    </div>
    '''
    return HTMLResponse(render_page(content))


@app.get("/logout")
async def logout():
    db.current_user = None
    return RedirectResponse(url="/", status_code=303)


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    if not db.current_user:
        return RedirectResponse(url="/login", status_code=303)

    user_bugs = [b for b in db.bugs if b["author"] == db.current_user.get("username")]

    bugs_html = ''
    for bug in user_bugs[:3]:
        bugs_html += f'''
        <div class="bug-item">
            <div class="bug-info">
                <span class="bug-title">{bug["title"]}</span>
                <span class="bug-severity {bug["severity"].lower()}">{bug["severity"]}</span>
            </div>
            <div class="bug-meta">
                <span>💰 {bug["reward"]} ₽</span>
                <span class="bug-status {bug["status"].lower().replace(' ', '-')}">{bug["status"]}</span>
            </div>
        </div>
        '''

    if not bugs_html:
        bugs_html = '<p class="no-bugs">Пока нет найденных багов. Начните охоту!</p>'

    content = f'''
    <div class="dashboard-container">
        <div class="dashboard-header">
            <h1>📊 Панель управления</h1>
            <div class="user-greeting">
                <span>Добро пожаловать, </span>
                <strong>{db.current_user["username"]}</strong>
                <span class="role-badge {db.current_user["role"]}">{db.current_user["role"]}</span>
            </div>
        </div>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon">🐛</div>
                <div class="stat-info">
                    <span class="stat-value">{len(user_bugs)}</span>
                    <span class="stat-label">Найдено багов</span>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">💰</div>
                <div class="stat-info">
                    <span class="stat-value">{sum(b["reward"] for b in user_bugs)} ₽</span>
                    <span class="stat-label">Заработано</span>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">⭐</div>
                <div class="stat-info">
                    <span class="stat-value">{db.current_user.get("rating", 0)}</span>
                    <span class="stat-label">Рейтинг</span>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">📈</div>
                <div class="stat-info">
                    <span class="stat-value">{db.current_user.get("bugs_found", 0)}</span>
                    <span class="stat-label">Всего найдено</span>
                </div>
            </div>
        </div>
        <div class="dashboard-grid">
            <div class="dashboard-card">
                <h3>📋 По статусам</h3>
                <div class="status-list">
                    <div class="status-item">
                        <span>🔴 Critical</span>
                        <span class="status-count">{len([b for b in user_bugs if b["severity"] == "Critical"])}</span>
                    </div>
                    <div class="status-item">
                        <span>🟠 High</span>
                        <span class="status-count">{len([b for b in user_bugs if b["severity"] == "High"])}</span>
                    </div>
                    <div class="status-item">
                        <span>🟡 Medium</span>
                        <span class="status-count">{len([b for b in user_bugs if b["severity"] == "Medium"])}</span>
                    </div>
                    <div class="status-item">
                        <span>🟢 Low</span>
                        <span class="status-count">{len([b for b in user_bugs if b["severity"] == "Low"])}</span>
                    </div>
                </div>
            </div>
            <div class="dashboard-card">
                <h3>📝 Последние баги</h3>
                <div class="bug-list">
                    {bugs_html}
                </div>
            </div>
        </div>
    </div>
    '''
    return HTMLResponse(render_page(content, db.current_user))


@app.get("/reports", response_class=HTMLResponse)
async def reports_page(request: Request):
    if not db.current_user:
        return RedirectResponse(url="/login", status_code=303)

    bugs_html = ''
    for bug in db.bugs:
        bugs_html += f'''
        <tr>
            <td>#{bug["id"]}</td>
            <td>{bug["title"]}</td>
            <td>{bug["company"]}</td>
            <td><span class="severity-badge {bug["severity"].lower()}">{bug["severity"]}</span></td>
            <td><span class="status-badge {bug["status"].lower().replace(' ', '-')}">{bug["status"]}</span></td>
            <td>💰 {bug["reward"]} ₽</td>
            <td>{bug["date"]}</td>
            <td>{bug["author"]}</td>
        </tr>
        '''

    programs_options = ''
    for program in db.programs:
        programs_options += f'<option value="{program["company"]}">{program["company"]}</option>'

    content = f'''
    <div class="reports-container">
        <div class="reports-header">
            <h1>📄 Все отчеты</h1>
            <button class="new-report-btn" onclick="showNewBugForm()">+ Новый отчет</button>
        </div>
        <div class="filters">
            <input type="text" id="searchInput" placeholder="Поиск по названию..." class="filter-input">
            <select id="severityFilter" class="filter-select">
                <option value="">Все уровни</option>
                <option value="Critical">Critical</option>
                <option value="High">High</option>
                <option value="Medium">Medium</option>
                <option value="Low">Low</option>
            </select>
            <select id="statusFilter" class="filter-select">
                <option value="">Все статусы</option>
                <option value="Open">Open</option>
                <option value="In Review">In Review</option>
                <option value="Closed">Closed</option>
            </select>
        </div>
        <div class="reports-table-container">
            <table class="reports-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Название</th>
                        <th>Компания</th>
                        <th>Уровень</th>
                        <th>Статус</th>
                        <th>Награда</th>
                        <th>Дата</th>
                        <th>Автор</th>
                    </tr>
                </thead>
                <tbody id="reportsBody">
                    {bugs_html}
                </tbody>
            </table>
        </div>
        <div id="newBugModal" class="modal" style="display: none;">
            <div class="modal-content">
                <span class="modal-close" onclick="closeModal()">&times;</span>
                <h2>🐛 Создать новый отчет</h2>
                <form id="newBugForm">
                    <div class="form-group">
                        <label for="bugTitle">Название уязвимости</label>
                        <input type="text" id="bugTitle" name="title" required>
                    </div>
                    <div class="form-group">
                        <label for="bugDescription">Описание</label>
                        <textarea id="bugDescription" name="description" rows="4" required></textarea>
                    </div>
                    <div class="form-group">
                        <label for="bugSeverity">Уровень критичности</label>
                        <select id="bugSeverity" name="severity" required>
                            <option value="Critical">Critical</option>
                            <option value="High">High</option>
                            <option value="Medium">Medium</option>
                            <option value="Low">Low</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="bugCompany">Компания</label>
                        <select id="bugCompany" name="company" required>
                            {programs_options}
                        </select>
                    </div>
                    <button type="submit" class="submit-btn">Отправить отчет</button>
                </form>
            </div>
        </div>
    </div>
    '''
    return HTMLResponse(render_page(content, db.current_user))


@app.get("/programs", response_class=HTMLResponse)
async def programs_page(request: Request):
    programs_html = ''
    for program in db.programs:
        programs_html += f'''
        <div class="program-card-full">
            <div class="program-card-header">
                <div>
                    <h3 class="program-name-full">{program["name"]}</h3>
                    <p class="program-company-full">{program["company"]}</p>
                </div>
                <span class="program-status {program["status"].lower()}">{program["status"]}</span>
            </div>
            <div class="program-card-body">
                <div class="program-details-grid">
                    <div class="detail-item">
                        <span class="detail-label">Максимальная награда</span>
                        <span class="detail-value">💰 {program["max_reward"]} ₽</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Минимальная награда</span>
                        <span class="detail-value">💵 {program["min_reward"]} ₽</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Участников</span>
                        <span class="detail-value">👥 {program["participants"]}</span>
                    </div>
                </div>
            </div>
            <div class="program-card-footer">
                <button class="join-btn" onclick="showNotification('Вы присоединились к программе!')">
                    Присоединиться
                </button>
            </div>
        </div>
        '''

    content = f'''
    <div class="programs-container">
        <h1 class="page-title">🚀 Программы Bug Bounty</h1>
        <p class="page-subtitle">Участвуйте в программах и зарабатывайте на найденных уязвимостях</p>
        <div class="programs-grid-full">
            {programs_html}
        </div>
    </div>
    '''
    return HTMLResponse(render_page(content, db.current_user))


@app.get("/api/bugs")
async def get_bugs():
    return {"bugs": db.bugs}


@app.get("/api/stats")
async def get_stats():
    return {
        "total_bugs": len(db.bugs),
        "total_earnings": sum(b.get("reward", 0) for b in db.bugs),
        "active_programs": len([p for p in db.programs if p["status"] == "Active"])
    }


@app.post("/api/bugs/new")
async def create_bug(
        request: Request,
        title: str = Form(...),
        description: str = Form(...),
        severity: str = Form(...),
        company: str = Form(...)
):
    if not db.current_user:
        raise HTTPException(status_code=401, detail="Необходима авторизация")

    new_bug = {
        "id": len(db.bugs) + 1,
        "title": title,
        "description": description,
        "severity": severity,
        "company": company,
        "status": "Open",
        "reward": 10000 if severity == "Critical" else 5000 if severity == "High" else 2000,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "author": db.current_user.get("username")
    }
    db.bugs.append(new_bug)
    return {"success": True, "bug": new_bug}


def open_browser():
    time.sleep(2)
    webbrowser.open("http://127.0.0.1:8000")


def run_server():
    """Запуск сервера без reload для избежания ошибки"""
    print("=" * 50)
    print("🛡️  ХАБ БАГХАНТЕРА - Запуск приложения")
    print("=" * 50)
    print("🌐 Открывается браузер...")
    print("\n👤 Тестовые аккаунты:")
    print("   🐛 Хакер:    login - hacker1,  password - pass123")
    print("   🏢 Компания: login - company1, password - pass123")
    print("\n💡 После входа откроются все функции платформы")
    print("=" * 50)
    print("\n🚀 Сервер запущен на http://127.0.0.1:8000")
    print("🔄 Нажмите Ctrl+C для остановки сервера")
    print("=" * 50)

    # Запускаем открытие браузера в отдельном потоке
    threading.Thread(target=open_browser, daemon=True).start()

    # Запускаем сервер БЕЗ reload=True
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    run_server()