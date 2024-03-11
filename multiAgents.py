from GameStatus_5120 import GameStatus


def minimax(game_state: GameStatus, depth: int, maximizingPlayer: bool, alpha=float('-inf'), beta=float('inf')):
    terminal = game_state.is_terminal()
    if (depth == 0) or terminal:
        utility_value = game_state.get_scores()
        return utility_value, None

    if maximizingPlayer:
        max_value = float('-inf')
        best_move_max = None
        # Initialize the best move and value to negative infinity

        # Loop through all possible moves

        for move in game_state.get_moves():
            print("MAXIMIZING PLAYER")
            print(move)
            # Make the move and get the new game state

            total_temp_set = []
            for i in range(len(game_state.board_state)):
                temp_set = []
                for j in range(len(game_state.board_state)):
                    temp = game_state.board_state[i][j]
                    temp_set.append(temp)
                total_temp_set.append(temp_set)
            temp_game = GameStatus(total_temp_set, False)

            new_game_state = game_state.get_new_state(move)

            # Get the value and best move for the minimizing player

            value, new_move = minimax(new_game_state, depth - 1, False, alpha, beta)

            game_state.board = total_temp_set

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
        best_move_min = None
        min_value = float('inf')
        # Initialize the best move and value to infinity

        # Loop through all possible moves

        for move in game_state.get_moves():
            print("MINIMIZING PLAYER")
            print(move)
            # Make the move and get the new game state
            total_temp_set = []
            for i in range(len(game_state.board_state)):
                temp_set = []
                for j in range(len(game_state.board_state)):
                    temp = game_state.board_state[i][j]
                    temp_set.append(temp)
                total_temp_set.append(temp_set)
            temp_game = GameStatus(total_temp_set, False)

            new_game_state = game_state.get_new_state(move)

            # Get the value and best move for the maximizing player

            value, new_move = minimax(new_game_state, depth - 1, True, alpha, beta)

            game_state.board = total_temp_set

            if value < min_value:
                min_value = value
                best_move_min = move

            # Prune the search tree if necessary
            beta = min(beta, value)
            if alpha >= beta:
                break

        # Return the best value and best move
        return min_value, best_move_min


def negamax(game_state: GameStatus, depth: int,alpha=float('-inf'), beta=float('inf')):
    terminal = game_state.is_terminal()
    if (depth == 0) or terminal:
        scores = game_state.get_negamax_scores()
        return -1 * scores, None
    # Initialize the best move and value to negative infinity
    max_value = float('-inf')
    best_move_max = None
    # Loop through all possible moves
    for move in game_state.get_moves():
        # Make the move and get the new game state

        total_temp_set = []
        for i in range(len(game_state.board_state)):
            temp_set = []
            for j in range(len(game_state.board_state)):
                temp = game_state.board_state[i][j]
                temp_set.append(temp)
            total_temp_set.append(temp_set)
        temp_game = GameStatus(total_temp_set, False)
        new_game_status = game_state.get_new_state(move)

        # Call negamax recursively with the opposite turn_multiplier
        value, _ = negamax(new_game_status, depth - 1, -beta, -alpha)

        game_state.board_state = total_temp_set
        # Update the best move and value
        if value > max_value:
            max_value = value
            best_move_max = move
        # Prune the search tree if necessary
        alpha = max(alpha, value)
        if alpha >= beta:
            break
    # Return the best value and best move
    return -1 * max_value, best_move_max
