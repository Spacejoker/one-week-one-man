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
		self.name = 'dungeon'
		self.bg = pygame.image.load(os.path.join(BGS,'dungeon.png'))
		self.treasure = load_image(MISC, 'treasure')
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

		self.enemies = {}
		self.spawn = (16,8)
		self.divel_pos = (1,1)

		self.inactive_minions = []
		for i in range(1, 10):
			self.inactive_minions.append(Enemy(level=randrange(1, 5)))

		self.heroes = []
		self.start_time = pygame.time.get_ticks()
		self.model = model
		self.choice = 0
		self.old_msg = []
		self.pos = (1,1)	
		self.treasure_pos = (1,1)
		self.divel = load_image(MISC, 'enemy_boss')
		self.console_messages = []
		self.show_minions = False
		self.add_hero()
		self.chosen_inactive = 0
		self.chosen_item = 0
		self.items = model.game_state['inventory']
		self.bet = 10

	def add_hero(self):
		hero = Hero('fighter', 10)
		self.heroes.append(hero)
		self.console_messages.append({'msg' : hero.name + ' enters the cage', 'time' : pygame.time.get_ticks(), 'type' : 'event'})

	def fight(self, monster, hero, monster_pos):
		hero_action = hero.get_action()
		if hero_action['action'] == 'attack':
			hdmg = 	hero_action['value']
			totdmg = hdmg - monster.defense
			if totdmg <= 0:
				self.console_messages.append({'msg' : hero.name + " does no damage to " + monster.name, 'time' : pygame.time.get_ticks(), 'type' : 'event'})
			else:
				self.console_messages.append({'msg' : hero.name + " does " + str(totdmg) + " damage to " + monster.name, 'time' : pygame.time.get_ticks(), 'type' : 'event'})
				monster.hp -= totdmg

				if monster.hp > 0:
					self.console_messages.append({'msg' : monster.name + " hp seems to be around " + str(monster.hp), 'time' : pygame.time.get_ticks(), 'type' : 'event'})
		if monster.hp <= 0:
			#todo kill monster 
			self.console_messages.append({'msg' :  monster.name + " is defeated", 'time' : pygame.time.get_ticks(), 'type' : 'event'})
			del self.enemies[monster_pos]

		mdmg = monster.roll_dmg()
		totdmg = mdmg - hero.defense
		if monster.hp < 0:
			pass
		elif totdmg <= 0:
			self.console_messages.append({'msg' : monster.name + " does no damage to " + hero.name, 'time' : pygame.time.get_ticks(), 'type' : 'event'})
		else:
			self.console_messages.append({'msg' : monster.name + " does " + str(totdmg) + " damage to " + hero.name, 'time' : pygame.time.get_ticks(), 'type' : 'event'})
			hero.hp -= totdmg
		if hero.hp <= 0:
			self.console_messages.append({'msg' : hero.name + " is defeated", 'time' : pygame.time.get_ticks(), 'type' : 'event'})

	def isfree(self, pos):
		return self.field[pos[1]][pos[0]] == '.' and pos not in [x.pos for x in self.heroes]

	def use_item(self, item):
		pos = self.divel_pos
		e = None
		if pos in self.enemies:
			e = self.enemies[pos]

		pots = {'Potion' : 5, 'Mega Potion' : 100, 'Super Mega Potion' : 500}
		if item.name in pots:
			if e == None:
				return
			e.hp = max(e.hp + pots[item.name], e.maxhp)
			self.items[self.chosen_item].quantity -= 1
			if self.items[self.chosen_item].quantity == 0:
				del self.items[self.chosen_item]
				if len(self.items) > 0:
					self.chosen_item %= len(self.items)
				else:
					self.chosen_item = 0
			self.console_messages.append({'msg' : 'Used ' + item.name + ' on ' + e.name, 'time' : pygame.time.get_ticks(), 'type' : 'event'})



	def update(self, events, time_passed):
		update_now = False
		for event in events:
			move_map = {pygame.K_DOWN : (self.divel_pos[0] , self.divel_pos[1] + 1),
			pygame.K_UP : (self.divel_pos[0] , self.divel_pos[1] - 1),
			pygame.K_LEFT : (self.divel_pos[0] - 1, self.divel_pos[1] ),
			pygame.K_RIGHT : (self.divel_pos[0] + 1, self.divel_pos[1] )}

			for h in self.heroes:
				h.path = []

			if event.type == pygame.KEYDOWN:
				if event.key  in move_map:
					mods = pygame.key.get_mods() # an integer representing the
					if mods & (pygame.KMOD_CTRL): # pressed modifier keys (shift, alt, ctrl...)
						if event.key == pygame.K_UP:
							self.chosen_item -= 1
						if event.key == pygame.K_DOWN:	
							self.chosen_item += 1	
						l = len(self.items)
						if l > 0:
							self.chosen_item += l
							self.chosen_item %= l
					elif mods & (pygame.KMOD_SHIFT):
						if event.key == pygame.K_DOWN:
							self.chosen_inactive -= 1
						if event.key == pygame.K_UP:
							self.chosen_inactive += 1
					else:
						new_pos = move_map[event.key]
						if self.isfree(new_pos):
							self.divel_pos = new_pos
				if event.key == pygame.K_RETURN:
					self.use_item(self.items[self.chosen_item])
				if event.unicode in ['d', 'D']:
					if self.divel_pos in self.enemies:
						rem = self.enemies[self.divel_pos]
						del self.enemies[self.divel_pos]
						self.inactive_minions.append(rem)
						self.console_messages.append({'msg' : 'Deleted mob' , 'time' : pygame.time.get_ticks(), 'type' : 'action'})
				if event.unicode in ['a', 'A'] and self.isfree(self.divel_pos):
					pos = self.divel_pos
					if pos not in self.enemies and len(self.inactive_minions) > 0:
						im = self.inactive_minions
						e = im[self.chosen_inactive]
						del im[self.chosen_inactive]
						self.inactive_minions = im
						self.enemies[pos] = e
				if event.unicode == '+':
					val = 1
					while val <= self.bet:
						val *= 1.8
					val = int(val)
					#add treasure
					curg = self.model.game_state['gold']
					cando = min(val, curg)
					self.model.game_state['gold'] -= cando
					self.bet += cando
				if event.unicode == '-':
					if self.bet > 0:
						val = 1
						while val * 1.8 < self.bet:
							val *= 1.8
						val = int(val)
						#add treasure
						curg = self.model.game_state['gold']
						cando = val
						self.model.game_state['gold'] += cando
						self.bet -= cando

				l = len(self.inactive_minions)
				if l > 0:
					self.chosen_inactive += l
					self.chosen_inactive %= l
				

		if pygame.time.get_ticks() - self.start_time > 1000:
			update_now = True
			self.start_time = pygame.time.get_ticks()
			self.archive()

			self.heroes = [x for x in self.heroes if x.hp > 0]
			for h in self.heroes:
				if h.pos == self.treasure_pos:
					self.model.new_scene = 'post_dungeon'
					self.model.success = False
					return
				dirs = [(1,0), (-1,0), (0,1), (0,-1)]
				fight = False
				for d in dirs:
					newpos = (h.pos[0] + d[0], h.pos[1] + d[1])
					if newpos in self.enemies:
						self.fight(self.enemies[newpos], h, newpos)
						fight = True
				if fight:
					continue

				if h.path == None or len(h.path) == 0:
					visited = []
					parent = {}
					queue = deque()
					queue.append(h.pos)
					visited.append(h.pos)
					target = self.treasure_pos
					while len(queue) > 0:
						pop = queue.popleft()
						if pop == target:
							break
						random.shuffle(dirs)
						for d in dirs:
							newpos = (pop[0] + d[0], pop[1] + d[1])
							if self.isfree(newpos) and newpos not in visited:
								queue.append(newpos)
								parent[newpos] = pop
								visited.append(newpos)

					path = deque()
					pos = target
					while(pos != h.pos) and pos in parent:
						path.append(pos)
						pos = parent[pos]
					path.reverse()
					h.path = path
				if len(h.path) > 0:
					h.pos = h.path.popleft()
				h.path = deque()

			if random.random() > 0.85 and self.spawn not in [x.pos for x in self.heroes] and len(self.heroes) <= 4:
				self.add_hero()
			if random.random() > 0.2 and len(self.heroes) == 0:
				self.add_hero()

		state = self.model.game_state

	def archive(self):
		if len( self.console_messages) > 7:
			self.console_messages = self.console_messages[-7:]
