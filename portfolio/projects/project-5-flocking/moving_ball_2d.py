##
## Author: Kristina Striegnitz
##
## Version: Fall 2011 
##
## This file defines a ball class that can move in two dimensions and
## can bounce off other balls. It also bounces off the edges of the
## screen.

import pygame
import math

from vector import Vector

def getDistance(v1:Vector, v2:Vector) -> float:
    """
    Gets the distance between two vectors
    """
    distx = (v2.x - v1.x)
    disty = (v2.y - v1.y)

    return math.sqrt(distx**2) + math.sqrt(disty**2)


class MovingBall :

    p = Vector(0.0,0.0)

    r = 25
    m = 0.0

    v = Vector(0.0, 0.0)
    a = Vector(0.0, 0.0)

    e = 0.0

    speedlimit = Vector(500.0, 500.0) 

    color = pygame.color.Color('darkgreen')

    def __init__ (self, x, y, r, m, color, xv, yv):
        self.p = Vector(float(x), float(y))
        self.r = r
        self.m = float(m)
        self.color = color
        self.v = Vector(float(xv),float(yv))
        self.drawvec = True 

    def set_elasticity (self, e):
        self.e = e

    def move (self, dt, world):
        total_acceleration = self.a + world.gravity
        self.v = self.v + (total_acceleration*dt*world.timescale)
        self.clamp_v ()
        self.stop_v ()
        self.p = self.p + (self.v *dt*world.timescale)

    def collide_edge (self, world):
        width = world.width
        height = world.height
        if self.p.x < 0+self.r:
            self.p.x = self.r
            self.v.x *= -1
        elif self.p.x > width-self.r:
            self.p.x = width-self.r
            self.v.x *= -1
        if self.p.y < 0+self.r:
            self.p.y = self.r
            self.v.y *= -1
        elif self.p.y > height-self.r:
            self.p.y = height-self.r
            self.v.y *= -1

    def collide_object (self, other):
        """ Check whether there is a collision with another object. If
        so, calculate the impulse j due to the impact and apply
        impulse to both objects."""
        o = other
        n = self.collide(o)  
        if n != None:
            j = (-(1+self.e)*self.v.minus(o.v).dot(n))/(n.dot(n)*(1/self.m + 1/o.m))
            self.apply_impulse (j, n)
            o.apply_impulse (-j, n)

    def collide (self, other):
        """
        Checks whether two circles collide. If they do and are already
        intersecting, they get moved apart a bit. The return value is
        None if there is no collision, and the vector pointing from
        the center of the first to the center of the second ball if
        there is a collision.
        """
        # d: vector from self to the other ball. We can use the length
        # of d to determine whether the two balls overlap; and the
        # direction of d indicates the direction along which the
        # impact is happening, i.e. the collision normal.
        d = self.p - other.p
        if d.length() < self.r + other.r:
            self.repair_position (d, other)
            return d
        else:
            return None

    def apply_impulse (self, j, n):
        """ j is the impulse; n the collision normal, i.e. the
        direction along which the impact happens."""
        self.v = self.v + n * (j / self.m)

    def repair_position (self, rel_pos, other):
        """ If two objects overlap, move them apart so that they are
        touching but not overlapping. How much each of the objects
        gets moved depends on its mass, so that objects with an
        infinite mass do not get moved."""
        # dividing by 10, because the length of our normal vector is 10 pixels
        repair = float(self.r + other.r - rel_pos.length())#/10
        rel_pos.normalize()
        if math.isinf (self.m):
            other.p = other.p + (rel_pos *-1*repair)
        elif math.isinf (other.m):
            self.p = self.p + (rel_pos* repair)
        else:
            self.p = self.p + (rel_pos*repair*(other.m/(self.m+other.m)))
            other.p = other.p + (rel_pos* -1 * repair*(self.m/(self.m+other.m)))

    def clamp_v (self):
        """ Reset the velocity in either dimension to the speed limit
        if it should be faster than the speed limit."""
        if self.v.length() > self.speedlimit.length():
            self.v = self.v.normalize() * (self.speedlimit.length())

    def stop_v (self):
        """ Reset the velocity to 0 if it gets very close. """
        if self.v.length() < 5:
            self.v = Vector (0,0)

    def draw (self, window):
        pygame.draw.circle(window, self.color, (int(self.p.x),int(self.p.y)),self.r)

    def getDistance(self, otherBall) -> float:
        """Gets the distance between this and another ball"""
        # assert isinstance(otherBall, type(self))
        return getDistance(self.p, otherBall.p)
