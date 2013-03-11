from menu import Scene
from cutscene import MISC, BGS, SOUND, CHARACTERS
import pygame
import os, sys
from constants import PLAY_SOUND, load_animation, Animation, load_image
import random
from random import randrange

class GameData():
	@staticmethod
	def gen_new_player():
		return {
			'level' : 1,
			'upgrades' : [],
			'gold' : 100,
			'inventory' : [Loot('potion', 5)]}
class Enemy():
	def __init__(self, enemy_type, level):
		self.name = enemy_type
		self.level = level
		self.img = load_image(MISC, 'enemy_' + enemy_type)
		self.loot = []
		self.loot.append(Loot('gold', random.randrange(1, level*2)))
		self.hp = level * 2
		self.defence = level/2

	def roll_dmg(self):
		if self.name == 'rabbit':
			return random.randrange(1, self.level + 1)
		if self.name == 'boss':
			return random.randrange(1, self.level * 5)
		raise NameError('unknown enemytpe:' + self.name) 
class Loot():
	def __init__(self, name, quantity):
		self.name = name
		self.quantity = quantity

class Hero():
	def __init__(self, hero_type, level):
		self.name = self.generate_name(hero_type)
		self.level = level
		if hero_type == 'fighter':
			self.small_img = load_image(CHARACTERS, 'small_fighter')
			self.hp = level * 3 + randrange(0, level)
			self.maxhp = self.hp
			self.defence = level*1.5
		self.loot = []
		self.loot.append(Loot('gold', random.randrange(1, level*2)))

	def generate_name(self, hero_type):
		return "Spjute"
	
	def add_loot(self, loot):
		self.loot.extend(loot)
		msg = []
		for l in loot:
			msg.append( self.name  + " looted " + str(l.quantity) + " " + str(l.name))
		return msg
	
		
	def get_action(self):
		return {'action' : 'attack', 'value' : random.randrange(self.level, self.level*3)}

class Town(Scene):
	def __init__(self, model):
		self.name = 'town'
		if not hasattr(model, 'game_state') or model.game_state is None:
			model.game_state = GameData.gen_new_player()

		model.places = {'places' : ['store', 'dungeons', 'something']}

		model.target_selection = target_selection = 0

		self.model = model
		self.bg =  pygame.image.load(os.path.join(BGS, 'town.png'))
		self.marker = pygame.image.load(os.path.join(MISC, 'menu_choice.png'))
		
		path = os.path.join(SOUND, 'cozy_melacholy.wav')

		song = pygame.mixer.Sound(path)
		model.song = song

		if PLAY_SOUND:
			model.song.play(loops=-1)
		
		self.choices =  [
				{ 'name' : 'start dungeon', 'method' : self.start_dungeon},
				{ 'name' : 'shop', 'method' : self.shop},
				{ 'name' : 'train', 'method' : self.train},
				{ 'name' : 'exit', 'method' : self.exit},
				]
		self.choice = 0
		imgs = load_animation('marker', 4)		
		self.marker = Animation(imgs, 400)

		self.cave_text = pygame.image.load(os.path.join(MISC, 'cave_text.png'))
		self.shop_text = pygame.image.load(os.path.join(MISC, 'shop_text.png'))
		self.workout_text = pygame.image.load(os.path.join(MISC, 'workout_text.png'))
		self.main_menu = pygame.image.load(os.path.join(MISC, 'main_menu_text.png'))

	def update(self, events, time_passed = 0 ):
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key  in [pygame.K_DOWN, pygame.K_RIGHT]:
					self.choice += 1
				if event.key in [pygame.K_UP, pygame.K_LEFT]:
					self.choice -= 1
				if event.key == pygame.K_RETURN:
					self.choices[self.choice]['method']()
					print 'enter'
		self.choice = self.choice % len(self.choices)
		pass
	
	def start_dungeon(self):
		self.model.new_scene = 'choose_dungeon'

	def shop(self):
		self.model.new_scene = 'shop'

	def train(self):
		self.model.new_scene = 'train'
	
	def exit(self):
		self.model.new_scene = 'main_menu'
