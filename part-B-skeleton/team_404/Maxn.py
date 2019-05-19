"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part B: Playing the Game
Authors: Haichao Song, Haolin Zhou
"""


from team_404.evaluate import *


class Maxn:
    """Describe the maxn agent that search all possible states in certain depth,
    assume every player max their own value and then find the best move for the
    current player"""

    def __init__(self, colour, depth, state):
        """create a new maxn agent"""

        self.colour = colour
        self.depth = depth
        self.evaluate = Evaluate(colour, state)

    def maxn(self, state, depth, colour, alpha):
        """Recursion method run depths of all possible move a player can make,
        use evaluate agent to evaluate values for all states and make best
        decision according to the value
        Use lazy evaluation, only evaluate the player we want to evaluate"""

        return_state = None
        curr_depth = depth
        curr_player = state.colour

        # evaluate the current state
        result = self.evaluate.evaluate_create(state, colour)

        # if its the last depth we want to search, return result
        if (len(state.pieces_dic[colour]) == 0) or (depth <= 0):
            return result, state

        best = {"red": float("-inf"),
                "green": float("-inf"),
                "blue": float("-inf")}

        # find all its next possible state and evaluate
        children = get_next_state(state, colour)
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
    """Return the colour of next moving player"""

    if colour == "red":
        return "green"
    elif colour == "green":
        return "blue"
    else:
        return "red"







