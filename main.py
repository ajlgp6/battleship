import pygame, sys, time, threading
import consts as c
from pygame.locals import *

from network import Client
from grid import Grid

grid = Grid()
opponent = Grid()
grid_size = 0
screen = None
clock = pygame.time.Clock()

# Data for ships that aren't placed
unplaced = dict()
allPlaced = False

# Multiplayer
client = None
opponentId = ""
doGameLoop = True

def draw_text(text, color, surface, x, y):
	#set font
	font = pygame.font.SysFont(None, 30)
	textobj = font.render(text, 1, color)
	textrect = textobj.get_rect()
	textrect.center = (x, y)
	surface.blit(textobj, textrect)

def main_menu():
	pygame.init()
	pygame.display.set_caption('Battleship')
	#set display size
	WINDOW_SIZE = (900, 620)
	screen = pygame.display.set_mode(WINDOW_SIZE,0,32)

	#get image
	background_image = pygame.image.load('battleship.jpg')
	#scale image
	background_image = pygame.transform.scale(background_image, WINDOW_SIZE)

	click = False

	pygame.mixer.init()
	pygame.mixer.music.load("assets/sound/mainmenu_bg.mp3")
	pygame.mixer.music.set_endevent(QUIT)
	#pygame.mixer.music.play()

	while True:
		#set picture
		screen.blit(background_image, (0,0))
		#get mouse position
		mx, my = pygame.mouse.get_pos()

		#creating button
		button_1 = pygame.Rect(50, 100, 200, 50)
		button_2 = pygame.Rect(50, 200, 200, 50)
		button_3 = pygame.Rect(50, 300, 200, 50)
		button_4 = pygame.Rect(50, 400, 200, 50)
		if button_1.collidepoint((mx, my)):
			if click:
				setup()
		if button_2.collidepoint((mx, my)):
			if click:
				draw_text('Game Settings', (0,0,0), screen, 220, 220)
		if button_3.collidepoint((mx, my)):
			if click:
				draw_text('Options', (0,0,0), screen, 220, 220)
		if button_4.collidepoint((mx, my)):
			if click:
				pygame.quit()
				sys.exit()

		#display of button
		pygame.draw.rect(screen, (0, 0, 0), (48, 98, 204, 54))
		pygame.draw.rect(screen, (25, 70, 227), button_1)
		pygame.draw.rect(screen, (0, 0, 0), (48, 198, 204, 54))
		pygame.draw.rect(screen, (25, 70, 227), button_2)
		pygame.draw.rect(screen, (0, 0, 0), (48, 298, 204, 54))
		pygame.draw.rect(screen, (25, 70, 227), button_3)
		pygame.draw.rect(screen, (0, 0, 0), (48, 398, 204, 54))
		pygame.draw.rect(screen, (25, 70, 227), button_4)

		#on top because after the display of button
		draw_text('Play', (0,0,0), screen, 150, 125)
		draw_text('Game Settings', (0,0,0), screen, 150, 225)
		draw_text('Options', (0,0,0), screen, 150, 325)
		draw_text('Quit', (0,0,0), screen, 150, 425)

		click = False
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True

		pygame.display.update()
		clock.tick(60)

def setup():
    global screen, grid_size
    global client, doGameLoop

    code = input("Enter game code (or blank to create a new game): ")

    # Connect to the server
    server = "127.0.0.1"
    if len(sys.argv) == 2:
        server = sys.argv[1]
    print(f"Connecting server at to {server}...")

    client = Client(server)
    try:
        joined = client.connect(code)
        if code == "":
            print(f"Created game {joined}")
    except Exception as ex:
        exit(f"Unable to connect to server: {ex}")

    pygame.init()
    pygame.display.set_caption('Place your ships')

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

    displayThread = threading.Thread(target = display)
    displayThread.start()

    # Check for updates from the server
    while doGameLoop:
        client.send("stats")
        stats = client.recv().split(",")
        if len(stats) < 1:
            continue

        client.debug(stats)

        try:
            # Opponent ready
            if stats[0] == "ready":
                refreshGrid(True)
        except:
            pass

        time.sleep(1)

