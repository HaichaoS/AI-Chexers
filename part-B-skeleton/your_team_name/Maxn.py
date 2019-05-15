from your_team_name.evaluate import *


class Maxn:

    def __init__(self, colour, depth, state):
        'create a new state'
        self.colour = colour
        self.depth = depth
        self.state = state
        self.evaluate = Evaluate(colour, state)

    def maxn(self, state, depth, colour, alpha):
        return_state = None
        curr_depth = depth
        curr_player = state.colour

        result = self.evaluate.evaluate_create(state, colour)
        children = get_next_state(state)

        if (len(state.pieces) == 0) or (depth <= 0):
            return result, state

        best = {"red": float("-inf"),
                "green": float("-inf"),
                "blue": float("-inf")}

        for child in children:
            result, next_state = self.maxn(child, curr_depth-1, next_colour(colour), best[colour])
            if result[colour] is None:
                self.evaluate.evaluate_add(result, state, colour)
            if result[colour] > best[colour]:
                best = result
                if (curr_depth == self.depth) and (curr_player == self.colour):
                    return_state = child
            if result[colour] > float("inf") - alpha:
                return result, next_state
        return best, return_state


def next_colour(colour):

    if colour == "red":
        return "green"
    elif colour == "green":
        return "blue"
    else:
        return "red"





