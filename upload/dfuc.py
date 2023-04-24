import random

def dfuc(im):
    # create an array that generates 4 numbers randomly between 0 and 1 and rounds them to 2 decimal places
    random_floats = [round(random.uniform(0, 1), 4) for _ in range(4)]

    return random_floats
