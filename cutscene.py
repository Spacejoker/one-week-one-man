import pygame 
from pygame.movie import Movie 
import os, sys 
import time
from constants import *

BGS = os.path.join('images','bg') 
CHARACTERS =os.path.join('images','characters') 
MISC =os.path.join('images','misc') 
SOUND = 'sound'

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
			screen.blit(img, (0, 0, WIDTH, HEIGHT))
			time.sleep(0.01)
			pygame.display.flip()

	@staticmethod
	def show(name, screen):
		font = pygame.font.SysFont("consolas", 40)
		scene = None
		if name == 'intro':
			scene = IntroScene()
		if scene == None:
			return
		bg = None
		character_face = None
		talk_box = None
		for event in scene.script['steps']:

			cmd = event['command']

			if bg != None:
				screen.blit(bg, (0,0))
			if talk_box != None:
				screen.blit(talk_box, (30,500))
			if character_face != None:
				screen.blit(character_face, (30,350))

			if cmd == 'set_bg':
				bg = pygame.image.load(os.path.join(BGS, event['value'] + '.png'))
				screen.blit(bg, (0,0))
				Cutscene.fade( bg, screen )

			if cmd == 'movie':
				Cutscene.play_movie('intro', screen)

			if cmd == 'fade_out':
				Cutscene.fade(bg, screen, fade_in= False)
			if cmd == 'show_character':	
				character_face = pygame.image.load(os.path.join(CHARACTERS, event['value'] + '.png'))
			if cmd == 'say':
				#write some text
				Cutscene.print_line(event, screen, font)

			if cmd == 'show_talkbox':
				if event['value'] == 'True':
					talk_box = pygame.image.load(os.path.join(BGS, 'talkbox.png'))
				else:
					talk_box = None

			if cmd != 'say':
				continue
			#print the stuff and wait for UI
			pygame.display.flip()
			while True:
				keymap = {}
				event = pygame.event.wait()
				if event.type == pygame.KEYDOWN:
					if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
						return
					break

	@staticmethod
	def print_line(event, screen, font):
		tot_string = event['line']
		y = 530
		x = 220
		label = font.render(event['character'] + ":" , 1, (20,0,0))
		screen.blit(label ,(x-30 - (len(event['character']) + 1) * 20, y))
		threshold = 40
		words = tot_string.split(" ")
		cur = ""
		for i,w in enumerate(words):
			newlen = len(w)  + len(cur)
			if newlen> threshold or i == len(words) -1:
				last = i == len(words) - 1
				if last:
					cur += w
				label = font.render(cur , 1, (20,0,0))
				screen.blit(label ,(x, y))
				cur = ""
				y += 45
				if last:
					break
			cur += w + " "
		label = font.render(cur , 1, (20,0,0))
		screen.blit(label ,(x, y))

