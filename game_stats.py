class GameStats():
	def __init__(self,ai_settings):
		""" Initalize statistics"""
		self.ai_settings = ai_settings
		# High score should never be reset
		self.high_score = 0
		self.reset_stats()

	def reset_stats(self):
		""" Initalize statistics that can change during the game """
		self.ship_left = self.ai_settings.ship_limit
		self.game_active = False
		self.score = 0
		# level
		self.level = 1


