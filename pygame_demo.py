import sys, pygame
pygame.init()

size = width, height = 2000, 1000
speed = [1, 1]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball = pygame.image.load("Sprites/Bird.bmp")
ballrect = ball.get_rect()

while 1:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # step simulation
    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    # refresh screen
    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()