##
## Author: John Rieffel

## Version: Fall 2022 
##


import pygame
import random

try:
    from gridworld import GridWorld
    from vector import Vector
    from astarrunner import *
    from navigating_character import NaviBeakBall

except ModuleNotFoundError:
    try:
        from path.vector import Vector
        from path.gridworld import GridWorld
        from path.astarrunner import *
        from path.navigating_character import NaviBeakBall

    except:
        from games.path.vector import Vector
        from games.path.gridworld import GridWorld
        from games.path.astarrunner import *
        from games.path.navigating_character import NaviBeakBall


from simplepygamemenus.menu import Menu

class PathPlanning:

    def __init__(self, screen:pygame.Surface=None, x=1000, y=800, gridscale=50, menu_func=None, localmenu=False, parent=None):
        
        if screen is None:
            # set our own world
            self.SCREEN = pygame.display.set_mode((x,y)) 
            
        else: self.SCREEN = screen
        self.parent = parent
        self.preflight(gridscale, menu_func, localmenu)

    def preflight(self, gridscale, menu_function, doLocalMenu=False):
        pygame.init()

        self.main = None
        self.menu_func = menu_function

        self.height = self.SCREEN.get_height()
        self.width  = self.SCREEN.get_width()

        self.gridwidth = self.width // gridscale
        self.gridheight = self.height // gridscale

        self.world = GridWorld(self.gridwidth,self.gridheight,gridscale)

        self.runner = AStarRunner(self.world)

        self.nav_character = NaviBeakBall (10, 10, 10, 1, pygame.color.Color("darkorange"))

        if doLocalMenu: self.create_menu()

    def handle_menu_escape(self, event):
        if self.menu_func is not None and event.key == pygame.K_ESCAPE:
            self.menu_func()

    def create_menu(self):
        
        self.main = Menu(caption="Path Planning", title="Path Planning Demo", world=self.SCREEN, main=self.parent)

        self.create_instruction_menu()

        self.main.add_button(label="Play Game", function=self.instructions_menu.run_menu, x=self.width//2, y=self.height//2, basecolor=(255,255,255), hovercolor=(255,255,25))
        self.main.add_text(text="By Leonardo Ferrisi", x=self.width//2, y=self.height//4, size=20)
        self.menu_func = self.main.run_menu

    def create_instruction_menu(self):

        self.instructions_menu = Menu(caption="Instructions", title="Instructions", world=self.SCREEN, displaytitle=False, main=self.main)
        self.instructions_menu.add_text(text="Instructions", x= self.width//2, y=80)
        instruction_string = \
        "To change Modes and States:                                     \n " + \
        "Press 'r' to reset screen                                       \n " + \
        "Press 'v' to use verbose mode with terminal (warning, its SLOW!)\n " + \
        "Press 'p' to use plain mode                                     \n " + \
        "                                                                \n " + \
        "To change Algorithms:                                           \n " + \
        "Press 'b' to use Breadth First Search                           \n " + \
        "Press 'd' to use Depth First Search                             \n " + \
        "Press 'a' to use A - Star Search                                \n " + \
        "                                                                \n " + \
        "To Edit Map:                                                    \n " + \
        "Press 'g' to add grass                                          \n " + \
        "Press 'w' to add wall                                           \n " + \
        "Press 'm' to add mud                                            \n "

        
        self.instructions_menu.add_text(text=instruction_string, x=self.width//2, y=200, size=20)
        self.instructions_menu.add_button(label="OK", function=self.run_game, x=self.width//2, y=self.height-80, basecolor=(255,255,255), hovercolor=(255,255,25))



    def play(self):

        if self.main is not None: self.run_main_menu()
        else: self.run_game()

    def run_main_menu(self):

        if self.main is not None: self.main.run_menu()

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
                    try:
                        path = self.runner.search(startpt,endpt,my_win,self.world)
                        # scale path back up from grid coordinates to window coordinates
                        # for our agent
                        newpath = [(x*self.world.gridsize + self.world.gridsize/2,y*self.world.gridsize+self.world.gridsize/2) for (x,y) in path]
                        ## tell our agent where to go
                        self.nav_character.set_route (newpath)
                    except:
                        print("NO PATH POSSIBLE, have I been walled in?")
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

    # main = Menu(caption="Path Planning", title="Path Planning Demo", world=dispo)
    
    # p = PathPlanning(screen=dispo, menu_func=main.run_menu)
    
    # main.add_button(label="Play Game", function=p.run_game, x=700, y=700, basecolor=(255,255,255), hovercolor=(255,255,25))

    # main.run_menu()

    p = PathPlanning(screen=dispo, localmenu=True)
    p.play()




# m = Menu(x=800, y=800)
# m.add_button(label="play", function=run_game)
