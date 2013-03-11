import pygame
from pygame.movie import Movie
import os, sys
import time
from graphics import Graphics
from menu import MainMenu
from cutscene import RunIntro
from game import Town, Dungeon, Enemy
from dungeon import ChooseDungeon

scenes = {'main_menu' : MainMenu,
		'run_intro' : RunIntro,
		'town' : Town,
		'start_dungeon' : Dungeon,
		'choose_dungeon' : ChooseDungeon
		}

pygame.mixer.init()

def loop():
	g = Graphics()
	last_paint = 0

	model = type('Model', (object,), {})
	model.exit = False
	model.new_scene = 'main_menu'
	model.boss = Enemy('boss', level = 10)
	model.boss.loot = []
	model.boss.hp = 100
	model.boss.defence = 10
	model.wait = False	

	t = time.time()
	while not model.exit:
		
		while model.new_scene != None:
			next_scene = model.new_scene
			model.new_scene = None
			clazz = scenes[next_scene]
			#give the scene a handle to the mixer
			scene = clazz(model)



		events = pygame.event.get()
		keymap = {}
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					return
			
		scene.update(events, time_passed = time.time() - t)
		t = time.time()

		if time.time() - last_paint > 1/30.0 or model.wait:
			last_paint = time.time()
			g.paint(scene, model)

		if model.wait:
			event = pygame.event.wait()
			if event.type == pygame.KEYDOWN:
				if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					return
			model.wait = False
			if hasattr(scene, 'start_time'):
				scene.start_time = pygame.time.get_ticks()
				scene.console_messages = []

if __name__ == '__main__':
	pygame.init()
	loop()
	sys.exit()
