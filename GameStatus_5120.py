# -*- coding: utf-8 -*-
import numpy as np

class GameStatus:
    def __init__(self, board_state, turn_0):
        # Initialize the game state with the board state and player turn
        self.board_state = board_state
        self.turn_0 = turn_0
        self.oldScores = 0

        self.winner = ""

    def is_terminal(self):
        # if returns true, there is a winner

        # Check rows for a win
        for row in self.board_state:
            if np.all(row == 1) or np.all(row == -1):
                return True

        # Check columns for a win, by using a transpose in numpy (.T)
        for col in self.board_state.T:
            if np.all(col == 1) or np.all(col == -1):
                return True

        # Check the diagonals
        if np.all(np.diag(self.board_state) == 1) or np.all(np.diag(self.board_state) == -1):
            return True
        if np.all(np.diag(np.fliplr(self.board_state)) == 1) or np.all(np.diag(np.fliplr(self.board_state)) == -1):
            return True

        # Check if the board is full
        return np.all(self.board_state != 0)


    def get_scores(self, terminal):
        """
        Calculate the scores. Make sure you add the score for each player by checking 
        each triplet in the board in each direction (horizontal, vertical, and any diagonal direction)
        
        You should then return the calculated score which can be positive (human player wins),
        negative (AI player wins), or 0 (draw)
        
        """    
        rows = len(self.board_state)
        cols = len(self.board_state[0])
        scores = [0, 0]
        check_point = 3 if terminal else 2

        # Check horizontal scores
        for i in range(rows):
            for j in range(cols - 2):
                if self.board_state[i][j] == self.board_state[i][j + 1] == self.board_state[i][j + 2] and self.board_state[i][j] != 0:
                    scores[self.board_state[i][j] // check_point] += self.board_state[i][j]

        # Check vertical scores
        for i in range(rows - 2):
            for j in range(cols):
                if self.board_state[i][j] == self.board_state[i + 1][j] == self.board_state[i + 2][j] and self.board_state[i][j] != 0:
                    scores[self.board_state[i][j] // check_point] += self.board_state[i][j]

        # Check diagonal scores
        for i in range(rows - 2):
            for j in range(cols - 2):
                if self.board_state[i][j] == self.board_state[i + 1][j + 1] == self.board_state[i + 2][j + 2] and self.board_state[i][j] != 0:
                    scores[self.board_state[i][j] // check_point] += self.board_state[i][j]

        # Check anti-diagonal scores
        for i in range(rows - 2):
            for j in range(2, cols):
                if self.board_state[i][j] == self.board_state[i + 1][j - 1] == self.board_state[i + 2][j - 2] and self.board_state[i][j] != 0:
                    scores[self.board_state[i][j] // check_point] += self.board_state[i][j]

        return scores
    
    def get_negamax_scores(self, terminal):
        """
        Calculate negamax scores. This function should exactly be the same of get_scores unless
        you set the score for negamax to a value that is not an increment of 1 (e.g., you can do scores = scores + 100 
        instead of scores = scores + 1)
        """
        rows = len(self.board_state)
        cols = len(self.board_state[0])
        scores = [0, 0]
        check_point = 3 if terminal else 2
        
         # Calculate negamax scores
        for i in range(rows):
         for j in range(cols):
            if self.board_state[i][j] == 0:
                # Get the maximum score for the current player
                max_score = -float('inf')
                for move in self.get_valid_moves(i, j):
                    new_game_state = self.make_move(move)
                    score, _ = self.get_negamax_scores(new_game_state, terminal)
                    max_score = max(max_score, score)

                # Update the score for the current player
                scores[self.turn_O] += max_score

            return scores


    def get_moves(self):
        moves = []

        for i in range(len(self.board_state)):
            for j in range(len(self.board_state[0])):
                if self.board_state[i][j] == 0:
                    moves.append((i, j))

        return moves

    def get_new_state(self, move):
        new_board_state = self.board_state.copy()
        x, y = move[0], move[1]
        new_board_state[x, y] = 1 if self.turn_O else -1
        return GameStatus(new_board_state, not self.turn_O)
