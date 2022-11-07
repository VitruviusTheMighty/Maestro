import pygame
import random

from world import World
from steering_character import BeakBall
from moving_ball_2d import MovingBall
from vector import Vector

if __name__ == "__main__":

    num_agents = 1

    pygame.init()

    width = 1024
    height = 768
    my_win = pygame.display.set_mode((width,height))
    world = World(width, height)

    beak_balls = []

    for i in range(num_agents):
        ## our character
        # x = random.randint(0,width)
        # y = random.randint(0,height)
        x = width // 2
        y = height // 2
        color = (random.randrange(255), random.randrange(255), random.randrange(255))
        c = BeakBall(x, y, 10, 1, color, 0, 0)
        beak_balls.append(c)

    ## setting up the clock
    clock = pygame.time.Clock()
    dt = 0

    acc = 0.1
    ax = -0.0001
    ay = -0.0001

    keepGoing = True    
    while (keepGoing):
        
        my_win.fill((0,0,0))

        dt = clock.tick()
        if dt > 500:
            continue

        ## Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
        
        for c in beak_balls:
            c.apply_steering()
            c.move(dt, world)
            c.collide_edge (world)

            c.rotate(5.0, 0.1)

        my_win.fill((0,0,0))

        for c in beak_balls:
            c.draw(my_win)
        

    
        
     
        # Swap display

        pygame.display.update()

    ## The game loop ends here.
    pygame.quit()