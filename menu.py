import pygame
from cutscene import MISC, BGS
from constants import load_animation, Animation
import os

class Scene():
	def __init__(self):
		self.name = 'base scene'
		pass
	def update(self, events, time_passed = 0):
		raise NameError("Sub classes must implement me")

class MainMenu(Scene):
	def __init__(self, model):
		self.name = 'main_menu'
		self.choices =  [
				{ 'name' : 'New Game', 'method' : self.new_game},
				{ 'name' : 'play intro', 'method' : self.intro},
				{ 'name' : 'exit', 'method' : self.exit},
				]
		self.choice = 0
		imgs = load_animation('marker', 4)		
		self.menu_choice = Animation(imgs, 400)
		self.bg =  pygame.image.load(os.path.join(BGS, 'main_menu.png'))
		self.model = model

	def intro(self):
		self.model.new_scene = 'run_intro'

	def new_game(self):
		self.model.new_scene = 'town'
		self.model.game_state = None

	def update(self, events, time_passed = 0):
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_DOWN:
					self.choice += 1
				if event.key == pygame.K_UP:
					self.choice -= 1
				if event.key == pygame.K_RETURN:
					self.choices[self.choice]['method']()
		self.choice = self.choice % len(self.choices)

	def exit(self):
		self.model.exit = True

