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
import sys
from button import Button


def getCenteroid(flock:list):
    """
    Gets the Center of Mass of a Swarm of Steering Agents

    Args:
        flock (list of SteeringBall obj):
    """
    
    center_of_mass = Vector(0, 0)

    for agent in flock:
        center_of_mass += agent.p
    
    center_of_mass = center_of_mass / len(flock)

    return center_of_mass


# def main():
#     pygame.init()
#     width = 1024
#     height = 768
#     my_win = pygame.display.set_mode((width,height))

#     title_screen(my_win)

    
# def title_screen(screen):
#     while True:

#         MOUSE_POS = pygame.mouse.get_pos()
#         screen.fill("black")

#         PLAY = Button(image=None, pos=(cx, 300), text_input="TOGGLE AUDIO", font=get_font(25), base_color="White", hovering_color="Green")
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
#                     self.main_menu()
#                 if AUDIOTOGGLE.checkForInput(OPTIONS_MOUSE_POS):
#                     self.audio_toggle()



def run_game(screen=None, numAgents=10):
    """
    Runs a steering flock game
    """
    
    ## Initialize the pygame submodules and set up the display window.
    pygame.init()

    width = 1024
    height = 768
    my_win = pygame.display.set_mode((width,height))

    ## setting up the game world
    world = World (width, height)

    weight = 1.0/30


    # our flock

    flock = []

    for agent in range(numAgents):
        ## our character
        x = random.randint(0,width)
        y = random.randint(0,height)
        color = (random.randrange(255), random.randrange(255), random.randrange(255))
        c = SteeringBall (x, y, 10, 1, color, 0, 0)
        flock.append(c)

    ## the target
    target = MovingBall (150, 175, 20, float('inf'), pygame.color.Color("red"), 0, 0)

    target2 = MovingBall (150, 175, 20, float('inf'), pygame.color.Color("blue"), 0, 0)

    
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

        centerVector = getCenteroid(flock)

        target2.p = centerVector
        
        ## Simulate game world
        target.move (dt, world)
        target.collide_edge (world)

        # target2.move (dt, world)
        # target2.collide_edge (world)

        # centerBall.move(dt, world)
        # centerBall.collide_edge(world)

        # Flee - Arrive - Steer flock
        for c in flock:
            c.steering = []
            # print(f"Distance: {target.getDistance(c)}. Target: {target.p}, Ball: {c.p}")
            # Seek - Fleeing behavior
            dist_thres = 100.0

            if not c.fleeing:
                if target.getDistance(c) > dist_thres:
                    # Arrival
                    c.arrive(target)
                    c.cohesion(centerVector, weight)
                    c.separation(flock, weight)
                    c.align(flock)
                    c.speedlimit = c.defaultspeed
                else: c.fleeing = True
            else:
                if c.fleeing and  target.getDistance(c) < dist_thres*3:
                    c.flee(target, weight, dt, world, dist_thres)
                else: c.fleeing = False


            c.apply_steering()
            c.move(dt, world)
            c.collide_edge (world)

            

        # update pos for centeroid ball

        ## Rendering
        # Draw frame
        my_win.fill(pygame.color.Color("gray14"))

        target.draw(my_win)
        target2.draw(my_win)

        # Draw flock
        for c in flock:
            c.draw(my_win)

        centerVector = getCenteroid(flock)

        # centerBall = MovingBall(centerVector.x, centerVector.y, 50, 20.0, pygame.color.Color("blue"), 0, 0)
    

        try:
            # print("drawing")
            pygame.draw.circle(my_win, pygame.color.Color("blue"), (centerVector.x, centerVector.y), 20) # Here <<<
            # print("drew it")
        except:
            raise Exception("Did not draw ball")

        # centerBall.draw(my_win)
        
        # print(f"Centeroid pos : {centerVector}, CenterBall = {centerBall.p.x}, {centerBall.p.y}")

        # Swap display
        pygame.display.update()

    ## The game loop ends here.

    pygame.quit()


## Start game
run_game()
