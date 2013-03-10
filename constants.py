from cutscene import MISC, BGS
import pygame
import os, sys

WIDTH = 1280
HEIGHT = 720
PLAY_SOUND = False
def load_image(directory, image):
	return pygame.image.load(os.path.join(directory, image + '.png'))

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
