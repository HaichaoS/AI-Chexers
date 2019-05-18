"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part B: Playing the Game
Authors: Haichao Song, Haolin Zhou
"""

from your_team_name.State import *


class Evaluate:
    """Describe the evaluation agent that calculate a value for every state
    in the game. Therefore maxn can make decision on which state is the best
     to perform"""

    def __init__(self, colour, state):
        self.colour = colour
        self.state = state
        self.eat_weight = 100
        self.exit_weight = 100
        self.dist_weight = 1
        self.bound_weight = 0.1
        self.avoid_weight = 0.01
        self.side_weight = 0.01

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
        avoid_distance = avoid(pieces, enemy_pieces)
        bound_value = bound(pieces)
        exit_value = can_exit(state, colour)
        side_value = side(state, colour)

        # Get evaluation value in different situations and return value:
        if (state.action == "EXIT") and exit_value:
            value = eat * self.eat_weight - pieces_distance * self.dist_weight\
                    + exit_value * self.exit_weight + bound_value * \
                    self.bound_weight + avoid_distance * self.avoid_weight
        elif (exit_value < 0) and (avoid_distance > 2):
            value = eat * self.eat_weight + pieces_distance * self.dist_weight\
                    + bound_value * self.bound_weight + side_value * self.side_weight
        else:
            value = eat * self.eat_weight - pieces_distance * self.dist_weight\
                    + exit_value * self.exit_weight + bound_value * self.bound_weight
        return value


def heuristic(pieces, desti, exit_value):
    """Calculate the distance to the destination. If the player has equal to or less
    than four pieces, return average distance of all pieces. If the player has more
    than four pieces, only return the average distance of closest four pieces ( including
    exit pieces). """

    total_heur = 0
    if len(pieces) == 0:
        return 0
    else:
        pieces_distance = []
        for piece in pieces:
            heur_list = []
            for end in desti:
                piece_z = - piece[0] - piece[1]
                end_z = - end[0] - end[1]
                heur_list.append((abs(piece[0] - end[0]) + abs(piece[1] - end[1]) +
                                  abs(piece_z - end_z)) / 2 + 1)
            pieces_distance.append(min(heur_list))

        if (len(pieces) + exit_value) <= 4:
            for value in pieces_distance:
                total_heur += value
            return total_heur/len(pieces_distance)
        elif exit_value == 4:
            return 0
        else:
            for i in range(4-exit_value):
                total_heur += min(pieces_distance)
                pieces_distance.remove(min(pieces_distance))
            return total_heur/(4-exit_value)


def avoid(mine, enemy):
    """Calculate the distance to enemy pieces. Return the average distance to
    the closest enemy piece for every own pieces"""

    enemy_avoid = 0
    if (len(mine) == 0) or (len(enemy) == 0):
        return 0
    else:
        for node in mine:
            enemy_list = []
            for end in enemy:
                node_z = - node[0] - node[1]
                end_z = - end[0] - end[1]
                enemy_list.append((abs(node[0] - end[0]) + abs(node[1] - end[1]) +
                                   abs(node_z - end_z)) / 2 + 1)
            enemy_avoid += min(enemy_list)
    return enemy_avoid/len(mine)


def eater(state, colour):
    """Return the value our own pieces (including exit pieces)"""

    return len(state.pieces_dic[colour]) + state.exit_dic[colour]


def bound(pieces):
    """Calculate number of our own pieces around every pieces.
    The value will be higher if pieces bounded together"""

    bound_value = 0
    for piece in pieces:
        for change in NEIGHBOR:
            neigh = [piece[0] + change[0], piece[1] + change[1]]
            if neigh in pieces:
                bound_value += 1
    return bound_value


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
    return side_value





