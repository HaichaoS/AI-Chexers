from random import randrange


def evaluate(state):

    return {"red": randrange(-10, 10),
            "green": randrange(-10, 10),
            "blue": randrange(-10, 10)}
