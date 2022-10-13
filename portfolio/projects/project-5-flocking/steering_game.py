##
## Author: Kristina Striegnitz
## Author: John Rieffel 
##
## Version: Fall 2022 
##
## A character shows a simple seek behavior that makes it move towards
## a target.
##

import pygame
import random

from vector import Vector
from steering_ball import SteeringBall
from moving_ball_2d import MovingBall
from world import World

def run_game():
    
    ## Initialize the pygame submodules and set up the display window.
    pygame.init()

    width = 1024
    height = 768
    my_win = pygame.display.set_mode((width,height))

    ## setting up the game world
    world = World (width, height)

    ## our character
    x = random.randint(0,width)
    y = random.randint(0,height)
    c = SteeringBall (x, y, 10, 1, pygame.color.Color("darkorange"), 0, 0)

    ## the target
    target = MovingBall (150, 175, 20, float('inf'), pygame.color.Color("red"), 0, 0)
    
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
##            if event.type == pygame.MOUSEBUTTONDOWN:
##                mousepos = pygame.mouse.get_pos()
##                mousepos = Vector(mousepos[0],mousepos[1])
##                target.p = mousepos
                


        mousepos = pygame.mouse.get_pos()
        mousepos = Vector(mousepos[0],mousepos[1])
        target.p = mousepos
        
        ## Simulate game world
        target.move (dt, world)
        target.collide_edge (world)

        c.steering = []
        c.seek (target, 1.0/30)

        c.apply_steering()
        c.move(dt, world)
        c.collide_edge (world)

        
        ## Rendering
        # Draw frame
        my_win.fill(pygame.color.Color("gray14"))

        target.draw(my_win)
        c.draw(my_win)

        # Swap display
        pygame.display.update()

    ## The game loop ends here.

    pygame.quit()


## Start game
run_game()
