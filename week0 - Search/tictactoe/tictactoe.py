"""
Tic Tac Toe Player
"""

import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0
    for row in board:
        for cell in row:
            if cell == X:
                x_count += 1
            elif cell == O:
                o_count += 1
    return X if o_count >= x_count else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                actions.add((i, j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if (
        action[0] < 0
        or action[0] >= len(board)
        or action[1] < 0
        or action[1] >= len(board[0])
    ):
        raise IndexError("Index must be between 0 and 2")
    if board[action[0]][action[1]] != EMPTY:
        raise ValueError("Position not empty")

    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check around middle
    if board[1][1] != EMPTY:
        if (
            (board[1][0] == board[1][1] and board[1][2] == board[1][1])
            or (board[0][1] == board[1][1] and board[2][1] == board[1][1])
            or (board[0][0] == board[1][1] and board[2][2] == board[1][1])
            or (board[0][2] == board[1][1] and board[2][0] == board[1][1])
        ):
            return board[1][1]

    # Check from top left
    if board[0][0] != EMPTY:
        if (board[0][1] == board[0][0] and board[0][2] == board[0][0]) or (
            board[1][0] == board[0][0] and board[2][0] == board[0][0]
        ):
            return board[0][0]

    # Check from bottom right
    if board[2][2] != EMPTY:
        if (board[2][1] == board[2][2] and board[2][0] == board[2][2]) or (
            board[1][2] == board[2][2] and board[0][2] == board[2][2]
        ):
            return board[2][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    isWinner = winner(board)
    if isWinner == None:
        for row in board:
            for cell in row:
                if cell == EMPTY:
                    return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    the_winner = winner(board)
    return 1 if the_winner == X else -1 if the_winner == O else 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if not terminal(board):
        if player(board) == X:
            action = max_value(board)[0]
            return action
        else:
            action = min_value(board)[0]
            return action
    return None


def min_value(board):
    if terminal(board):
        return None, utility(board)
    possible_actions = actions(board)
    minimum = float("inf")
    min_action = None
    for action in possible_actions:
        temp = max_value(result(board, action))[1]
        if temp < minimum:
            minimum = temp
            min_action = action
            if minimum == -1:
                return min_action, minimum
    return min_action, minimum


def max_value(board):
    if terminal(board):
        return None, utility(board)
    possible_actions = actions(board)
    maximum = float("-inf")
    max_action = None
    for action in possible_actions:
        temp = min_value(result(board, action))[1]
        if temp > maximum:
            maximum = temp
            max_action = action
            if maximum == 1:
                return action, maximum
    return max_action, maximum
