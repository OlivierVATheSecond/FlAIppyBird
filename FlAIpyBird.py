import sys
import pygame
from frame import Frame

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

        # check state
        if frame.collides():
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, collision=True))

        # refresh screen
        screen.fill(background)
        frame.paint(screen)
        pygame.display.flip()


main()
