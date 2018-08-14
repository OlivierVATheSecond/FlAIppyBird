import sys
import pygame
import math
import random
import time
import frame

class EquiWorldFrame(frame.Frame):

    def __init__(self, width, height, first_pipe):
        self.next_pipe = first_pipe
        super().__init__(width=width, height=height)

    def set_next_pipe(self, pipe):
        self.next_pipe = pipe

    def _create_pipe(self):
        return self.next_pipe

class Individual:

    def __init__(self, genome=None):
        self.genome = [random.uniform(-5, +5) for i in range(8)] if genome is None else genome
        self.died = 0
        self.impulses = 0

    def cross(self, other):
        child = Individual()
        cut_point = random.randint(0, len(self.genome) - 1)
        child.genome = [self.genome[i] if i < cut_point else other.genome[i] for i in range(8)]
        return child

    def mutant(self, chance):
        child = Individual(self.genome)
        if random.random() <= chance:
            child.genome[random.randint(0, len(child.genome) -  1)] += random.uniform(-0.2, 0.2)
        return child

    @staticmethod
    def _normalize(value, min_val, max_val):
        return 2.0 * ((value - min_val) / (max_val - min_val)) - 1.0

    def _state(self, current_frame):
        bird_rect = current_frame.bird_rect()
        bird_center = current_frame.bird_rect().center

        next_pipe = current_frame._next_pipe(30)
        lower_rect = current_frame._lower_pipe(next_pipe)
        upper_rect = current_frame._upper_pipe(next_pipe)

        gap_rect = pygame.Rect(next_pipe[0], next_pipe[1] - current_frame._gap_height,
            current_frame._pipe_width, current_frame._gap_height)
        gap_center = gap_rect.center
        opposite = gap_center[1] - bird_center[1]
        adjacent = gap_center[0] - bird_center[0]
        angle = math.atan2(opposite, adjacent)

        return [
            1.0,
            #self._normalize(current_frame.bird_altitude, 0, current_frame.height),
            self._normalize(current_frame.bird_velocity, frame.MAX_DOWN_VELOCITY, frame.MAX_UP_VELOCITY),
            self._normalize(current_frame.impulse_ticks, 0, frame.IMPULSE_DURATION),
            self._normalize(lower_rect.left - bird_rect.right,
                -current_frame._pipe_width - current_frame._bird_sprite_rect.width,
                current_frame._pipe_distance
            ),
            self._normalize(bird_rect.bottom - lower_rect.top, -current_frame.height, current_frame.height),
            self._normalize(bird_rect.top - upper_rect.bottom, -current_frame.height, current_frame.height),
            0 #self._normalize(angle, -math.pi, math.pi)
        ]

    def decide(self, current_frame):
        s = 0.0

        state = self._state(current_frame)
        for i in range(len(state)):
            s += self.genome[i] * state[i]
        return s > 0

TOP = 8
MUTATION_CHANCE = 0.09

def random_pipe(width, height):
    return width, random.randint(frame.MIN_PIPE_SIZE + 200, height - frame.MIN_PIPE_SIZE)

def create_frames(width, height, count, generation=None):
    first_pipe = random_pipe(width, height)
    return [(Individual() if generation is None else generation[i],
        EquiWorldFrame(width, height, first_pipe)) for i in range(count)]

def evolve(population):
    ordered = sorted(population, key=lambda i: -i.died)
    best = ordered[0:TOP] + random.sample(ordered[TOP:], TOP)
    print(['{:.3}'.format(b) for b in best[0].genome])
    new = [best[a].cross(best[b]) if a != b else best[a]
        for a in range(len(best))
        for b in range(len(best))]
    return [i.mutant(MUTATION_CHANCE) for i in new]

def main():
    pygame.init()

    size = width, height = 1000, 1080
    background = 196, 240, 255
    screen = pygame.display.set_mode(size)

    tick = 0
    generation = 0
    frames = create_frames(width, height, TOP * TOP + TOP)

    while 1:
        to_paint = True #generation % 2 == 0

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                sys.exit()

        # refresh screen
        if to_paint:
            screen.fill(background)

        one_alive = False
        next_pipe = random_pipe(width, height)
        for current in frames:
            ai = current[0]

            if not ai.died:
                current_frame = current[1]

                if not one_alive:
                    one_alive = True
                    if True: #to_paint:
                        for pipe in current_frame.pipes:
                            current_frame._paint_pipe(screen, current_frame._lower_pipe(pipe))
                            current_frame._paint_pipe(screen, current_frame._upper_pipe(pipe))
                
                # AI
                if ai.decide(current_frame):
                    current_frame.impulse()
                    ai.impulses += 1

                # step simulation
                current_frame.tick()

                if to_paint:
                    current_frame._paint_bird(screen)
                
                current_frame.set_next_pipe(next_pipe)

                # check state
                if current_frame.collides():
                    ai.died = tick

        tick += 1
        if to_paint:
            pygame.display.flip()

        if not one_alive:
            next_generation = evolve([a[0] for a in frames])
            frames = create_frames(width, height, len(next_generation), next_generation)
            tick = 0
            generation += 1

main()
