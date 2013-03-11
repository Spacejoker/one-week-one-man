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
		self.draw_stats(scene, model)
	
	def draw_dungeon(self, scene, model):
		screen = self.screen
		screen.blit(scene.bg, (0,0))
		x0 = 20
		xsize = 50
		y0 = 20
		ysize = 50
		for y, line in enumerate(scene.field):
			for x, c in enumerate(scene.field[y]):
				scrpos = (x0 + x*xsize, y0 + y*ysize)
				if scene.field[y][x] == '.':
					screen.blit(scene.path_img, scrpos)

		for key in scene.enemies:
			x = x0 + key[0]*xsize
			y = y0 + key[1]*ysize
			scrpos = (x, y)
			enemy = scene.enemies[key]
			screen.blit(enemy.img, scrpos)
			hp_perc = enemy.hp / (enemy.maxhp + 0.0)
			hp_perc = max(0, (min(1, hp_perc)))
			pygame.draw.rect(screen, (int(255 - 255*hp_perc),min(255, int(400*hp_perc)),0), (x, y, int(xsize*hp_perc), 4))
		
		y = 520
		x = 58
		scene.console_messages.reverse()
		for id, msg in enumerate(scene.console_messages):
			if id > 7:
				break
			text_color = int(15 + max(0,135*min(1, (pygame.time.get_ticks() - msg['time'] - 1000 )/500.0)))
			col = (text_color, text_color, text_color)
			if msg['type'] == 'action':
				col = (255 - text_color, text_color - 15,text_color - 15)
			self.draw_text(msg['msg'], (x,y), small=True, color=col)
			y += 25
		scene.console_messages.reverse()

		x = 1075
		y = 93
		for id, item in enumerate(model.game_state['inventory']):
			self.draw_text(item.name + ' (' + str(item.quantity) + ')', (x,y), small=True)
			x += 30
	
		for hero in scene.heroes:
			pos =(x0 + xsize*hero.pos[0], y0 + ysize*hero.pos[1])
			screen.blit(hero.small_img,pos) 
			hp_perc = hero.hp / (hero.max_hp + 0.0)
			hp_perc = max(0, (min(1, hp_perc)))
			pygame.draw.rect(screen, (int(255 - 255*hp_perc),min(255, int(400*hp_perc)),0), (x, y, int(xsize*hp_perc), 4))
		
		self.draw_stats(scene, model)
		self.draw_hero_stats(scene, model)
		screen.blit(scene.divel, (x0 + xsize*scene.divel_pos[0], y0 + ysize*scene.divel_pos[1]))

	def draw_text(self, text, position, small = False, color = (250, 250, 250)):
		font = self.font
		if small:
			font = self.small_font
		label = font.render(text , True, color)
		self.screen.blit(label ,position)

	def draw_post(self, scene, model):
		self.screen.blit(scene.bg, (0,0))
		if scene.model.hero.hp < 0:
			self.draw_text("The hero " + model.hero.name  + " was defeated!", (50, 50))
			x = 50
			y = 100
			if len(model.game_state['loot']) == 0:
				self.draw_text("No loot! You minions must have stolen it.", (x, y), small = True)
			else:
				self.draw_text("The following was found on his/her corpse:", (x, y), small = True)

			y += 50
			x += 10

			for item in model.game_state['loot']:
				self.draw_text(str(item.quantity) + " "+ item.name, (x, y), small = True)
				y += 50
		else:
			self.draw_text("Divel was defeated, your treasure is lost!", (50, 50))

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
		self.draw_stats(scene, model)
	
	def draw_stats(self, scene, model):
		self.screen.blit(scene.character_bg, (870, 5))

		self.draw_text('Boss Level: ' + str( model.game_state['level']), (897, 35), small = True)
		self.draw_text('Gold: ' + str( model.game_state['gold'] ) , (897, 60), small = True)
		self.draw_text('Hp: ' + str( model.game_state['hp'] )  + ' / ' + str( model.game_state['max_hp'] ), (897, 85), small = True)

	def draw_hero_stats(self, scene, model):
		self.screen.blit(scene.character_bg, (870, 185))
		if len(scene.inactive_minions) == 0:
			return
		e = scene.inactive_minions[scene.chosen_inactive]
		self.screen.blit(e.img, (900, 210))

		self.draw_text(e.name + ', level ' + str(e.level) , (897, 270), small = True)
