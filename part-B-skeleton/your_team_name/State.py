NEIGHBOR = [[1, -1], [0, -1], [-1, 0], [1, 0], [-1, 1], [0, 1]]


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
        self.exit_value = 0
        self.parent = None
        self.before = None
        self.after = None
        self.action = None


def get_next_state(state):
    """Return a list of neighbouring states."""
    pieces = state.pieces
    enemy1_pieces = state.enemy1_pieces
    enemy2_pieces = state.enemy2_pieces

    next_state = []
    for position, piece in enumerate(pieces):

        # move the piece out of the pieces list once it reaches the destination
        if piece in state.desti:
            remove_pieces = pieces.copy()
            remove_pieces.remove(piece)
            new_state = State(state.colour, remove_pieces.copy(), state.desti_dic, state.enemy1_colour,
                              state.enemy2_colour, state.enemy1_pieces, state.enemy2_pieces)
            new_state.before = piece.copy()
            new_state.after = "EXIT"
            new_state.parent = state
            new_state.action = "EXIT"
            new_state.exit_value = state.exit_value + 1
            next_state.append(new_state)
            break

        # find the possible positions that the current piece could reach
        for change in NEIGHBOR:

            new_piece = [piece[0] + change[0], piece[1] + change[1]]
            new_pieces = pieces.copy()
            action = None

            if not piece_in_board(new_piece):
                continue

            # add positions that the piece could move to
            if (new_piece not in pieces) and (new_piece not in enemy1_pieces) \
                    and (new_piece not in enemy2_pieces):
                new_pieces[position] = new_piece
                action = "MOVE"

            # add positions that the piece could jump to
            else:
                new_piece = [piece[0] + 2 * change[0], piece[1] + 2 * change[1]]
                if not piece_in_board(new_piece):
                    continue
                if (new_piece not in pieces) and (new_piece not in enemy1_pieces) \
                        and (new_piece not in enemy2_pieces):
                    new_pieces[position] = new_piece
                    action = "JUMP"

            new_state = State(state.colour, new_pieces.copy(), state.desti_dic, state.enemy1_colour,
                              state.enemy2_colour, state.enemy1_pieces, state.enemy2_pieces)
            new_state.before = piece
            new_state.after = new_piece.copy()
            new_state.parent = state
            new_state.action = action
            if action:
                next_state.append(new_state)

    return next_state


def piece_in_board(piece):
    """Check whether the piece is contained in the board."""
    piece_z = - piece[0] - piece[1]
    if piece[0] < -3 or piece[0] > 3:
        return False
    if piece[1] < -3 or piece[1] > 3:
        return False
    if piece_z < -3 or piece_z > 3:
        return False
    return True
