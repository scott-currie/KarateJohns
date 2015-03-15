import os
import pygame
import sys

SCALE = 8 
IMG_WIDTH = 26
IMG_HEIGHT = 28

class MainMenu():
	# SCALE = 8
	def __init__(self):
		global SCALE
		pygame.font.init()	#--Must include to prevent font not initialized error
		self.title_font = pygame.font.Font(os.path.join('resources/fonts', 'arcadeclassic.regular.ttf'), 60)
		self.menu_font = pygame.font.Font(os.path.join('resources/fonts', 'arcadeclassic.regular.ttf'), 22)

		self.image_0 = pygame.image.load(os.path.join('resources/graphics', 'john00.png'))			# 0 : idle right
		self.image_1 = pygame.image.load(os.path.join('resources/graphics', 'john01.png'))			# 1 : punch right 1
		self.image_2 = pygame.image.load(os.path.join('resources/graphics', 'john02.png'))			# 2 : punch right 2
		self.image_3 = pygame.image.load(os.path.join('resources/graphics', 'john03.png'))			# 3 : kick right 1
		self.image_4 = pygame.image.load(os.path.join('resources/graphics', 'john04.png'))			# 4 : kick right 2
		self.image_5 = pygame.image.load(os.path.join('resources/graphics', 'john10.png'))			# 5 : walk right
		self.image_6 = pygame.image.load(os.path.join('resources/graphics', 'john05.png'))			# 6 : idle left
		self.image_7 = pygame.image.load(os.path.join('resources/graphics', 'john11.png'))			# 7 : walk left		
		self.image_8 = pygame.image.load(os.path.join('resources/graphics', 'john06.png'))			# 8 : punch left 1
		self.image_9 = pygame.image.load(os.path.join('resources/graphics', 'john07.png'))			# 9 : punch left 2	
		self.image_10 = pygame.image.load(os.path.join('resources/graphics', 'john08.png'))			# 10 : kick left 1
		self.image_11 = pygame.image.load(os.path.join('resources/graphics', 'john09.png'))			# 11 : kick left 2	
		self.image_12 = pygame.image.load(os.path.join('resources/graphics', 'john12.png'))			# 12 : reel right
		self.image_13 = pygame.image.load(os.path.join('resources/graphics', 'john13.png'))			# 12 : reel left

		self.images = [self.image_0, self.image_1, self.image_2, self.image_3, self.image_4, self.image_5, self.image_6, self.image_7, self.image_8, self.image_9, self.image_10, self.image_11, self.image_12, self.image_13]
		#--scale all images by global SCALE
		for image in self.images:
			# self.images[image] = pygame.transform.scale(self.images[image], (self.images[image].get_rect().width * SCALE, self.images[image].get_rect().height * SCALE))
			self.images[self.images.index(image)] = pygame.transform.scale(image, (IMG_WIDTH * SCALE, IMG_HEIGHT * SCALE)).convert_alpha()

		self.animation = []
		self.color_index = 0
		self.animation_timer = 0
		self.animation_sub_timer = 0
		self.menu_choices = ['Start Game', 'Quit Game']
		self.menu_selection = 0

	def update(self, keys):
		#--animation timer determines which john image will be displayed. Return to zero if exceeds max.
		self.animation_sub_timer += 1
		if self.animation_sub_timer > 2:
			self.animation_sub_timer = 0
			self.animation_timer += 1
			if self.animation_timer == len(self.images):
				self.animation_timer = 0

		#--color_index increases by 15 each update to make title flash. Return to zero if exceeds max.
		self.color_index += 15
		if self.color_index > 255:
			self.color_index = 0

		#--Handle input to change selected menu item
		if keys[0] == 1:
			self.menu_selection += 1
			keys[0] = 0
		elif keys[1] == 1:
			self.menu_selection -= 1
			keys[1] = 0
		if keys[4] ==1 or keys[5] == 1:
			if self.menu_choices[self.menu_selection] == 'Quit Game':
				pygame.quit()
				sys.exit()
			elif self.menu_choices[self.menu_selection] == 'Start Game':
				return 1
		if self.menu_selection == len(self.menu_choices):
			self.menu_selection = 0
		elif self.menu_selection == -1:
			self.menu_selection = len(self.menu_choices) - 1

		return 0

	def render(self, background):
		#--Fill background
		background.fill((255, 0, 0))
		self.image_index = self.animation_timer

		self.color = (self.color_index, self.color_index, self.color_index)
		self.title_text = self.title_font.render("KARATE  JOHNS", 1, self.color)		
		
		#--get center of background to align title text
		self.title_pos = self.title_text.get_rect()
		self.title_pos.centerx = background.get_rect().centerx
		
		#--Draw menu text
		for self.menu_choice in self.menu_choices:
			if self.menu_choices.index(self.menu_choice) == self.menu_selection:
				self.menu_color = self.color
			else:
				self.menu_color = (0,0,0)		
			self.menu_text = self.menu_font.render(self.menu_choice, 1, self.menu_color)
			self.menu_pos = self.menu_text.get_rect()
			self.menu_pos.centerx = background.get_rect().centerx
			self.menu_pos.top = self.images[self.image_index].get_rect().bottom + 150 + (self.menu_choices.index(self.menu_choice) * self.menu_text.get_rect().height)
			background.blit(self.menu_text, self.menu_pos)

		#--get center x and y of background to center image
		self.image_pos = self.images[self.image_index].get_rect()
		self.image_pos.centerx = background.get_rect().centerx
		self.image_pos.centery = background.get_rect().centery
		
		#--blit text and image to background
		background.blit(self.images[self.image_index], self.image_pos)
		background.blit(self.title_text, self.title_pos)
		# background.blit(self.menu_text, self.menu_pos)
