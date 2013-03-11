from menu import Scene
from cutscene import MISC, BGS, SOUND, CHARACTERS
import pygame
import os, sys
from constants import PLAY_SOUND, load_animation, Animation, load_image
import random
from random import randrange
from game import Hero, Enemy, Loot

from namegen import NameGen

class ChooseDungeon(Scene):
	def __init__(self, model):
		self.name = 'choose'

		self.model = model
		self.bg =  pygame.image.load(os.path.join(BGS, 'choose.png'))
		imgs = load_animation('marker', 4)		
		self.marker = Animation(imgs, 400)
		
		gold_opts = [1] * 4
		
		val = 1
		while val < model.game_state['gold']:
			gold_opts.append(int(val))
			val *= 1.8
		gold_opts = gold_opts[-3:]
		gold_opts.append(model.game_state['gold'])
		self.gold_opts = gold_opts
		self.step = 0
		self.choices =  [
				{ 'name' : 'small', 'method' : self.gold},
				{ 'name' : 'medium', 'method' : self.gold},
				{ 'name' : 'large', 'method' : self.gold},
				{ 'name' : 'all_in', 'method' : self.gold},
				]

		self.choice = 0
		self.current_bet = 0
		self.current_hero = 0

	def gold(self):
		self.current_bet = self.gold_opts[self.choice]
		generator = NameGen('name_gen_file.txt')
		heroes = []
		for i in range(0,4):

			hero = Hero('fighter', 3)
			hero.name = generator.gen_word()
			heroes.append(hero)
			
		self.step2_choices = [
				{ 'name' : heroes[0].name + '(lvl ' + str(heroes[0].level) + ')', 'method' : self.hero},
				{ 'name' : heroes[1].name + '(lvl ' + str(heroes[1].level) + ')', 'method' : self.hero},
				{ 'name' : heroes[2].name + '(lvl ' + str(heroes[2].level) + ')', 'method' : self.hero},
				{ 'name' : heroes[3].name + '(lvl ' + str(heroes[3].level) + ')', 'method' : self.hero},
			]
		self.heroes = heroes

	def hero(self):
		self.chosen_hero = self.heroes[self.choice-4]


	def update(self, events, time_passed = 0 ):
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key  in [pygame.K_DOWN, pygame.K_RIGHT]:
					self.choice += 1
				if event.key in [pygame.K_UP, pygame.K_LEFT]:
					self.choice -= 1
				if event.key == pygame.K_RETURN:
					if self.step == 0:
						self.choices[self.choice]['method']()
						self.step = 1
					else:
						self.step2_choices[self.choice]['method']()
						self.model.new_scene = 'start_dungeon'

		self.choice = self.choice % len(self.choices)
		pass
