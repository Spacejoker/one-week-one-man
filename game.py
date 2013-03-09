from menu import Scene
from cutscene import MISC, BGS
import pygame
import os, sys
class GameData():
	def __init__(self, data):
		self.data = data

	@staticmethod
	def gen_new_player():
		return GameData({
			'level' : 1,
			'upgrades' : [],
			'money' : 100})


class Town(Scene):
	def __init__(self, model):
		self.name = 'town'

		if not hasattr(model, 'game_state'):
			model.game_state = GameData.gen_new_player()

		model.places = {'places' : ['store', 'dungeons', 'something']}

		model = target_selection = 0

		self.model = model
		self.bg =  pygame.image.load(os.path.join(BGS, 'town.png'))
	
	def update(self, events):
		pass	
