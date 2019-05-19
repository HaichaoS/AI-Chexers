from team_404.evaluate import *


class Paranoid:

    def __init__(self, colour, depth, state):
        'create a new state'
        self.colour = colour
        self.depth = depth
        self.state = state

    def alphabeta(self, state, depth, colour, alpha, beta):

        return_state = None
        curr_depth = depth
        curr_player = state.colour

        result = evaluate_create(state, colour)
        # print(colour, state.pieces, result)
        # print(depth, colour, result)
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
