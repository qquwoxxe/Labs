import tkinter as tk
from tkinter import messagebox


class CheckerPiece:
    def __init__(self, is_white):
        self.is_white = is_white
        self.is_king = False


class Board:
    SIZE = 8

    def __init__(self):
        self.grid = [[None] * self.SIZE for _ in range(self.SIZE)]
        for row in range(self.SIZE):
            for col in range(self.SIZE):
                if (row + col) % 2 == 1:
                    if row == 2 and col != 7:  # убираем крайнюю правую шашку (col=7)
                        self.grid[row][col] = CheckerPiece(True)
                    elif row > 4:
                        self.grid[row][col] = CheckerPiece(False)

    def get_piece(self, row, col):
        return self.grid[row][col] if 0 <= row < self.SIZE and 0 <= col < self.SIZE else None

    def move_piece(self, start, end, captures):
        sr, sc = start;
        er, ec = end
        piece = self.grid[sr][sc]
        self.grid[sr][sc] = None
        self.grid[er][ec] = piece
        for cr, cc in captures: self.grid[cr][cc] = None
        if not piece.is_white and er == 0: piece.is_king = True


class Game:
    def __init__(self):
        self.board = Board()
        self.selected = None
        self.possible_moves = []

    def select_piece(self, row, col):
        piece = self.board.get_piece(row, col)
        if not piece or piece.is_white: return False
        self.selected = (row, col)
        self.possible_moves = self.get_moves(row, col)
        return bool(self.possible_moves)

    def get_moves(self, row, col):
        piece = self.board.get_piece(row, col)
        if not piece: return []
        captures = self.get_captures(row, col)
        if captures: return captures
        moves = []
        dirs = [(-1, -1), (-1, 1)] if not piece.is_king else [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in dirs:
            nr, nc = row + dr, col + dc
            if self.is_valid(nr, nc) and not self.board.get_piece(nr, nc):
                moves.append((nr, nc, []))
        return moves

    def get_captures(self, row, col, caps=None):
        if caps is None: caps = set()
        piece = self.board.get_piece(row, col)
        if not piece: return []
        captures = []
        dirs = [(-1, -1), (-1, 1)] if not piece.is_king else [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in dirs:
            er, ec = row + dr, col + dc
            jr, jc = row + 2 * dr, col + 2 * dc
            if not self.is_valid(jr, jc): continue
            enemy = self.board.get_piece(er, ec)
            land = self.board.get_piece(jr, jc)
            if enemy and enemy.is_white and not land and (er, ec) not in caps:
                new_caps = caps | {(er, ec)}
                further = self.get_captures(jr, jc, new_caps)
                if further:
                    captures.extend(further)
                else:
                    captures.append((jr, jc, list(new_caps)))
        return captures

    def is_valid(self, row, col):
        return 0 <= row < Board.SIZE and 0 <= col < Board.SIZE

    def make_move(self, end_row, end_col):
        if not self.selected: return False, "Выберите шашку"
        for move in self.possible_moves:
            if move[0] == end_row and move[1] == end_col:
                self.board.move_piece(self.selected, (move[0], move[1]), move[2])
                self.selected = None;
                self.possible_moves = []
                if self.check_win(): return True, "Победа!"
                return True, "Ход выполнен"
        return False, "Неверный ход"

    def check_win(self):
        for row in range(Board.SIZE):
            for col in range(Board.SIZE):
                if self.board.get_piece(row, col) and self.board.get_piece(row, col).is_white:
                    return False
        return True


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Английские шашки - Поддавки")
        self.game = Game()
        self.cell_size = 60
        self.setup_ui()
        self.draw_board()

    def setup_ui(self):
        self.canvas = tk.Canvas(self.root, width=Board.SIZE * self.cell_size, height=Board.SIZE * self.cell_size)
        self.canvas.pack(padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.on_click)
        tk.Button(self.root, text="Новая игра", command=self.new_game).pack(pady=5)

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(Board.SIZE):
            for col in range(Board.SIZE):
                x1 = col * self.cell_size;
                y1 = row * self.cell_size
                color = '#eeeed2' if (row + col) % 2 == 0 else '#769656'
                self.canvas.create_rectangle(x1, y1, x1 + self.cell_size, y1 + self.cell_size, fill=color, outline="")

        if self.game.selected:
            r, c = self.game.selected
            self.highlight_cell(r, c, '#b5c7e0')
            for move in self.game.possible_moves:
                self.highlight_cell(move[0], move[1], '#ff9999' if move[2] else '#a8d8a8')

        for row in range(Board.SIZE):
            for col in range(Board.SIZE):
                piece = self.game.board.get_piece(row, col)
                if piece: self.draw_piece(row, col, piece)

    def draw_piece(self, row, col, piece):
        x = col * self.cell_size + self.cell_size // 2
        y = row * self.cell_size + self.cell_size // 2
        r = self.cell_size // 2 - 5
        color = 'white' if piece.is_white else 'black'
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline='black', width=2)
        if piece.is_king:
            cr = r // 2
            self.canvas.create_oval(x - cr, y - cr, x + cr, y + cr, fill='gold' if piece.is_white else 'yellow',
                                    outline='black', width=1)

    def highlight_cell(self, row, col, color):
        x1 = col * self.cell_size;
        y1 = row * self.cell_size
        self.canvas.create_rectangle(x1, y1, x1 + self.cell_size, y1 + self.cell_size, fill=color, outline="")

    def on_click(self, event):
        col = event.x // self.cell_size;
        row = event.y // self.cell_size
        if self.game.selected:
            success, msg = self.game.make_move(row, col)
            if success:
                self.draw_board()
                if "Победа" in msg: messagebox.showinfo("Победа!", msg)
            else:
                if not self.game.select_piece(row, col):
                    self.game.selected = None
                    self.draw_board()
        else:
            self.game.select_piece(row, col)
            self.draw_board()

    def new_game(self):
        self.game = Game()
        self.draw_board()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    GUI().run()