import pygame
from pygame.movie import Movie
import os, sys
import time
from graphics import Graphics
from menu import MainMenu
from cutscene import RunIntro
from game import Town, Enemy
from dungeon import ChooseDungeon, PostDungeon, Dungeon
from training import TrainingGround
from platform import Platform

scenes = {'main_menu' : MainMenu,
		'run_intro' : RunIntro,
		'town' : Town,
		'start_dungeon' : Dungeon,
		'choose_dungeon' : ChooseDungeon,
		'post_dungeon' : PostDungeon,
		'train' : TrainingGround,
		'platform' : Platform
		}

pygame.mixer.init()
def loop():
	g = Graphics()
	last_paint = 0

	pygame.key.set_repeat(500, 100)

	model = type('Model', (object,), {})
	model.exit = False
	model.new_scene = 'main_menu'
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
			print 'fps: ', 1.0/(time.time() - last_paint)
			last_paint = time.time()
			g.paint(scene, model)


if __name__ == '__main__':
	pygame.init()
	loop()
	sys.exit()
