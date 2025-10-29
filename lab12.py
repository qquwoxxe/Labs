import tkinter as tk
from tkinter import messagebox, ttk
import random


class BattleshipGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Морской бой")
        self.root.resizable(False, False)

        # Размеры поля
        self.board_size = 10
        self.cell_size = 30

        # Корабли: [количество, размер]
        self.ships = [
            [1, 4],  # 1
            [2, 3],  # 2
            [3, 2],  # 3
            [4, 1]  # 4
        ]

        # Игровые поля
        self.player_board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.computer_board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.computer_board_hidden = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]

        # Статус игры
        self.game_started = False
        self.player_turn = True
        self.selected_strategy = "Центральная концентрация"
        self.computer_strategy = None
        self.show_computer_ships = False  # Флаг показа кораблей компьютера

        self.setup_ui()
        self.place_computer_ships()

    def setup_ui(self):
        """Создание интерфейса"""
        # Фрейм для выбора стратегии
        strategy_frame = tk.Frame(self.root)
        strategy_frame.pack(pady=5)

        tk.Label(strategy_frame, text="Стратегия:", font=('Arial', 10)).pack(side=tk.LEFT)

        self.strategy_var = tk.StringVar(value="Центральная концентрация")
        strategies = ["Центральная концентрация", "Диагональная защита"]
        strategy_combo = ttk.Combobox(strategy_frame, textvariable=self.strategy_var,
                                      values=strategies, state="readonly", width=20)
        strategy_combo.pack(side=tk.LEFT, padx=5)
        strategy_combo.bind('<<ComboboxSelected>>', self.on_strategy_change)

        # Фрейм для игровых полей
        boards_frame = tk.Frame(self.root)
        boards_frame.pack(pady=10)

        # Поле игрока
        player_frame = tk.Frame(boards_frame)
        player_frame.grid(row=0, column=0, padx=20)

        tk.Label(player_frame, text="Ваше поле", font=('Arial', 12, 'bold')).pack()
        self.player_canvas = tk.Canvas(player_frame,
                                       width=self.board_size * self.cell_size,
                                       height=self.board_size * self.cell_size,
                                       bg='lightblue')
        self.player_canvas.pack()

        # Поле компьютера
        computer_frame = tk.Frame(boards_frame)
        computer_frame.grid(row=0, column=1, padx=20)

        tk.Label(computer_frame, text="Противник", font=('Arial', 12, 'bold')).pack()
        self.computer_canvas = tk.Canvas(computer_frame,
                                         width=self.board_size * self.cell_size,
                                         height=self.board_size * self.cell_size,
                                         bg='lightblue')
        self.computer_canvas.pack()
        self.computer_canvas.bind('<Button-1>', self.player_shot)

        # Кнопки управления
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        self.auto_button = tk.Button(control_frame, text="Расставить корабли",
                                     command=self.strategic_place_player_ships)
        self.auto_button.pack(side=tk.LEFT, padx=5)

        self.restart_button = tk.Button(control_frame, text="Новая игра",
                                        command=self.restart_game)
        self.restart_button.pack(side=tk.LEFT, padx=5)

        # Кнопка показа/скрытия кораблей компьютера
        self.toggle_ships_button = tk.Button(control_frame, text="Показать корабли противника",
                                             command=self.toggle_computer_ships)
        self.toggle_ships_button.pack(side=tk.LEFT, padx=5)

        # Статус игры
        self.status_label = tk.Label(self.root, text="Выберите стратегию и расставьте корабли",
                                     font=('Arial', 10))
        self.status_label.pack(pady=5)

        # Описание стратегий
        self.strategy_info = tk.Label(self.root, text="", font=('Arial', 9), wraplength=400, justify=tk.LEFT)
        self.strategy_info.pack(pady=5)
        self.update_strategy_info()

        self.draw_boards()

    def toggle_computer_ships(self):
        """Переключение показа кораблей компьютера"""
        self.show_computer_ships = not self.show_computer_ships

        if self.show_computer_ships:
            self.toggle_ships_button.config(text="Скрыть корабли противника")
            self.status_label.config(text="Корабли противника показаны (режим обучения)")
        else:
            self.toggle_ships_button.config(text="Показать корабли противника")
            if self.game_started:
                self.status_label.config(text="Игра продолжается! Ваш ход.")
            else:
                self.status_label.config(text="Выберите стратегию и расставьте корабли")

        self.draw_boards()

    def on_strategy_change(self, event):
        """Обработка смены стратегии"""
        self.selected_strategy = self.strategy_var.get()
        self.update_strategy_info()

    def update_strategy_info(self):
        """Обновление информации о выбранной стратегии"""
        if self.selected_strategy == "Центральная концентрация":
            info = "Стратегия: Корабли сосредоточены в центре поля. Преимущество: защита от обстрела краев, сложнее обнаружить все корабли."
        else:
            info = "Стратегия: Корабли расположены по диагоналям. Преимущество: создает 'мертвые зоны', усложняет поиск кораблей противнику."
        self.strategy_info.config(text=info)

    def strategic_place_player_ships(self):
        """Стратегическая расстановка кораблей игрока"""
        self.player_board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]

        if self.strategy_var.get() == "Центральная концентрация":
            self.central_concentration_strategy(self.player_board)
        else:  # "Диагональная защита"
            self.diagonal_defense_strategy(self.player_board)

        self.game_started = True
        self.show_computer_ships = False
        self.toggle_ships_button.config(text="Показать корабли противника")
        self.status_label.config(text=f"Игра началась! Ваш ход. Ваша стратегия: {self.selected_strategy}")
        self.draw_boards()

    def place_computer_ships(self):
        """Компьютер случайно выбирает одну из двух стратегий"""
        self.computer_board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.computer_board_hidden = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]

        # Случайный выбор стратегии для компьютера
        self.computer_strategy = random.choice(["Центральная концентрация", "Диагональная защита"])

        if self.computer_strategy == "Центральная концентрация":
            self.central_concentration_strategy(self.computer_board)
        else:  # "Диагональная защита"
            self.diagonal_defense_strategy(self.computer_board)

        # Копируем расстановку в скрытое поле
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.computer_board_hidden[i][j] = self.computer_board[i][j]

    def central_concentration_strategy(self, board):
        """Стратегия 1: Центральная концентрация"""
        center_start = 2
        center_end = 7

        for ship_count, ship_size in self.ships:
            for _ in range(ship_count):
                placed = False
                attempts = 0

                while not placed and attempts < 100:
                    attempts += 1
                    orientation = random.choice(['horizontal', 'vertical'])

                    if ship_size == 1:
                        row = random.randint(center_start, center_end)
                        col = random.randint(center_start, center_end)
                    else:
                        if orientation == 'horizontal':
                            row = random.randint(center_start, center_end)
                            col = random.randint(center_start, center_end - ship_size + 1)
                        else:
                            row = random.randint(center_start, center_end - ship_size + 1)
                            col = random.randint(center_start, center_end)

                    if self.can_place_ship(board, row, col, ship_size, orientation):
                        self.place_ship(board, row, col, ship_size, orientation)
                        placed = True

                if not placed:
                    self.place_ship_priority_center(board, ship_size)

    def diagonal_defense_strategy(self, board):
        """Стратегия 2: Диагональная защита"""
        for ship_count, ship_size in self.ships:
            for _ in range(ship_count):
                placed = False
                attempts = 0

                while not placed and attempts < 100:
                    attempts += 1

                    if ship_size == 1:
                        placed = self.place_single_on_diagonal(board)
                    else:
                        main_diagonal = random.choice([True, False])

                        if main_diagonal:
                            # Главная диагональ
                            max_start = self.board_size - ship_size
                            start_pos = random.randint(0, max_start)

                            orientation = random.choice(['horizontal', 'vertical'])
                            if orientation == 'horizontal':
                                row = start_pos
                                col = start_pos
                                if col + ship_size <= self.board_size:
                                    if self.can_place_ship(board, row, col, ship_size, orientation):
                                        self.place_ship(board, row, col, ship_size, orientation)
                                        placed = True
                            else:
                                row = start_pos
                                col = start_pos
                                if row + ship_size <= self.board_size:
                                    if self.can_place_ship(board, row, col, ship_size, orientation):
                                        self.place_ship(board, row, col, ship_size, orientation)
                                        placed = True
                        else:
                            # Побочная диагональ
                            max_start = self.board_size - ship_size
                            start_row = random.randint(0, max_start)
                            start_col = self.board_size - 1 - start_row

                            orientation = random.choice(['horizontal', 'vertical'])
                            if orientation == 'horizontal':
                                row = start_row
                                col = max(0, start_col - ship_size + 1)
                                if col >= 0:
                                    if self.can_place_ship(board, row, col, ship_size, orientation):
                                        self.place_ship(board, row, col, ship_size, orientation)
                                        placed = True
                            else:
                                row = start_row
                                col = start_col
                                if row + ship_size <= self.board_size:
                                    if self.can_place_ship(board, row, col, ship_size, orientation):
                                        self.place_ship(board, row, col, ship_size, orientation)
                                        placed = True

                if not placed:
                    if ship_size == 1:
                        self.place_single_near_diagonal(board)
                    else:
                        self.place_ship_random(board, ship_size)

    def place_single_on_diagonal(self, board):
        for i in range(self.board_size):
            if self.can_place_ship(board, i, i, 1, 'horizontal'):
                self.place_ship(board, i, i, 1, 'horizontal')
                return True

        for i in range(self.board_size):
            if self.can_place_ship(board, i, self.board_size - 1 - i, 1, 'horizontal'):
                self.place_ship(board, i, self.board_size - 1 - i, 1, 'horizontal')
                return True

        return False

    def place_single_near_diagonal(self, board):
        for i in range(self.board_size):
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1)]:
                r, c = i + dr, i + dc
                if 0 <= r < self.board_size and 0 <= c < self.board_size:
                    if self.can_place_ship(board, r, c, 1, 'horizontal'):
                        self.place_ship(board, r, c, 1, 'horizontal')
                        return True

        for i in range(self.board_size):
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1)]:
                r, c = i + dr, (self.board_size - 1 - i) + dc
                if 0 <= r < self.board_size and 0 <= c < self.board_size:
                    if self.can_place_ship(board, r, c, 1, 'horizontal'):
                        self.place_ship(board, r, c, 1, 'horizontal')
                        return True

        return self.place_ship_random(board, 1)

    def place_ship_priority_center(self, board, ship_size):
        """Размещение корабля с приоритетом центральных позиций"""
        center_positions = []

        for row in range(2, 8):
            for col in range(2, 8):
                center_positions.append((row, col))

        random.shuffle(center_positions)

        for row, col in center_positions:
            for orientation in ['horizontal', 'vertical']:
                if orientation == 'horizontal' and col + ship_size <= self.board_size:
                    if self.can_place_ship(board, row, col, ship_size, orientation):
                        self.place_ship(board, row, col, ship_size, orientation)
                        return True
                elif orientation == 'vertical' and row + ship_size <= self.board_size:
                    if self.can_place_ship(board, row, col, ship_size, orientation):
                        self.place_ship(board, row, col, ship_size, orientation)
                        return True

        return self.place_ship_random(board, ship_size)

    def place_ship_random(self, board, ship_size):
        placed = False
        attempts = 0
        while not placed and attempts < 200:
            attempts += 1
            orientation = random.choice(['horizontal', 'vertical'])
            if orientation == 'horizontal':
                row = random.randint(0, self.board_size - 1)
                col = random.randint(0, self.board_size - ship_size)
            else:
                row = random.randint(0, self.board_size - ship_size)
                col = random.randint(0, self.board_size - 1)

            if self.can_place_ship(board, row, col, ship_size, orientation):
                self.place_ship(board, row, col, ship_size, orientation)
                placed = True
        return placed

    def can_place_ship(self, board, row, col, size, orientation):
        """Проверка возможности размещения корабля"""
        if orientation == 'horizontal':
            for i in range(size):
                if (col + i >= self.board_size or
                        board[row][col + i] != ' ' or
                        self.has_adjacent_ships(board, row, col + i)):
                    return False
        else:
            for i in range(size):
                if (row + i >= self.board_size or
                        board[row + i][col] != ' ' or
                        self.has_adjacent_ships(board, row + i, col)):
                    return False
        return True

    def has_adjacent_ships(self, board, row, col):
        """Проверка соседних клеток на наличие кораблей"""
        for r in range(max(0, row - 1), min(self.board_size, row + 2)):
            for c in range(max(0, col - 1), min(self.board_size, col + 2)):
                if board[r][c] == 'S':
                    return True
        return False

    def place_ship(self, board, row, col, size, orientation):
        """Размещение корабля на поле"""
        if orientation == 'horizontal':
            for i in range(size):
                board[row][col + i] = 'S'
        else:
            for i in range(size):
                board[row + i][col] = 'S'

    def draw_boards(self):
        """Отрисовка игровых полей"""
        self.player_canvas.delete("all")
        self.computer_canvas.delete("all")

        # Отрисовка поля игрока
        for row in range(self.board_size):
            for col in range(self.board_size):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                self.player_canvas.create_rectangle(x1, y1, x2, y2, outline='black')

                cell = self.player_board[row][col]
                if cell == 'S':
                    self.player_canvas.create_rectangle(x1 + 1, y1 + 1, x2 - 1, y2 - 1, fill='gray')
                elif cell == 'X':
                    self.player_canvas.create_line(x1 + 2, y1 + 2, x2 - 2, y2 - 2, width=2, fill='red')
                    self.player_canvas.create_line(x1 + 2, y2 - 2, x2 - 2, y1 + 2, width=2, fill='red')
                elif cell == 'O':
                    self.player_canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, outline='blue', width=2)

        # Отрисовка поля компьютера
        for row in range(self.board_size):
            for col in range(self.board_size):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                self.computer_canvas.create_rectangle(x1, y1, x2, y2, outline='black')

                if self.show_computer_ships:
                    display_board = self.computer_board
                else:
                    display_board = self.computer_board_hidden

                cell = display_board[row][col]
                if cell == 'S' and self.show_computer_ships:
                    self.computer_canvas.create_rectangle(x1 + 1, y1 + 1, x2 - 1, y2 - 1, fill='darkred')
                elif cell == 'X':
                    self.computer_canvas.create_line(x1 + 2, y1 + 2, x2 - 2, y2 - 2, width=2, fill='red')
                    self.computer_canvas.create_line(x1 + 2, y2 - 2, x2 - 2, y1 + 2, width=2, fill='red')
                elif cell == 'O':
                    self.computer_canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, outline='blue', width=2)

    def player_shot(self, event):
        """Обработка выстрела игрока"""
        if not self.game_started or not self.player_turn:
            return

        col = event.x // self.cell_size
        row = event.y // self.cell_size

        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            if self.computer_board_hidden[row][col] in ['X', 'O']:
                return

            if self.computer_board_hidden[row][col] == 'S':
                self.computer_board_hidden[row][col] = 'X'
                self.computer_board[row][col] = 'X'
                self.status_label.config(text="Попадание! Стреляйте еще.")
                if self.check_ship_sunk(self.computer_board_hidden, row, col):
                    self.status_label.config(text="Потоплен! Стреляйте еще.")
                if self.check_win(self.computer_board_hidden):
                    messagebox.showinfo("Победа!", "Вы выиграли! Стратегия сработала!")
                    self.game_started = False
            else:
                self.computer_board_hidden[row][col] = 'O'
                self.computer_board[row][col] = 'O'
                self.status_label.config(text="Промах! Ход компьютера.")
                self.player_turn = False
                self.root.after(1000, self.computer_shot)

            self.draw_boards()

    def computer_shot(self):
        """Ход компьютера"""
        while True:
            row = random.randint(0, self.board_size - 1)
            col = random.randint(0, self.board_size - 1)

            if self.player_board[row][col] not in ['X', 'O']:
                break

        if self.player_board[row][col] == 'S':
            self.player_board[row][col] = 'X'
            if self.check_ship_sunk(self.player_board, row, col):
                self.status_label.config(text="Компьютер потопил ваш корабль! Ваш ход.")
            else:
                self.status_label.config(text="Компьютер попал! Ваш ход.")

            if self.check_win(self.player_board):
                messagebox.showinfo("Поражение", f"Компьютер выиграл! Его стратегия: {self.computer_strategy}")
                self.game_started = False
            else:
                self.root.after(1000, self.computer_shot)
        else:
            self.player_board[row][col] = 'O'
            self.status_label.config(text="Компьютер промахнулся! Ваш ход.")
            self.player_turn = True

        self.draw_boards()

    def check_ship_sunk(self, board, row, col):
        """Проверка, потоплен ли корабль"""
        ship_cells = []
        visited = set()

        def find_ship_cells(r, c):
            if (r, c) in visited or r < 0 or r >= self.board_size or c < 0 or c >= self.board_size:
                return
            visited.add((r, c))
            if board[r][c] == 'S' or board[r][c] == 'X':
                ship_cells.append((r, c))
                for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    find_ship_cells(r + dr, c + dc)

        find_ship_cells(row, col)
        return all(board[r][c] == 'X' for r, c in ship_cells)

    def check_win(self, board):
        """Проверка победы"""
        for row in range(self.board_size):
            for col in range(self.board_size):
                if board[row][col] == 'S':
                    return False
        return True

    def restart_game(self):
        """Перезапуск игры"""
        self.player_board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.computer_board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.computer_board_hidden = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.game_started = False
        self.player_turn = True
        self.show_computer_ships = False
        self.toggle_ships_button.config(text="Показать корабли противника")

        self.place_computer_ships()
        self.status_label.config(text="Выберите стратегию и расставьте корабли")
        self.draw_boards()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    game = BattleshipGame()
    game.run()