import pygame
from constants import *
graphics = {}

class Graphics():
	def __init__(self):

		self.font = pygame.font.SysFont("consolas", 40)
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		self.paintmodes = {
				'main_menu' : self.draw_main_menu,
				'town' : self.draw_town
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

		self.screen.blit(scene.menu_choice, (x-40, y0 + scene.choice*50))
	
	def draw_town(self, scene, model):
		
		font = self.font
		self.screen.blit(scene.bg, (0,0))
		if scene.choice == 0:
			self.screen.blit(scene.marker.get_frame(), (233, 216))
		elif scene.choice == 1:
			self.screen.blit(scene.marker.get_frame(), (258, 596))
		pass
