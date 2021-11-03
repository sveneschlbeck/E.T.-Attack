"""Main settings centralized in this file"""

class Settings():
	"""A class to store all settings for E.T.-Attack"""

	def __init__(self):
		"""Initialize the game's static settings"""
		# Display settings
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (255, 255, 255)
		# Ship settings
		self.ship_limit = 3
		# Bullet settings
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullets_allowed = 3
		# UFOs settings
		self.fleet_drop_speed = 10
		# Intensity of game's acceleration
		self.speedup_scale = 1.1
		# Intensity of score increase
		self.score_scale = 1.5
		# Volume of sounds
		self.volume = 0.05

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""Initialize settings that change throughout the game"""
		self.ship_speed = 1.5
		self.bullet_speed = 1.5
		self.et_speed = 0.4
		# The value 1 for fleet_direction means "to the right", -1 means "to the left"
		self.fleet_direction = 1
		# Score reglement
		self.et_points = 50

	def increase_speed(self):
		"""Increase speed settings and E.T. point values"""
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.et_speed *= self.speedup_scale
		self.et_points = int(self.et_points * self.score_scale)
		# print(self.et_points)