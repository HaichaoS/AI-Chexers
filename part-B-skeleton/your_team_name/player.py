from your_team_name.State import State
from your_team_name.Maxn import Maxn
from your_team_name.evaluate import heuristic

start_dic = {
    "red": [[-3, 0], [-3, 1], [-3, 2],[-3, 3]],
    "blue": [[3, 0], [2, 1], [1, 2], [0, 3]],
    "green": [[0, -3], [1, -3], [2, -3], [3, -3]]
}
desti_dic = {
    "red": [[3, -3], [3, -2], [3, -1], [3, 0]],
    "blue": [[0, -3], [-1, -2], [-2, -1], [-3, 0]],
    "green": [[-3, 3], [-2, 3], [-1, 3], [0, 3]]
}
start_action_dic = {
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
        if colour == 'red':
            enemy1 = 'green'
            enemy2 = 'blue'
        elif colour == 'blue':
            enemy1 = 'red'
            enemy2 = 'green'
        else:
            enemy1 = 'blue'
            enemy2 = 'red'
        state = State(colour, start_dic[colour], desti_dic,
                      enemy1, enemy2, start_dic[enemy1], start_dic[enemy2])
        self.state = state
        self.colour = colour
        self.past_state = None
        self.maxn = Maxn(self.colour, 3, self.state)

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

        if self.state.turn < 3:
            action = start_action(self.state, self.state.turn)

        # elif (len(self.state.pieces) <= 2) and \
        #     (self.state.exit_value + len(self.state.pieces) < 4):
        #     if len(self.state.enemy1_pieces) > len(self.state.enemy2_pieces):
        #         action = defend(self.state, self.state.enemy1_colour)
        #     else:
        #         action = defend(self.state, self.state.enemy2_colour)

        else:
            if len(self.state.pieces) == 0:
                return ("PASS", None)

            result, state = self.maxn.maxn(self.state, 3, self.colour, -float("inf"))
            if state.action == "EXIT":
                action = (state.action, tuple(state.before))
            elif state.action == "MOVE" or state.action == "JUMP":
                action = (state.action, (tuple(state.before), tuple(state.after)))
            else:
                action = ("PASS", None)

        self.update(self.colour, action)
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
            if self.state.colour == colour:
                if before in self.state.pieces:
                    self.state.pieces.remove(before)
                    self.state.pieces.append(after)
            elif self.state.enemy1_colour == colour:
                if before in self.state.enemy1_pieces:
                    self.state.enemy1_pieces.remove(before)
                    self.state.enemy1_pieces.append(after)
            elif self.state.enemy2_colour == colour:
                if before in self.state.enemy2_pieces:
                    self.state.enemy2_pieces.remove(before)
                    self.state.enemy2_pieces.append(after)

        elif action[0] == "JUMP":
            before = list(action[1][0])
            after = list(action[1][1])
            if self.state.colour == colour:
                if before in self.state.pieces:
                    self.state.pieces.remove(before)
                    self.state.pieces.append(after)
                    middle = find_jump_over(before, after)
                    if middle in self.state.enemy1_pieces:
                        self.state.enemy1_pieces.remove(middle)
                        self.state.pieces.append(middle)
                    elif middle in self.state.enemy2_pieces:
                        self.state.enemy2_pieces.remove(middle)
                        self.state.pieces.append(middle)

            elif self.state.enemy1_colour == colour:
                if before in self.state.enemy1_pieces:
                    self.state.enemy1_pieces.remove(before)
                    self.state.enemy1_pieces.append(after)
                    middle = find_jump_over(before, after)
                    if middle in self.state.pieces:
                        self.state.pieces.remove(middle)
                        self.state.enemy1_pieces.append(middle)
                    elif middle in self.state.enemy2_pieces:
                        self.state.enemy2_pieces.remove(middle)
                        self.state.enemy1_pieces.append(middle)

            elif self.state.enemy2_colour == colour:
                if before in self.state.enemy2_pieces:
                    self.state.enemy2_pieces.remove(before)
                    self.state.enemy2_pieces.append(after)
                    middle = find_jump_over(before, after)
                    if middle in self.state.pieces:
                        self.state.pieces.remove(middle)
                        self.state.enemy2_pieces.append(middle)
                    elif middle in self.state.enemy1_pieces:
                        self.state.enemy1_pieces.remove(middle)
                        self.state.enemy2_pieces.append(middle)

        elif action[0] == "EXIT":
            exit = list(action[1])
            if self.state.colour == colour:
                if exit in self.state.pieces:
                    self.state.pieces.remove(exit)
            elif self.state.enemy1_colour == colour:
                if exit in self.state.enemy1_pieces:
                    self.state.enemy1_pieces.remove(exit)
            elif self.state.enemy2_colour == colour:
                if exit in self.state.enemy2_pieces:
                    self.state.enemy2_pieces.remove(exit)

    # def defend(self, state, target):
    #     distance = heuristic(state.pieces, defend_dic[target])
    #     if distance == 0:




def find_jump_over(parent, kid):
    x = parent[0] - kid[0]
    y = parent[1] - kid[1]
    if (x == -2) and (y == 2):
        return [parent[0] + 1, parent[1] - 1]
    elif (x == 2) and (y == -2):
        return [parent[0] - 1, parent[1] + 1]
    elif x == -2:
        return [parent[0] + 1, parent[1]]
    elif x == 2:
        return [parent[0] - 1, parent[1]]
    elif y == -2:
        return [parent[0], parent[1] + 1]
    elif y == 2:
        return [parent[0], parent[1] - 1]


def start_action(state, turn):

    return start_action_dic[state.colour][turn]