class IntroScene():
	def __init__(self):
		self.script = {'steps' : [
			{'command' : 'set_bg', 'value': "jens_house"},
			{'command' : 'show_talkbox', 'value': "True"},
			{'command' : 'show_character', 'value': "sensei"},
			{'command' : 'say', 'character' : 'Sensei', 'line' : "Finally the day has come for me to retire as protector of the village, and one of you youngsters must take my place. It is a very honorable position."},
			{'command' : 'say', 'character' : 'Sensei', 'line' : "The most honorable in fact, as you all know I am married to the most beutiful girl in the village. She would not notice me if it was not for this job."},
			{'command' : 'say', 'character' : 'Sensei', 'line' : "Anyway rookies, let me explain this again to avoid confusion. I will take on mentorship for the most promising of you all. This is a once in a lifetime opportunity."},
			{'command' : 'show_character', 'value': "jens"},
			{'command' : 'say', 'character' : 'Jens', 'line' : "Hey Billy, I will beat you this time. I have practiced everyday for a year, you won't stand a chance."},
			{'command' : 'show_character', 'value': "billy"},
			{'command' : 'say', 'character' : 'Billy',  'line' : "Hehe whatever."},
			{'command' : 'say', 'character' : 'Billy',  'line' : "I have a special trick in store for you."},

			{'command' : 'show_character', 'value': "sensei"},
			{'command' : 'say', 'character' : 'Sensei', 'line' : "Shut up you two. We all know you are the favourites, but only the winner will take the place as my adept."},
			{'command' : 'fade_out'},
			{'command' : 'set_bg', 'value': "running_tracks"},
			{'command' : 'show_character', 'value': "sensei"},
			{'command' : 'say', 'character' : 'Sensei', 'line' : "Ok this is the test. The fastest runner will win."},
			{'command' : 'fade_out'},
#			{'command' : "movie",'value' : "jens_loss"},
			{'command' : 'set_bg', 'value': "running_tracks"},
			{'command' : 'show_character', 'value': "sensei"},
			{'command' : 'say', 'character' : 'Sensei', 'line' : "Congratulations Billy, you will be my new mentee. You can look forward to a life of glory and fame."},
			{'command' : 'show_character', 'value': "jens"},
			{'command' : 'say', 'character' : 'Jens', 'line' : "How could I loose. This can't be..."},
			{'command' : 'fade_out'},
#			{'command' : "movie", 'value' : "old jens"},
			{'command' : 'set_bg', 'value': "jens_house"},
			{'command' : 'show_character', 'value': "divel"},
			{'command' : 'say', 'character' : "Divel", 'line' : "So you are still upset about that race huh?"},
			{'command' : 'show_character', 'value': "jens"},
			{'command' : 'say', 'character' : 'Jens', 'line' : "Who are you?"},
			{'command' : 'show_character', 'value': "divel"},
			{'command' : 'say', 'character' : "Divel", 'line' : "I am here to help."},
			{'command' : 'show_character', 'value': "jens"},
			{'command' : 'say', 'character' : 'Jens', 'line' : "Well, after that day my life basically turned to shit. I am miserable. It is not fair."},
			{'command' : 'show_character', 'value': "divel"},
			{'command' : 'say', 'character' : "Divel", 'line' : "That is where I come in you see - i can help you get back at the world."},
			{'command' : 'show_character', 'value': "jens"},
			{'command' : 'say', 'character' : 'Jens', 'line' :  "I'm listening"},
			{'command' : 'show_character', 'value': "divel"},
			{'command' : 'say', 'character' : "Divel", 'line' : "Billy is a hero, right?"},
			{'command' : 'show_character', 'value': "jens"},
			{'command' : 'say', 'character' : 'Jens', 'line' : "Yeah, I guess. That cheap bastard!"},
			{'command' : 'show_character', 'value': "divel"},
			{'command' : 'say', 'character' : "Divel", 'line' : "And he runs dungeons and does other heroic stuff, right?"},
			{'command' : 'show_character', 'value': "jens"},
			{'command' : 'say', 'character' : 'Jens', 'line' : "Yeah, so? He is so much stronger than me, I cannot hurt him."},
			{'command' : 'show_character', 'value': "divel"},
			{'command' : 'say', 'character' : "Divel", 'line' : "No not you, weakling. But I can. I work as a dungeon boss, or well did, before i got unemployed."},
			{'command' : 'show_character', 'value': "jens"},
			{'command' : 'say', 'character' : 'Jens', 'line' : "Give me a break, you are like 2 sticks tall."},
			{'command' : 'show_character', 'value': "divel"},
			{'command' : 'say', 'character' : "Divel", 'line' : "With the right diet and training I can get stronger than any man. Then if we spread word about a great treasure and it gets to Billy, I can guard it."},
			{'command' : 'show_character', 'value': "jens"},
			{'command' : 'say', 'character' : 'Jens', 'line' : "Hmm, so what is the deal here?"},
			{'command' : 'show_character', 'value': "divel"},
			{'command' : 'say', 'character' : "Divel", 'line' : "Well, you help me become strong engouh to conquer the world and I promise I will get back at Billy."},
			{'command' : 'show_character', 'value': "jens"},
			{'command' : 'say', 'character' : 'Jens', 'line' : "..."},
			{'command' : 'say', 'character' : 'Jens', 'line' : "Ok, I'll do it. On one condition."},
			{'command' : 'show_character', 'value': "divel"},
			{'command' : 'say', 'character' :  "Divel",'line' : "Anything, dear."},
			{'command' : 'show_character', 'value': "jens"},
			{'command' : 'say', 'character' : 'Jens', 'line' : "That you kill him slowly."},
			{'command' : 'show_character', 'value': "divel"},
			{'command' : 'say', 'character' :  "Divel",'line' : "Of course, that will be my pleasure."},
			{'command' : 'say', 'character' :  "Divel",'line' : "Now let's get to work. You must help me become stronger in order for me to conquer the w... ahem Kill Billy Svensson."}]}

class RunIntro():
	def __init__(self, model):
		self.model = model
		Cutscene.show('intro', pygame.display.get_surface())
		self.model.new_scene = 'main_menu'

if __name__ == '__main__':

	pygame.init()
	#window = pygame.display.set_mode((WIDTH, HEIGHT)) 
	#Cutscene.show('intro', window)
	sys.exit()
