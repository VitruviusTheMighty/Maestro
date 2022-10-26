##
## Author: John Rieffel

## Version: Fall 2022 
##


import pygame
import random

from vector import Vector

from gridworld import GridWorld
from astarrunner import *

from navigating_character import NaviBeakBall

def run_game():

    print("Instructions:")
    print("(r)eset screen")
    print("Left Click to set Destination")
    print("(v)erbose or (p)lain")
    print("==================")
    print("To Switch Algorithms:")
    print("(b)readth first")
    print("(d)epth first")
    print("bes(t) first")
    print("(a)-star")
    
    print("==================")
    print("Map Editing:")
    print("(g)rass")
    print("(w)all")
    print("(m)ud")
    
    drawpath = True

    #font_black = pygame.font.SysFont("Impact", 32)
    
    ## Initialize the pygame submodules and set up the display window.
    pygame.init()


    keymap = {}

    gridwidth = 10
    gridheight = 10
    gridscale = 50

    ## A grid world allows us to break the continuous 
    ## pixel world into discrete intervals 
    world = GridWorld(gridwidth,gridheight,gridscale)
    ## An A-Star-Runner finds best paths
    runner = AStarRunner(world)


    ## Initialization Code
    startpt = (0,0)
    endpt = (7,0)
    width = world.width*world.gridsize
    height = world.height*world.gridsize
    my_win = pygame.display.set_mode((width,height)) 

    ## Our navigating character
    c = NaviBeakBall (10, 10, 10, 1, pygame.color.Color("darkorange"))
##
    click = False

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
            elif event.type == pygame.KEYDOWN:
                key = event.key
                keymap[key] = True
            elif event.type == pygame.KEYUP:
                key = event.key
                keymap[key] = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                mpos = pygame.mouse.get_pos()
            
        # outsourcing events to the world and the astar runner
        world.handle_events(keymap)
        runner.handle_events(keymap)

        # if the user clicks, find a path
        if click:
            
            click = False
            # find closest navi_graph node to c
            startpt = world.find_closest_gridloc((c.p.x, c.p.y))
            # find closest navi_graph node to click/mpos
            endpt = world.find_closest_gridloc(mpos)

            if world.isLegitimate(endpt):
                path = runner.search(startpt,endpt,my_win,world)
                # scale path back up from grid coordinates to window coordinates
                # for our agent
                newpath = [(x*world.gridsize + world.gridsize/2,y*world.gridsize+world.gridsize/2) for (x,y) in path]
                ## tell our agent where to go
                c.set_route (newpath)
            else:
                print("i can't go there!")


        # we're in one of two states, either following a path or waiting for a path
        c.fsm.update(world)
        c.execute_actions()
        c.move (dt, world)

      

        world.draw(my_win)

        if drawpath:

            runner.draw(world,my_win)

        c.draw(my_win)

        # Swap display
        pygame.display.update()

    ## The game loop ends here.

    pygame.quit()


## Start game
run_game()
