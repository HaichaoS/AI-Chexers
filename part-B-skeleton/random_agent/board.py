from random_agent.State import State
class Board(object):
    def __init__(self):
        self=self

    def get_all_actions(self,player,state):
        """Return a list of neighbouring states."""
        desti = player.desti
        pieces = player.pieces
        blocks = state.enemy1.pieces + state.enemy2.pieces
        next_state = []
        for position, piece in enumerate(pieces):

            # move the piece out of the pieces list once it reaches the destination
            if piece in desti:
                remove_pieces = pieces.copy()
                remove_pieces.remove(piece)
                new_state = State(remove_pieces.copy(),desti)
                new_state.before = piece.copy()
                new_state.after = "EXIT"
                new_state.parent = state
                new_state.action = "EXIT"
                next_state.append(new_state)
                break

            # find the possible positions that the current piece could reach
            for change in [[1, -1], [0, -1], [-1, 0], [1, 0], [-1, 1], [0, 1]]:
                new_piece = [piece[0] + change[0], piece[1] + change[1]]
                new_pieces = pieces.copy()
                action = None

                if not piece_in_board(new_piece):
                    continue
                # add positions that the piece could move to
                if new_piece not in pieces and new_piece not in blocks:
                    new_pieces[position] = new_piece
                    action = "MOVE"

                # add positions that the piece could jump to
                else:
                    new_piece = [piece[0] + 2 * change[0], piece[1] + 2 * change[1]]
                    if not piece_in_board(new_piece):
                        continue
                    if new_piece not in pieces and new_piece not in blocks:
                        new_pieces[position] = new_piece
                        action = "JUMP"

                new_state = State(new_pieces.copy(),state.desti)
                new_state.before = piece.copy()
                new_state.after = new_piece.copy()
                new_state.parent = state
                new_state.action = action
                if(action!=None):
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
