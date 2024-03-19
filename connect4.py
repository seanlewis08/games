import tkinter as tk
from tkinter import messagebox, simpledialog, colorchooser
import numpy as np

class Connect4:
    def __init__(self, root):
        self.ROWS = 6
        self.COLS = 7
        self.CELL_SIZE = 100
        self.board = np.zeros((self.ROWS, self.COLS), int)
        self.selected_col = 0
        self.turn = 0
        self.root = root
        self.canvas_width = self.COLS * self.CELL_SIZE + 200
        self.canvas_height = self.ROWS * self.CELL_SIZE
        self.label_offset = 20
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height + self.label_offset, bg="blue")
        self.canvas.pack()

        self.player_names = ["Placeholder 1","Player 1", "Player 2", "Placeholder 2"]
        self.player_colors = ["black","red", "yellow", "black"]
        self.player_names[0] = "Player 1:"
        self.player_names[1] = simpledialog.askstring("Player 1", "Enter name for Player 1:", parent=root) or "Player 1"
        self.player_names[2] = "Player 2:"
        self.player_names[3] = simpledialog.askstring("Player 2", "Enter name for Player 2:", parent=root) or "Player 2"
        self.player_colors[0] = "white"
        self.player_colors[1] = colorchooser.askcolor(title="Choose color for Player 1")[1] or "red"
        self.player_colors[2] = "white"
        self.player_colors[3] = colorchooser.askcolor(title="Choose color for Player 2")[1] or "yellow"

        self.winning_sequence = []

        self.draw_board()
        self.root.bind("<KeyPress-Left>", self.on_key_press)
        self.root.bind("<KeyPress-Right>", self.on_key_press)
        self.root.bind("<KeyPress-Return>", self.on_key_press)
        self.root.bind("<KeyPress-space>", self.on_key_press)
        self.new_game_button = tk.Button(root, text="New Game", command=self.initialize_board)
        self.new_game_button.pack()

    def initialize_board(self):
        self.board = np.zeros((self.ROWS, self.COLS), int)
        self.turn = 0
        self.selected_col = 0
        self.winning_sequence = []  # Clear the winning sequence
        self.draw_board()

    def is_valid_location(self, col):
        return self.board[self.ROWS - 1, col] == 0

    def get_next_open_row(self, col):
        for r in range(self.ROWS):
            if self.board[r, col] == 0:
                return r
        return None

    def drop_piece(self, row, col, piece):
        self.board[row, col] = piece

    def check_win(self, piece):
        # Check horizontal locations
        for c in range(self.COLS - 3):
            for r in range(self.ROWS):
                if self.board[r][c] == piece and self.board[r][c + 1] == piece and \
                        self.board[r][c + 2] == piece and self.board[r][c + 3] == piece:
                    self.winning_sequence = [(r, c), (r, c + 1), (r, c + 2), (r, c + 3)]
                    return True
        # Check vertical locations
        for c in range(self.COLS):
            for r in range(self.ROWS - 3):
                if self.board[r][c] == piece and self.board[r + 1][c] == piece and \
                        self.board[r + 2][c] == piece and self.board[r + 3][c] == piece:
                    self.winning_sequence = [(r, c), (r + 1, c), (r + 2, c), (r + 3, c)]
                    return True
        # Check positively sloped diagonals
        for c in range(self.COLS - 3):
            for r in range(self.ROWS - 3):
                if self.board[r][c] == piece and self.board[r + 1][c + 1] == piece and \
                        self.board[r + 2][c + 2] == piece and self.board[r + 3][c + 3] == piece:
                    self.winning_sequence = [(r, c), (r + 1, c + 1), (r + 2, c + 2), (r + 3, c + 3)]
                    return True
        # Check negatively sloped diagonals
        for c in range(self.COLS - 3):
            for r in range(3, self.ROWS):
                if self.board[r][c] == piece and self.board[r - 1][c + 1] == piece and \
                        self.board[r - 2][c + 2] == piece and self.board[r - 3][c + 3] == piece:
                    self.winning_sequence = [(r, c), (r - 1, c + 1), (r - 2, c + 2), (r - 3, c + 3)]
                    return True
        return False

    def draw_board(self):
        self.canvas.create_text(100, 100, text="Test", font=("Arial", 24, "bold"), fill="red")
        self.canvas.delete("all")
        for row in range(self.ROWS):
            for col in range(self.COLS):
                x0 = col * self.CELL_SIZE + 10
                y0 = (self.ROWS - 1 - row) * self.CELL_SIZE + 10
                x1 = (col + 1) * self.CELL_SIZE - 10
                y1 = (self.ROWS - row) * self.CELL_SIZE - 10
                fill_color = "white"
                if (row, col) in self.winning_sequence:
                    # Determine the player's color for the winning sequence
                    player_color_index = 3 if self.board[row, col] == 2 else 1
                    winning_color = self.player_colors[player_color_index]

                    four = self.get_complementary_color(winning_color)
                    # Calculate the center of the cell to place the "4"
                    cx = (x0 + x1) / 2
                    cy = (y0 + y1) / 2
                    self.canvas.create_oval(x0, y0, x1, y1, fill=winning_color, tags=f"cell_{row}_{col}")
                    self.canvas.create_text(cx, cy, text="4", font=("Arial", 16, "bold"), fill=four)

                else:
                    if self.board[row, col] == 1:
                        fill_color = self.player_colors[1]
                    elif self.board[row, col] == 2:
                        fill_color = self.player_colors[3]
                    self.canvas.create_oval(x0, y0, x1, y1, fill=fill_color, tags=f"cell_{row}_{col}")

        self.draw_selector()

        # Drawing the player names and their colors
        name_display_offset_x = self.COLS * self.CELL_SIZE + 10
        name_display_offset_y = 50
        name_gap = 30
        for i, name in enumerate(self.player_names):
            self.canvas.create_text(name_display_offset_x, name_display_offset_y + i * name_gap,
                                    text=f"{name}", anchor="w",
                                    fill=self.player_colors[i], font=("Arial", 16))



    def get_complementary_color(self, hex_color):
        # Convert hex to RGB
        rgb_color = [int(hex_color[i:i+2], 16) for i in (1, 3, 5)]  # Skip the '#' symbol
        # Calculate complementary color
        comp_color = [255 - c for c in rgb_color]
        # Convert back to hex
        hex_comp_color = '#' + ''.join(['{:02x}'.format(c) for c in comp_color])

        return hex_comp_color

    def draw_selector(self):
        self.canvas.delete("selector")
        x0 = self.selected_col * self.CELL_SIZE
        y0 = 0
        x1 = (self.selected_col + 1) * self.CELL_SIZE
        y1 = self.ROWS * self.CELL_SIZE
        outline = self.get_complementary_color("#0000FF")
        self.canvas.create_rectangle(x0, y0, x1, y1, outline=outline, width=4, tags="selector")

    def on_key_press(self, event):
        if event.keysym == "Left":
            self.selected_col = max(0, self.selected_col - 1)
        elif event.keysym == "Right":
            self.selected_col = min(self.COLS - 1, self.selected_col + 1)
        elif event.keysym in ("Return", "space"):
            if self.is_valid_location(self.selected_col):
                row = self.get_next_open_row(self.selected_col)
                if row is not None:
                    self.drop_piece(row, self.selected_col, 1 if self.turn == 0 else 2)
                    if self.check_win(1 if self.turn == 0 else 2):
                        messagebox.showinfo("Game Over", f"{self.player_names[self.turn]} wins!")
                        self.draw_board()  # Commented out to stop automatic reset
                        return
                    self.turn = (self.turn + 1) % 2
        self.draw_board()


def main():
    root = tk.Tk()
    root.title("Connect 4")
    game = Connect4(root)
    root.mainloop()

if __name__ == "__main__":
    main()
