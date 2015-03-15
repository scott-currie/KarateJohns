import game_over
import main_menu
import os
import pygame
from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
screen = pygame.display.set_mode((640, 480))
import enemy
import stage_1
import sys

#--Constants
FPS = 30
#--Scenes
scenes = []
scenes.insert(0, main_menu.MainMenu())   # = main_menu.MainMenu()
scenes.insert(1, stage_1.Stage1())
scenes.insert(2, game_over.GameOver())
#--Sound
snd_theme = pygame.mixer.music.load(os.path.join('resources/sounds', 'tuff.wav'))
pygame.mixer.music.play(-1)
#--Controller
if pygame.joystick.get_count() > 0:
	controller = pygame.joystick.Joystick(0)
	controller.init()

def init_scenes():
	pass

def main():
	#--Set up display and background
	pygame.display.set_caption('Karate Johns v.01')
	background = pygame.Surface(screen.get_size())
	background.fill((255, 0, 0))
	background = background.convert()

	clock = pygame.time.Clock()
	scene = 0
	keys = [0, 0, 0, 0, 0, 0, 0, 0] #-- up, down, left, right, space, enter, z (punch), x (kick)

	while 1:
		# Event handling	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == K_UP:
					keys[0] = 1
				if event.key == K_DOWN:
					keys[1] = 1
				if event.key == K_LEFT:
					keys[2] = 1
				if event.key == K_RIGHT:
					keys[3] = 1
				if event.key == K_SPACE:
					keys[4] = 1
				if event.key == K_RETURN:
					keys[5] = 1
				if event.key == K_z:
					keys[6] = 1
				if event.key == K_x:
					keys[7] = 1
			if event.type == pygame.KEYUP:
				if event.key == K_UP:
					keys[0] = 0
				if event.key == K_DOWN:
					keys[1] = 0
				if event.key == K_LEFT:
					keys[2] = 0
				if event.key == K_RIGHT:
					keys[3] = 0
				if event.key == K_SPACE:
					keys[4] = 0
				if event.key == K_RETURN:
					keys[5] = 0
				if event.key == K_z:
					keys[6] = 0
				if event.key == K_x:
					keys[7] = 0
			if event.type == pygame.JOYHATMOTION:
				if event.dict['value'][0] == -1:
					keys[2] = 1
				elif event.dict['value'][0] == 1:
					keys[3] = 1
				else:
					'''Hat motion does not involve L/R movement. Set L/R keys to 0 '''
					keys[2] = 0
					keys[3] = 0
				if event.dict['value'][1] == -1:
					keys[1] = 1
				elif event.dict['value'][1] == 1:
					keys[0] = 1
				else:
					'''Hat motion does not involve U/D movement. Set U/D keys to 0 '''					
					keys[0] = 0
					keys[1] = 0	
			if event.type == pygame.JOYBUTTONDOWN:
				if event.dict['button'] == 0:
					keys[6] = 1	
				elif event.dict['button'] == 2:
					keys[7] = 1
			if event.type == pygame.JOYBUTTONUP:
				if event.dict['button'] == 0:
					keys[6] = 0
				elif event.dict['button'] == 2:
					keys[7] = 0
		# Update
		scene = scenes[scene].update(keys)

		#Render
		scenes[scene].render(background)
		screen.blit(background, (0,0))
		pygame.display.flip()

		#Finish loop
		clock.tick(FPS)

if __name__ == "__main__":
	main()