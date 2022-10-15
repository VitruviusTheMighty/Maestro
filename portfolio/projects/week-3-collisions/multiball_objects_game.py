##
## Authors: Kristina Striegnitz, John Rieffel
##
## Version: Fall 2013 
##
## Testing your Ball class.
##

from tkinter import XView
import pygame

from ball_2d_novector import *
        

def run_game():
    
    ## Initialize the pygame submodules and set up the display window.

    pygame.init()

    width = 1024
    height = 768
    my_win = pygame.display.set_mode((width,height))

    
    ballList = []


    

    ## setting up the clock
    clock = pygame.time.Clock()
    
    ## The game loop starts here.

    keepGoing = True    
    while (keepGoing):


        ## Handle events.

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    radius = random.randint(5, 30)
                    b = Ball(r=radius,m=0,color=pygame.color.Color('red')  )
                    b.setRandomColor()
                    b.randomizePosition(width, height)
                    xv = random.uniform(0.1, 3)
                    yv = random.uniform(0.1, 3)
                    b.setVelocity(xv, yv)
                    ballList.append(b)

        ## Simulate game world
        # nothing to simulate right now

        ## Draw frame
        my_win.fill(pygame.color.Color("black"))

        ## update ball position with current velocity

        for ball in ballList:
            ball.simulate()
            ball.draw(my_win)

        ## Swap display

        pygame.display.update()

    ## The game loop ends here.

    pygame.quit()


## Start game
run_game()
