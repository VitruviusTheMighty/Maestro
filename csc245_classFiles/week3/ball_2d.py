##
## Author: Kristina Striegnitz
##
## Version: Fall 2011 
##
## This file defines a simple ball class. The ball is stationary; we
## just get to define its position, size and color. This
## implementation uses the vector class.

import pygame

from vector import Vector

class Ball:

    p = Vector(0.0,0.0)

    r = 25
    m = 0.0

    color = pygame.color.Color('darkgreen')


    def __init__ (self, x, y, r, m, color):
        self.p = Vector(float(x), float(y))
        self.r = r
        self.m = float(m)
        self.color = color

        
    def draw (self, window):
        pygame.draw.circle(window, self.color, (int(self.p.x),int(self.p.y)),self.r)

