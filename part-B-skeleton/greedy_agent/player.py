from greedy_agent.State import *
from greedy_agent.Maxn import Maxn

start_dic = {
    "red": [[-3, 0], [-3, 1], [-3, 2], [-3, 3]],
    "blue": [[3, 0], [2, 1], [1, 2], [0, 3]],
    "green": [[0, -3], [1, -3], [2, -3], [3, -3]]
}
desti_dic = {
    "red": [[3, -3], [3, -2], [3, -1], [3, 0]],
    "blue": [[0, -3], [-1, -2], [-2, -1], [-3, 0]],
    "green": [[-3, 3], [-2, 3], [-1, 3], [0, 3]]
}
defend_dic = {
    "red": [[3, -3], [3, 0]],
    "green": [[-3, 3], [0, 3]],
    "blue": [[-3, 0], [0, -3]]
}


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
        # TODO: Set up state representation.
        state = State(colour, start_dic, desti_dic)
        self.state = state
        self.colour = colour
        self.maxn = Maxn(self.colour, 1, self.state)

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
        # TODO: Decide what action to take.

        # elif (len(self.state.pieces) <= 2) and \
        #     (self.state.exit_value + len(self.state.pieces) < 4):
        #     if len(self.state.enemy1_pieces) > len(self.state.enemy2_pieces):
        #         action = defend(self.state, self.state.enemy1_colour)
        #     else:
        #         action = defend(self.state, self.state.enemy2_colour)

        if len(self.state.pieces_dic[self.colour]) == 0:
            return ("PASS", None)

        result, state = self.maxn.maxn(self.state, 1, self.colour, -float("inf"))

        if state.action == "EXIT":
            action = (state.action, tuple(state.before))
        elif state.action == "MOVE" or state.action == "JUMP":
            action = (state.action, (tuple(state.before), tuple(state.after)))
        else:
            action = ("PASS", None)

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

        if action[0] == "MOVE":
            before = list(action[1][0])
            after = list(action[1][1])
            if before in self.state.pieces_dic[colour]:
                self.state.pieces_dic[colour].remove(before)
                self.state.pieces_dic[colour].append(after)

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

        elif action[0] == "EXIT":
            exit_piece = list(action[1])
            if exit_piece in self.state.pieces_dic[colour]:
                self.state.pieces_dic[colour].remove(exit_piece)
                self.state.exit_dic[colour] += 1

        print("exit:", self.state.exit_dic[colour])




