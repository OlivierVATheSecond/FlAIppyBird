import sys
import pygame
from frame import Frame
import math
import time

class ReinforcementAI:

	def __init__(self):
		self.alpha = 0.0
		self.gamma = 0.01

	def _next_pipe(self, frame):
		for pipe in frame.pipes:
			if pipe[0] + frame._pipe_width > 200:
				return pipe

		print("no more pipes...")
		return None

	def _gap_rect(self, frame, pipe):
		return pygame.Rect(pipe[0], pipe[1] - frame._gap_height, frame._pipe_width, frame._gap_height)

	def decide(self, frame):
		if frame.impulse_ticks > 0:
			return False

		next_pipe = self._next_pipe(frame)
		if next_pipe is None:
			return False

		bird_center = frame.bird_rect().center
		gap_center = self._gap_rect(frame, next_pipe).center
		opposite = gap_center[1] - bird_center[1]
		adjacent = gap_center[0] - bird_center[0]
		if adjacent == 0.0:
			return False

		angle = math.atan2(opposite, adjacent)
		return angle < self.alpha

	def train(self, too_high):
		if too_high:
			self.alpha -= self.gamma
		else:
			self.alpha += self.gamma
		print(self.alpha)

def main():
	pygame.init()

	size = width, height = 1920, 1080
	gap_height = 175
	background = 196, 240, 255

	frame = Frame(width=width, height=height, gap_height=gap_height)
	screen = pygame.display.set_mode(size)

	ai = ReinforcementAI()

	while 1:
		# handle events
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				sys.exit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				frame.impulse()

		# AI
		if ai.decide(frame):
			frame.impulse()

		# step simulation
		frame.tick()

		# refresh screen
		screen.fill(background)
		frame.paint(screen)
		pygame.display.flip()

		# check state
		collission = frame.collides()
		if collission:
			time.sleep(0.2)
			ai.train(collission > 0)
			frame = Frame(width=width, height=height, gap_height=gap_height)


main()
