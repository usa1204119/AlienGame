import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	""" A class to initalize the alien"""
	def __init__(self,ai_settings,screen):
		super(Alien,self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings

		# load the image and get the rect attribute
		self.image = pygame.image.load('images/c.bmp')
		self.rect = self.image.get_rect()

		# set its position near the top left corner of the screen
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height 

		# store the aliens exact position
		self.x = float(self.rect.x)
	
	def check_edges(self):
		""" Return true if the alien is at the edge"""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True 
		elif self.rect.left <= 0:
			return True 
	def update(self):
		""" Move the alien right or left"""
		self.x += (self.ai_settings.alien_speed_factor
			* self.ai_settings.fleet_direction)
		self.rect.x = self.x 

	def blitme(self):
		""" Draw the aliens current position"""
		self.screen.blit(self.image,self.rect)

