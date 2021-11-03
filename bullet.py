"""This module contains the class Bullet"""

import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	"""A class to manage bullets fired from the ship"""

	def __init__(self, et_game):
		"""Create a bullet object at the ship's current position"""
		super(Bullet, self).__init__()
		self.screen = et_game.screen
		self.settings = et_game.settings
		self.color = self.settings.bullet_color

		# Creates a bullet rectangle at (0, 0) and then specifies the exact position
		self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
		self.rect.midtop = et_game.ship.rect.midtop

		# Saves the position (y-coordinate) of the bullet as float
		self.y = float(self.rect.y)

	def update(self):
		"""Move the bullet up the screen"""
		# Refreshes the float position of the bullet
		self.y -= self.settings.bullet_speed
		# Refreshes the position of the rectangle
		self.rect.y = self.y

	def draw_bullet(self):
		"""Draw the bullet to the screen"""
		pygame.draw.rect(self.screen, self.color, self.rect)