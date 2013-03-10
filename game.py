from menu import Scene
from cutscene import MISC, BGS, SOUND
import pygame
import os, sys
from constants import PLAY_SOUND

def load_animation(name, count):
	imgs = []
	for i in range(0, count):
		filename = name
		ending = str(i)
		while len(ending) < 4:
			ending  = "0" + ending
		filename += '_' + ending + '_a.png'
		print filename
		imgs.append(pygame.image.load(os.path.join(MISC, filename)))
	return imgs

class GameData():
	def __init__(self, data):
		self.data = data

	@staticmethod
	def gen_new_player():
		return GameData({
			'level' : 1,
			'upgrades' : [],
			'money' : 100})

class Animation():
	def __init__(self, images, delay):
		self.first_frame = pygame.time.get_ticks()
		self.images = images
		self.delay = delay	

	def get_frame(self):
		num = pygame.time.get_ticks()-self.first_frame
		num /= self.delay
		num = int(num)
		num %= len(self.images)
		return self.images[num]

class Town(Scene):
	def __init__(self, model):
		self.name = 'town'
		if not hasattr(model, 'game_state'):
			model.game_state = GameData.gen_new_player()

		model.places = {'places' : ['store', 'dungeons', 'something']}

		model.target_selection = target_selection = 0

		self.model = model
		self.bg =  pygame.image.load(os.path.join(BGS, 'town.png'))
		self.marker = pygame.image.load(os.path.join(MISC, 'menu_choice.png'))
		
		path = os.path.join(SOUND, 'cozy_melacholy.wav')

		song = pygame.mixer.Sound(path)
		model.song = song

		if PLAY_SOUND:
			model.song.play(loops=-1)
		
		self.choices =  [
				{ 'name' : 'start dungeon', 'method' : self.start_dungeon},
				{ 'name' : 'exit', 'method' : self.exit},
				]
		self.choice = 0
		imgs = load_animation('marker', 4)		
		self.marker = Animation(imgs, 400)
	
	def update(self, events, time_passed = 0 ):
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_DOWN:
					self.choice += 1
				if event.key == pygame.K_UP:
					self.choice -= 1
				if event.key == pygame.K_RETURN:
					self.choices[self.choice]['method']()
					print 'enter'
		self.choice = self.choice % len(self.choices)
		pass
	
	def start_dungeon(self):

		#set up dungeon data

		self.model.new_scene = 'start_dungeon'
	
	def exit(self):
		self.model.new_scene = 'main_menu'

class Dungeon(Scene):

	def __init__(self, model):
		self.name = 'dungeon'

	def update(self, events, time_passed):
		pass

