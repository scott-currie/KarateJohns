import os
import pygame
from pygame.locals import *
import sys

MOVE_SPEED = 6 			#Pixels to move each update
ATK_TIME = 2 			#Number of frames per attack animation. Should be multiple of 2
BOX_MARGIN = 4 			#Number of pixels in from left/right image boundaries to left/right boundaries of hitbox
SCALE = 3 				#Scale factor for character image
IMG_HEIGHT = 28 		#Pixel height of image loaded from disk
IMG_WIDTH = 26 			#Pixel width of image loaded from disk
HITS = 6 				#Number of hits allowed before character knocked down.

class Player(pygame.sprite.Sprite):
	global MOVE_SPEED
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		#--Load individual character images
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
		#--Scale all images
		for image in self.images:
			self.images[self.images.index(image)] = pygame.transform.scale(image, (IMG_WIDTH * SCALE, IMG_HEIGHT * SCALE)).convert_alpha()
		#--Add images from full list to animation sublists
		self.anim_punch_right = [self.images[1], self.images[2], self.images[2], self.images[1]]
		self.anim_punch_left = [self.images[8], self.images[9], self.images[9], self.images[8]]
		# self.anim_kick_right = [self.images[3], self.images[4], self.images[4], self.images[3]]
		# self.anim_kick_left = [self.images[10], self.images[11], self.images[11], self.images[10]]
		self.anim_kick_right = [self.images[3], self.images[4], self.images[4], self.images[4], self.images[4], self.images[4], self.images[3]]
		self.anim_kick_left = [self.images[10], self.images[11], self.images[11], self.images[11], self.images[11], self.images[11], self.images[10]]		
		#--Load sound
		self.snd_kick = pygame.mixer.Sound(os.path.join('resources/sounds', 'kick2.ogg'))	
		self.snd_punch = pygame.mixer.Sound(os.path.join('resources/sounds', 'punch2.ogg'))	
		self.snd_punch.set_volume(.075)
		self.snd_kick.set_volume(.075)
		
		#--State variables
		self.image = self.images[0]
		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.y = 0

		#----set up hitbox
		self.hitbox = pygame.Rect.copy(self.rect)
		self.hitbox.width -= (2 * BOX_MARGIN * SCALE)
		self.hitbox.centerx = self.rect.centerx
		self.hitbox.centery = self.rect.centery
		
		self.facing = 1 	# 0 = left, 1 = right	
		self.animation_timer = 0
		self.attack_timer = 0
		self.walk = False
		self.punch = False
		self.kick = False
		self.idle = True

	def choose_player_image(self):
		#--Punch animation
		image_index = 0
		image = self.images[0]

		if self.punch:
			# image_index = int(self.attack_timer / 1)			
			image_index = self.attack_timer
			if self.facing == 0:
				image = self.anim_punch_left[image_index]
			elif self.facing == 1:
				image = self.anim_punch_right[image_index]

		#--Kick animation
		elif self.kick:
			# image_index = int(self.attack_timer / 1)			
			image_index = self.attack_timer
			if self.facing == 0:
				image = self.anim_kick_left[image_index]
			elif self.facing == 1:
				image = self.anim_kick_right[image_index]		

		#--Walk animation
		elif self.walk:
			if self.facing == 0:
				if self.animation_timer <= 3:
					image = self.images[6]
				else:
					image = self.images[7]
			elif self.facing == 1:

				if self.animation_timer <= 3:
					image = self.images[0]
				else:
					image = self.images[5]
		#--Return idle image
		elif self.idle:
			if self.facing == 0:
				image = self.images[6]
			elif self.facing == 1:
				image = self.images[0]
		return image

	def update(self, keys, enemy):
		#--If punching or kicking and attack duration not reached, increment attack_timer
		# if (self.punch or self.kick) and self.attack_timer < ATK_TIME:
		if (self.punch and self.attack_timer < len(self.anim_punch_right) - 1) or (self.kick and self.attack_timer < len(self.anim_kick_right) - 1):
			self.attack_timer += 1
		else:
			self.attack_timer = 0
			self.punch = False
			self.kick = False

		if not self.kick and not self.punch:
			#--Check keys for keyboard input and set flags. Punch and kick take priority over walk.
			#----punch or kick
			if keys[6] == 1:
				self.punch = True
				self.snd_punch.play()
				keys[6] = 0
			elif keys[7] == 1:
				self.kick = True
				self.snd_kick.play()				
				keys[7] = 0
			#----any walk key. Set walk flag and move rectangle represented by image boundaries (not hitbox)
			elif keys[0] or keys[1] or keys[2] or keys[3]:
				self.walk = True
				if keys[0] == 1:
					if self.rect.bottom > 246:
						self.rect.y -= MOVE_SPEED
				elif keys[1] == 1:
					if self.rect.bottom < 479:
						self.rect.y += MOVE_SPEED
				if keys[2] == 1:
					self.facing = 0
					if self.rect.x >= MOVE_SPEED:
						self.rect.x -= MOVE_SPEED
				if keys[3] == 1:
					self.facing = 1
					if self.rect.right < 640 - MOVE_SPEED:
						self.rect.x += MOVE_SPEED
				#move center hitbox on rectangle.
				self.hitbox.centerx = self.rect.centerx
				self.hitbox.centery = self.rect.centery
			#--If not punch, kick, or walk, then idle
			else:
				self.idle = True
				self.walk = False

		#--Find out if a punch or kick hit an enemy
		if self.punch or self.kick:
			#--Does player hitbox collide with enemy hitbox?
			if self.hitbox.colliderect(enemy.hitbox):
				#--Is player facing enemy?
				if (self.facing == 0 and self.hitbox.right > enemy.hitbox.right) or (self.facing == 1 and self.hitbox.left < enemy.hitbox.left): 
					#--If player on first animation frame only, reel enemy. This allows for longer kick animation than enemy reel time
					#---while only reeling enemy once per attack
					if self.attack_timer == 0:
						#--Is enemy already reeling or down? Can't hit him again.
						if not enemy.reel and not enemy.down:
							enemy.reel = True
					
		#--Iterate/loop animation timer
		self.animation_timer += 1
		if self.animation_timer > 7:
			self.animation_timer = 0

		#--Choose image to draw this render pass
		self.image = self.choose_player_image()		

	def render(self, background):
		background.blit(self.image, (self.rect.x, self.rect.y))
		#-Uncomment to make boxes visible
		# pygame.draw.rect(background, (0,0,0), self.rect, 1)
		pygame.draw.rect(background, ( 0, 255 ,0), self.hitbox, 1)		