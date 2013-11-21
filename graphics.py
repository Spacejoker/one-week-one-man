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
				'post' : self.draw_post,
				'training' : self.draw_training,
				'platform' : self.draw_platform,
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

	def draw_platform(self, scene, model):
		x0, y0 = scene.get_map_pos()#wrong sign!, render something at x,y on x+x0, y+y0
		sz = scene.tilesize
		startpos = (x0/sz, y0/sz)
		xmod = x0 % sz
		ymod = y0 % sz
		w = WIDTH/sz + 2
		h = HEIGHT/sz + 2
		

		for y in range(-1, h):
			for x in range(-1, + w):
				tilenr = scene.get_tile_at((x - startpos[0],y-startpos[1]))
				img = scene.tiles[tilenr]
				self.screen.blit(img, (x*sz + xmod, y*sz + ymod))#((x-startpos[0])*sz + xmod, (y-startpos[1])*sz + ymod))
				
		if scene.clickpos != None:
			clicktarget = (scene.clickpos[0] + x0, scene.clickpos[1] + y0)
			self.screen.blit(scene.tiles[12], map(sum, zip(clicktarget,(-sz/2, -sz/2))))

		#draw crew
		c = scene.crew.leader
		self.screen.blit(c.image, (x0 + c.x, y0 + c.y))

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
		
		screen.blit(scene.treasure, (scene.treasure_pos[0]*xsize + x0, y0 + scene.treasure_pos[1]*ysize)) 

		for key in scene.enemies:
			x = x0 + key[0]*xsize
			y = y0 + key[1]*ysize
			scrpos = (x, y)
			enemy = scene.enemies[key]
			screen.blit(enemy.img, scrpos)
			hp_perc = enemy.hp / (enemy.maxhp + 0.0)
			hp_perc = max(0, (min(1, hp_perc)))
			pygame.draw.rect(screen, (int(255 - 255*hp_perc),min(255, int(400*hp_perc)),0), (x, y, int(xsize*hp_perc), 3))
			self.draw_text(str(enemy.level), (x + 30, y + 30), small=True)
		
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

	
		for hero in scene.heroes:
			pos =(x0 + xsize*hero.pos[0], y0 + ysize*hero.pos[1])
			screen.blit(hero.small_img,pos) 
			hp_perc = hero.hp / (hero.max_hp + 0.0)
			hp_perc = max(0, (min(1, hp_perc)))
			pygame.draw.rect(screen, (int(255 - 255*hp_perc),min(255, int(400*hp_perc)),0), (pos[0], pos[1], int(xsize*hp_perc), 3))
			self.draw_text(str(hero.level), (pos[0] + 30, pos[1] + 30), small=True)
		
		self.draw_stats(scene, model)
		self.draw_hero_stats(scene, model)
		screen.blit(scene.divel, (x0 + xsize*scene.divel_pos[0], y0 + ysize*scene.divel_pos[1]))
	
		opts = [item['name'] + ' (' + str(item['qty']) + ')' for item in scene.items]
		x = 700
		y = 526
		self.draw_scroll_menu(scene.chosen_item, opts, x, y)
		#for id in range(scene.chosen_item, scene.chosen_item + min(len(scene.items), 5)):
			#item = scene.items[id % len(scene.items)]
			#self.draw_text(item.name + ' (' + str(item.quantity) + ')', (x,y), small = True, color = (15, 15,15))
			#y += 30



	def draw_text(self, text, position, small = False, color = (250, 250, 250)):
		font = self.font
		if small:
			font = self.small_font
		label = font.render(text , True, color)
		self.screen.blit(label ,position)

	def draw_post(self, scene, model):
		self.screen.blit(scene.bg, (0,0))
		if scene.model.success:
			self.draw_text("Win! Show some xp", (50, 50))
		else:
			self.draw_text("The treasure was lost!", (50, 50))

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
		if hasattr(scene, 'bet'):
			self.draw_text('Current chest gold: ' + str(scene.bet), (897, 110), small = True)

	def draw_hero_stats(self, scene, model):
		self.screen.blit(scene.character_bg, (870, 185))
		if len(scene.inactive_minions) == 0:
			return
		e = scene.inactive_minions[scene.chosen_inactive]
		self.screen.blit(e.img, (900, 210))

		self.draw_text(e.name + ', level ' + str(e.level) , (897, 270), small = True)

	def draw_training(self, scene, model):
		self.screen.blit(scene.bg, (0,0))
		x0 = 107
		y0 = 170
		self.draw_scroll_menu(scene.chosen_option, [o['name'] + " " + str( o['price'] ) + " gold" for o in scene.options], x0, y0, num=15)

	def draw_scroll_menu(self, chosen, options, x0, y0, num=5):
		x = x0
		y = y0
		for id in range(chosen, chosen + min(len(options), num)):
			item = options[id % len(options)]
			self.draw_text(item, (x,y), small = True, color = (15, 15,15))
			y += 30
