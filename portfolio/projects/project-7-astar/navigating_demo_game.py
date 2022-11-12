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

from simplepygamemenus.menu import Menu

class PathPlanning:

    def __init__(self, screen:pygame.Surface=None, x=1000, y=800, gridscale=50, menu_func=None):

        if screen is None:
            # set our own world
            self.SCREEN = pygame.display.set_mode((x,y)) 
            
        else: self.SCREEN = screen
        self.preflight(gridscale, menu_func)

    def preflight(self, gridscale, menu_function):
        pygame.init()

        self.menu_func = menu_function

        self.height = self.SCREEN.get_height()
        self.width  = self.SCREEN.get_width()

        self.gridwidth = self.width // gridscale
        self.gridheight = self.height // gridscale

        self.world = GridWorld(self.gridwidth,self.gridheight,gridscale)

        self.runner = AStarRunner(self.world)

        self.nav_character = NaviBeakBall (10, 10, 10, 1, pygame.color.Color("darkorange"))

    def handle_menu_escape(self, event):
        if self.menu_func is not None and event.key == pygame.K_ESCAPE:
            self.menu_func()

    def run_game(self):

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


        ## A grid world allows us to break the continuous 
        ## pixel world into discrete intervals 
        ## An A-Star-Runner finds best paths


        ## Initialization Code
        startpt = (0,0)
        endpt = (7,0)

        my_win = self.SCREEN

        ## Our navigating character
        c = self.nav_character

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
                    self.handle_menu_escape(event)
                    key = event.key
                    keymap[key] = True
                elif event.type == pygame.KEYUP:
                    key = event.key
                    keymap[key] = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    click = True
                    mpos = pygame.mouse.get_pos()
                
            # outsourcing events to the world and the astar runner
            self.world.handle_events(keymap)
            self.runner.handle_events(keymap)

            # if the user clicks, find a path
            if click:
                
                click = False
                # find closest navi_graph node to c
                startpt = self.world.find_closest_gridloc((self.nav_character.p.x, self.nav_character.p.y))
                # find closest navi_graph node to click/mpos
                endpt = self.world.find_closest_gridloc(mpos)

                if self.world.isLegitimate(endpt):
                    path = self.runner.search(startpt,endpt,my_win,self.world)
                    # scale path back up from grid coordinates to window coordinates
                    # for our agent
                    newpath = [(x*self.world.gridsize + self.world.gridsize/2,y*self.world.gridsize+self.world.gridsize/2) for (x,y) in path]
                    ## tell our agent where to go
                    self.nav_character.set_route (newpath)
                else:
                    print("i can't go there!")


            # we're in one of two states, either following a path or waiting for a path
            self.nav_character.fsm.update(self.world)
            self.nav_character.execute_actions()
            self.nav_character.move (dt, self.world)

        

            self.world.draw(my_win)

            if drawpath:

                self.runner.draw(self.world,my_win)

            self.nav_character.draw(my_win)

            # Swap display
            pygame.display.update()

        ## The game loop ends here.s

        pygame.quit()

if __name__ == "__main__":

    dispo = pygame.display.set_mode((1400,900)) 

    main = Menu(caption="Path Planning", title="Path Planning Demo", world=dispo)
    
    p = PathPlanning(screen=dispo, menu_func=main.run_menu)
    
    main.add_button(label="Play Game", function=p.run_game, x=700, y=700, basecolor=(255,255,255), hovercolor=(255,255,25))

    main.run_menu()

