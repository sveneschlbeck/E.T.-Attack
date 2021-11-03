"""This module contains the E.T. class"""

import pygame
from pygame.sprite import Sprite

class ET(Sprite):
	"""A class to represent a single E.T. in the fleet"""

	def __init__(self, et_game):
		"""Initialize the E.T. and set its starting position"""
		super(ET, self).__init__()
		self.screen = et_game.screen
		self.settings = et_game.settings

		# Loads the image of the UFO and determines the rect attribute
		self.image = pygame.image.load('images/et.bmp')
		self.rect = self.image.get_rect()

		# Places each new UFO in the upper left corner of the screen
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		# Stores the exact position of the UFO
		self.x = float(self.rect.x)

	def check_edges(self):
		"""Return True if E.T. is at edge of screen"""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right or self.rect.left <= 0:
			return True

	def update(self):
		"""Move the E.T. right or left"""
		self.x += (self.settings.et_speed * self.settings.fleet_direction)
		self.rect.x = self.x