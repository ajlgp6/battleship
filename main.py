import pygame
import consts as c
from grid import Grid
from ship import Ship

grid = Grid()
screen = None
clock = pygame.time.Clock()

def setup():
    global screen

    ships = []
    ships.append(Ship((0, 2), (0, 6)))  # carrier (5)
    ships.append(Ship((2, 4), (2, 7)))  # battleship (4)
    ships.append(Ship((2, 1), (4, 1)))  # cruiser (3)
    ships.append(Ship((4, 8), (6, 8)))  # cruiser (3)
    ships.append(Ship((7, 3), (7, 4)))  # patrol boat (2)
    for ship in ships:
        grid.addShip(ship)

    pygame.init()
    size = (c.Drawing.WIDTH + c.Drawing.MARGIN) * c.Drawing.SQUARES + c.Drawing.MARGIN
    screen = pygame.display.set_mode([size, size])

    display()

def display():
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(grid)
                done = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                buttons = pygame.mouse.get_pressed()
                isLeft = buttons[0]
                isRight = buttons[2]

                # pygame returns mouse coordinates relative to the top left of the window
                # Since we need to map that to the coordinate of a square, divide the mouse coordinates by the square dimensions
                screen_pos = pygame.mouse.get_pos()
                rel_pos = relativeToSquare(screen_pos)

                print(f"Click at {screen_pos} mapped to {rel_pos}")

                state = grid[rel_pos]
                newState = c.Grid.EMPTY
                """
                Left click: Fire
                Right click: Place ship
                """

                if isLeft:
                    if state == c.Grid.EMPTY:
                        newState = c.Grid.MISSED
                    elif state == c.Grid.SHIP:
                        newState = c.Grid.SHIP_HIT
                    else:
                        warn(f"Unknown grid state {state}")
                        continue
                elif isRight and state == c.Grid.EMPTY:
                    newState = c.Grid.SHIP
                else:
                    warn(f"Unknown mouse button. State of buttons: {buttons}")
                    continue
                grid.update(rel_pos, newState)

            screen.fill(c.Colors.BLACK)
            for row in range(c.Drawing.SQUARES):
                for col in range(c.Drawing.SQUARES):
                    mapping = {
                        c.Grid.EMPTY: c.Colors.WATER,
                        c.Grid.SHIP: c.Colors.SHIP,
                        c.Grid.MISSED: c.Colors.MISS,
                        c.Grid.SHIP_HIT: c.Colors.SHIP_HIT
                    }

                    state = grid[(row, col)]
                    rect = [
                        (c.Drawing.WIDTH + c.Drawing.MARGIN) * col + c.Drawing.MARGIN,
                        (c.Drawing.WIDTH + c.Drawing.MARGIN) * row + c.Drawing.MARGIN,
                        c.Drawing.WIDTH,
                        c.Drawing.WIDTH
                    ]
                    pygame.draw.rect(screen, mapping[state], rect)

            clock.tick(100)
            pygame.display.flip()

def relativeToSquare(point):
    divisor = c.Drawing.WIDTH + c.Drawing.MARGIN
    return (point[1] // divisor, point[0] // divisor)

# TODO: replace with proper logging library
def warn(msg):
    print(f"[WRN] {msg}")

setup()
