import tkinter as tk
from tkinter import messagebox
import random

root = tk.Tk()
root.title("Tic Tac Toe")
root.geometry("400x500")
root.resizable(False, False)

# Game State
current_player = 'X'
game_mode = None
player1_name = "Player 1"
player2_name = "Player 2"
scores = {"X": 0, "O": 0}
buttons = [[None for _ in range(3)] for _ in range(3)]
theme = 'light'

# Theme Colors
themes = {
    'light': {'bg': 'white', 'fg': 'black', 'btn_bg': 'lightgray'},
    'dark': {'bg': '#222222', 'fg': 'white', 'btn_bg': '#444444'}
}

def apply_theme():
    colors = themes[theme]
    root.configure(bg=colors['bg'])
    score_label.configure(bg=colors['bg'], fg=colors['fg'])
    theme_btn.configure(bg=colors['btn_bg'], fg=colors['fg'])
    for row in buttons:
        for btn in row:
            btn.configure(bg=colors['btn_bg'], fg=btn.cget('fg'))

def toggle_theme():
    global theme
    theme = 'dark' if theme == 'light' else 'light'
    apply_theme()

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

def show_mode_selection():
    clear_window()
    tk.Label(root, text="Choose Game Mode", font=('Helvetica', 20)).pack(pady=10)
    tk.Button(root, text="🧑 Play with Friend", font=('Helvetica', 16), command=lambda: get_names('friend')).pack(pady=5)
    tk.Button(root, text="🤖 Play with Robot", font=('Helvetica', 16), command=lambda: get_names('robot')).pack(pady=5)

def get_names(mode):
    global game_mode
    game_mode = mode
    clear_window()

    name_frame = tk.Frame(root)
    name_frame.pack(pady=20)

    tk.Label(name_frame, text="Enter Player Name(s)", font=('Helvetica', 16)).grid(row=0, columnspan=2, pady=10)
    tk.Label(name_frame, text="Player 1 (X):").grid(row=1, column=0)
    entry1 = tk.Entry(name_frame)
    entry1.grid(row=1, column=1)

    if mode == 'friend':
        tk.Label(name_frame, text="Player 2 (O):").grid(row=2, column=0)
        entry2 = tk.Entry(name_frame)
        entry2.grid(row=2, column=1)
    else:
        entry2 = None

    def start():
        global player1_name, player2_name
        player1_name = entry1.get() or "Player 1"
        player2_name = entry2.get() if entry2 else "Robot"
        player2_name = player2_name or "Robot"
        name_frame.destroy()
        start_game()

    tk.Button(name_frame, text="Start Game", font=('Helvetica', 14), command=start).grid(row=3, columnspan=2, pady=10)

def start_game():
    global score_label, theme_btn
    clear_window()

    score_label = tk.Label(root, text="", font=('Helvetica', 14))
    score_label.pack(pady=5)
    update_score_label()

    theme_btn = tk.Button(root, text="Toggle Theme", font=('Helvetica', 12), command=toggle_theme)
    theme_btn.pack(pady=5)

    board_frame = tk.Frame(root)
    board_frame.pack()

    for r in range(3):
        for c in range(3):
            btn = tk.Button(board_frame, text="", font=('Helvetica', 32), width=4, height=2,
                            command=lambda r=r, c=c: on_click(r, c))
            btn.grid(row=r, column=c, padx=5, pady=5)
            buttons[r][c] = btn

    apply_theme()

def on_click(r, c):
    global current_player
    if buttons[r][c]["text"] == "":
        buttons[r][c]["text"] = current_player
        buttons[r][c]["fg"] = "blue" if current_player == 'X' else "green"
        winner = check_winner()
        if winner:
            show_result(winner)
        else:
            current_player = 'O' if current_player == 'X' else 'X'
            if game_mode == 'robot' and current_player == 'O':
                root.after(500, robot_move)

def robot_move():
    empty = [(r, c) for r in range(3) for c in range(3) if buttons[r][c]["text"] == ""]
    if empty:
        r, c = random.choice(empty)
        on_click(r, c)

def check_winner():
    board = [[buttons[r][c]["text"] for c in range(3)] for r in range(3)]
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "":
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]
    if all(cell != "" for row in board for cell in row):
        return "Tie"
    return None

def show_result(winner):
    global scores
    if winner == "Tie":
        messagebox.showinfo("Result", "It's a Tie!")
    else:
        name = player1_name if winner == 'X' else player2_name
        scores[winner] += 1
        messagebox.showinfo("Result", f"🎉 {name} wins!")
    reset_game()

def reset_game():
    global current_player
    current_player = 'X'
    for r in range(3):
        for c in range(3):
            buttons[r][c]["text"] = ""
    update_score_label()

def update_score_label():
    score_label.config(text=f"{player1_name} (X): {scores['X']}   |   {player2_name} (O): {scores['O']}")

show_mode_selection()
root.mainloop()
