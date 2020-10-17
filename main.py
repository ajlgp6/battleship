import pygame
import consts as c
from grid import Grid
from ship import Ship

grid = Grid()
grid_size = 0
screen = None
clock = pygame.time.Clock()

# Data for ships that aren't placed
unplaced = dict()

def setup():
    global screen
    global grid_size
    global unplaced

    pygame.init()

    grid_size = (c.Drawing.SIZE + c.Drawing.MARGIN) * c.Drawing.SQUARES + c.Drawing.MARGIN

    # Since the unplaced ships are on the right of the board, we need to add room for two columns of ships
    width = grid_size + c.Drawing.SIZE * 2 + 35
    screen = pygame.display.set_mode([width, grid_size])

    # Setup all unplaced ships (carrier, battleship, cruiser 1, cruiser 2, and patrol boat)
    # The first column only has room for two ships - the carrier (5) and the battleship (4)
    margin = c.Drawing.MARGIN + 15
    initial_x = grid_size + margin
    unplaced["carrier"] = [initial_x, c.Drawing.MARGIN, c.Drawing.SIZE, c.Drawing.SIZE * 5]
    unplaced["battleship"] = [initial_x, unplaced["carrier"][3] + (c.Drawing.MARGIN * 3), c.Drawing.SIZE, c.Drawing.SIZE * 4]

    # The second column can fit all of the other ships - the two cruisers (3) and the patrol boat (2)
    margin -= 5
    initial_x += c.Drawing.SIZE + margin
    unplaced["cruiser1"] = [initial_x, c.Drawing.MARGIN, c.Drawing.SIZE, c.Drawing.SIZE * 3]
    unplaced["cruiser2"] = [initial_x, unplaced["cruiser1"][3] + (c.Drawing.MARGIN * 3), c.Drawing.SIZE, c.Drawing.SIZE * 3]
    unplaced["patrol"] = [initial_x, unplaced["cruiser2"][3] + unplaced["cruiser2"][1] + (c.Drawing.MARGIN * 3), c.Drawing.SIZE, c.Drawing.SIZE * 2]

    display()

def display():
    global grid_size
    global unplaced

    dragging = ""       # the ship name that is currently being dragged
    dragRotate = False

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(grid)
                done = True

            elif event.type == pygame.MOUSEBUTTONUP and dragging != "":
                pos = pygame.mouse.get_pos()
                rel_pos = relativeToSquare(pos)

                index = 3
                if dragRotate:
                    index = 2

                height = (unplaced[dragging][index] // c.Drawing.SIZE) - 1

                ship_pos = (rel_pos[0] + height, rel_pos[1])
                if dragRotate:
                    ship_pos = (rel_pos[0], rel_pos[1] + height)

                grid.addShip(Ship(rel_pos, ship_pos))
                unplaced.pop(dragging)
                dragging = ""
                dragRotate = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                buttons = pygame.mouse.get_pressed()
                isLeft = buttons[0]

                # pygame returns mouse coordinates relative to the top left of the window
                # Since we need to map that to the coordinate of a square, divide the mouse coordinates by the square dimensions
                screen_pos = pygame.mouse.get_pos()
                if screen_pos[0] < grid_size:
                    # The user clicked inside the placed ship grid
                    rel_pos = relativeToSquare(screen_pos)

                    state = grid[rel_pos]
                    newState = c.Grid.EMPTY

                    if isLeft:
                        if state == c.Grid.EMPTY:
                            newState = c.Grid.MISSED
                        elif state == c.Grid.SHIP:
                            newState = c.Grid.SHIP_HIT
                        else:
                            warn(f"Unknown grid state {state}")
                            continue
                    else:
                        warn(f"Unknown mouse button. State of buttons: {buttons}")
                        continue
                    grid.update(rel_pos, newState)
                else:
                    # The user clicked outside the grid and must be attempting to drag a ship
                    ship = relativeToShip(screen_pos)
                    if ship != "":
                        dragging = ship

            elif event.type == pygame.MOUSEMOTION:
                if dragging != "":
                    pos = pygame.mouse.get_pos()
                    unplaced[dragging][0] = pos[0] - c.Drawing.SIZE / 2.5
                    unplaced[dragging][1] = pos[1] - c.Drawing.SIZE / 2.5

            elif event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()

                # Rotate dragged ship
                if (pressed[pygame.K_r] or pressed[pygame.K_e]) and dragging != "":
                    unplaced[dragging][2], unplaced[dragging][3] = unplaced[dragging][3], unplaced[dragging][2]
                    dragRotate = not dragRotate

                # Quit
                elif pressed[pygame.K_q]:
                    done = True

            # Blank the screen
            screen.fill(c.Colors.BLACK)

            # Draw the ships in the grid
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
                        (c.Drawing.SIZE + c.Drawing.MARGIN) * col + c.Drawing.MARGIN,
                        (c.Drawing.SIZE + c.Drawing.MARGIN) * row + c.Drawing.MARGIN,
                        c.Drawing.SIZE,
                        c.Drawing.SIZE
                    ]
                    pygame.draw.rect(screen, mapping[state], rect)

            # Draw the ships (if any) that still need to be dragged into the grid
            for key in unplaced:
                pygame.draw.rect(screen, c.Colors.SHIP, unplaced[key])

            # Render ("flip") the display
            clock.tick(1000)
            pygame.display.flip()

def relativeToSquare(point):
    divisor = c.Drawing.SIZE + c.Drawing.MARGIN
    return (point[1] // divisor, point[0] // divisor)

def relativeToShip(point):
    global unplaced

    x = point[0]
    y = point[1]
    for key in unplaced:
        ship = unplaced[key]

        if x < ship[0] or y < ship[1]:
            continue
        elif x > ship[0] + ship[2] or y > ship[1] + ship[3]:
            continue

        return key

    return ""

# TODO: replace with proper logging library
def warn(msg):
    print(f"[WRN] {msg}")

setup()
