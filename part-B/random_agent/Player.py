import random_agent.Board as board
from random import randrange
from random_agent.State import State

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
        self.board = board.Board()
        self.colour = colour
        start_dic = {
            "red": [[-3,0],[-3,1],[-3,2],[-3,3]],
            "blue": [[3, 0], [2, 1], [1, 2], [0, 3]],
            "green": [[0,-3], [1,-3], [2,-3], [3,-3]]
        }
        desti_dic = {
            "red": [[3, -3], [3, -2], [3, -1], [3, 0]],
            "blue": [[0, -3], [-1, -2], [-2, -1], [-3, 0]],
            "green": [[-3, 3], [-2, 3], [-1, 3], [0, 3]]
        }
        if colour == 'red':
            self.enemy1 = 'blue'
            self.enemy2 = 'green'
            self.pieces = start_dic[colour]
        elif colour == 'blue':
            self.enemy1 = 'red'
            self.enemy2 = 'green'
            self.pieces = [[3, 0], [2, 1], [1, 2], [0, 3]]
        elif colour == 'green':
            self.enemy1 = 'blue'
            self.enemy2 = 'red'
            self.pieces = [[0,-3], [1,-3], [2,-3], [3,-3]]
        self.desti = desti_dic[colour]
        self.state = State(self.pieces, self.desti)
        self.state.enemy1 = State(start_dic[self.enemy1],desti_dic[self.enemy1])
        self.state.enemy2 = State(start_dic[self.enemy2],desti_dic[self.enemy2])


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
        actions = self.board.get_all_actions(self,self.state)
        if len(actions) > 0:
            our_action = actions[randrange(0, len(actions))]
            if our_action.action == "EXIT":
                return ("EXIT", (tuple(our_action.before)))
            elif our_action.action == "MOVE":
                return ("MOVE", ((tuple(our_action.before), tuple(our_action.after))))
            elif our_action.action == "JUMP":
                return ("JUMP", ((tuple(our_action.before), tuple(our_action.after))))
        else:
            return ("PASS", None)


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
        if colour == self.enemy1:
            if action[0] == 'EXIT':
                self.state.enemy1.pieces.remove(list(action[1]))
            else:
                if action[0] == 'JUMP':
                    eat = list(find_jump_over(action[1][0], action[1][1]))
                    if(eat in self.pieces):
                        self.pieces.remove(eat)
                        self.state.enemy1.pieces.append(eat)
                    elif (eat in self.state.enemy2.pieces):
                        self.state.enemy2.pieces.remove(eat)
                        self.state.enemy1.pieces.append(eat)
                for n, pos in enumerate(self.state.enemy1.pieces):
                    if pos == list(action[1][0]):
                        self.state.enemy1.pieces[n]=list(action[1][1])

        if colour == self.enemy2:
            if action[0] == 'EXIT':
                self.state.enemy2.pieces.remove(list(action[1]))
            else:
                if action[0] == 'JUMP':
                    eat = list(find_jump_over(action[1][0], action[1][1]))
                    if (eat in self.pieces):
                        self.pieces.remove(eat)
                        self.state.enemy2.pieces.append(eat)
                    elif (eat in self.state.enemy1.pieces):
                        self.state.enemy1.pieces.remove(eat)
                        self.state.enemy2.pieces.append(eat)
                for n, pos in enumerate(self.state.enemy2.pieces):
                    if pos == list(action[1][0]):
                        self.state.enemy2.pieces[n]=list(action[1][1])

        if colour == self.colour:
            if action[0] == 'EXIT':
                self.pieces.remove(list(action[1]))
            else:
                if action[0] == 'JUMP':
                    eat = list(find_jump_over(action[1][0], action[1][1]))
                    if (eat in self.state.enemy2.pieces):
                        self.state.enemy2.pieces.remove(eat)
                        self.pieces.append(eat)
                    elif (eat in self.state.enemy1.pieces):
                        self.state.enemy1.pieces.remove(eat)
                        self.pieces.append(eat)
                for n, pos in enumerate(self.pieces):
                    if pos == list(action[1][0]):
                        self.pieces[n] = list(action[1][1])


def find_jump_over(parent, kid):
    x=parent[0]-kid[0]
    y=parent[1]-kid[1]
    if(x==-2 and y==2):
        return (parent[0]+1,parent[1]-1)
    elif(x==2 and y==-2):
        return (parent[0]-1,parent[1]+1)
    elif(x==-2):
        return (parent[0]+1,parent[1])
    elif(x==2):
        return (parent[0]-1,parent[1])
    elif(y==-2):
        return (parent[0],parent[1]+1)
    elif(y==2):
        return (parent[0],parent[1]-1)
