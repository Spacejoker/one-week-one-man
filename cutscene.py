import pygame
from pygame.movie import Movie
import os, sys
import time

WIDTH = 1280
HEIGHT = 720
BGS = os.path.join('images','bg')
class Cutscene():

	@staticmethod
	def fade(bg, screen, fade_in=True):
		FPS = 30
		fpsClock = pygame.time.Clock()
		DURATION = 0.5 # seconds
		start_time = time.clock()
		ratio = 0.0 # alpha as a float [0.0 .. 1.0]
		while ratio < 1.0:
			current_time = time.clock()
			ratio = (current_time - start_time) / DURATION
			if ratio > 1.0: # we're a bit late
				ratio = 1.0
			
			if not fade_in:
				ratio = 1 - ratio
			# all your drawing details go in the following call
			screen.fill((0,0,0), (0,0,WIDTH, HEIGHT))
			bg.set_alpha(ratio*255)
			screen.blit(bg, (0,0))
			pygame.display.flip()
			fpsClock.tick(FPS)

			if current_time - start_time > DURATION:
				break
	@staticmethod
	def play_movie(name, screen):
		imgs = []

		for i in range(0, 150):
			filename = 'Intro_'
			ending = str(i)
			while len(ending) < 5:
				ending  = "0" + ending
			filename += ending + '.png'
			imgs.append(pygame.image.load(os.path.join('movies', name, filename)))

		for img in imgs:
			window.blit(img, (0, 0, WIDTH, HEIGHT))
			time.sleep(0.01)
			pygame.display.flip()


	@staticmethod
	def show(name, screen):
		font = pygame.font.SysFont("consolas", 15)	
		if name == 'intro':
			scene = IntroScene()
			bg = None
			for event in scene.script['steps']:
				print event['command']
				cmd = event['command']
				if bg != None:
					screen.blit(bg, (0,0))

				if cmd == 'set_bg':
					bg = pygame.image.load(os.path.join(BGS, event['value'] + '.png'))
					screen.blit(bg, (0,0))
					Cutscene.fade( bg, screen )
					continue
				
				if cmd == 'movie':
					Cutscene.play_movie('intro', screen)
					continue

				if cmd == 'fade_out':
					Cutscene.fade(bg, screen, fade_in= False)
					continue
				
				if cmd == 'say':
					#write some text
					
					label = font.render(event['line'], 1, (255,255,255))
					screen.blit(label ,(300, 550))
					
				#print the stuff and wait for UI
				pygame.display.flip()
				while True:
					keymap = {}
					event = pygame.event.wait()
					if event.type == pygame.KEYDOWN:
						if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
							return
						break
class IntroScene():
	def __init__(self):
		self.script = {'steps' : [
			{'command' : 'set_bg', 'value': "jens_house"},
			{'command' : 'say', 'character' : "Mum", 'line' : "Good luck today Jens, I hope you win. I know how much you want this."},
			{'command' : 'say', 'character' : "Jens", 'line' : "Thank you mum, I will show all of them that I am the strongest."},
			{'command' : 'fade_out'},
			{'command' : 'set_bg', 'value': "old_man"},
			{'command' : 'say', 'character' : 'Sensei', 'line' : "Finally the day has come for me to retire as protector of the village, and one of you youngsters must take my place. It is a very honorable position. The most honorable in fact, as you all know I am married to the most beutiful girl in the village. She would not notice me if it was not for this job. Anyway rookies, let me explain this again to avoid confusion. I will take on mentorship for the most promising of you all. This is a once in a lifetime opportunity."},
			{'command' : 'say', 'character' : 'Jens', 'line' : "Hey Billy, I will beat you this time. I have practiced everyday for a year, you won't stand a chance."},
			{'command' : 'say', 'character' : 'Billy',  'line' : "Hehe whatever."},
			{'command' : 'say', 'character' : 'Sensei', 'line' : "Shut up you two. We all know you are the favourites, but only the winner will take the place as my adept."},
			{'command' : 'fade_out'},
			{'command' : 'set_bg', 'value': "running_tracks"},
			{'command' : 'say', 'character' : 'Sensei', 'line' : "Ok this is the test. The fastest runner will win."},
			{'command' : 'fade_out'},
			{'command' : "movie",'value' : "jens_loss"},
			{'command' : 'set_bg', 'value': "running_tracks"},
			{'command' : 'say', 'character' : 'Sensei', 'line' : "Congratulations Billy, you will be my new mentee. You can look forward to a life of glory and fame."},
			{'command' : 'say', 'character' : 'Jens', 'line' : "How could I loose. This can't be..."},
			{'command' : 'fade_out'},
			{'command' : "movie", 'value' : "old jens"},
			{'command' : 'set_bg', 'value': "jens_house"},
			{'command' : 'say', 'character' : "???", 'line' : "So you are still upset about that race huh?"},
			{'command' : 'say', 'character' : 'Jens', 'line' : "Who are you?"},
			{'command' : 'say', 'character' : "???", 'line' : "I am here to help."},
			{'command' : 'say', 'character' : 'Jens', 'line' : "Well, after that day my life basically turned to shit. I am miserable. It is not fair."},
			{'command' : 'say', 'character' : "???", 'line' : "That is where I come in you see - i can help you get back at the world."},
			{'command' : 'say', 'character' : 'Jens', 'line' :  "I'm listening"},
			{'command' : 'say', 'character' : "???", 'line' : "Billy is a hero now, right?"},
			{'command' : 'say', 'character' : 'Jens', 'line' : "Well yeah, that cheap bastard!"},
			{'command' : 'say', 'character' : "???", 'line' : "So he like, runs dungeons and stuff?"},
			{'command' : 'say', 'character' : 'Jens', 'line' : "Yeah, so? He is so much stronger than me, I cannot hurt him."},
			{'command' : 'say', 'character' : "???", 'line' : "No not you, weakling. But I. I can."},
			{'command' : 'say', 'character' : 'Jens', 'line' : "Give me a break, you are like 2 sticks tall."},
			{'command' : 'say', 'character' : "???", 'line' : "Whit the right diet and training I can get stronger any man."},
			{'command' : 'say', 'character' : 'Jens', 'line' : "So what is the deal?"},
			{'command' : 'say', 'character' : "???", 'line' : "Well, you help me become strong engouh to conquer the world and I promise I will get back at Billy."},
			{'command' : 'say', 'character' : 'Jens', 'line' : "..."},
			{'command' : 'say', 'character' : 'Jens', 'line' : "Ok, I'll do it. On one condition."},
			{'command' : 'say', 'character' :  "???",'line' : "Anything, dear."},
			{'command' : 'say', 'character' : 'Jens', 'line' : "That you kill him slowly."},
			{'command' : 'say', 'character' :  "???",'line' : "Of course, that will be my pleasure."},
			{'command' : 'say', 'character' :  "???",'line' : "Now let's get to work. You must help me become stronger in order for me to conquer the w... eh Kill Billy Svensson I mean."}]}
if __name__ == '__main__':

	pygame.init()
	window = pygame.display.set_mode((WIDTH, HEIGHT)) 
	Cutscene.show('intro', window)
	sys.exit()
