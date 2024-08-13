import numpy as np
import tkinter as tk
from tkinter import messagebox
import random

# Constants
ROWS = 6
COLUMNS = 7
EMPTY = 0
PLAYER_1 = 1
PLAYER_2 = 2
PLAYERS = [PLAYER_1, PLAYER_2]
COLORS = ["", "red", "yellow"]  # Player 1 is red, Player 2 is yellow
class FourInARow:
    def __init__(self):
        self.board = self.create_board()
        self.turn = 0
        self.vs_computer = False
        self.winning_coords = []  # Initialize winning coordinates
        self.window = tk.Tk()
        self.window.title("4-in-a-Row Game")
        self.buttons = []
        self.show_menu()
        self.window.mainloop()

    def show_menu(self):
        menu_frame = tk.Frame(self.window, bg="lightblue")
        menu_frame.pack(pady=100)

        title = tk.Label(menu_frame, text="4-in-a-Row Game", font=("Helvetica", 24, "bold"), bg="lightblue", fg="black")
        title.pack(pady=20)

        play_computer_button = tk.Button(menu_frame, text="Play vs Computer", font=("Helvetica", 16), bg="skyblue", fg="black",
                                         activebackground="blue", activeforeground="white",
                                         command=lambda: self.start_game(vs_computer=True))
        play_computer_button.pack(pady=10)

        play_friend_button = tk.Button(menu_frame, text="Play vs Friend", font=("Helvetica", 16), bg="skyblue", fg="black",
                                       activebackground="blue", activeforeground="white",
                                       command=lambda: self.start_game(vs_computer=False))
        play_friend_button.pack(pady=10)

    def start_game(self, vs_computer):
        self.vs_computer = vs_computer
        for widget in self.window.winfo_children():
            widget.destroy()
        self.board = self.create_board()
        self.turn = 0
        self.create_buttons()
        self.canvas = tk.Canvas(self.window, width=COLUMNS*100, height=ROWS*100)
        self.canvas.pack()
        self.draw_board()

    def create_board(self):
        return np.zeros((ROWS, COLUMNS), dtype=int)

    def create_buttons(self):
        frame = tk.Frame(self.window, bg="lightblue")
        frame.pack()
        for col in range(COLUMNS):
            button = tk.Button(frame, text="↓", font=("Helvetica", 16, "bold"), bg="skyblue", fg="black",
                               activebackground="blue", activeforeground="white",
                               command=lambda c=col: self.drop_disc(c))
            button.grid(row=0, column=col, padx=5, pady=5)
            self.buttons.append(button)

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(ROWS):
            for c in range(COLUMNS):
                color = COLORS[int(self.board[r][c])]
                oval = self.canvas.create_oval(c*100, r*100, c*100+100, r*100+100, fill=color, outline="black")
                # Draw winning discs with a thicker border
                if (c, r) in self.winning_coords:
                    self.canvas.itemconfig(oval, outline="green", width=4)
        # Draw the grid lines
        for c in range(COLUMNS):
            self.canvas.create_line(c*100, 0, c*100, ROWS*100, fill="black", width=2)
        for r in range(ROWS):
            self.canvas.create_line(0, r*100, COLUMNS*100, r*100, fill="black", width=2)

        # Draw the winning line if there's a winner
        if self.winning_coords:
            self.draw_winning_line()

    def draw_winning_line(self):
        if len(self.winning_coords) >= 4:
            (x1, y1), (x2, y2) = self.winning_coords[0], self.winning_coords[-1]
            self.canvas.create_line(x1*100 + 50, y1*100 + 50, x2*100 + 50, y2*100 + 50, fill="green", width=4)

    def drop_disc(self, col):
        if self.is_valid_location(col):
            row = self.get_next_open_row(col)
            self.board[row][col] = PLAYERS[self.turn % 2]
            self.draw_board()

            if self.winning_move(PLAYERS[self.turn % 2]):
                # Draw winning line and highlight winning discs before showing the message
                self.draw_board()
                self.window.after(500, self.show_winner_message, PLAYERS[self.turn % 2])
            elif np.all(self.board != EMPTY):
                self.window.after(500, self.show_draw_message)
            else:
                self.turn += 1
                if self.vs_computer and self.turn % 2 == 1:
                    self.computer_move()

    def show_winner_message(self, player):
        messagebox.showinfo("Game Over", f"Player {PLAYERS.index(player) + 1} ({COLORS[player]}) wins!")
        self.reset_game()

    def show_draw_message(self):
        messagebox.showinfo("Game Over", "It's a draw!")
        self.reset_game()

    def computer_move(self):
        available_columns = [c for c in range(COLUMNS) if self.is_valid_location(c)]
        col = random.choice(available_columns)
        self.drop_disc(col)

    def is_valid_location(self, col):
        return self.board[0][col] == EMPTY

    def get_next_open_row(self, col):
        for r in range(ROWS-1, -1, -1):
            if self.board[r][col] == EMPTY:
                return r

    def winning_move(self, player):
        self.winning_coords = []  # Reset the list of winning coordinates
        # Check horizontal locations for win
        for c in range(COLUMNS-3):
            for r in range(ROWS):
                if self.board[r][c] == player and self.board[r][c+1] == player and self.board[r][c+2] == player and self.board[r][c+3] == player:
                    self.winning_coords = [(c+i, r) for i in range(4)]
                    return True

        # Check vertical locations for win
        for c in range(COLUMNS):
            for r in range(ROWS-3):
                if self.board[r][c] == player and self.board[r+1][c] == player and self.board[r+2][c] == player and self.board[r+3][c] == player:
                    self.winning_coords = [(c, r+i) for i in range(4)]
                    return True

        # Check positively sloped diagonals for win
        for c in range(COLUMNS-3):
            for r in range(ROWS-3):
                if self.board[r][c] == player and self.board[r+1][c+1] == player and self.board[r+2][c+2] == player and self.board[r+3][c+3] == player:
                    self.winning_coords = [(c+i, r+i) for i in range(4)]
                    return True

        # Check negatively sloped diagonals for win
        for c in range(COLUMNS-3):
            for r in range(3, ROWS):
                if self.board[r][c] == player and self.board[r-1][c+1] == player and self.board[r-2][c+2] == player and self.board[r-3][c+3] == player:
                    self.winning_coords = [(c+i, r-i) for i in range(4)]
                    return True

        return False

    def reset_game(self):
        self.board = self.create_board()
        self.turn = 0
        self.winning_coords = []  # Clear winning coordinates
        self.draw_board()

if __name__ == "__main__":
    FourInARow()
