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
			scrpos = (600 + step[0]*50, 200 + step[1]*50))
			screen.blit(scene.path_img, scrpos)
			if pos == scene.hero_pos:
				screen.blit(scene.hero.small_img, scrpos)
				break
		
		y = 520
		x = 58
		for id, msg in enumerate(scene.console_messages):
			if id > 4:
				break
			label = self.small_font.render(msg , 1, (15,15, 15))
			self.screen.blit(label ,(x, y))
			y += 25
