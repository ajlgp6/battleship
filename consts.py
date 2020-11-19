class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    WATER = (25, 210, 227)
    SHIP = (177, 177, 177)

    #FOR DIFFERENT FRUITS (red, green, orange, purple, pink)
    SHIP1 = (255, 0, 0) #APPLE
    SHIP2 = (0, 255, 0) #WATERMELON
    SHIP3 = (255, 165, 0) #ORANGE
    SHIP4 = (255, 192, 203) #STRAWBERRY 
    SHIP5 = (128, 0, 128) #GRAPES
    
    SHIP_HIT = (150, 75, 75)

    MISS = (25, 99, 227)

class Grid:
    EMPTY = 0
    #SHIP = 1
    SHIP1 = 1
    SHIP2 = 4
    SHIP3 = 5
    SHIP4 = 6
    MISSED = 2
    SHIP_HIT = 3

class Drawing:
    SQUARES = 10
    SIZE = 60
    MARGIN = 1

class Networking:
    BIND = "0.0.0.0"
    PORT = 2313
