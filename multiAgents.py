from GameStatus_5120 import GameStatus


def minimax(game_state: GameStatus, depth: int, maximizingPlayer: bool, alpha=float('-inf'), beta=float('inf')):
    terminal = game_state.is_terminal()
    if (depth == 0) or terminal:
        utility_value = game_state.get_scores()
        return utility_value, None

    if maximizingPlayer:
        # Initialize the best move and value to negative infinity
        max_value = float('-inf')
        best_move_max = None

        # Loop through all possible moves

        for move in game_state.get_moves():
            # Make the move and get the new game state

            new_game_state = game_state.get_new_state(move)

            # Get the value and best move for the minimizing player

            value, best_move_max = minimax(new_game_state, depth - 1, False, alpha, beta)


            if value > max_value:
                max_value = value
                best_move_max = move

            # Prune the search tree if necessary
            alpha = max(alpha, value)
            if alpha >= beta:
                break

        # Return the best value and best move
        return max_value, best_move_max

    else:
        # Initialize the best move and value to infinity
        min_value = float('inf')
        best_move_min = None

        # Loop through all possible moves

        for move in game_state.get_moves():
            # Make the move and get the new game state
            new_game_state = game_state.get_new_state(move)

            # Get the value and best move for the maximizing player

            value, best_move_min = minimax(new_game_state, depth - 1, True, alpha, beta)

            if value < min_value:
                min_value = value
                best_move_min = move

            # Prune the search tree if necessary
            beta = min(beta, value)
            if alpha >= beta:
                break

        # Return the best value and best move
        return min_value, best_move_min


def negamax(game_status: GameStatus, depth: int, turn_multiplier: int, alpha=float('-inf'), beta=float('inf')):
    terminal = game_status.is_terminal()
    if (depth == 0) or (terminal):
        scores = game_status.get_negamax_scores(terminal)
        return scores, None
    """
    YOUR CODE HERE TO CALL NEGAMAX FUNCTION. REMEMBER THE RETURN OF THE NEGAMAX SHOULD BE THE OPPOSITE OF THE CALLING
    PLAYER WHICH CAN BE DONE USING -NEGAMAX(). THE REST OF YOUR CODE SHOULD BE THE SAME AS MINIMAX FUNCTION.
    YOU ALSO DO NOT NEED TO TRACK WHICH PLAYER HAS CALLED THE FUNCTION AND SHOULD NOT CHECK IF THE CURRENT MOVE
    IS FOR MINIMAX PLAYER OR NEGAMAX PLAYER
    RETURN THE FOLLOWING TWO ITEMS
    1. VALUE
    2. BEST_MOVE
    
    THE LINE TO RETURN THESE TWO IS COMMENTED BELOW WHICH YOU CAN USE
    
    """
# return value, best_move
