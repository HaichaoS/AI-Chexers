from your_team_name.evaluate import *


class Maxn:

    def __init__(self, colour, depth, state):
        'create a new state'
        self.colour = colour
        self.depth = depth
        self.state = state

    def maxn(self, state, depth, colour, alpha):
        return_state = None
        curr_depth = depth
        curr_player = state.colour

        result = evaluate_create(state, colour)
        print(colour, state.pieces, result)
        # print(depth, colour, result)
        children = get_next_state(state)

        if (len(state.pieces) == 0) or (depth <= 0):
            # lazy
            return result, state

        best = {"red": float("-inf"),
                "green": float("-inf"),
                "blue": float("-inf")}

        for child in children:
            result, next_state = self.maxn(child, curr_depth-1, next_colour(colour), best[colour])
            if result[colour] is None:
                evaluate_add(result, state, colour)
            if result[colour] > best[colour]:
                best = result
                if (curr_depth == self.depth) and (curr_player == self.colour):
                    # print(">>>> ", next_state is not None)
                    return_state = child
            if result[colour] > float("inf") - alpha:
                print(colour, state.pieces, result)
                return result, next_state
        print(colour, state.pieces, result)
        return best, return_state


def next_colour(colour):

    if colour == "red":
        return "green"
    elif colour == "green":
        return "blue"
    else:
        return "red"





