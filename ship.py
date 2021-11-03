"""Modul to construct the ship"""

import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	"""A class to manage the ship"""

	def __init__(self, et_game):
		"""Initialize the ship and set its starting position"""
		super(Ship, self).__init__()
		self.screen = et_game.screen
		self.settings = et_game.settings
		self.screen_rect = et_game.screen.get_rect()

		# Loads the ship's image and calls it's surrounding rectangle
		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()

		# Placing each new ship in the middle of the screen bottom
		self.rect.midbottom = self.screen_rect.midbottom

		# Saving a float number for ship middle point
		self.x = float(self.rect.x)

		# Movement flags
		self.moving_right = False
		self.moving_left = False

	def update(self):
		"""Update the ship's position based on the movement flag"""
		# Update the value for the ship's middle point, not that of the rectangle
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.x += self.settings.ship_speed
		if self.moving_left and self.rect.left > 0:
			self.x -= self.settings.ship_speed

		# Updates the rect object on the basis of self.x
		self.rect.x = self.x

	def blitme(self):
		"""Draw the ship at its current location"""
		self.screen.blit(self.image, self.rect)

	def center_ship(self):
		"""Center the ship on the screen"""
		self.rect.midbottom = self.screen_rect.midbottom
		self.x = float(self.rect.x)