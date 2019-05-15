from your_team_name.State import State
from your_team_name.evaluate import *

NEIGHBOR = [[1, -1], [0, -1], [-1, 0], [1, 0], [-1, 1], [0, 1]]


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
                return result, next_state

        return best, return_state


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


def next_colour(colour):

    if colour == "red":
        return "green"
    elif colour == "green":
        return "blue"
    else:
        return "red"





