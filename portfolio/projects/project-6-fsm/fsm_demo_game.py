##
## Author: Kristina Striegnitz
##
## Version: Fall 2011 
##
## A finite state controlled character wanders around the
## screen. While it is on the green part it wanders slowing; when it
## is on the red it starts running.
##

import pygame
import random

from vector import Vector
from fsm_character import FSMBeakBall
from world import World

def run_game(num_agents=30):
    
    ## Initialize the pygame submodules and set up the display window.
    pygame.init()

    width = 1024
    height = 768
    my_win = pygame.display.set_mode((width,height))

    ## setting up the game world
    world = World (width, height)

    beak_balls = []

    for i in range(num_agents):
        ## our character
        x = random.randint(0,width)
        y = random.randint(0,height)
        color = (random.randrange(255), random.randrange(255), random.randrange(255))
        c = FSMBeakBall (x, y, 10, 1, color, 0, 0)
        beak_balls.append(c)

    for c in beak_balls:
        c.add_world_params(world)

    ## a dictionary to remember which keys are pressed
    keymap = {}

    ## setting up the clock
    clock = pygame.time.Clock()
    dt = 0
    
    ## The game loop starts here.

    keepGoing = True    
    while (keepGoing):

        dt = clock.tick()
        if dt > 500:
            continue

        ## Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False

        ## Rendering
        
        ## Simulate game world

        for c in beak_balls:
            c.fsm.update (world)
            c.execute_actions ()
        
            c.move(dt, world)
            c.collide_edge (world)

        # Draw frame
        pygame.draw.rect (my_win, pygame.color.Color("green"), (0,0,width/2,height))
        pygame.draw.rect (my_win, pygame.color.Color("red"), (width/2,0,width/2,height))

        for c in beak_balls:
            c.draw(my_win)
            # print("drew one")

        # Swap display
        pygame.display.update()

    ## The game loop ends here.

    pygame.quit()


## Start game
run_game(num_agents=1)
