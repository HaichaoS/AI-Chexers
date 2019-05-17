from your_team_name.State import *

COLOURS = ["red", "green", "blue"]


class Evaluate:

    def __init__(self, colour, state):
        self.colour = colour
        self.state = state
        self.eat_weight = 100
        self.dist_weight = 1
        # self.exit_weight = 10
        # self.avoid_weight = 0.01
        # self.bound_weight = 0.1
        # self.enemy1_eat_weight = 0
        # self.enemy1_dist_weight = 0.1
        # self.enemy2_eat_weight = 0
        # self.enemy2_dist_weight = 0.1

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
        # print("colour:", colour)
        # print("action: ", state.action)
        # print("before:  ", state.before)
        # print("after: ", state.after)
        pieces_distance = heuristic(pieces, state.desti_dic[colour], state.exit_dic[colour])
        eat = eater(state, colour)
        avoid_distance = avoid(pieces, enemy_pieces)
        bound_value = bound(pieces)
        exit_value = can_exit(state, colour):
        value = eat * self.eat_weight - pieces_distance * self.dist_weight
        return value

        # if colour == state.colour:
        #     value = self.evaluate_self(state, colour)
        # elif colour == state.enemy1_colour:
        #     value = self.evaluate_enemy1(state, colour)
        # else:
        #     value = self.evaluate_enemy2(state, colour)
        # return value

    # def evaluate_self(self, state, colour):
    #     pieces = state.pieces
    #     enemy_pieces = state.enemy1_pieces + state.enemy2_pieces
    #     pieces_distance = heuristic(pieces, state.desti_dic[colour])
    #     eat = eater(pieces, enemy_pieces)
    #     value = (eat + state.exit_value) * self.eat_weight - pieces_distance * self.dist_weight
    #     return value

    # def evaluate_enemy1(self, state, colour):
    #     pieces = state.enemy1_pieces
    #     enemy_pieces = state.pieces + state.enemy2_pieces
    #     pieces_distance = heuristic(pieces, state.desti_dic[colour])
    #     eat = eater(pieces, enemy_pieces)
    #     value = (eat + state.exit_value) * self.enemy1_eat_weight - pieces_distance * self.enemy1_dist_weight
    #     return value
    #
    # def evaluate_enemy2(self, state, colour):
    #     pieces = state.enemy2_pieces
    #     enemy_pieces = state.pieces + state.enemy1_pieces
    #     pieces_distance = heuristic(pieces, state.desti_dic[colour])
    #     eat = eater(pieces, enemy_pieces)
    #     value = (eat + state.exit_value) * self.enemy2_eat_weight - pieces_distance * self.enemy2_dist_weight
    #     return value


def heuristic(start, desti, exit_value):

    total_heur = 0
    if len(start) == 0:
        return 0
    else:
        exit_node = []
        # print("length:", start)
        for node in start:
            heur_list = []
            for end in desti:
                node_z = - node[0] - node[1]
                end_z = - end[0] - end[1]
                heur_list.append((abs(node[0] - end[0]) + abs(node[1] - end[1]) + abs(node_z - end_z)) / 2 + 1)
            exit_node.append(min(heur_list))

        # print(exit_node)
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


def avoid(mine, enemy):
    enemy_avoid = 0
    if (len(mine) == 0) or (len(enemy) == 0):
        return 0
    else:
        for node in mine:
            enemy_list = []
            for end in enemy:
                node_z = - node[0] - node[1]
                end_z = - end[0] - end[1]
                enemy_list.append((abs(node[0] - end[0]) + abs(node[1] - end[1]) + abs(node_z - end_z)) / 2 + 1)
            enemy_avoid += min(enemy_list)
    return enemy_avoid


def eater(state, colour):
    return len(state.pieces_dic[colour]) + state.exit_dic[colour]


def bound(pieces):
    bound_value = 0
    for piece in pieces:
        for change in NEIGHBOR:
            neigh = [piece[0] + change[0], piece[1] + change[1]]
            if neigh in pieces:
                bound_value += 1
    return bound_value

# def desti(state, colour):
#     desti_value = 0
#     for piece in state.pieces_dic[colour]:
#         if piece in state.desti_dic[colour]:
#             desti_value += 1
#     return desti_value

def can_exit(state, colour):
    if (state.exit_dic[colour] + len(state.pieces_dic[colour])) >= 4:
        return state.exit_dic[colour]
    else:
        return -1





