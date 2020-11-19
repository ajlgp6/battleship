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

grape = pygame.image.load("assets/sprites/grape.png")
apple = pygame.image.load("assets/sprites/apple.png")
orange = pygame.image.load("assets/sprites/orange.png")
strawberry = pygame.image.load("assets/sprites/strawberry.png")
watermelon = pygame.image.load("assets/sprites/watermelon.png")

def draw_text(text, color, surface, x, y):
	#set font
	font = pygame.font.SysFont(None, 30)
	textobj = font.render(text, 1, color)
	textrect = textobj.get_rect()
	textrect.center = (x, y)
	surface.blit(textobj, textrect)

def soundSettings():
	running = True
	click = False
	timer = 0
	update = False
	updating = False
	while running:
		pygame.display.set_mode(WINDOW_SIZE,0,32)
		screen.blit(background_image, (0,0))
		screen.blit(background_image, (0,0))
		screen.blit(grape, (310,150))
		screen.blit(apple, (460,20))
		screen.blit(orange, (615,90))
		screen.blit(strawberry, (760,0))
		screen.blit(watermelon, (750,210))
		#get mouse position
		mx, my = pygame.mouse.get_pos()
		
		#creating button
		button_1 = pygame.Rect(50, 80, 200, 50)
		button_2 = pygame.Rect(50, 150, 200, 50)
		button_3 = pygame.Rect(50, 220, 200, 50)
		button_4 = pygame.Rect(50, 290, 200, 50)
		button_5 = pygame.Rect(50, 360, 200, 50)
		button_6 = pygame.Rect(50, 430, 200, 50)
		
		if button_1.collidepoint((mx, my)):
			if click:
				pygame.mixer.music.set_volume(1.0)
				update = True
				new = "100%"
		if button_2.collidepoint((mx, my)):
			if click:
				pygame.mixer.music.set_volume(0.75)
				update = True
				new = "75%"
		if button_3.collidepoint((mx, my)):
			if click:
				pygame.mixer.music.set_volume(0.5)
				update = True
				new = "50%"
		if button_4.collidepoint((mx, my)):
			if click:
				pygame.mixer.music.set_volume(0.25)
				update = True
				new = "25%"
		if button_5.collidepoint((mx, my)):
			if click:
				pygame.mixer.music.set_volume(0.0)
				update = True
				new = "Muted"
		if button_6.collidepoint((mx, my)):
			if click:
				running = False
		
		if update:
			pygame.draw.rect(screen, (0,0,0), (348, 0, 204, 54))
			pygame.draw.rect(screen, (25, 130, 227), (350, 2, 200, 50))
			draw_text("Now "+new, (0,0,0), screen, 450, 27)
			timer += 1
			
		if (timer == 50):
			pygame.display.update()
			timer = 0
			update = False
		
		#display of button
		pygame.draw.rect(screen, (0, 0, 0), (48, 78, 204, 54))
		pygame.draw.rect(screen, (25, 70, 227), button_1)
		pygame.draw.rect(screen, (0, 0, 0), (48, 148, 204, 54))
		pygame.draw.rect(screen, (25, 70, 227), button_2)
		pygame.draw.rect(screen, (0, 0, 0), (48, 218, 204, 54))
		pygame.draw.rect(screen, (25, 70, 227), button_3)
		pygame.draw.rect(screen, (0, 0, 0), (48, 288, 204, 54))
		pygame.draw.rect(screen, (25, 70, 227), button_4)
		pygame.draw.rect(screen, (0, 0, 0), (48, 358, 204, 54))
		pygame.draw.rect(screen, (25, 70, 227), button_5)
		pygame.draw.rect(screen, (0, 0, 0), (48, 428, 204, 54))
		pygame.draw.rect(screen, (25, 70, 227), button_6)

		#on top because after the display of button
		draw_text('100%', (0,0,0), screen, 150, 105)
		draw_text('75%', (0,0,0), screen, 150, 175)
		draw_text('50%', (0,0,0), screen, 150, 245)
		draw_text('25%', (0,0,0), screen, 150, 315)
		draw_text('Mute', (0,0,0), screen, 150, 385)
		draw_text('Back', (0,0,0), screen, 150, 455)

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
		

