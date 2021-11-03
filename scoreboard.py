"""This module contains the class Scoreboard"""

import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
	"""A class to report scoring information"""

	def __init__(self, et_game):
		"""Initialize scorekeeping attributes"""
		self.et_game = et_game
		self.screen = et_game.screen
		self.screen_rect = self.screen.get_rect()
		self.settings = et_game.settings
		self.stats = et_game.stats

		# Fond type for score display
		self.text_color = (120, 120, 120)
		self.font = pygame.font.SysFont(None, 20)

		# Initializes the starting images for the score and high score display
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ships()

	def prep_score(self):
		"""Turn the score into a rendered image"""
		rounded_score = int(round(self.stats.score, -1))
		score_str = "{:,}".format(rounded_score)
		self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

		# Shows the score in the upper right corner of the screen
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20

	def prep_high_score(self):
		"""Turn the high score into a rendered image"""
		high_score = int(round(self.stats.high_score, -1))
		high_score_str = "{:,}".format(high_score)
		self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

		# Centers the high score display in the upper middle of the screen
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = self.score_rect.top

	def prep_level(self):
		"""Turn the level into a rendered image"""
		level_str = str(self.stats.level)
		self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)
		# Places the level display under the score display
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.score_rect.right
		self.level_rect.top = self.score_rect.bottom + 10

	def prep_ships(self):
		"""Show how many ships are left"""
		self.ships = Group()
		for ship_number in range(self.stats.ships_left):
			ship = Ship(self.et_game)
			ship.rect.x = 10 + ship_number * ship.rect.width
			ship.rect.y = 10
			self.ships.add(ship)

	def show_score(self):
		"""Draw scores, level and remaining ships to the screen"""
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.level_image, self.level_rect)
		self.ships.draw(self.screen)

	def check_high_score(self):
		"""Check to see if there's a new high score"""
		if self.stats.score > self.stats.high_score:
			self.stats.high_score = self.stats.score
			self.prep_high_score()