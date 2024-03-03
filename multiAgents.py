from GameStatus_5120 import GameStatus


def minimax(game_state: GameStatus, depth: int, maximizingPlayer: bool, alpha=float('-inf'), beta=float('inf')):
    terminal = game_state.is_terminal()
    if (depth==0) or (terminal):
        new_scores = game_state.get_scores(terminal)
        return new_scores, None

    if maximizingPlayer:
        # Initialize the best move and value to negative infinity
        best_value = float('-inf')
        best_move = None

        # Loop through all possible moves
        for move in game_state.get_valid_moves():
            # Make the move and get the new game state
            new_game_state = game_state.make_move(move)

            # Get the value and best move for the minimizing player
            value, best_move = minimax(new_game_state, depth-1, False, alpha, beta)

            # Update the best value if necessary
            if value > best_value:
                best_value = value
                best_move = move

            # Prune the search tree if necessary
            alpha = max(alpha, value)
            if alpha >= beta:
                break

        # Return the best value and best move
        return best_value, best_move

    else:
        # Initialize the best move and value to infinity
        best_value = float('inf')
        best_move = None

        # Loop through all possible moves
        for move in game_state.get_valid_moves():
            # Make the move and get the new game state
            new_game_state = game_state.make_move(move)

            # Get the value and best move for the maximizing player
            value, best_move = negamax(new_game_state, depth-1, True, alpha, beta)

            # Update the best value if necessary
            if value < best_value:
                best_value = value
                best_move = move

            # Prune the search tree if necessary
            beta = min(beta, value)
            if alpha >= beta:
                break

        # Return the best value and best move
        return -best_value, best_move


def negamax(game_status: GameStatus, depth: int, turn_multiplier: int, alpha=float('-inf'), beta=float('inf')):
    terminal = game_status.is_terminal()
    if (depth==0) or (terminal):
        scores = game_status.get_negamax_scores(terminal)
        return scores, None

    # Determine if it's the maximizing player's turn
    if turn_multiplier == 1:
        # Initialize the best move and value to negative infinity
        best_value = float('-inf')
        best_move = None

        # Loop through all possible moves
        for move in game_status.get_valid_moves():
            # Make the move and get the new game state
            new_game_status = game_status.make_move(move)

            # Get the value and best move for the minimizing player
            value, best_move = negamax(new_game_status, depth-1, -1, alpha, beta)

            # Update the best value if necessary
            best_value = max(best_value, value * turn_multiplier)

            # Prune the search tree if necessary
            alpha = max(alpha, best_value)
            if alpha >= beta:
                break

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