from menu import Scene
from cutscene import MISC, BGS, SOUND, CHARACTERS
import pygame
import os, sys
from constants import PLAY_SOUND, load_animation, Animation, load_image
import random
from random import randrange
from game import Hero, Enemy, Loot
from collections import deque
from namegen import NameGen

class ChooseDungeon(Scene):
	def __init__(self, model):
		self.character_bg = load_image(MISC, 'character')
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
		model.boss = Enemy(enemy_type = 'boss', level = model.game_state['level'])
		model.boss.loot = []
		model.boss.hp = model.game_state['hp']
		model.boss.defense = model.game_state['defense']

	def gold(self):
		self.current_bet = self.gold_opts[self.choice]
		generator = NameGen('name_gen_file.txt')
		heroes = []
		for i in range(0,4):

			hero = Hero('fighter', randrange(1,int(max(3, self.current_bet/1000))))
			hero.name = generator.gen_word()
			heroes.append(hero)
			
		self.step2_choices = [
				{ 'name' : heroes[0].name + '(lvl ' + str(heroes[0].level) + ')', 'method' : self.hero},
				{ 'name' : heroes[1].name + '(lvl ' + str(heroes[1].level) + ')', 'method' : self.hero},
				{ 'name' : heroes[2].name + '(lvl ' + str(heroes[2].level) + ')', 'method' : self.hero},
				{ 'name' : heroes[3].name + '(lvl ' + str(heroes[3].level) + ')', 'method' : self.hero},
			]
		self.heroes = heroes
		self.model.bet = self.current_bet

	def hero(self):
		self.chosen_hero = self.heroes[self.choice-4]
		self.model.hero = self.chosen_hero


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

class PostDungeon(Scene):

	def __init__(self, model):
		self.character_bg = load_image(MISC, 'character')
		self.name = 'post'

		self.model = model

		#self.gained_gold = model.game_state['gained_gold']
		#model.game_state['gold']  = model.game_state['gold']  + self.gained_gold
		s = model.game_state
		for item in model.game_state['loot']:
			if item.name == 'gold':
				s['gold'] += item.quantity
			else:
				if item.name in s:
					s[item.name] += item.quantity
				else:
					s[item.name] = item.quantity

			

		self.bg =  pygame.image.load(os.path.join(BGS, 'choose.png'))

	def update(self, events, time_passed = 0 ):
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key  in [pygame.K_RETURN]:
					self.model.game_state['loot'] = {}
					self.model.new_scene = 'town'

class Dungeon(Scene):

	def __init__(self, model):
		self.character_bg = load_image(MISC, 'character')
		self.hero = model.hero
		self.name = 'dungeon'
		self.bg = pygame.image.load(os.path.join(BGS,'dungeon.png'))
		self.path_img = load_image(MISC, 'path')
		self.field = [
			 '##################',
			 '#................#',
			 '#................#',
			 '#................#',
			 '#......##........#',
			 '#......##........#',
			 '#................#',
			 '#................#',
			 '#................#',
			 '##################']


		enemies = {}
		for i in range(1, 20):
			if random.random() > 0.6:
				x = randrange(0, 14)
				y = randrange(0,9)
				pos = (x,y)
				if self.field[y][x] == '.' and pos not in enemies:
					enemies[pos] = Enemy(level=randrange(1, 25))

		self.enemies = enemies
		self.divel_pos = (1,1)
		self.heroes = [Hero('fighter', 4)]
		self.start_time = pygame.time.get_ticks()
		self.console_messages = [self.hero.name + " enters the dungeon"]
		self.enemies = enemies
		self.model = model
		self.choice = 0
		self.old_msg = []

	def fight(self, monster, hero):
		hero_action = hero.get_action()
		if hero_action['action'] == 'attack':
			hdmg = 	hero_action['value']
			totdmg = hdmg - monster.defense
			if totdmg <= 0:
				self.console_messages.append(hero.name + " does no damage to " + monster.name)
			else:
				self.console_messages.append(hero.name + " does " + str(totdmg) + " damage to " + monster.name)
				monster.hp -= totdmg

				if monster.hp > 0:
					self.console_messages.append(monster.name + " hp seems to be around " + str(monster.hp))
		if monster.hp <= 0:
			#todo kill monster 
			self.console_messages.append( monster.name + " is defeated")
			loot_msg = hero.add_loot(monster.loot)
			for m in loot_msg:
				self.console_messages.append( m)

		mdmg = monster.roll_dmg()
		totdmg = mdmg - hero.defense
		if monster.hp < 0:
			pass
		elif totdmg <= 0:
			self.console_messages.append(monster.name + " does no damage to " + hero.name)
		else:
			self.console_messages.append(monster.name + " does " + str(totdmg) + " damage to " + hero.name)
			hero.hp -= totdmg
		if hero.hp <= 0 or self.enemies[len(self.path) -1] == None:
			self.console_messages.append(hero.name + " is defeated")

	def update(self, events, time_passed):
		update_now = False
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key  in [pygame.K_DOWN, pygame.K_RIGHT]:
					self.choice += 1
					self.divel_pos = (self.dviel_pos[0] + 1, self.divel_pos[1] + 1)
					return
				if event.key  in [pygame.K_SPACE]:
					update_now = True

		if pygame.time.get_ticks() - self.start_time > 1000:
			update_now = True
			self.start_time = pygame.time.get_ticks()
			self.archive()
		#if self.in_fight:
			#self.fight()
			#if self.enemies[hero_pos + 1] == None:
				#self.in_fight = False
		#elif self.enemies[hero_pos + 1] != None:
			#enemy = self.enemies[hero_pos +1]
			#self.console_messages.append(self.hero.name + " encounters a " + enemy.name + "(lvl " + str(enemy.level) + ")")
			#self.in_fight = True
		#else:
			for h in self.heroes:
				if h.path == None or len(h.path) == 0:
					dirs = [(1,0), (-1,0), (0,1), (0,-1)]
					visited = []
					parent = {}
					queue = deque()
					queue.append(h.pos)
					visited.append(h.pos)
					target = (1,1)
					while len(queue) > 0:
						pop = queue.popleft()
						if pop == target:
							break
						random.shuffle(dirs)
						for d in dirs:
							newpos = (pop[0] + d[0], pop[1] + d[1])
							if newpos not in visited and self.field[newpos[1]][newpos[0]] == '.':
								queue.append(newpos)
								parent[newpos] = pop
								visited.append(newpos)

					path = deque()
					pos = target
					while(pos != h.pos):
						path.append(pos)
						pos = parent[pos]
					path.reverse()
					h.path = path

				h.pos = h.path.popleft()

			self.console_messages.append(h.name + " continues exploring the dungeon")
			#self.hero_pos = min(self.hero_pos + 1, len(self.path) -2)

		state = self.model.game_state

	def archive(self):
		self.old_msg.extend(self.console_messages)
		self.console_messages = []

		if len( self.old_msg) > 7:
			self.old_msg = self.old_msg[-7:]
