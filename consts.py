class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    WATER = (25, 210, 227)
    SHIP = (177, 177, 177)
    SHIP_HIT = (150, 75, 75)

    MISS = (25, 99, 227)

class Grid:
    EMPTY = 0
    SHIP = 1
    MISSED = 2
    SHIP_HIT = 3

class Drawing:
    SQUARES = 10
    SIZE = 60
    MARGIN = 1

class Networking:
    BIND = "0.0.0.0"
    PORT = 2313