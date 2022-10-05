##
## Authors: Kristina Striegnitz, John Rieffel
##
## Version: Fall 2022 
##
## using lists to represent balls
##
## 1. We changed how speed decreases in ball positions and we repaired the bug in Y's if statement. 

import pygame

def resetPos(ball, width, height):

    # check edge case and put inside bounds

    pass


def updateBallPosition(ball,width,height):
    '''
    if a ball is a list, we can unpack that data and update the position
    based on the velocities.  We'll handle bouncing here too.
    '''

    #unpack list
    x,y,r,xv,yv = ball
    #update velocities
    x+=xv
    y+=yv
    #handle bounces
    if (x <= r) or (x >=width-r):

        # reset position
        resetPos(ball, width=width, height=height)

        xv *= -.9 #what happens?
        #xv *= -1

    if (y <= r) or (y >= height-r):

        # reset position
        resetPos(ball, width=width, height=height)

        #yv *= -1
        yv *= -.9
        
    #repack list
    ball[0] = x
    ball[1] = y
    ball[2] = r
    ball[3] = xv
    ball[4] = yv

    #return nothing because we changed the input list
    #this is bad.
    return 

def get_random_c
def drawball(ball,window):
    x,y,r,xv,yv = ball
    pygame.draw.circle(window, "red", (x,y),r)


def run_game():
    
    ## Initialize the pygame submodules and set up the display window.

    pygame.init()

    width = 1024
    height = 768
    my_win = pygame.display.set_mode((width,height))

    
    ballList = []
    ballspeed = 10

    b1 = [500,300, 31, .5*ballspeed,.5*ballspeed]
    b2= [100,300, 20, 1*ballspeed,1*ballspeed]
    b3= [150,100, 20, -1*ballspeed,1*ballspeed]
    

    ballList.append(b1)
    ballList.append(b2)
    ballList.append(b3)

    ## setting up the clock
    clock = pygame.time.Clock()
    
    ## The game loop starts here.

    keepGoing = True    
    while (keepGoing):

        clock.tick(500)
        ## Handle events.

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False

        ## Simulate game world
        # nothing to simulate right now

        ## Draw frame
        my_win.fill(pygame.color.Color("black"))

        ## update ball position with current velocity

        for ball in ballList:
            updateBallPosition(ball,width,height)

        ## draw ball in window
        for ball in ballList:
            drawball(ball,my_win)
   

    

        ## Swap display

        pygame.display.update()

    ## The game loop ends here.

    pygame.quit()


## Start game
run_game()
