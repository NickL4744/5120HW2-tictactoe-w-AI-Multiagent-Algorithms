from GameStatus_5120 import GameStatus


def minimax(board, player, maximizingPlayer):
    # Check if the game is over
    result = game_result(board)
    if result == "X":
        return -1
    elif result == "O":
        return 1
    elif result == "Draw":
        return 0
    
    # Initialize best move and score
    best_move = None
    if maximizingPlayer:
        best_score = -float("inf")
    else:
        best_score = float("inf")
    
    # Loop through all empty cells
    for i in range(len(board)):
        if board[i] == "":
            # Make the move
            board[i] = player
            
            # Recursive call to minimax
            score = minimax(board, "X" if player == "O" else "O", not maximizingPlayer)
            
            # Undo the move
            board[i] = ""
            
            # Update best move and score
            if (maximizingPlayer and score > best_score) or (not maximizingPlayer and score < best_score):
                best_score = score
                best_move = i
    
    # Return the best move or best score
    if best_move is not None:
        return best_move
    else:
        return best_score

def game_result(board):
    # Check rows, columns, and diagonals
    for i in range(0, 9, 3):
        if board[i] == board[i+1] == board[i+2] != "":
            return board[i]
    for i in range(3):
        if board[i] == board[i+3] == board[i+6] != "":
            return board[i]
    if board[0] == board[4] == board[8] != "":
        return board[0]
    if board[2] == board[4] == board[6] != "":
        return board[2]
    
    # Check for a draw
    if "" not in board:
        return "Draw"
    
    # Game is not over yet
    return None

def negamax(game_status, depth, turn_multiplier, alpha=float('-inf'), beta=float('inf')):
    terminal = game_status.is_terminal()  # Check if the game state is terminal
    if depth == 0 or terminal:
        scores = game_status.get_negamax_scores(terminal)
        return scores, None

    # Determine if it's the maximizing player's turn
    if turn_multiplier == 1:
        # Initialize the best value to negative infinity
        best_value = float('-inf')
        best_move = None

        # Loop through all possible moves
        for move in game_status.get_moves():
            # Make the move and get the new game state
            new_game_status = game_status.get_new_state(move)

            # Get the value and best move for the minimizing player
            value, _ = negamax(new_game_status, depth - 1, -1, alpha, beta)

            # Update the best value if necessary
            best_value = max(best_value, value * turn_multiplier)

            # Update alpha and beta
            alpha = max(alpha, best_value)
            if alpha >= beta:
                break

            # Set the best move
            if value * turn_multiplier == best_value:
                best_move = move

        # Return the best value and best move
        return best_value, best_move

    else:
        # Initialize the best move and value to infinity
        best_value = float('inf')
        best_move = None

        # Loop through all possible moves
        for move in game_status.get_valid_moves():
            # Make the move and get the new game state
            new_game_status = game_status.make_move(move)

            # Get the value and best move for the maximizing player
            value, best_move = negamax(new_game_status, depth-1, 1, alpha, beta)

            # Update the best value if necessary
            best_value = min(best_value, value * turn_multiplier)

            # Prune the search tree if necessary
            beta = min(beta, best_value)
            if alpha >= beta:
                break

        # Return the best value and best move
        return -best_value, best_move