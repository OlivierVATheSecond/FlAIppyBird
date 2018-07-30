import sys
import pygame
import random

MAX_DOWN_VELOCITY = -2
IMPULSE_VELOCITY = 3
IMPULSE_ACCELERATION = 4

class Frame:

    def __init__(self, width=1000, height=500,
                 bird_altitude=None, bird_velocity=0,
                 pipe_width=70, gap_height=250, pipe_distance=500):
        self.width = width
        self.height = height
        self.bird_altitude = height / 2 if bird_altitude is None else bird_altitude
        self.bird_velocity = bird_velocity
        self.bird_acceleration = -1

        self._pipe_width = pipe_width
        self._gap_height = gap_height
        self._pipe_distance = pipe_distance

        self.pipes = [(width + 10, 50)]

        self._bird_sprite = pygame.image.load("Sprites/Bird.bmp")
        self._bird_sprite_rect = self._bird_sprite.get_rect()
        self._pipe_color = 255, 255, 255

    def tick(self):
        self.bird_altitude = max(self.bird_altitude + self.bird_velocity, 0)
        self.bird_velocity = max(self.bird_velocity + self.bird_acceleration, MAX_DOWN_VELOCITY)
        self.bird_acceleration = max(self.bird_acceleration - 1, -1)

        self.pipes = [(x-1, y) for (x, y) in self.pipes if x + self._pipe_width > 0]
        if self.pipes[-1][0] < self.width - self._pipe_distance:
            self.pipes.append((self.width, random.randint(50, self.height - 50)))

    def impulse(self):
        self.bird_velocity = IMPULSE_VELOCITY
        self.bird_acceleration = IMPULSE_ACCELERATION

    def has_impact(self):
        return False

    def paint(self, screen):
        screen.blit(self._bird_sprite, (200, self.height - self.bird_altitude - self._bird_sprite_rect.height))

        for pipe in self.pipes:
            screen.fill(self._pipe_color,
                        pygame.Rect(pipe[0], self.height - pipe[1], self._pipe_width, self.height - pipe[1]))
            screen.fill(self._pipe_color,
                        pygame.Rect(pipe[0], 0, self._pipe_width, self.height - pipe[1] - self._gap_height))


def main():
    pygame.init()

    size = width, height = 2000, 1000
    black = 0, 0, 0

    frame = Frame(width=width, height=height)

    screen = pygame.display.set_mode(size)

    while 1:
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                frame.impulse()


        # step simulation
        frame.tick()

        # refresh screen
        screen.fill(black)
        frame.paint(screen)
        pygame.display.flip()


main()
