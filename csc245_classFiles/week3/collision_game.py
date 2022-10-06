##
## Author: John Rieffel
##
## Version: Fall 2022 
##
## starter code for collisions
##

import pygame
import random

from moving_ball_sprite_2d import MovingBall
from box_sprite import Box 
from vector import Vector

def run_game():
    
    ## Initialize the pygame submodules and set up the display window.

    pygame.init()

    ## keep track of key presses
    keymap = {}
    mousepos = (0,0)
    objects = []
    
    width = 640
    height = 480
    my_win = pygame.display.set_mode((width,height))

    ## important properties of the environment
    env = {'ground':height, 'g':100.0}

    ## initialize the balls
    numballs = 2

    ball1 = MovingBall (20, 10+height/2, 20, 20, pygame.color.Color("darkmagenta"), 0, 0)
    box1 = Box(0, 0, 200, 200)

    objects.append(box1)
    objects.append(ball1)

    ## setting up the clock
    clock = pygame.time.Clock()
    dt = 0
    
    ## The game loop starts here.

    keepGoing = True    
    while (keepGoing):


        #dt = clock.tick(50)
        #print dt

        ## Handle events.

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                key = event.key
                keymap[key] = True
                if key == pygame.K_RIGHT:
                    ball1.setVelocity(Vector(.1,0))
                elif key == pygame.K_LEFT:
                    ball1.setVelocity(Vector(-0.1,0))

            elif event.type == pygame.KEYUP:
                key = event.key
                keymap[key] = False
                if (key == pygame.K_RIGHT) or (key == pygame.K_LEFT):
                    ball1.setVelocity(Vector(0,0))

        mousepos = pygame.mouse.get_pos()

                

        ## Simulate game world
        for o in objects:
            o.simulate(width, height)



        ## Draw frame
        
        my_win.fill(pygame.color.Color("gray14"))


        for o in objects:
                o.draw(my_win)

        ## Swap display

        pygame.display.update()

    ## The game loop ends here.

    pygame.quit()


## Start game
run_game()
