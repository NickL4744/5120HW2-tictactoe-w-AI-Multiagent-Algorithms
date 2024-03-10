import tkinter as tk
import numpy as np
from GameStatus_5120 import GameStatus
from multiAgents import minimax, negamax

class TicTacToe:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.buttons = []
        self.button_position_list = []
        self.current_player = "X"
        self.game_score = 0  # 0 means draw, > 0 means player won, < 0 means computer won
        self.game_size = 3  # Initial grid size is 3x3
        self.board = [""] * (self.game_size ** 2)
        self.completed_sets = []
        self.player_wins = {"X": 0, "O": 0}
        self.game_status = GameStatus(np.zeros((self.game_size, self.game_size), dtype=int), True)
        self.game_mode = "Human vs Human"
        # Add a Reset button
        reset_button = tk.Button(self.root, text="Reset", command=self.reset_game, bg="orange", fg="black")
        reset_button.grid(row=0, column=0, padx=10, pady=10)
        # Add an Exit button
        exit_button = tk.Button(self.root, text="Exit", command=self.exit_game, bg="orange", fg="black")
        exit_button.grid(row=0, column=1, padx=10, pady=10)
        # Add labels for player wins
        self.player_x_label = tk.Label(self.root, text=f"Player X Wins: {self.player_wins['X']}", font=("Helvetica", 12))
        self.player_x_label.grid(row=0, column=2, padx=10, pady=10)
        self.player_o_label = tk.Label(self.root, text=f"Player O Wins: {self.player_wins['O']}", font=("Helvetica", 12))
        self.player_o_label.grid(row=0, column=3, padx=10, pady=10)
        # Add a turn label
        self.turn_label = tk.Label(self.root, text=f"Turn: {self.current_player}", font=("Helvetica", 12))
        self.turn_label.grid(row=0, column=4, padx=10, pady=10)
        human_vs_human_button = tk.Button(self.root, text="Human vs Human", command=self.set_human_vs_human, bg="orange", fg="black")
        human_vs_human_button.grid(row=1, column=0, padx=10, pady=10)
        human_vs_computer_button = tk.Button(self.root, text="Human vs Computer", command=self.set_human_vs_computer, bg="orange", fg="black")
        human_vs_computer_button.grid(row=1, column=2, padx=10, pady=10)
        self.create_board()
        # Add a menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        # Add a menu for grid size selection
        grid_menu = tk.Menu(menubar, tearoff=0)
        grid_menu.add_command(label="3x3", command=lambda: self.change_grid_size(3))
        grid_menu.add_command(label="4x4", command=lambda: self.change_grid_size(4))
        grid_menu.add_command(label="5x5", command=lambda: self.change_grid_size(5))
        menubar.add_cascade(label="Grid Size", menu=grid_menu)
        # Initialize the timer
        self.timer_time = 0
        self.timer_label = tk.Label(self.root, text="Time: 0 seconds", font=("Helvetica", 12))
        self.timer_label.grid(row=1, column=0, columnspan=self.game_size, padx=10, pady=5)
        # Start the timer
        self.update_timer()
        
    def set_human_vs_human(self):
        # Change the game mode to "Human vs Human"
        self.game_mode = "Human vs Human"
        self.reset_game()
        
    def set_human_vs_computer(self):
        # Change the game mode to "Human vs Computer"
        self.game_mode = "Human vs Computer"
        self.reset_game()
        if self.current_player == "O":
            self.make_computer_move()

    def make_computer_move(self):
        if self.game_mode == "Human vs Computer":
            # Implement the logic for the computer's move using the minimax algorithm
            best_move = self.minimax(self.board, "O")  # Assuming "O" is the computer's symbol
            self.update_board(best_move)
            self.check_for_sets()
            if self.is_board_full():
                self.reset_game()
            else:
                self.current_player = "X"
                self.turn_label.config(text=f"Turn: {self.current_player}")

    def make_human_move(self, button_position):
        board_position = self.button_position_list.index(button_position)
        if self.board[board_position] == "":
            self.board[board_position] = self.current_player
            self.buttons[board_position].config(text=self.current_player)
            self.check_for_sets()
            if self.is_board_full():
                self.reset_game()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.turn_label.config(text=f"Turn: {self.current_player}")
                if self.game_mode == "Human vs Computer":
                    self.make_computer_move()

    def create_board(self):
        for row in range(self.game_size):
            for col in range(self.game_size):
                button_position = [row, col]
                self.button_position_list.append(button_position)
                button = tk.Button(self.root, text="", font=("Helvetica", 24), height=2, width=5,
                                   command=lambda button_position=button_position: self.clicked(button_position))
                button.grid(row=row + 2, column=col, padx=5, pady=5, sticky="nswe")
                self.buttons.append(button)
        # Configure row and column properties to make buttons resize properly
        for i in range(self.game_size):
            self.root.grid_rowconfigure(i + 2, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

    def change_grid_size(self, size):
        self.game_size = size
        for button in self.buttons:
            button.destroy()
        self.buttons.clear()
        self.button_position_list.clear()
        self.board = [""] * (self.game_size ** 2)
        self.create_board()

    def clicked(self, button_position):
        if self.game_mode == "Human vs Human":
            self.make_human_move(button_position)
        elif self.current_player == "X":  # Only allow human move when it's X's turn in Human vs Computer mode
            self.make_human_move(button_position)

    def check_for_sets(self):
        for row in range(self.game_size):
            for col in range(self.game_size):
                # There are 8 directions you could go in to find a set
                # The direction starts north and goes clockwise for each direction iteration
                direction_logic = [[[row + 1, col], [row + 2, col]], [[row + 1, col + 1], [row + 2, col + 2]],
                                   [[row, col + 1], [row, col + 2]], [[row - 1, col + 1], [row - 2, col + 2]],
                                   [[row - 1, col], [row - 2, col]], [[row - 1, col - 1], [row - 2, col - 2]],
                                   [[row, col - 1], [row, col - 2]], [[row + 1, col - 1], [row + 2, col - 2]]]
                for direction in range(8):
                    try:
                        temp_position_1 = self.button_position_list.index([row, col])
                        temp_position_2 = self.button_position_list.index(direction_logic[direction][0])
                        temp_position_3 = self.button_position_list.index(direction_logic[direction][1])
                        temp_set = [temp_position_1, temp_position_2, temp_position_3]
                        inverted_temp_set = [temp_position_3, temp_position_2, temp_position_1]
                        if self.board[temp_position_1] \
                                == self.board[temp_position_2] \
                                == self.board[temp_position_3] == "X" and temp_set not in self.completed_sets:
                            self.player_wins["X"] += 1
                            self.highlight_winning_set(temp_set, "X")
                            self.completed_sets.append(temp_set)
                            self.completed_sets.append(inverted_temp_set)
                        elif self.board[temp_position_1] \
                                == self.board[temp_position_2] \
                                == self.board[temp_position_3] == "O" and temp_set not in self.completed_sets:
                            self.player_wins["O"] += 1
                            self.highlight_winning_set(temp_set, "O")
                            self.completed_sets.append(temp_set)
                            self.completed_sets.append(inverted_temp_set)
                    except:
                        pass

    def highlight_winning_set(self, winning_set, player):
        for position in winning_set:
            self.buttons[position].config(bg="green", text=player)

    def reset_game(self):
        # Clear the board and reset the game
        for button in self.buttons:
            button.config(text="")
            button.config(bg="white smoke")
        self.board = [""] * (self.game_size ** 2)
        self.current_player = "X"
        self.turn_label.config(text=f"Turn: {self.current_player}")
        self.timer_time = 0
        self.update_win_labels()
        self.completed_sets = []

    def exit_game(self):
        self.root.destroy()

    def update_timer(self):
        self.timer_time += 1
        self.timer_label.config(text=f"Time: {self.timer_time} seconds")
        self.root.after(1000, self.update_timer)  # Update every 1000ms (1 second)

    def update_win_labels(self):
        self.player_x_label.config(text=f"Player X Wins: {self.player_wins['X']}")
        self.player_o_label.config(text=f"Player O Wins: {self.player_wins['O']}")

    def run(self):
        self.root.mainloop()

    def is_board_full(self):
        return "" not in self.board
    
    def update_board(self, move):
        # Update the board with the given move
        row = move // self.game_size
        col = move % self.game_size
        board_position = row * self.game_size + col
        if board_position < len(self.board) and self.board[board_position] == "":
            self.board[board_position] = self.current_player
            self.buttons[board_position].config(text=self.current_player)
            self.current_player = "O" if self.current_player == "X" else "X"
            self.turn_label.config(text=f"Turn: {self.current_player}")
            self.check_for_sets()
            if self.is_board_full():
                self.reset_game()

    def minimax(self, board, player):
        # Convert board to numpy array
        np_board = np.array(board).reshape(self.game_size, self.game_size)

        # Call minimax or negamax algorithm here and return the best move
        # Example: best_move = minimax(np_board, player)
        # Implement the minimax or negamax function in the multiAgents module
        best_move = minimax(board, "O", True)
        
        return best_move

if __name__ == "__main__":
    game = TicTacToe()
    game.run()