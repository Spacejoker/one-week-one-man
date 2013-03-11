import pygame
from constants import *
graphics = {}

class Graphics():
	def __init__(self):

		self.font = pygame.font.SysFont("consolas", 40)
		self.small_font = pygame.font.SysFont("consolas", 20)
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		self.paintmodes = {
				'main_menu' : self.draw_main_menu,
				'town' : self.draw_town,
				'dungeon' : self.draw_dungeon,
				'choose':  self.draw_choose,
				'post' : self.draw_post
				}

	def paint(self, scene, model):

		if scene.name in self.paintmodes:
			self.paintmodes[scene.name](scene, model)

		pygame.display.flip()

	def draw_main_menu(self, scene, model):
		font = self.font
		self.screen.blit(scene.bg, (0,0))
		y0 = 200
		y = y0
		x = 500
		for c in scene.choices:
			name = c['name']
			label = font.render(name , True, (255,255,255))
			self.screen.blit(label ,(500, y))
			y += 50

		self.screen.blit(scene.menu_choice.get_frame(), (x-70, y0 - 10 + scene.choice*50))
	
	def draw_town(self, scene, model):
		
		font = self.font
		self.screen.blit(scene.bg, (0,0))
		if scene.choice == 0:
			self.screen.blit(scene.marker.get_frame(), (233, 216))
			self.screen.blit(scene.cave_text, (170, 120))
		elif scene.choice == 1:
			self.screen.blit(scene.marker.get_frame(), (258, 596))
			self.screen.blit(scene.shop_text, (92, 402))
		elif scene.choice == 2:
			self.screen.blit(scene.marker.get_frame(), (1003, 307))
			self.screen.blit(scene.workout_text, (790, 210))
		elif scene.choice == 3:
			self.screen.blit(scene.marker.get_frame(), (1125, 634))
			self.screen.blit(scene.main_menu, (700, 470))
	
	def draw_dungeon(self, scene, model):
		screen = self.screen
		screen.blit(scene.bg, (0,0))
		for pos, step in enumerate(scene.path):
			scrpos = (600 + step[0]*50, 200 + step[1]*50)
			if pos > scene.hero_pos + 1 and pos != len(scene.path) - 1:
				continue
			screen.blit(scene.path_img, scrpos)
			if scene.bgitems[pos] != None and scene.enemies[pos] == None:
				screen.blit(scene.bgitems[pos], scrpos)
			if pos == scene.hero_pos and scene.hero.hp > 0:
				screen.blit(scene.hero.small_img, scrpos)
			elif scene.enemies[pos] != None:
				screen.blit(scene.enemies[pos].img, scrpos)
		
		y = 520
		x = 58
		for id, msg in enumerate(scene.console_messages):
			if id > 7:
				break
			label = self.small_font.render(msg , 1, (15,15, 15))
			self.screen.blit(label ,(x, y))
			y += 25
		
		x = 1075
		y = 93
		for id, item in enumerate(model.game_state['inventory']):
			self.draw_text(item.name + ' (' + str(item.quantity) + ')', (x,y), small=True)
			x += 30

	def draw_text(self, text, position, small = False):
		font = self.font
		if small:
			font = self.small_font
		label = font.render(text , True, (255,255,255))
		self.screen.blit(label ,position)

	def draw_post(self, scene, model):
		self.screen.blit(scene.bg, (0,0))
		if scene.model.hero.hp < 0:
			self.draw_text("The hero " + model.hero.name  + " was defeated!", (50, 50))
		x = 50
		y = 100
		if len(model.game_state['loot']) == 0:
			self.draw_text("No loot! You minions must have stolen it.", (x, y), small = True)

		for item in model.game_state['loot']:
			self.draw_text(str(item.quantity) + " "+ item.name, (x, y), small = True)
			y += 50

	def draw_choose(self, scene, model):
		self.screen.blit(scene.bg, (0,0))
		y0 = 100
		y = y0
		x = 300
		mod = 130
		
		if scene.step == 0:
			label = self.font.render("Choose treasure" , True, (255,255,255))
			self.screen.blit(label ,(50, 59))
			for i, c in enumerate(scene.choices):
				x = 300 + (i/4)*500
				y = y0  + mod* (i % 4)
				
				name = c['name']
				label = self.font.render(name , True, (255,255,255))
				self.screen.blit(label ,(x, y))
				if i < 4:
					label = self.font.render("(" + str(scene.gold_opts[i]) + " gold)" , True, (255,255,255))
					self.screen.blit(label ,(x, y+50))
		elif scene.step == 1:
			label = self.font.render("Chosen treasure yielded the following interest:"  , True, (255,255,255))
			self.screen.blit(label ,(50, 59))
			for i, c in enumerate(scene.step2_choices):
				x = 300 + (i/4)*500
				y = y0  + mod* (i % 4)
				
				name = c['name']
				label = self.font.render(name , True, (255,255,255))
				self.screen.blit(label ,(x, y))

		x = 300 + (scene.choice / 4)*500
		y = mod * (scene.choice % 4)

		self.screen.blit(scene.marker.get_frame(), (x-70,y0 +  y - 10 ))

		if scene.step == 1:
			label = self.font.render("chosen treasure: " + str(scene.current_bet) , True, (255,255,255))
			self.screen.blit(label ,(50, 640))
