##
## Author: Kristina Striegnitz, John Rieffel
##
## Version: Fall 2022 
##
## This file defines a simple ball class. The ball is stationary; we
## just get to define its position, size and color. This
## implementation uses the vector class.

import pygame


class Ball:

    #initialize state variables

    def __init__ (self, x, y, r, m, color):
        self.x = x
        self.y = y
        self.xv = 0
        self.yv = 0
        self.r = r
        self.m = float(m)
        self.color = color

    def setVelocity(self,inVelocityX,inVelocityY):
        self.xv, self.yv = inVelocityX,inVelocityY


    def updatePosition(self):
        self.x = self.x + self.xv
        self.y = self.y + self.yv

        
    def draw (self, window):
        #print "hello"
        #print self.p.x, " ", self.p.y, " ", self.r
        pygame.draw.circle(window, self.color, (int(self.x),int(self.y)),self.r)

