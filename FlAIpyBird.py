import os
import time

class Frame:

    def __init__(self, width=1000, height=500, bird_altitude=None, bird_velocity=0, pipe_width=20, gap_height=50):
        self.width = width
        self.height = height
        self.bird_altitude = height / 2 if bird_altitude is None else bird_altitude
        self.bird_velocity = bird_velocity

        self.pipe_width = pipe_width
        self.gap_height = gap_height

        self.pipes = []

    def tick(self):
        self.bird_altitude = max(self.bird_altitude + self.bird_velocity, 0)
        self.bird_velocity = max(self.bird_velocity - 1, -5)

        self.pipes = [(x-1, y) for (x,y) in self.pipes if x + self.pipe_width > 0]

    def impulse(self):
        self.bird_velocity = 10

    def has_impact(self):
        return False


def print_frame(frame):
    for y in range(frame.height, -1, -1):
        for x in range(frame.width):
            if x == 20 and y == frame.bird_altitude:
                print("@", end='')
            else:
                print(".", end='')
        print()


def main():
    frame = Frame(width=100, height=40)
    for ticks in range(20):
        os.system('clear')
        print_frame(frame)
        frame.tick()
        time.sleep(0.1)

main()