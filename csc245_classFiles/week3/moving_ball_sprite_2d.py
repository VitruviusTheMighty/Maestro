##
## Author: Kristina Striegnitz
##
## Version: Fall 2011 
##
## Updates: John Rieffel, Fall 2022
##
## This file defines a ball class that can move in two dimensions and
## can bounce off other balls.

from hashlib import new
import pygame
import math

from vector import Vector
from ball_2d import Ball


class MovingBall (Ball):

    v = Vector(0.0, 0.0)

    speedlimit = 500

    def __init__ (self, x, y, r, m, color, xv, yv):

        Ball.__init__(self, x, y, r, m, color)

        self.v = Vector(float(xv),float(yv))


    def simulate (self,width, height):
        self.move()


    def move (self):

        self.p = self.p + self.v


    def collide (self, other):
        """
        Checks whether two circles collide. If they do and are already
        intersecting, they get moved apart a bit. The return value is
        None, if there is no collision, and the vector pointing from
        the center of the first to the center of the second ball if
        there is a collision.
        """
        pass

    def getResponse(self,other,normvector):
        '''
        Calculates the new velocity after a collision
        '''
                            # new velocity is 
                    # v1_normal' = v1_normal*(m1-m2)+2*m2*v2_normal
                    #              ----------------------------      
                    #                   m1 + m2
        pass

    def bounce (self, response, n):
        '''
        given a response vector, 
        change's balls velocity according to the energy/momentum conserving equations
        '''
        pass

    def setVelocity(self,v):
        self.v = v

    def intersectsWithLineSegment(self,line):
        '''

        given a line, returns True if the ball intersects the line,
        False otehrwise

        a line is described as a tuple of two Vector objects

        Algorithm is described here
        https://www.baeldung.com/cs/circle-line-segment-collision-detection
        '''
        pass

    # only works on axis-aligned boxes
    def collidesWithAABB(self,box):
      '''
      given an AABB, returns true of the ball collides
      '''  
        pass
