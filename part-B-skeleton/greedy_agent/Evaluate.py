
COLOURS = ["red", "green", "blue"]


class Evaluate:
    """Greedy Algorithm evaluation agent
    Only consider eating and exiting. Prefer to eat when it can
    and make steps to exit"""

    def __init__(self, colour, state):
        self.colour = colour
        self.state = state
        self.eat_weight = 100
        self.dist_weight = 1
        self.exit_weight = 1000

    def evaluate_create(self, state, colour):
        values = {"red": None,
                  "green": None,
                  "blue": None}
        value = self.evaluate(state, colour)
        values[colour] = value
        return values

    def evaluate_add(self, values, state, colour):

        value = self.evaluate(state, colour)
        values[colour] = value

    def evaluate(self, state, colour):

        pieces = state.pieces_dic[colour]
        enemy_pieces = []
        for key in state.pieces_dic.keys():
            if colour != key:
                enemy_pieces += state.pieces_dic[key]
        pieces_distance = heuristic(pieces, state.desti_dic[colour], state.exit_dic[colour])
        eat = eater(state, colour)
        value = eat * self.eat_weight - pieces_distance * self.dist_weight + \
            state.exit_dic[colour] * self.exit_weight
        return value


def heuristic(start, desti, exit_value):

    total_heur = 0
    if len(start) == 0:
        return 0
    else:
        exit_node = []
        for node in start:
            heur_list = []
            for end in desti:
                node_z = - node[0] - node[1]
                end_z = - end[0] - end[1]
                heur_list.append((abs(node[0] - end[0]) + abs(node[1] - end[1]) + abs(node_z - end_z)) / 2 + 1)
            exit_node.append(min(heur_list))

        if (len(exit_node) + exit_value) <= 4:
            for value in exit_node:
                total_heur += value
            return total_heur/len(exit_node) - exit_value
        elif exit_value == 4:
            return 0
        else:
            for i in range(4-exit_value):
                total_heur += min(exit_node)
                exit_node.remove(min(exit_node))
            return total_heur/(4-exit_value) - exit_value


def eater(state, colour):
    return len(state.pieces_dic[colour]) + state.exit_dic[colour]





