"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part B: Playing the Game
Authors: Haichao Song, Haolin Zhou
"""

from your_team_name.State import *
from your_team_name.Maxn import Maxn


# The Start of all pieces in the board
START_DIC = {
    "red": [[-3, 0], [-3, 1], [-3, 2], [-3, 3]],
    "blue": [[3, 0], [2, 1], [1, 2], [0, 3]],
    "green": [[0, -3], [1, -3], [2, -3], [3, -3]]
}

# The destination of each colour in the board
DESTI_DIC = {
    "red": [[3, -3], [3, -2], [3, -1], [3, 0]],
    "blue": [[0, -3], [-1, -2], [-2, -1], [-3, 0]],
    "green": [[-3, 3], [-2, 3], [-1, 3], [0, 3]]
}

# The planned starting action for each colour in the game
START_ACTION_DIC = {
    "red": [("MOVE", ((-3, 0), (-2, 0))),
            ("MOVE", ((-2, 0), (-2, 1))),
            ("MOVE", ((-3, 3), (-2, 2)))],
    "green": [("MOVE", ((3, -3), (2, -2))),
              ("MOVE", ((2, -2), (1, -2))),
              ("MOVE", ((0, -3), (0, -2)))],
    "blue": [("MOVE", ((0, 3), (0, 2))),
              ("MOVE", ((0, 2), (1, 1))),
              ("MOVE", ((3, 0), (2, 0)))]
}

# Depth for Maxn search
MAXN_DEPTH = 3


class ExamplePlayer:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the 
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your 
        program will play as (Red, Green or Blue). The value will be one of the 
        strings "red", "green", or "blue" correspondingly.
        """
        # Set up state representation and maxn agent
        state = State(colour, START_DIC, DESTI_DIC)
        self.state = state
        self.colour = colour
        self.maxn = Maxn(self.colour, MAXN_DEPTH, self.state)

    def action(self):
        """
        This method is called at the beginning of each of your turns to request 
        a choice of action from your program.

        Based on the current state of the game, your player should select and 
        return an allowed action to play on this turn. If there are no allowed 
        actions, your player must return a pass instead. The action (or pass) 
        must be represented based on the above instructions for representing 
        actions.
        """

        # Decide what action to take.
        # for the first three steps, do the planned job
        action = None
        if self.state.turn < 3:
            action = start_action(self.state, self.state.turn)

        # Run maxn with three depth if we still have pieces
        if action is None:
            if len(self.state.pieces_dic[self.colour]) == 0:
                return ("PASS", None)

            result, state = self.maxn.maxn(self.state, MAXN_DEPTH, self.colour,
                                           -float("inf"))

            if state is None:
                action = ("PASS", None)
            # Get action form according to the state maxn gives us
            elif state.action == "EXIT":
                action = (state.action, tuple(state.before))
            elif state.action == "MOVE" or state.action == "JUMP":
                action = (state.action, (tuple(state.before), tuple(state.after)))
            else:
                action = ("PASS", None)

        # Add turn count
        self.state.turn += 1

        return action

    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s 
        turns) to inform your player about the most recent action. You should 
        use this opportunity to maintain your internal representation of the 
        game state and any other information about the game you are storing.

        The parameter colour will be a string representing the player whose turn
        it is (Red, Green or Blue). The value will be one of the strings "red", 
        "green", or "blue" correspondingly.

        The parameter action is a representation of the most recent action (or 
        pass) conforming to the above in- structions for representing actions.

        You may assume that action will always correspond to an allowed action 
        (or pass) for the player colour (your method does not need to validate 
        the action/pass against the game rules).
        """
        # TODO: Update state representation in response to action.

        # For MOVE action, change its own pieces place
        if action[0] == "MOVE":
            before = list(action[1][0])
            after = list(action[1][1])
            if before in self.state.pieces_dic[colour]:
                self.state.pieces_dic[colour].remove(before)
                self.state.pieces_dic[colour].append(after)

        # For JUMP action, change its own pieces place and
        # if it jumps other colours piece, change to its own colour
        elif action[0] == "JUMP":
            before = list(action[1][0])
            after = list(action[1][1])
            if before in self.state.pieces_dic[colour]:
                self.state.pieces_dic[colour].remove(before)
                self.state.pieces_dic[colour].append(after)
            middle_piece = find_jump_over(before, after)
            for key in self.state.pieces_dic.keys():
                if middle_piece in self.state.pieces_dic[key]:
                    self.state.pieces_dic[key].remove(middle_piece)
                    self.state.pieces_dic[colour].append(middle_piece)

        # For EXIT action, move the exit piece and add its exit value
        elif action[0] == "EXIT":
            exit_piece = list(action[1])
            if exit_piece in self.state.pieces_dic[colour]:
                self.state.pieces_dic[colour].remove(exit_piece)
                self.state.exit_dic[colour] += 1


def start_action(state, turn):
    """
    This method is called at the first three turns of game to let player
    plays planned steps for its pieces in order to bound its pieces together
    to get best result in the end.

    The parameter state will be the current situations on the board.

    The parameter turn will be the current turn the player at.
    """

    # if the target place is empty, move to that target
    if list(START_ACTION_DIC[state.colour][turn][1][1]) \
            not in get_all_pieces(state):
        return START_ACTION_DIC[state.colour][turn]
    else:
        return None



