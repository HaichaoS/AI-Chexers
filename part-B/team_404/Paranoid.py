"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part B: Playing the Game
Authors: Haichao Song, Haolin Zhou
"""

from team_404.Evaluate import *


class Paranoid:
    """Paranoid agent used to tried analyze state and generate best move
    Compared to Max n it has its weakness therefore abandoned.
    NOT USED MAY HAVE ERROR RUNNING"""

    def __init__(self, colour, depth, state):
        'create a new state'
        self.colour = colour
        self.depth = depth
        self.state = state

    def alphabeta(self, state, depth, colour, alpha, beta):

        # return_state = None
        # curr_depth = depth
        curr_player = state.colour

        result = self.evaluate_create(state, colour)
        children = get_next_state(state)

        if (len(state.pieces) == 0) or (depth <= 0):
            if curr_player == self.colour:
                return result, state
            else:
                return -result, state

        for child in children:
            if (curr_player == self.colour) or (next_colour(curr_player) == self.colour):
                result, nest_state = self.alphabeta(child, depth-1, next_colour(colour), -beta, -alpha)
                alpha = max(alpha, -result)
            else:
                result, next_state = self.alphabeta(child, depth-1, next_colour(colour), alpha, beta)
                alpha = max(alpha, result)
        if alpha > beta:
            return beta, child
        return alpha, child


def next_colour(colour):

    if colour == "red":
        return "green"
    elif colour == "green":
        return "blue"
    else:
        return "red"
