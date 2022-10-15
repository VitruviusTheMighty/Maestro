##
## Author: Leonardo Ferrisi
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
import math

# def getDistance(v1:Vector, v2:Vector) -> float:
#     """
#     Gets the distance between two vectors
#     """
#     distx = (v2.x - v1.x)
#     disty = (v2.y - v1.y)

#     return math.sqrt(distx**2) + (math.sqrt(disty**2))

# def getDistance(mb1, mb2):


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

        # have a distance based method


        # print(f"Distance: {target.getDistance(c)}. Target: {target.p}, Ball: {c.p}")


        # Seek - Fleeing behavior
        dist_thres = 100.0

        if not c.fleeing:
            if target.getDistance(c) > dist_thres:
                # Arrival
                c.arrive(target, 1.0/30)
                c.speedlimit = c.defaultspeed
            else: c.fleeing = True
        else:
            if c.fleeing and  target.getDistance(c) < dist_thres*8:
                c.flee(target, 1.0/30, dt, world, dist_thres)
            else: c.fleeing = False


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
