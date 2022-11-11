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

try:
    from vector import Vector
    from fsm_character import FSMBeakBall
    from world import World

except ModuleNotFoundError:
    try:
        from vector import Vector
        from fsm_character import FSMBeakBall
        from world import World
    except:
        from games.fsm.vector import Vector
        from games.fsm.fsm_character import FSMBeakBall
        from games.fsm.world import World

class FSM_GAME:

    def __init__(self, num_agents=5, world=None, width=1400, height=900):
        self.num_agents = num_agents
        self.world      = world

        if not world:
            self.width  = width
            self.height = height

        else:
            self.width  = world.get_width()
            self.height = world.get_height()

    def load_game_select(self, menu_select_func):

        self.menu = menu_select_func
        
    def run_game(self):
        
         ## Initialize the pygame submodules and set up the display window.
        pygame.init()

        if self.world != None:
            my_win = self.world

        else:
            my_win = pygame.display.set_mode((self.width,self.height))

            ## setting up the game world
        world = World (self.width, self.height)

        beak_balls = []

        for i in range(self.num_agents):
            ## our character
            x = random.randint(0,self.width)
            y = random.randint(0,self.height)
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
                if event.type==pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.menu != None:
                            self.menu()
                        else:
                            pygame.quit()

            ## Simulate game world

            for c in beak_balls:
                c.fsm.update (world)
                c.execute_actions ()
            
                c.move(dt, world)
                print()
                c.collide_edge (world)

            # Draw frame
            pygame.draw.rect (my_win, pygame.color.Color("green"), (0,0,self.width/2,self.height))
            pygame.draw.rect (my_win, pygame.color.Color("red"), (self.width/2,0,self.width/2,self.height))

            for c in beak_balls:
                c.draw(my_win)
                # print("drew one")

            # Swap display
            pygame.display.update()

        ## The game loop ends here.

        pygame.quit()

if __name__ == "__main__":

    f = FSM_GAME(num_agents=5)
    f.run_game()

