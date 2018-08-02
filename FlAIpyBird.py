import sys
import pygame
import random

BIRD_LEFT = 200
MAX_UP_VELOCITY = 3.0
MAX_DOWN_VELOCITY = -3.0
MIN_PIPE_SIZE = 250
ACCELERATION = 0.15


class Frame:

    def __init__(self, width=1000, height=500,
                 bird_altitude=None, bird_velocity=0,
                 pipe_width=100, gap_height=200, pipe_distance=400):
        self.width = width
        self.height = height
        self.bird_altitude = height / 2 if bird_altitude is None else bird_altitude
        self.bird_velocity = bird_velocity
        self.impulse_ticks = 0

        self._pipe_width = pipe_width
        self._gap_height = gap_height
        self._pipe_distance = pipe_distance

        self.pipes = [self._create_pipe()]

        self._bird_sprite = pygame.image.load("Sprites/Bird.bmp")
        self._bird_sprite_rect = self._bird_sprite.get_rect()
        self._bird_max_height = self.height - self._bird_sprite_rect.height

        self._pipe_sprite = pygame.image.load("Sprites/Pipe_Upper_Desing2.bmp")

    def _create_pipe(self):
        return self.width, random.randint(MIN_PIPE_SIZE + self._gap_height, self.height - MIN_PIPE_SIZE)

    def tick(self):
        self.bird_altitude = min(self.bird_altitude - self.bird_velocity, self._bird_max_height)
        if self.bird_altitude == self._bird_max_height:
            self.bird_velocity = 0

        self.bird_velocity = min(
            MAX_UP_VELOCITY,
            max(
                MAX_DOWN_VELOCITY,
                self.bird_velocity + ACCELERATION if self.impulse_ticks > 0 else self.bird_velocity - ACCELERATION
            )
        )
        self.impulse_ticks = self.impulse_ticks - 1 if self.impulse_ticks > 0 else 0

        self.pipes = [(x-1, y) for (x, y) in self.pipes if x + self._pipe_width > 0]
        if self.pipes[-1][0] < self.width - self._pipe_distance:
            self.pipes.append(self._create_pipe())

        if self.collides():
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, collision=True))

    def collides(self):
        if self.bird_altitude >= self._bird_max_height:
            return True

        bird_rect = pygame.Rect(BIRD_LEFT, self.bird_altitude,
                                self._bird_sprite_rect.width, self._bird_sprite_rect.height)

        for pipe in self.pipes:
            if bird_rect.colliderect(self._lower_pipe(pipe)) or bird_rect.colliderect(self._upper_pipe(pipe)):
                return True

        return False

    def impulse(self):
        self.impulse_ticks = 50

    def _lower_pipe(self, pipe):
        return pygame.Rect(pipe[0], pipe[1], self._pipe_width, self.height - pipe[1])

    def _upper_pipe(self, pipe):
        return pygame.Rect(pipe[0], 0, self._pipe_width, pipe[1] - self._gap_height)

    def _paint_pipe(self, screen, sprite, pipe_rect):
        screen.blit(sprite,
                    dest=(pipe_rect.left, pipe_rect.top),
                    area=pygame.Rect(0, 0, pipe_rect.width, pipe_rect.height))

        # screen.fill((255, 255, 255, 50), pygame.Rect(pipe_rect.left, pipe_rect.top, pipe_rect.width, pipe_rect.height))

    def paint(self, screen):
        screen.blit(self._bird_sprite, dest=(BIRD_LEFT, self.bird_altitude))

        for pipe in self.pipes:
            self._paint_pipe(screen, self._pipe_sprite, self._lower_pipe(pipe))
            self._paint_pipe(screen, self._pipe_sprite, self._upper_pipe(pipe))


def main():
    pygame.init()

    size = width, height = 2000, 1000
    background = 196, 240, 255

    frame = Frame(width=width, height=height)
    screen = pygame.display.set_mode(size)

    while 1:
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                frame.impulse()
            if event.type == pygame.USEREVENT and event.collision:
                print("oops...")
                sys.exit()

        # step simulation
        frame.tick()

        # refresh screen
        screen.fill(background)
        frame.paint(screen)
        pygame.display.flip()


main()
