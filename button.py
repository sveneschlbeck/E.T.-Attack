"""This module contains the code for the class Button"""

import pygame.font

class Button:

	def __init__(self, et_game, msg):
		"""Initialize button attributes"""
		self.screen = et_game.screen
		self.screen_rect = self.screen.get_rect()

		# Defines the dimensions and attributes of the button
		self.width, self.height = 200, 50
		self.button_color = (0, 0, 0)
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont(None, 48)

		# Creates the rect object (button) and centers it
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = self.screen_rect.center

		# The button's text must only be initialized once
		self._prep_msg(msg)

	def _prep_msg(self, msg):
		"""Turn msg into a rendered image and center text on the button"""
		self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center

	def draw_button(self):
		"""Draws an empty button and then the text"""
		self.screen.fill(self.button_color, self.rect)
		self.screen.blit(self.msg_image, self.msg_image_rect)