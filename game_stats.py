"""This module contains all information about the game statistics"""

class GameStats:
	"""Track statistics for E.T.-Attack"""

	def __init__(self, et_game):
		"""Initialize statistics"""
		self.settings = et_game.settings
		# Starts E.T.-Attack in inactive state
		self.game_active = False
		self.reset_stats()

		# Loading high score from high_score.txt
		filename = 'high_score.txt'
		with open(filename, 'r') as f:
			try:
				self.high_score = int(f.read())
			except:
				self.hight_score = 0

	def reset_stats(self):
		"""Initialize statistics that can change during the game"""
		self.ships_left = self.settings.ship_limit
		self.score = 0
		self.level = 1