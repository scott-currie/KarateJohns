import os
import pygame
from pygame.locals import *
import random
import sys

#--Constants
MOVE_SPEED = 3 			#Pixels to move each update. Less than player MOVE_SPEED and even divisor of player MOVE_SPEED
BOX_MARGIN = 4 			#Number of pixels in from left/right image boundaries to left/right boundaries of hitbox
IMG_HEIGHT = 28 		#Pixel height of image loaded from disk
IMG_WIDTH = 26 			#Pixel width of image loaded from disk
SCALE = 3 				#Scale factor for character image
HITS = 6 				#Number of hits allowed before character knocked down.
AGGRESSION = .8		#Represents threshold above which random roll means to attack

class Enemy(pygame.sprite.Sprite):
	# global MOVE_SPEED
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		#--Load individual character images		
		self.image_0 = pygame.image.load(os.path.join('resources/graphics', 'thug00.png'))			# 0 : idle right
		self.image_1 = pygame.image.load(os.path.join('resources/graphics', 'thug01.png'))			# 1 : punch right 1
		self.image_2 = pygame.image.load(os.path.join('resources/graphics', 'thug02.png'))			# 2 : punch right 2
		self.image_3 = pygame.image.load(os.path.join('resources/graphics', 'thug03.png'))			# 3 : kick right 1
		self.image_4 = pygame.image.load(os.path.join('resources/graphics', 'thug04.png'))			# 4 : kick right 2
		self.image_5 = pygame.image.load(os.path.join('resources/graphics', 'thug10.png'))			# 5 : walk right
		self.image_6 = pygame.image.load(os.path.join('resources/graphics', 'thug05.png'))			# 6 : idle left
		self.image_7 = pygame.image.load(os.path.join('resources/graphics', 'thug11.png'))			# 7 : walk left		
		self.image_8 = pygame.image.load(os.path.join('resources/graphics', 'thug06.png'))			# 8 : punch left 1
		self.image_9 = pygame.image.load(os.path.join('resources/graphics', 'thug07.png'))			# 9 : punch left 2	
		self.image_10 = pygame.image.load(os.path.join('resources/graphics', 'thug08.png'))			# 10 : kick left 1
		self.image_11 = pygame.image.load(os.path.join('resources/graphics', 'thug09.png'))			# 11 : kick left 2
		self.image_12 = pygame.image.load(os.path.join('resources/graphics', 'thug12.png'))			# 12 : reel right
		self.image_13 = pygame.image.load(os.path.join('resources/graphics', 'thug13.png'))			# 13 : reel left	
		self.image_14 = pygame.image.load(os.path.join('resources/graphics', 'thug14.png'))			# 14 : fall right 1	
		self.image_15 = pygame.image.load(os.path.join('resources/graphics', 'thug15.png'))			# 15 : fall right 2	
		self.image_16 = pygame.image.load(os.path.join('resources/graphics', 'thug16.png'))			# 16 : fall left 1	
		self.image_17 = pygame.image.load(os.path.join('resources/graphics', 'thug17.png'))			# 17 : fall left 2									
		#--Add loaded images to list
		self.images = [self.image_0, self.image_1, self.image_2, self.image_3, self.image_4, self.image_5, self.image_6, self.image_7, self.image_8, self.image_9, self.image_10, self.image_11, self.image_12, self.image_13, self.image_14, self.image_15, self.image_16, self.image_17]
		#--Scale all images
		for image in self.images:
			self.images[self.images.index(image)] = pygame.transform.scale(image, (IMG_WIDTH * SCALE, IMG_HEIGHT * SCALE)).convert_alpha()
		#--Add images from full list to animation sublists
		self.anim_punch_right = [self.images[1], self.images[2], self.images[2], self.images[1]]
		self.anim_punch_left = [self.images[8], self.images[9], self.images[9], self.images[8]]
		self.anim_kick_right = [self.images[3], self.images[4], self.images[4], self.images[4], self.images[4], self.images[4], self.images[3]]
		self.anim_kick_left = [self.images[10],  self.images[11], self.images[11], self.images[11], self.images[11], self.images[11], self.images[10]]
		self.anim_fall_right = [self.images[14], self.images[15], self.images[15], self.images[15], self.images[15], self.images[15], self.images[15], self.images[15], self.images[15], self.images[15], self.images[15], self.images[15], self.images[15]]
		self.anim_fall_left = [self.images[16], self.images[17], self.images[17], self.images[17], self.images[17], self.images[17], self.images[17], self.images[17], self.images[17], self.images[17], self.images[17], self.images[17], self.images[17]]
		self.anim_reel_right = [self.images[12], self.images[12], self.images[12], self.images[12]]
		self.anim_reel_left = [self.images[13], self.images[13], self.images[13], self.images[13]]

		self.image = self.images[0]
		self.rect = self.image.get_rect()
		self.rect.x = 550
		self.rect.y = 400

		#----set up hitbox
		self.hitbox = pygame.Rect.copy(self.rect)
		self.hitbox.width -= (2 * BOX_MARGIN * SCALE)
		self.hitbox.centerx = self.rect.centerx
		self.hitbox.centery = self.rect.centery

		self.facing = 0 		
		self.animation_timer = 0
		self.attack_timer = 0
		self.reel_timer = 0
		self.fall_timer = 0
		self.walk = False
		self.punch = False
		self.kick = False
		self.idle = True
		self.reel = False
		self.down = False
		self.hits = HITS
		self.alive = True

	def choose_image(self):
		#--Reeling or down animations
		if self.reel:
			if self.facing == 0:
				image = self.anim_reel_left[self.reel_timer]
			elif self.facing == 1:
				image = self.anim_reel_right[self.reel_timer]
		elif self.down:
			if self.facing == 0:
				image = self.anim_fall_left[self.fall_timer]
			elif self.facing == 1:
				image = self.anim_fall_right[self.fall_timer]
		#--Punching animation
		elif self.punch:		
			if self.facing == 0:
				image = self.anim_punch_left[self.attack_timer]
			elif self.facing == 1:
				image = self.anim_punch_right[self.attack_timer]
		#--Kick animation
		elif self.kick:
			if self.facing == 0:
				image = self.anim_kick_left[self.attack_timer]
			elif self.facing == 1:
				image = self.anim_kick_right[self.attack_timer]		
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
		#--Idle animation (default)
		elif self.idle:
			if self.facing == 0:
				image = self.images[6]
			elif self.facing == 1:
				image = self.images[0]
		return image

	def update(self, player):
		#Assume walk is false unless update sets walk flag
		self.walk = False
		#Enemy only knows it's hit if it is reeling. Enemy reel flag is set to true in player's update
		#method if player makes contact. Enemy reeling takes precredence over other actions. Enemy 
		#can't act while reeling.
		if self.reel:
			#Use reel_timer == 0 as a condition to determine if this is the first update of the
			#enemy's reel duration. Decrement hits by one on this condition to be sure we only
			#decrement hits once per player hit.
			if self.reel_timer == 0:
				self.hits -= 1
			#Decide if enemy reels or is knocked down, depending on whether enemy has any hits left.
			if self.hits > 0:
				#Hits left, so enemy reels
				#Decrement reel time
				if self.reel_timer < len(self.anim_reel_left) - 1:
					self.reel_timer += 1
				#If reel time is up, enemy no longer reeling
				else:
					self.reel_timer = 0
					self.reel = False
			#Do knock down	
			else:
				#No hits left, so enemy is knocked down.
				self.reel = False
				self.down = True			
				self.fall_timer += 1
		elif self.down:
			if self.fall_timer < len(self.anim_fall_left) - 1:
				self.fall_timer += 1
			else:
				self.alive = False

		#Do this stuff if not reeling
		else:	#Player is not reeling or down and is free to act according to behavior rules
			if not self.punch and not self.kick:
				#Should we should try to punch or kick the player.
				#First, are we colliding with player hitbox?
				if self.hitbox.colliderect(player.hitbox):
					if random.random() > AGGRESSION:
						self.punch = True
						self.idle = False
						self.attack_timer = 0
						print('Enemy punch!')


				#If not choosing to attack, consider doing all the other possible stuff
				else:
					#If enemy position to right of player, walk left and face left
					if self.hitbox.left > player.hitbox.right:
						self.rect.x -= MOVE_SPEED
						self.walk = True
						self.facing = 0
					#If enemy position to left of player, walk right and face right
					elif self.hitbox.right < player.hitbox.left:
						self.rect.x += MOVE_SPEED
						self.walk = True
						self.facing = 1
					#If enemy hitbox intersecting player hitbox, enemy walks backward, preserving facing
					#-Enemy to left of player and overlap of hitboxes at least as great as MOVE_SPEED
					if self.hitbox.left < player.hitbox.left and self.hitbox.right > player.hitbox.left and (self.hitbox.right - player.hitbox.left >= MOVE_SPEED):
						self.walk = True
						self.rect.x -= MOVE_SPEED
					#-Enemy to right of player and overlap of hitboxes at least as great as MOVE_SPEED
					elif self.hitbox.right > player.hitbox.right and self.hitbox.left < player.hitbox.right and (player.hitbox.right - self.hitbox.left >= MOVE_SPEED):
						self.walk = True
						self.rect.x += MOVE_SPEED
					#If enemy bottom above player bottom, walk down and preserve facing
					if self.rect.bottom < player.rect.bottom:
						self.rect.y += MOVE_SPEED
						self.walk = True
					#If enemy bottom below player bottom, walk up and preserve facing
					elif self.rect.bottom > player.rect.bottom:
						self.rect.y -= MOVE_SPEED
						self.walk = True
					#If not walking or reeling, just idle
					if self.walk == False:
						self.idle = True
			#If we're doing this, enemy is in punch or kick state
			else:
				#If attacking and attack_timer hasn't reached count of last image of corresponding animation, increment attack_timer by 1
				if (self.punch and self.attack_timer < len(self.anim_punch_right) - 1) or (self.kick and self.attack_timer < len(self.anim_kick_right) - 1):
					self.attack_timer += 1
				#If attacking and attack_timer has reached count of last image of corresponding animation, zero attack_timer and set enemy state to idle
				else:
					self.attack_timer = 0
					self.punch = False
					self.kick = False
					self.idle = True 

			#--move hitbox along with base rect
			#check if either center coord of hitbox not aligned with rect defined by image position. If so, 
			#set hitbox center to rect center. I assume that this approach will eliminate a bit of overhead 
			#by centering the hitbox center using a single assignment. Keep in mind that character movement
			#is achieved by moving image rect, not hitbox.
			if self.hitbox.centerx != self.rect.centerx or self.hitbox.centery != self.rect.centery:
				self.hitbox.center = self.rect.center
		
		#--Select image to display this update
		self.image = self.choose_image()	
		#--Iterate/loop animation timer
		self.animation_timer += 1
		if self.animation_timer > 7:
			self.animation_timer = 0	

	def render(self, background):
		background.blit(self.image, (self.rect.x, self.rect.y))
		#--Uncomment to make boxes visible
		# pygame.draw.rect(background, (0,0,0), self.rect, 1)
		pygame.draw.rect(background, (255, 0 ,0), self.hitbox, 1)
