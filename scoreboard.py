import pygame

from pygame.sprite import Group

from ship import Ship

class Scoreboard():
	""" Create a scoreboard to show game statistics"""
	def __init__(self,ai_settings,screen,stats):
		""" Initalize the scoreboard attributes"""
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.ai_settings = ai_settings
		self.stats = stats

		# Font settings for scoring information
		self.text_color = (30,30,30)
		self.font = pygame.font.SysFont(None,48)

		# prepare image for score
		self.prep_score()
		# prepare the high score
		self.prep_high_score()
		# prepare to show level
		self.prep_level()
		# prepare a group of ship
		self.prep_ship()

	def prep_score(self):
		""" Turn the score into a rendered image """
		rounded_score = int(round(self.stats.score,-1))
		score_str = "{:,}".format(rounded_score)
		self.score_image = self.font.render(score_str,True,self.text_color,
			self.ai_settings.bg_color)

		# Display the image at the top right corner of the screen
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20

	def prep_high_score(self):
		""" Turn the high score into rendered image"""
		high_score = int(round(self.stats.high_score,-1))
		high_score_str = "{:,}".format(high_score)
		self.high_score_image = self.font.render(high_score_str,True,
							self.text_color,self.ai_settings.bg_color)

		# Display the high score at the top center of the screen
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx 
		self.high_score_rect.top = 20

	def prep_level(self):
		""" Turn the level into rendered image """
		self.level_image = self.font.render(str(self.stats.level),True,self.text_color
			,self.ai_settings.bg_color)
		# position the level below the score
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.score_rect.right
		self.level_rect.top = self.score_rect.bottom + 10

	def prep_ship(self):
		""" Show how many ship are left """
		self.ships = Group()
		for ship_number in range(self.stats.ship_left):
			ship = Ship(self.ai_settings,self.screen)
			ship.rect.x = 10 + ship_number * ship.rect.width
			ship.rect.y = 10
			self.ships.add(ship)

	def show_score(self):
		""" Draw the image on the screen """
		self.screen.blit(self.score_image ,self.score_rect)
		self.screen.blit(self.high_score_image,self.high_score_rect)
		self.screen.blit(self.level_image,self.level_rect)
		self.ships.draw(self.screen)


