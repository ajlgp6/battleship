import pygame, sys, time, threading
import consts as c
from menu import soundSettings
from pygame.locals import *

from network import Client
from grid import Grid

grid = Grid()
opponent = Grid()
grid_size = 0
screen = None
clock = pygame.time.Clock()
chooseAI = False
bothAI = False
smart_AI = False

#music setup
pygame.mixer.init()
pygame.mixer.music.load("assets/sound/mainmenu_bg.mp3")
pygame.mixer.music.set_endevent(QUIT)
pygame.mixer.music.play()

# Data for ships that aren't placed
unplaced = dict()
allPlaced = False

# Multiplayer
client = None
opponentId = ""
doGameLoop = True

#set display size
WINDOW_SIZE = (900, 620)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
#get image
background_image = pygame.image.load("assets/background1.jpg")
#scale image
background_image = pygame.transform.scale(background_image, WINDOW_SIZE)


#get sprites
grape = pygame.image.load("assets/sprites/grape.png")
apple = pygame.image.load("assets/sprites/apple.png")
orange = pygame.image.load("assets/sprites/orange.png")
strawberry = pygame.image.load("assets/sprites/strawberry.png")
watermelon = pygame.image.load("assets/sprites/watermelon.png")
background = pygame.image.load("assets/sprites/background.jpg")
splatter = pygame.image.load("assets/sprites/splatter.png")
'''
Notes for myself:
-in order to add fruit sprite, change the mapping at the bottom of this file
-add individual fruit per square (orange, apple, strawberry, kiwi, grapes)
-change the ship hit to fruit splatter

-change SHIP const to different types to differentiate fruits
-change SHIPCOLOR and SHIPGRID occurences to incorporate more than one color
-use getSize to differentiate ships or getID
'''


