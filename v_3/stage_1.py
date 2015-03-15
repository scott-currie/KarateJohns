import os
from enemy import Enemy
from player import Player
import pygame
from pygame.locals import *



class Stage1():

	def __init__(self):
		# global the_player
		self.background = pygame.image.load(os.path.join('resources/graphics', 'background.png')).convert()
		self.player = Player()
		self.enemy = Enemy()
		self.player.rect.bottom = 400

	def update(self, keys):
		self.player.update(keys, self.enemy)
		if self.enemy.alive:
			self.enemy.update(self.player)
		else:
			self.enemy = Enemy()
		return 1

	def render(self, background):
		background.blit(self.background, (0,0))
		self.enemy.render(background)
		self.player.render(background)