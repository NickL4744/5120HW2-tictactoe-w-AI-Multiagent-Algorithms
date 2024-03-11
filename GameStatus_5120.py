# -*- coding: utf-8 -*-


class GameStatus:

    def __init__(self, board_state, turn_O):
        self.board_state = board_state
        self.turn_O = turn_O
        self.oldScores = 0
        self.completed_sets = []
        self.score = 0
        self.button_position_list = []
        self.board_values = []
        self.winner = ""

        for row in range(len(self.board_state)):
            for col in range(len(self.board_state)):
                button_position = [row, col]
                self.button_position_list.append(button_position)

        for row in self.board_state:
            for col in row:
                self.board_values.append(col)

    def is_terminal(self):

        for row in self.board_state:
            for col in row:
                if col == 0:
                    return False
        return True

    def get_scores(self):
        for row in range(len(self.board_state)):
            for col in range(len(self.board_state)):
                # There are 8 directions you could go in to find a set
                # The direction starts north and goes clockwise for each direction iteration
                direction_logic = [[[row + 1, col], [row + 2, col]], [[row + 1, col + 1], [row + 2, col + 2]],
                                   [[row, col + 1], [row, col + 2]], [[row - 1, col + 1], [row - 2, col + 2]],
                                   [[row - 1, col], [row - 2, col]], [[row - 1, col - 1], [row - 2, col - 2]],
                                   [[row, col - 1], [row, col - 2]], [[row + 1, col - 1], [row + 2, col - 2]]]
                for direction in direction_logic:
                    try:
                        temp_value_1 = self.button_position_list.index([row, col])
                        temp_value_2 = self.button_position_list.index(direction[0])
                        temp_value_3 = self.button_position_list.index(direction[1])
                        temp_set = [temp_value_1, temp_value_2, temp_value_3]
                        inverted_temp_set = [temp_value_3, temp_value_2, temp_value_1]
                        if self.board_values[temp_value_1] \
                                == self.board_values[temp_value_2] \
                                == self.board_values[temp_value_3] == 1 and temp_set not in self.completed_sets:
                            self.score += 1
                            self.completed_sets.append(temp_set)
                            self.completed_sets.append(inverted_temp_set)
                        elif self.board_values[temp_value_1] \
                                == self.board_values[temp_value_2] \
                                == self.board_values[temp_value_3] == -1 and temp_set not in self.completed_sets:
                            self.score -= 1
                            self.completed_sets.append(temp_set)
                            self.completed_sets.append(inverted_temp_set)
                    except:
                        pass
        return self.score

    def get_negamax_scores(self):
        for row in range(len(self.board_state)):
            for col in range(len(self.board_state)):
                # There are 8 directions you could go in to find a set
                # The direction starts north and goes clockwise for each direction iteration
                direction_logic = [[[row + 1, col], [row + 2, col]], [[row + 1, col + 1], [row + 2, col + 2]],
                                   [[row, col + 1], [row, col + 2]], [[row - 1, col + 1], [row - 2, col + 2]],
                                   [[row - 1, col], [row - 2, col]], [[row - 1, col - 1], [row - 2, col - 2]],
                                   [[row, col - 1], [row, col - 2]], [[row + 1, col - 1], [row + 2, col - 2]]]
                for direction in direction_logic:
                    try:
                        temp_value_1 = self.button_position_list.index([row, col])
                        temp_value_2 = self.button_position_list.index(direction[0])
                        temp_value_3 = self.button_position_list.index(direction[1])
                        temp_set = [temp_value_1, temp_value_2, temp_value_3]
                        inverted_temp_set = [temp_value_3, temp_value_2, temp_value_1]
                        if self.board_values[temp_value_1] \
                                == self.board_values[temp_value_2] \
                                == self.board_values[temp_value_3] == 1 and temp_set not in self.completed_sets:
                            self.score += 1
                            print(self.score)
                            self.completed_sets.append(temp_set)
                            self.completed_sets.append(inverted_temp_set)
                        elif self.board_values[temp_value_1] \
                                == self.board_values[temp_value_2] \
                                == self.board_values[temp_value_3] == -1 and temp_set not in self.completed_sets:
                            self.score -= 1
                            print(self.score)
                            self.completed_sets.append(temp_set)
                            self.completed_sets.append(inverted_temp_set)
                    except:
                        pass
        return self.score

    def get_moves(self):
        moves = []
        row = -1
        for row_set in self.board_state:
            row += 1
            col = -1
            for col_val in row_set:
                col += 1
                if col_val == 0:
                    moves.append([row, col])

        return moves

    def get_new_state(self, move):

        total_temp_set = []
        for i in range(len(self.board_state)):
            temp_set = []
            for j in range(len(self.board_state)):
                temp = self.board_state[i][j]
                temp_set.append(temp)
            total_temp_set.append(temp_set)
        new_board_state = total_temp_set
        x, y = move[0], move[1]
        if self.turn_O:
            new_board_state[x][y] = 1
        else:
            new_board_state[x][y] = -1
        return GameStatus(new_board_state, not self.turn_O)

    def determine_winner(self):
        final_score = self.get_scores()
        if final_score > 0:
            message = f"'X' wins! Score: {final_score}"
        elif final_score < 0:
            message = f"'O' wins! Score: {final_score}"
        else:
            message = "Draw! Score: 0"
        return message
