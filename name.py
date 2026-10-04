import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox


class GameLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Игровой портал")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        # Настройка стиля
        style = ttk.Style()
        style.configure('Title.TLabel', font=('Arial', 20, 'bold'))
        style.configure('Game.TButton', font=('Arial', 12), padding=10)

        # Заголовок
        title = ttk.Label(root, text="Выберите игру", style='Title.TLabel')
        title.pack(pady=30)

        # Список игр с URL
        self.games = [
            ("❌ Крестики-нолики", "https://playtictactoe.org/"),
            ("♟ Шахматы", "https://www.chess.com/play/computer"),
            ("♠ Пасьянс", "https://www.solitaire.com/"),
            ("🎯 Сапер", "https://minesweeper.online/"),
            ("🀄 Маджонг", "https://mahjong.com/"),
            ("🎱 Бильярд", "https://www.8ballpool.com/"),
            ("🧩 Судоку", "https://sudoku.com/")
        ]

        # Создание кнопок для каждой игры
        for game_name, url in self.games:
            btn = ttk.Button(
                root,
                text=game_name,
                style='Game.TButton',
                command=lambda u=url: self.open_game(u)
            )
            btn.pack(pady=5, padx=50, fill='x')

        # Кнопка выхода
        exit_btn = ttk.Button(
            root,
            text="🚪 Выход",
            style='Game.TButton',
            command=self.exit_app
        )
        exit_btn.pack(pady=20, padx=50, fill='x')

        # Статусная строка
        self.status = ttk.Label(root, text="Готов к работе", font=('Arial', 10))
        self.status.pack(side='bottom', pady=10)

    def open_game(self, url):
        """Открывает сайт с игрой в браузере"""
        try:
            webbrowser.open(url)
            self.status.config(text=f"✅ Открыт: {url}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть сайт:\n{str(e)}")
            self.status.config(text="❌ Ошибка открытия")

    def exit_app(self):
        """Закрывает приложение"""
        if messagebox.askyesno("Выход", "Вы уверены, что хотите выйти?"):
            self.root.destroy()


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = GameLauncher(root)
    root.mainloop()