def display():
    global screen, doGameLoop

    dragging = ""       # the ship name that is currently being dragged
    dragRotate = False  # if the current ship has been rotated

    while doGameLoop:
        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            doGameLoop = False
            sys.exit(0)

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

            if client.placeShip(rel_pos, ship_pos):
                unplaced.pop(dragging)

            dragging = ""
            dragRotate = False

            # Check to see if the window needs to be resized
            checkUnplaced()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            buttons = pygame.mouse.get_pressed()
            isLeft = buttons[0]

            # pygame returns mouse coordinates relative to the top left of the window
            # Since we need to map that to the coordinate of a square, divide the mouse coordinates by the square dimensions
            screen_pos = pygame.mouse.get_pos()
            if screen_pos[0] < grid_size:
                # The user clicked inside the placed ship grid
                rel_pos = relativeToSquare(screen_pos)

                if isLeft:
                    state = client.fire(rel_pos)
                    if state != -1:
                        opponent.update(rel_pos, state)
                else:
                    warn(f"Unknown mouse button. State of buttons: {buttons}")
                    continue
            else:
                # The user clicked outside the grid and must be attempting to drag a ship
                ship = relativeToShip(screen_pos)
                if ship != "":
                    dragging = ship

        elif event.type == pygame.MOUSEMOTION:
            if dragging != "":
                pos = pygame.mouse.get_pos()
                unplaced[dragging][0] = pos[0] - (c.Drawing.SIZE / 2.5)
                unplaced[dragging][1] = pos[1] - (c.Drawing.SIZE / 2.5)

        elif event.type == pygame.KEYDOWN:
            pressed = pygame.key.get_pressed()

            # Rotate dragged ship
            if (pressed[pygame.K_r] or pressed[pygame.K_e]) and dragging != "":
                unplaced[dragging][2], unplaced[dragging][3] = unplaced[dragging][3], unplaced[dragging][2]
                dragRotate = not dragRotate

            # Quit
            elif pressed[pygame.K_q]:
                doGameLoop = False

            # Use ships from template 1
            elif pressed[pygame.K_1] and len(unplaced) == 5:
                client.placeShip((0, 2), (0, 6))        # carrier
                client.placeShip((2, 4), (2, 7))        # battleship
                client.placeShip((2, 1), (4, 1))        # cruiser
                client.placeShip((4, 8), (6, 8))        # cruiser
                client.placeShip((7, 3), (7, 4))        # patrol boat
                unplaced.clear()

                checkUnplaced()

            # Use ships from template 2
            elif pressed[pygame.K_2] and len(unplaced) == 5:
                client.placeShip((5, 8), (9, 8))
                client.placeShip((6, 2), (8, 2))
                client.placeShip((5, 5), (8, 5))
                client.placeShip((6, 0), (7, 0))
                client.placeShip((3, 7), (3, 9))

                unplaced.clear()

                checkUnplaced()

            elif pressed[pygame.K_a]:
                client.send("ai")

        # Blank the screen
        screen.fill(c.Colors.BLACK)

        # If all ships have been placed, draw our ships in the upper left and the opponents grid in the main screen
        if allPlaced:
            drawGrid(opponent)
            drawGrid(grid, True)
        else:
            drawGrid(grid)

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

def refreshGrid(checkOpponent = False):
    global grid, opponent

    client.updateGrid()
    updated = client.recv()
    grid.load(updated)

    if checkOpponent:
        client.updateOpponentGrid()
        updated = client.recv()
        opponent.load(updated)

def checkUnplaced():
    global screen, allPlaced

    if len(unplaced.keys()) == 0:
        screen = pygame.display.set_mode([int(grid_size * 1.47), grid_size])
        allPlaced = True

    refreshGrid()

def drawGrid(grid, offset=False):
    size = c.Drawing.SIZE
    delta = 0
    if offset:
        size //= 2.5
        delta = (c.Drawing.SIZE + c.Drawing.MARGIN) * 10 + 30

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
                (size + c.Drawing.MARGIN) * col + c.Drawing.MARGIN + delta,
                (size + c.Drawing.MARGIN) * row + c.Drawing.MARGIN,
                size,
                size
            ]
            pygame.draw.rect(screen, mapping[state], rect)

# TODO: replace with proper logging library
def warn(msg):
    print(f"[WRN] {msg}")

#setup()
main_menu()
