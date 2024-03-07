import tkinter as tk
from tkinter import messagebox


class TicTacToe:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.buttons = []
        self.button_position_list = []
        self.current_player = "X"
        self.game_score = 0  # 0 means draw, > 0 means player won, < 0 means computer won
        self.game_size = 3  # Hardcoded NxN game size that the user can change with buttons most likely
        self.board = [""] * (self.game_size ** 2)
        self.completed_sets = []

        for row in range(self.game_size):
            for col in range(self.game_size):
                button_position = [row, col]
                self.button_position_list.append(button_position)
                button = tk.Button(self.root, text="", font=("Helvetica", 24), height=2, width=5,
                                   command=lambda button_position=button_position: self.clicked(button_position))
                button.grid(row=row, column=col)
                self.buttons.append(button)

        # Add a Reset button
        reset_button = tk.Button(self.root, text="Reset", command=self.reset_game, bg="orange", fg="black")
        reset_button.grid(row=4, column=0, padx=10, pady=10)

        # Add an Exit button
        exit_button = tk.Button(self.root, text="Exit", command=self.exit_game, bg="orange", fg="black")
        exit_button.grid(row=4, column=1, padx=10, pady=10)

        # Add a turn label
        self.turn_label = tk.Label(self.root, text=f"Turn: {self.current_player}", font=("Helvetica", 12))
        self.turn_label.grid(row=5, columnspan=4)

        # Initialize the timer
        self.timer_time = 0
        self.timer_label = tk.Label(self.root, text="Time: 0 seconds", font=("Helvetica", 12))
        self.timer_label.grid(row=6, columnspan=4)

        # Start the timer
        self.update_timer()

    def clicked(self, button_position):
        board_position = self.button_position_list.index(button_position)
        if self.board[board_position] == "":
            self.board[board_position] = self.current_player
            self.buttons[board_position].config(text=self.current_player)
            self.current_player = "O" if self.current_player == "X" else "X"
            self.turn_label.config(text=f"Turn: {self.current_player}")
            self.check_for_sets()

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
                            self.game_score += 1
                            self.completed_sets.append(temp_set)
                            self.completed_sets.append(inverted_temp_set)
                            print("game score incremented")
                        elif self.board[temp_position_1] \
                                == self.board[temp_position_2] \
                                == self.board[temp_position_3] == "O" and temp_set not in self.completed_sets:
                            self.game_score -= 1
                            self.completed_sets.append(temp_set)
                            self.completed_sets.append(inverted_temp_set)
                            print("game score decremented")
                    except:
                        pass

    def reset_game(self):
        # Clear the board and reset the game
        for button in self.buttons:
            button.config(text="")
        self.board = [""] * 16
        self.current_player = "X"
        self.turn_label.config(text=f"Turn: {self.current_player}")
        self.timer_time = 0
        self.print_game_results()
        self.game_score = 0

    def exit_game(self):
        self.print_game_results()
        self.root.destroy()

    def update_timer(self):
        self.timer_time += 1
        self.timer_label.config(text=f"Time: {self.timer_time} seconds")
        self.root.after(1000, self.update_timer)  # Update every 1000ms (1 second)

    def print_game_results(self):
        if self.game_score > 0:
            print(f"The player has won with a score of {self.game_score}")
        elif self.game_score < 0:
            print(f"The player has lost with a score of {self.game_score}")
        else:
            print(f"The game is a draw with a score of {self.game_score}")
            
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    game = TicTacToe()
    game.run()
