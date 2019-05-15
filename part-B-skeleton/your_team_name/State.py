
class State:

    """ Describe a state witch contains the information of the board, the positions of
        the pieces and blocks, the parent(successor), the heuristic value and cost.
        Also includes the action that turn it into the current state."""

    def __init__(self, colour, pieces, desti_dic, enemy1, enemy2, enemy1_pieces, enemy2_pieces):
        'create a new state'
        self.colour = colour
        self.pieces = pieces
        self.desti = desti_dic[colour]
        self.enemy1_colour = enemy1
        self.enemy2_colour = enemy2
        self.enemy1_pieces = enemy1_pieces
        self.enemy2_pieces = enemy2_pieces
        self.enemy1_desti = desti_dic[enemy1]
        self.enemy2_desti = desti_dic[enemy2]
        self.desti_dic = desti_dic
        self.turn = 0
        self.parent = None
        self.before = None
        self.after = None
        self.action = None
