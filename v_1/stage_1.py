import os
import enemy
import player
import pygame
from pygame.locals import *

MOVE_SPEED = 5
the_player = player.Player()
the_enemy = enemy.Enemy()

class Stage1():
	# global the_enemy, player, MOVE_SPEED
	
	def __init__(self):
		global the_player
		self.background = pygame.image.load(os.path.join('resources/graphics', 'background.png')).convert()
		the_player.rect.bottom = 400

	def update(self, keys):
		global the_player, the_enemy
		the_player.update(keys, the_enemy)
		if the_enemy.alive:
			the_enemy.update(the_player)
		else:
			the_enemy = enemy.Enemy()
		return 1

	def render(self, background):
		global the_enemy, the_player
		background.blit(self.background, (0,0))
		the_enemy.render(background)
		the_player.render(background)