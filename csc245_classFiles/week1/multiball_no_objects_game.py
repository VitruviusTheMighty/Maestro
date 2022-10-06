##
## Authors: Kristina Striegnitz, John Rieffel
##
## Version: Fall 2022 
##
## using lists to represent balls
##

import pygame

class Ball:

    def __init__(self,x,y,r,xv,yv):
        self.x = x 
        self.y = y
        self.r = r
        self.xv = xv
        self.yv = yv

    def updateBallPosition(self,ball,width,height):
        '''
        if a ball is a list, we can unpack that data and update the position
        based on the velocities.  We'll handle bouncing here too.
        '''

        #unpack list
        self.x,self.y,self.r,self.xv,self.yv = ball
        #update velocities
        x+=xv
        y+=yv
        #handle bounces
        if (x <= r) or (x >=width-r):
            #xv *= -.9 #what happens?
            xv *= -1
        if (y < r) or (y > height-r):
            #yv *= -.9 #what happens?
            yv *= -1
        #repack list
        ball[0] = x
        ball[1] = y
        ball[2] = r
        ball[3] = xv
        ball[4] = yv

        #return nothing because we changed the input list
        #this is bad.
        return 

    def drawball(self,ball,window,color = "red"):
        x,y,r,xv,yv = ball
        pygame.draw.circle(window, color, (x,y),r)
    
    def setColor(self,ball,window,color):
        self.drawball(ball,window,color)
        



    def run_game():
    
    ## Initialize the pygame submodules and set up the display window.

        pygame.init()

        width = 1024
        height = 768
        my_win = pygame.display.set_mode((width,height))

        
        ballList = []

        b1 = [500,300, 31, .5,.5]
        b2= [100,300, 20, 1,1]
        b3= [150,100, 20, -1,1]
        b4 = [200,200,20,1,1]
        

        ballList.append(b1)
        ballList.append(b2)
        ballList.append(b3)
        ballList.append(b4)


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
