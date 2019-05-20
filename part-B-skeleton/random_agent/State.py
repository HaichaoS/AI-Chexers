class State:

    """ Describe a state witch contains the information of the board, the positions of
        the pieces and blocks, the parent(successor), the heuristic value and cost.
        Also includes the action that turn it into the current state."""

    def __init__(self, pieces, desti):
        """create a new state"""

        self.pieces = pieces
        self.desti = desti
        self.enemy1 = None
        self.enemy2 = None
        self.parent = None
        self.before = None
        self.after = None
        self.action = None

