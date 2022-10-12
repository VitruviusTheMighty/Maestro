##
## Author: Kristina Striegnitz, John Rieffel
##
## Version: Fall 2022 
##
## This file defines a simple ball class. The ball is stationary; we
## just get to define its position, size and color. This
## implementation uses the vector class.

import pygame, random


class Ball:

    #initialize state variables

    def __init__ (self, r, m, color, x=None, y=None, display=None):
        self.x = x
        self.y = y
        self.xv = 0
        self.yv = 0
        self.r = r
        self.m = float(m)
        self.color = color
        self.display = display

    def setVelocity(self,inVelocityX,inVelocityY):
        self.xv, self.yv = inVelocityX,inVelocityY

    def randomizePosition(self, width, height):
        self.x = random.randint(0+self.r, width-self.r)
        self.y = random.randint(0+self.r, height-self.r)
        self.y_bound = height
        self.x_bound = width
        
    def updatePosition(self):
        self.x = self.x + self.xv
        self.y = self.y + self.yv

    def setColor(self, color:str):
        self.color = color
    
    def simulate(self):
        self.bounce()
        self.updatePosition()

    def setRandomColor(self):
        colors = ["red", "green", "orange", "blue", "purple", "magenta", "white", "yellow", "cyan"]
        l = len(colors)-1
        i = random.randint(0, l)
        self.setColor(color=colors[i])

    def getPos(self):
        return self.x, self.y

    def isAtEdge(self):
        if self.atHorzWall() or self.atVertWall():
            return True
        else:
            return False

    def atHorzWall(self):
        x = self.x
        w = self.x_bound
        r = self.r
        if ( ((self.x) >= self.x_bound - self.r) or ((self.x) <= 0+self.r) ):
            return True
        else:
            return False

    def atVertWall(self):
        y = self.y
        h = self.y_bound
        r = self.r

        if ( ((self.y) >= self.y_bound - self.r) or ((self.y) <= 0+self.r) ):
            return True
        else:
            return False

    def bounce(self):

        if self.isAtEdge():
            if self.atHorzWall():
                self.xv *= -1
            if self.atVertWall():
                self.yv*= -1

            self.setRandomColor()

    def collidesWith(self, obj):
        
        if isinstance(obj, Ball):

            # collision detection
            pass

        else:
            raise TypeError("Object is supposed to be ball!")

    def draw (self, window):
        #print "hello"
        #print self.p.x, " ", self.p.y, " ", self.r
        pygame.draw.circle(window, self.color, (int(self.x),int(self.y)),self.r)

