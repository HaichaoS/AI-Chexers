"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part B: Playing the Game
Authors: Haichao Song, Haolin Zhou
"""

from team_404.State import *


class Evaluate:
    """Describe the evaluation agent that calculate a value for every state
    in the game. Therefore maxn can make decision on which state is the best
     to perform"""

    def __init__(self, colour, state):
        self.colour = colour
        self.state = state
        self.eat_weight = 100
        self.exit_weight = 70
        self.dist_weight = 10
        self.bound_weight = 1
        self.side_weight = 0.01
        self.danger_colour_weight = 60
        self.danger_pieces_weight = 5

    def evaluate_create(self, state, colour):
        """When first evaluate in third depth, create dictionary to store evaluation
        values and return the dictionary to maxn"""

        values = {"red": None,
                  "green": None,
                  "blue": None}
        value = self.evaluate(state, colour)
        values[colour] = value
        return values

    def evaluate_add(self, values, state, colour):
        """Evaluate the value for specific colour in first and second depth and add
         the value to dictionary"""

        value = self.evaluate(state, colour)
        values[colour] = value

    def evaluate(self, state, colour):
        """Calculate different factors in the evaluation function and times their
        weight to get their final values. For state in different situations, values
        are calculated differently"""

        # Get the player's pieces and enemy's pieces
        pieces = state.pieces_dic[colour]
        enemy_pieces = []
        for key in state.pieces_dic.keys():
            if colour != key:
                enemy_pieces += state.pieces_dic[key]

        # Calculate different factors
        pieces_distance = heuristic(pieces, state.desti_dic[colour], state.exit_dic[colour])
        eat = eater(state, colour)
        # avoid_distance = heuristic(pieces, enemy_pieces, state.exit_dic[colour])
        bound_value = bound(pieces)
        exit_value = can_exit(state, colour)
        side_value = side(state, colour)
        danger_colour_value = danger_colour(state, colour)
        danger_pieces_value = danger_pieces(state, colour)
        if colour == state.colour:
            value = eat * self.eat_weight - pieces_distance * self.dist_weight \
                    + exit_value * self.exit_weight + bound_value * self.bound_weight \
                    - danger_colour_value * self.danger_colour_weight + side_value * \
                    self.side_weight - danger_pieces_value * self.danger_pieces_weight
        else:
            value = eat * self.eat_weight - pieces_distance * self.dist_weight

        # Get evaluation value in different situations and return value:
        # if ((state.action == "EXIT") or in_desti) and exit_value:
        #     value = eat * self.eat_weight - pieces_distance * self.dist_weight\
        #             + exit_value * self.exit_weight + avoid_distance * \
        #             self.avoid_weight + side_value * self.side_weight + \
        #             bound_value * self.bound_weight
        #     # print("USE VALUE 1")
        # elif (exit_value < 0) and (avoid_distance > 2):
        #     value = eat * self.eat_weight + pieces_distance * self.dist_weight\
        #             + bound_value * self.bound_weight + side_value * self.side_weight
        #     # print("USE VALUE 2")
        # else:
        #     value = eat * self.eat_weight - pieces_distance * self.dist_weight\
        #             + exit_value * self.exit_weight + bound_value * self.bound_weight\
        #             + side_value * self.side_weight
        #     # print("USE VALUE 3")
        return value


def heuristic(pieces, desti, exit_value):
    """Calculate the distance to the destination. If the player has equal to or less
    than four pieces, return average distance of all pieces. If the player has more
    than four pieces, only return the average distance of closest four pieces ( including
    exit pieces). """

    total_heur = 0
    if len(pieces) == 0 and (exit_value < 4):
        return float("inf")

    pieces_distance = []
    for piece in pieces:
        heur_list = []
        for end in desti:
            piece_z = - piece[0] - piece[1]
            end_z = - end[0] - end[1]
            heur_list.append((abs(piece[0] - end[0]) + abs(piece[1] - end[1]) +
                              abs(piece_z - end_z)) / 2 + 1)
        if len(heur_list) > 0:
            pieces_distance.append(min(heur_list))

    if (len(pieces) + exit_value) < 4:
        for value in pieces_distance:
            total_heur += value
        return total_heur/len(pieces_distance)
    elif exit_value == 4:
        return float("-inf")
    else:
        for i in range(4-exit_value):
            total_heur += min(pieces_distance)
            pieces_distance.remove(min(pieces_distance))
        return total_heur/(4-exit_value)


def eater(state, colour):
    """Return the value our own pieces (including exit pieces)"""

    return len(state.pieces_dic[colour]) + state.exit_dic[colour]


def bound(pieces):
    """Calculate number of our own pieces around every pieces.
    The value will be higher if pieces bounded together"""

    if len(pieces) == 0:
        return 0
    bound_value = 0
    for piece in pieces:
        for change in NEIGHBOR:
            neigh = [piece[0] + change[0], piece[1] + change[1]]
            if neigh in pieces:
                bound_value += 1
    return bound_value/len(pieces)


def can_exit(state, colour):
    """Return number of exited pieces if we have more than four pieces
    Return -1 if we cannot win the game use the pieces we have"""

    if (state.exit_dic[colour] + len(state.pieces_dic[colour])) >= 4:
        return state.exit_dic[colour]
    else:
        return -1


def side(state, colour):
    """Return a relative side value to make pieces get higher marks at the
    sides of the board, especially at the corner since it safer"""

    if len(state.pieces_dic[colour]) == 0:
        return float("-inf")
    side_value = 0
    for piece in state.pieces_dic[colour]:
        if (piece[0] == -3) or (piece[0] == 3):
            side_value += 1
        if (piece[1] == 3) or (piece[1] == -3):
            side_value += 1
        if ((piece[0] + piece[1]) == 3) or ((piece[0] + piece[1]) == 3):
            side_value += 1
        for board_colour in state.pieces_dic.keys():
            if colour != board_colour:
                if piece in state.desti_dic[board_colour]:
                    side_value += 1
    return side_value / len(state.pieces_dic[colour])


def danger_colour(state, colour):
    """Return how many opponent can eat our pieces in next round"""

    danger_value = 0
    for opponent in state.pieces_dic.keys():
        dangerous = 0
        if opponent != colour:
            for piece in state.pieces_dic[colour]:
                for change in NEIGHBOR:
                    new_piece = [piece[0] + change[0], piece[1] + change[1]]
                    if new_piece in state.pieces_dic[opponent]:
                        opposite_piece = [piece[0] - change[0], piece[1] - change[1]]
                        if not piece_in_board(opposite_piece):
                            continue
                        if opposite_piece not in get_all_pieces(state):
                            dangerous = 1
        if dangerous == 1:
            danger_value += 1
    return danger_value


def danger_pieces(state, colour):
    """Return how many pieces are exposed to opponents in nest round"""

    danger_pieces_value = 0
    for piece in state.pieces_dic[colour]:
        dangerous = 0
        for change in NEIGHBOR:
            new_piece = [piece[0] + change[0], piece[1] + change[1]]
            if (new_piece in get_all_pieces(state)) and (new_piece not in state.pieces_dic[colour]):
                opposite_piece = [piece[0] - change[0], piece[1] - change[1]]
                if not piece_in_board(opposite_piece):
                    continue
                if opposite_piece not in get_all_pieces(state):
                    dangerous = 1
        if dangerous == 1:
            danger_pieces_value += 1
    return danger_pieces_value




