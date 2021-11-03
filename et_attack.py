"""Main module for setting up the game environment"""

import sys
from time import sleep

import subprocess
import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from et import ET

class ETAttack:
	"""Overall class to manage game assets and behavior"""

	def __init__(self):
		"""Initialize the game and create game resources"""
		pygame.init()
		pygame.mixer.pre_init(44100, -16, 2, 512)
		pygame.mixer.init()
		self.settings = Settings()

		# Choosing individual window size
		# self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
		# pygame.display.set_caption("'E.T.-Attack' by Sven Eschlbeck")

		# Running game in full-screen mode
		self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("'E.T.-Attack' by Sven Eschlbeck")

		# Creates an instance to save the game stats and display a scoreboard
		self.stats = GameStats(self)
		self.sb = Scoreboard(self)

		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.ets = pygame.sprite.Group()

		self._create_fleet()

		# Creates the 'Play button'
		self.play_button = Button(self, "Play")

		# Play game opening sound
		game_opener_sound = pygame.mixer.Sound('sounds/game_opener.wav')
		game_opener_sound.set_volume(self.settings.volume)
		game_opener_sound.play()

	def run_game(self):
		"""Start the main loop for the game"""
		while True:
			self._check_events()

			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				# print(len(self.bullets))
				self._update_ets()
				
			self._update_screen()

	# Leading underscore marks help method
	def _check_events(self):
		"""Respond to keypresses and mouse events"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)
				if self.stats.game_active == False:
					mouse_sound = pygame.mixer.Sound('sounds/mouse_click.wav')
					mouse_sound.set_volume(self.settings.volume)
					mouse_sound.play()				
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)

	def _check_play_button(self, mouse_pos):
		"""Start a new game when the player clicks 'Play'"""
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			# Sets back the game stats
			self.settings.initialize_dynamic_settings()
			self.stats.reset_stats()
			self.stats.game_active = True
			self.sb.prep_score()
			self.sb.prep_level()
			self.sb.prep_ships()

			# Deletes the remaining UFOs and bullets
			self.ets.empty()
			self.bullets.empty()

			# Creates a new fleet and centers the own ship
			self._create_fleet()
			self.ship.center_ship()

			# Hide mouse cursor
			pygame.mouse.set_visible(False)

			# Wait for 1/10 second
			pygame.time.delay(100)

	def _check_keydown_events(self, event):
		"""Respond to keypresses"""
		if event.key == pygame.K_RIGHT:
			# Moves the ship to the right by setting the flag to True
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			# Move the ship to the left by setting the flag to True
			self.ship.moving_left = True
		elif event.key == pygame.K_p and self.stats.game_active == True:
			# Pauses the game when 'p' is pressed and the game is running
			self.stats.game_active = False
		elif event.key == pygame.K_p and self.stats.game_active == False:
			# Continues the game when 'p' is pressed and the game is paused
			self.stats.game_active = True
			pygame.time.delay(1000)
		elif event.key == pygame.K_q:
			# Save high score before quitting the game
			filename = 'high_score.txt'
			with open(filename, 'w') as f:
				f.write(str(self.stats.high_score))
			# Quit the game
			sys.exit()
		elif event.key == pygame.K_SPACE:
			# Fire bullet on space press
			self._fire_bullet()
		elif event.key == pygame.K_b:
			pygame.time.delay(5000)
		elif event.key == pygame.K_m and self.settings.volume != 0:
			self.settings.volume = 0
		elif event.key == pygame.K_m and self.settings.volume == 0:
			self.settings.volume = 0.05
		elif event.key == pygame.K_h and self.stats.game_active == True:
			# Open pdf file with commands
			path = 'controls.pdf'
			subprocess.Popen([path], shell=True)
			self.stats.game_active = False

	def _check_keyup_events(self, event):
		"""Respond to key releases"""
		if event.key == pygame.K_RIGHT:
			# Stops the ship by setting the flag to False
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			# Stops the ship by setting the flag to False
			self.ship.moving_left = False

	def _fire_bullet(self):
		"""Create a new bullet and add it to the bullets group"""
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)
			bullet_sound = pygame.mixer.Sound('sounds/shoot.wav')
			bullet_sound.set_volume(self.settings.volume)
			bullet_sound.play()

	def _update_bullets(self):
		"""Update position of bullets and get rid of old bullets"""
		# Refreshes the bullets' positions
		self.bullets.update()
		# Removing bullets that have left the screen
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)
		# Checks for collisions
		self._check_bullet_et_collisions()

	def _check_bullet_et_collisions(self):
		"""Respond to bullet-E.T. collisions"""
		# Checks if bullets have hit a UFO. If yes, both the bullet and its target get erased
		collisions = pygame.sprite.groupcollide(self.bullets, self.ets, True, True) # Returns a dictionary in the form (bullet:UFO)

		if collisions:
			for ets in collisions.values():
				# Play sound for shot E.T.
				collision_sound = pygame.mixer.Sound('sounds/et_killed.wav')
				collision_sound.set_volume(self.settings.volume)
				collision_sound.play()
				self.stats.score += self.settings.et_points * len(ets)
			self.sb.prep_score()
			self.sb.check_high_score()

		if not self.ets:
			# Destroys existing bullets and creates a new fleet
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()
			# Increases the level and play sound
			level_sound = pygame.mixer.Sound('sounds/level_rise.wav')
			level_sound.set_volume(self.settings.volume)
			level_sound.play()
			self.stats.level += 1
			self.sb.prep_level()

	def _update_ets(self):
		"""Check if the fleet is at an edge, then update the positons of all E.T.s in the fleet"""
		self._check_fleet_edges()
		self.ets.update()
		# Checks for collision between UFOs and own ship
		if pygame.sprite.spritecollideany(self.ship, self.ets):
			self._ship_hit()
		# Checks for UFOs hitting the screen bottom
		self._check_ets_bottom()

	def _create_fleet(self):
		"""Create the fleet of E.T.s"""
		# Creates a UFO and calculates the number of UFOs in a row
		# The distance between two UFOs is the width of a UFO
		et = ET(self)
		et_width, et_height = et.rect.size
		available_space_x = self.settings.screen_width - (2 * et_width)
		number_ets_x = available_space_x // (2 * et_width)

		# Defines the possible number of rows of UFOs on the screen
		ship_height = self.ship.rect.height
		available_space_y = (self.settings.screen_height - (3 * et_height) - ship_height)
		number_rows = available_space_y // (2 * et_height)

		# Spawns the E.T. fleet
		for row_number in range(number_rows):
			for et_number in range(number_ets_x):
				self._create_et(et_number, row_number)

	def _create_et(self, et_number, row_number):
		"""Create an E.T. and place it in the row"""
		et = ET(self)
		et_width, et_height = et.rect.size
		et.x = et_width + 2 * et_width * et_number
		et.rect.x = et.x
		et.rect.y = et.rect.height + 2 * et.rect.height * row_number
		self.ets.add(et)

	def _check_fleet_edges(self):
		"""Respond appropriately if any E.T.s have reached an edge"""
		for et in self.ets.sprites():
			if et.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""Drop the entire fleet and change the fleet's direction"""
		for et in self.ets.sprites():
			et.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def _ship_hit(self):
		"""Respond to the ship being hit by an E.T."""
		if self.stats.ships_left > 0:
			# Play life lost sound
			life_lost_sound = pygame.mixer.Sound('sounds/losing_life.wav')
			life_lost_sound.set_volume(self.settings.volume)
			life_lost_sound.play()
			# Lower ships_left by 1 and refresh the display
			self.stats.ships_left -= 1
			self.sb.prep_ships()
			# Deletes all remaining UFOs and bullets
			self.ets.empty()
			self.bullets.empty()
			# Creates a new fleet and centers the player's ship
			self._create_fleet()
			self.ship.center_ship()
			# Pauses the game for a short period of time
			sleep(0.5)
		else:
			# Play game over sound
			game_over_sound = pygame.mixer.Sound('sounds/game_over.wav')
			game_over_sound.set_volume(self.settings.volume)
			game_over_sound.play()
			# Save high score before quitting the game
			filename = 'high_score.txt'
			with open(filename, 'w') as f:
				f.write(str(self.stats.high_score))
			self.stats.game_active = False
			pygame.mouse.set_visible(True)

	def _check_ets_bottom(self):
		"""Check if any E.T.s have reached the bottom of the screen"""
		screen_rect = self.screen.get_rect()
		for et in self.ets.sprites():
			if et.rect.bottom >= screen_rect.bottom:
				# Same reaction as to a ship-UFO collision
				self._ship_hit()
				break

	def _update_screen(self):
		"""Update images on the screen and flip to the new screen"""
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.ets.draw(self.screen)

		# Draws the score information
		self.sb.show_score()

		# Draws the play button only when game is inactive
		if not self.stats.game_active:
			self.play_button.draw_button()

		# Visualizes the last rendered screen
		pygame.display.flip()

if __name__ == '__main__':
	# Creates an instance of the game and executes it
	et = ETAttack()
	et.run_game()