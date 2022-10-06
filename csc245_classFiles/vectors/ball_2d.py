##
## Author: Kristina Striegnitz, John Rieffel
##
## Version: Fall 2022 
##
## This file defines a simple ball class. The ball is stationary; we
## just get to define its position, size and color. This
## implementation uses the vector class.

import pygame

from vector import Vector

class Ball:

    #initialize state variables

    def __init__ (self, x, y, r, m, color):
        self.p = Vector(float(x), float(y))
        self.r = r
        self.m = float(m)
        self.color = color

    def setVelocity(self,inVelocityX,inVelocityY):
        self.velocityVec = Vector(inVelocityX,inVelocityY)


    def updatePosition(self):
        self.p.x = self.p.x + self.velocityVec.x
        self.p.y = self.p.y + self.velocityVec.y

        
    def draw (self, window):
        #print "hello"
        #print self.p.x, " ", self.p.y, " ", self.r
        pygame.draw.circle(window, self.color, (int(self.p.x),int(self.p.y)),self.r)