def draw_text(text, color, surface, x, y):
    #set font
    font = pygame.font.SysFont(None, 30)
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def main_menu():
    pygame.init()
    pygame.display.set_caption('Battlefruit')

    #background music to play over menu
    pygame.mixer.music.load("assets/sound/mainmenu_bg.mp3")
    pygame.mixer.music.set_endevent(QUIT)
    pygame.mixer.music.play(-1)

    click = False
    
    while True:
        pygame.display.set_mode(WINDOW_SIZE,0,32)
        #set picture
        screen.blit(background_image, (0,0))
        screen.blit(grape, (310,150))
        screen.blit(apple, (460,20))
        screen.blit(orange, (615,90))
        screen.blit(strawberry, (760,0))
        screen.blit(watermelon, (750,210))

        #get mouse position
        mx, my = pygame.mouse.get_pos()

        #creating button
        button_1 = pygame.Rect(50, 100, 200, 50)
        #button_2 = pygame.Rect(50, 200, 200, 50)
        button_3 = pygame.Rect(50, 200, 200, 50)
        button_4 = pygame.Rect(50, 300, 200, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                #setup()
                #pygame.mixer.music.set_volume(0.5)
                AIselection()
        if button_3.collidepoint((mx, my)):
            if click:
                draw_text('Sound Settings', (0,0,0), screen, 220, 220)
                #soundSettings()
                soundSettings()
        if button_4.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()

        #display of button
        pygame.draw.rect(screen, (0, 0, 0), (48, 98, 204, 54))
        pygame.draw.rect(screen, (25, 70, 227), button_1)
        pygame.draw.rect(screen, (0, 0, 0), (48, 198, 204, 54))
        pygame.draw.rect(screen, (25, 70, 227), button_3)
        pygame.draw.rect(screen, (0, 0, 0), (48, 298, 204, 54))
        pygame.draw.rect(screen, (25, 70, 227), button_4)

        #on top because after the display of button
        draw_text('Play', (0,0,0), screen, 150, 125)
        draw_text('Sound Settings', (0,0,0), screen, 150, 225)
        draw_text('Quit', (0,0,0), screen, 150, 325)

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

def AIselection():
    global chooseAI, bothAI
    running = True
    click = False
    while running:
        pygame.display.set_mode(WINDOW_SIZE,0,32)
        screen.blit(background_image, (0,0))
        screen.blit(grape, (310,150))
        screen.blit(apple, (460,20))
        screen.blit(orange, (615,90))
        screen.blit(strawberry, (760,0))
        screen.blit(watermelon, (750,210))
        #get mouse position
        mx, my = pygame.mouse.get_pos()
        
        #creating button
        button_1 = pygame.Rect(50, 100, 200, 50)
        button_2 = pygame.Rect(50, 200, 200, 50)
        button_3 = pygame.Rect(50, 300, 200, 50)
        button_4 = pygame.Rect(50, 400, 200, 50)
        
        #if button_1.collidepoint((mx, my)):
            #if click:
                #setup()
        if button_2.collidepoint((mx, my)):
            if click:
                chooseAI = True
                AIdifficult()
                #draw_text('Game Settings', (0,0,0), screen, 220, 220)
        if button_3.collidepoint((mx, my)):
            if click:
                setup()
        if button_4.collidepoint((mx, my)):
            if click:
                running = False
        
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
        draw_text('AI vs AI', (0,0,0), screen, 150, 125)
        draw_text('Player vs AI', (0,0,0), screen, 150, 225)
        draw_text('Player vs Player', (0,0,0), screen, 150, 325)
        draw_text('Back', (0,0,0), screen, 150, 425)

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
        
def AIdifficult():
    global smart_AI

    running = True
    click = False
    while running:
        pygame.display.set_mode(WINDOW_SIZE,0,32)
        screen.blit(background_image, (0,0))
        #get mouse position
        mx, my = pygame.mouse.get_pos()
        
        #creating button
        button_1 = pygame.Rect(50, 100, 200, 50)
        button_2 = pygame.Rect(50, 200, 200, 50)
        button_3 = pygame.Rect(50, 300, 200, 50)
        
        if button_1.collidepoint((mx, my)):
            if click:
                smart_AI = False
                setup()
        if button_2.collidepoint((mx, my)):
            if click:
                smart_AI = True
                setup()
        if button_3.collidepoint((mx, my)):
            if click:
                running = False
        
        #display of button
        pygame.draw.rect(screen, (0, 0, 0), (48, 98, 204, 54))
        pygame.draw.rect(screen, (25, 70, 227), button_1)
        pygame.draw.rect(screen, (0, 0, 0), (48, 198, 204, 54))
        pygame.draw.rect(screen, (25, 70, 227), button_2)
        pygame.draw.rect(screen, (0, 0, 0), (48, 298, 204, 54))
        pygame.draw.rect(screen, (25, 70, 227), button_3)

        #on top because after the display of button
        draw_text('Easy AI', (0,0,0), screen, 150, 125)
        draw_text('Hard AI', (0,0,0), screen, 150, 225)
        draw_text('Back', (0,0,0), screen, 150, 325)

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
    global bothAI

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
    pygame.display.set_caption(f"Place your fruit (game {joined})")

#in game options will have a choice to change the grid size
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
    count = 2
    while doGameLoop:
        client.updateStats(opponentDecreased, weDecreased)

        if client.ready:
            # Count is here to avoid requesting updates before the AI is ready
            if count < 0:
                refreshGrid(True)
            else:
                count -= 1

        time.sleep(0.5)

def opponentDecreased(remaining):
    print("Opponent ship sunk!")

    if client.opponentShipsPrev == 0:
        print("You win!")

    displayRemaining(remaining)

def weDecreased(remaining):
    print("Shp sunk :(")

    if client.ourShipsPrev == 0:
        print("You lose.")

    displayRemaining(remaining)

def displayRemaining(remaining):
    global doGameLoop

    print(f"{remaining} / 5 ships remain")
    if remaining == 0:
        doGameLoop = False

def display():
    global screen, doGameLoop
    global chooseAI, smart_AI

    length = 0
    dragging = ""       # the ship name that is currently being dragged
    dragRotate = False  # if the current ship has been rotated

    pygame.mixer.music.stop()

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
                    if state==2:
                        pygame.mixer.music.load('assets/sound/hit.mp3')
                        pygame.mixer.music.play(0)
                    if state==3:
                        pygame.mixer.music.load('assets/sound/miss.mp3')
                        pygame.mixer.music.play(0)
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


        # Blank the screen
        #screen.fill(c.Colors.BLACK)
        backgroundNew = pygame.transform.scale(background, WINDOW_SIZE)
        screen.blit(backgroundNew, (0,0))

        appleSprite = pygame.transform.scale(apple, (c.Drawing.SIZE, c.Drawing.SIZE))
        orangeSprite = pygame.transform.scale(orange, (c.Drawing.SIZE, c.Drawing.SIZE))
        strawberrySprite = pygame.transform.scale(strawberry, (c.Drawing.SIZE, c.Drawing.SIZE))
        watermelonSprite = pygame.transform.scale(watermelon, (c.Drawing.SIZE, c.Drawing.SIZE))

        # If all ships have been placed, draw our ships in the upper left and the opponents grid in the main screen
        if allPlaced:
            if(chooseAI):
                if(smart_AI):
                    client.send("smart_ai")
                else:
                    client.send("dumb_ai")
                chooseAI = False
            drawGrid(opponent)
            drawGrid(grid, True)
        else:
            drawGrid(grid)

        # Draw the ships (if any) that still need to be dragged into the grid
        for key in unplaced:
            if key == "carrier":
                #print(unplaced[key][0]," ",unplaced[key][1])
                #pygame.draw.rect(screen, c.Colors.SHIP2, unplaced[key])

                for i in range(5):
                    if dragRotate:
                        screen.blit(watermelonSprite, (int(unplaced["carrier"][0])+i*c.Drawing.SIZE, int(unplaced["carrier"][1])))
                    else:
                        screen.blit(watermelonSprite, (int(unplaced["carrier"][0]), int(unplaced["carrier"][1])+i*c.Drawing.SIZE))
                
            elif key == "battleship":
                #pygame.draw.rect(screen, c.Colors.SHIP1, unplaced[key])
                
                for i in range(4):
                    if dragRotate:
                        screen.blit(appleSprite, (int(unplaced["battleship"][0])+i*c.Drawing.SIZE, int(unplaced["battleship"][1])))
                    else:
                        screen.blit(appleSprite, (int(unplaced["battleship"][0]), int(unplaced["battleship"][1])+i*c.Drawing.SIZE))

                #screen.blit(appleSprite, (int(unplaced[key][0]), int(unplaced[key][1])))
                
            elif key == "cruiser1":
                #pygame.draw.rect(screen, c.Colors.SHIP3, unplaced[key])
                
                for i in range(3):
                    if dragRotate:
                        screen.blit(orangeSprite, (int(unplaced["cruiser1"][0])+i*c.Drawing.SIZE, int(unplaced["cruiser1"][1])))
                    else:
                        screen.blit(orangeSprite, (int(unplaced["cruiser1"][0]), int(unplaced["cruiser1"][1])+i*c.Drawing.SIZE))
                #screen.blit(orangeSprite, (int(unplaced[key][0]), int(unplaced[key][1])))
                
            elif key == "cruiser2":
                #pygame.draw.rect(screen, c.Colors.SHIP3, unplaced[key])
                
                for i in range(3):
                    if dragRotate:
                        screen.blit(orangeSprite, (int(unplaced["cruiser2"][0])+i*c.Drawing.SIZE, int(unplaced["cruiser2"][1])))
                    else:
                        screen.blit(orangeSprite, (int(unplaced["cruiser2"][0]), int(unplaced["cruiser2"][1])+i*c.Drawing.SIZE))
                #screen.blit(orangeSprite, (int(unplaced[key][0]), int(unplaced[key][1])))
                
            elif key == "patrol":
                #pygame.draw.rect(screen, c.Colors.SHIP4, unplaced[key])
                
                for i in range(2):
                    if dragRotate:
                        screen.blit(strawberrySprite, (int(unplaced["patrol"][0])+i*c.Drawing.SIZE, int(unplaced["patrol"][1])))
                    else:
                        screen.blit(strawberrySprite, (int(unplaced["patrol"][0]), int(unplaced["patrol"][1])+i*c.Drawing.SIZE))
                #screen.blit(strawberrySprite, (int(unplaced[key][0]), int(unplaced[key][1])))
                
            #pygame.draw.rect(screen, c.Colors.SHIP, unplaced[key]) #SHIPCOLOR

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

    #scaled sprites
    appleSprite = pygame.transform.scale(apple, (int(size), int(size)))
    orangeSprite = pygame.transform.scale(orange, (int(size), int(size)))
    strawberrySprite = pygame.transform.scale(strawberry, (int(size), int(size)))
    watermelonSprite = pygame.transform.scale(watermelon, (int(size), int(size)))
    splatterSprite = pygame.transform.scale(splatter, (int(size), int(size)))
    #backgroundNew = pygame.transform.scale(background, (int(size), int(size)))

    for row in range(c.Drawing.SQUARES):
        for col in range(c.Drawing.SQUARES):
            mapping = {
                c.Grid.EMPTY: c.Colors.WATER,
                c.Grid.SHIP1: c.Colors.SHIP1, #SHIPCOLOR
                c.Grid.SHIP2: c.Colors.SHIP2,
                c.Grid.SHIP3: c.Colors.SHIP3,
                c.Grid.SHIP4: c.Colors.SHIP4,
                c.Grid.MISSED: c.Colors.MISS,
                c.Grid.SHIP_HIT: c.Colors.SHIP_HIT
            }

            xCoord = (size + c.Drawing.MARGIN) * col + c.Drawing.MARGIN + delta
            yCoord = (size + c.Drawing.MARGIN) * row + c.Drawing.MARGIN

            state = grid[(row, col)]
            rect = [
                xCoord,
                yCoord,
                size,
                size
            ]
            if state == c.Grid.MISSED:
                pygame.draw.rect(screen, mapping[state], rect)
            elif state == c.Grid.SHIP_HIT:
                screen.blit(splatterSprite, (xCoord, yCoord))
            elif state == c.Grid.EMPTY and offset == False:
                pygame.draw.rect(screen, mapping[state], rect, 2)
            elif state == c.Grid.EMPTY and offset == True:
                pygame.draw.rect(screen, mapping[state], rect, 1)
            elif state == c.Grid.SHIP1:
                screen.blit(appleSprite, (xCoord, yCoord))
            elif state == c.Grid.SHIP2:
                screen.blit(watermelonSprite, (xCoord, yCoord))
            elif state == c.Grid.SHIP3:
                screen.blit(orangeSprite, (xCoord, yCoord))
            elif state == c.Grid.SHIP4:
                screen.blit(strawberrySprite, (xCoord, yCoord))
            #elif state == c.Grid.EMPTY:
            #    screen.blit(backgroundNew, (xCoord, yCoord))

# TODO: replace with proper logging library
def warn(msg):
    print(f"[WRN] {msg}")

#setup()
main_menu()
