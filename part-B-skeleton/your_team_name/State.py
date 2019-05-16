NEIGHBOR = [[1, -1], [0, -1], [-1, 0], [1, 0], [-1, 1], [0, 1]]


class State:

    """ Describe a state witch contains the information of the board, the positions of
        the pieces and blocks, the parent(successor), the heuristic value and cost.
        Also includes the action that turn it into the current state."""

    def __init__(self, colour, pieces_dic, desti_dic):
        self.colour = colour
        self.pieces_dic = pieces_dic.copy()
        self.desti_dic = desti_dic.copy()
        self.turn = 0
        self.exit_dic = {"red": 0, "green": 0, "blue": 0}
        self.before = None
        self.after = None
        self.action = None

    def get_red_pieces(self):
        return self.pieces_dic["red"]

    def get_green_pieces(self):
        return self.pieces_dic["green"]

    def get_blue_pieces(self):
        return self.pieces_dic["blue"]


def form_pieces_dic(red, green, blue):
    new_pieces_dic = {"red": red,
                      "green": green,
                      "blue": blue}
    return new_pieces_dic


def get_next_state(state, colour):
    """Return a list of neighbouring states."""

    new_states = []
    for piece in state.pieces_dic[colour]:

        new_pieces_dic = state.pieces_dic.copy()
        action_colour_pieces = new_pieces_dic[colour].copy()

        # move the piece out of the pieces list once it reaches the destination
        if piece in state.desti_dic[colour]:
            new_exit_dic = state.exit_dic.copy()
            new_exit_dic[colour] += 1
            action_colour_pieces.remove(piece)
            new_pieces_dic[colour] = action_colour_pieces
            new_state = State(state.colour, new_pieces_dic.copy(), state.desti_dic)
            new_state.before = piece
            new_state.after = "EXIT"
            new_state.action = "EXIT"
            new_state.exit_dic = new_exit_dic.copy()
            new_state.turn = state.turn + 1
            new_states.append(new_state)
            continue

        for change in NEIGHBOR:
            new_pieces_dic = state.pieces_dic.copy()
            action_colour_pieces = new_pieces_dic[colour].copy()
            new_piece = [piece[0] + change[0], piece[1] + change[1]]
            action = None

            if not piece_in_board(new_piece):
                continue

            if new_piece not in (state.pieces_dic["red"] + state.pieces_dic["green"] + state.pieces_dic["blue"]):
                action_colour_pieces.remove(piece)
                action_colour_pieces.append(new_piece)
                action = "MOVE"
            else:
                new_piece = [piece[0] + 2 * change[0], piece[1] + 2 * change[1]]
                if not piece_in_board(new_piece):
                    continue
                if new_piece not in (state.pieces_dic["red"] + state.pieces_dic["green"] + state.pieces_dic["blue"]):
                    action_colour_pieces.remove(piece)
                    action_colour_pieces.append(new_piece)
                    action = "JUMP"
                    middle_piece = find_jump_over(piece, new_piece)
                    for key in state.pieces_dic.keys():
                        if middle_piece in state.pieces_dic[key]:
                            remove_colour_pieces = state.pieces_dic[key].copy()
                            remove_colour_pieces.remove(middle_piece)
                            action_colour_pieces.append(middle_piece)
                            new_pieces_dic[key] = remove_colour_pieces
            new_pieces_dic[colour] = action_colour_pieces
            new_state = State(state.colour, new_pieces_dic.copy(), state.desti_dic)
            new_state.before = piece
            new_state.after = new_piece
            new_state.action = action
            new_state.turn = state.turn + 1
            if action:
                new_states.append(new_state)
    return new_states


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
