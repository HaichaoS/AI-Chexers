NEIGHBOR = [[1, -1], [0, -1], [-1, 0], [1, 0], [-1, 1], [0, 1]]
COLOURS = ["red", "green", "blue"]


def evaluate_create(state, colour):

    values = {"red": None,
              "green": None,
              "blue": None}
    value = evaluate(state, colour)
    values[colour] = value

    return values


def evaluate_add(values, state, colour):

    value = evaluate(state, colour)
    values[colour] = value


def evaluate(state, colour):

    if colour == state.colour:
        pieces = state.pieces
        enemy_pieces = state.enemy1_pieces + state.enemy2_pieces
    elif colour == state.enemy1_colour:
        pieces = state.enemy1_pieces
        enemy_pieces = state.pieces + state.enemy2_pieces
    else:
        pieces = state.enemy2_pieces
        enemy_pieces = state.pieces + state.enemy1_pieces

    pieces_distance = heuristic(pieces, state.desti_dic[colour])
    enemy_avoid = avoid(pieces, enemy_pieces)
    eat = eater(pieces, enemy_pieces)
    value = (-pieces_distance/10) + (eat*4)
    return value


def heuristic(start, desti):

    total_heur = 0
    for node in start:
        heur_list = []
        for end in desti:
            node_z = - node[0] - node[1]
            end_z = - end[0] - end[1]
            heur_list.append((abs(node[0] - end[0]) + abs(node[1] - end[1]) + abs(node_z - end_z)) / 2 + 1)
        total_heur += min(heur_list)
    return total_heur


def avoid(mine, enemy):
    enemy_avoid = 0
    for piece in mine:
        for change in NEIGHBOR:
            new_piece = [piece[0] + change[0], piece[1] + change[1]]
            if new_piece in enemy:
                enemy_avoid -= 1
    return enemy_avoid


def eater(mine, enemy):
    return len(mine) - len(enemy)
