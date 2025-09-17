from tkinter import *
import random


def win(n):
    global game
    win_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # горизонтальные
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # вертикальные
        [0, 4, 8], [2, 4, 6]  # диагональные
    ]

    for combo in win_combinations:
        if game[combo[0]] == n and game[combo[1]] == n and game[combo[2]] == n:
            return True
    return False


def is_board_full():
    return len(game_left) == 0


def computer_move():
    global game, game_left, turn

    for move in game_left:
        game[move] = 'O'
        if win('O'):
            game[move] = None
            return move
        game[move] = None

    for move in game_left:
        game[move] = 'X'
        if win('X'):
            game[move] = None
            return move
        game[move] = None

    if 4 in game_left:
        return 4
    corners = [0, 2, 6, 8]
    available_corners = [corner for corner in corners if corner in game_left]
    if available_corners:
        return random.choice(available_corners)


    return random.choice(game_left)


def push(b):
    global game, game_left, turn

    game[b] = 'X'
    buttons[b].config(text='X', state=DISABLED)
    game_left.remove(b)

    if win('X'):
        label.config(text="Вы победили!")
        disable_all_buttons()
        return

    if is_board_full():
        label.config(text="Ничья!")
        return

    root.after(300, make_computer_move)


def make_computer_move():
    global game, game_left, turn

    if not game_left:
        return

    t = computer_move()
    game[t] = 'O'
    buttons[t].config(text='O', state=DISABLED)
    game_left.remove(t)

    if win('O'):
        label.config(text="Вы проиграли!")
        disable_all_buttons()
        return

    if is_board_full():
        label.config(text="Ничья!")
        return

    turn += 1


def disable_all_buttons():
    for button in buttons:
        button.config(state=DISABLED)


game = [None] * 9
game_left = list(range(9))
turn = 0

root = Tk()
root.title("Крестики-нолики")

label = Label(width=20, text="Крестики-нолики", font=('Arial', 20, 'bold'))
buttons = [Button(width=5, height=2, font=('Arial', 28, 'bold'), bg="white", command=lambda x=i: push(x)) for i in range(9)]

label.grid(row=0, column=0, columnspan=3)
row = 1; col = 0
for i in range(9):
    buttons[i].grid(row=row, column=col)
    col += 1
    if col == 3:
        row += 1
        col = 0

root.mainloop()