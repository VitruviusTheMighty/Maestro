
import pygame
from moving_ball_2d import MovingBall
from vector import Vector
import math
import random
import time

class BeakBall (MovingBall):

    def __init__(self, x, y, r, m, color, xv, yv):
        super().__init__(x, y, r, m, color, xv, yv)
        self.beak_tip = Vector(0,20)
        self.max_acceleration = 200.0

        self.speedlimit = Vector(500,500)

        self.steering = []
        self.reference = None
        self.direction = 0.0

    def draw (self, window:pygame.Surface):
        # Draws the beak
        pygame.draw.circle(window, self.color, (int(self.p.x),int(self.p.y)),self.r)
        speed = self.v.length()
        if speed != 0:
            self.beak_tip = self.v.normalize() * 20
        pygame.draw.line(window,self.color,(int(self.p.x),int(self.p.y)),(self.p.x+self.beak_tip.x,self.p.y+self.beak_tip.y), 3)

        self.reference = Vector(window.get_width(), self.p.y)

        self.update_direction()
        
        
        print(f"pos: {self.p.x},{self.p.y} | beaktip: {self.p.x+self.beak_tip.x}, {self.p.y+self.beak_tip.y} | direction: {self.direction} | reference: {self.reference}")

        for vec in self.steering:
            arrowvec = Vector(0,0)
            arrowvec = arrowvec + vec
            arrowvec = arrowvec + self.p
            pygame.draw.line(window,pygame.color.Color("red"),(int(self.p.x),int(self.p.y)),(arrowvec.x,arrowvec.y),2)


    def update_direction(self):

        beaky = Vector(self.p.x+self.beak_tip.x, self.p.y+self.beak_tip.y)
        line1 = ( self.p, self.reference )
        line2 = ( self.p, beaky  )
        self.direction = ang(line1, line2)
        if beaky.y - self.p.y > 0: self.direction*=-1

    def rotate(self, degrees, weight):

        old = self.direction
        d = old+degrees if old > 0 else old-degrees
        beak_len = self.beak_tip.distanceFrom(self.p)
        point_len = beak_len*5

        # get new pos to target
        x,y = self.get_target_pos(d, point_len)

        self.seek(Vector(x,y),weight, 500.0)



    def get_target_pos(self, angle, len):

        if angle > 0:
            if angle > 90:
                diff = 180 - angle
                ytemp = math.cos(diff)*len
                xtemp = math.sin(diff)*len
                x = self.p.x - xtemp
                y = self.p.y - ytemp
            else:
                ytemp = math.cos(angle)*len
                xtemp = math.sin(angle)*len
                x = self.p.x + xtemp
                y = self.p.y - ytemp
        else:
            if angle < -90:
                diff = abs(-180 - angle)
                ytemp = math.cos(diff)*len
                xtemp = math.sin(diff)*len
                x = self.p.x - xtemp
                y = self.p.y + ytemp
            else:
                ytemp = math.cos(abs(angle))*len
                xtemp = math.sin(abs(angle))*len
                x = self.p.x + xtemp
                y = self.p.y + ytemp

        return x, y

        


    def __str__ (self):
        return str(self.p)+", "+str(self.v)+", "+str(self.a) 

    def apply_steering (self):
        # print(f"steering: {self.steering}")
        for s in self.steering:
            self.v = self.v + s
        # print(f"seek state:  {self.seeking}")

    def __get_rand_target(self, radius):
        """
        Picks a random target some radius away from me
        """
        assert self.world != None

        cx = self.p.x
        cy = self.p.y

        theta = random.random() * 2 * math.pi
        x = cx + math.cos(theta) * radius
        y = cy + math.sin(theta) * radius

        return x, y

    def seek(self, pos:Vector, weight, speed=None):
        """
        Seeks something
        """
        desired_direction = (pos - self.p).normalize()
        #multiply direction by max speed
        if speed==None:
            max_speed = self.speedlimit.length()
        else:
            max_speed = speed
        desired_velocity = desired_direction * max_speed
        
        ## first find the "error" between current velocity and desired velocity, and then multiply that error 
        ## by the weight, and then add it to steering inputs
        self.steering += [(desired_velocity - self.v)*weight]

    def wander(self, weight):
        '''
        pick a random target some radius away from me
        and seek it
        '''
        if not self.seeking:
            rx, ry = self.__get_rand_target(random.randint(10, 100))

            self.target = Vector(rx, ry)
            self.seeking = True
            # print(f"""
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            # New Target: {str(self.target)}

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # """)

        else:
            self.seek(self.target, weight)
            if self.p.distanceFrom(self.target) < 1.0:
                self.seeking = False



    # def get_direction(self):
    #     """
    #     Gets the direction returns a value in degrees
    #     """

    #     x = self.direction.x - self.p.x
    #     y = self.direction.y - self.p.y

    #     radians = math.atan2(y, x)
    #     degrees = math.degrees(radians)
        
    #     return degrees

    # # def get_dir_point(self, degrees):
        
    # #     dir = self.get_direction()

    # #     if dir >0:
    # #         desired_angle = dir+degrees
    # #     else:
    # #         desired_angle = dir-degrees

    # #     dist = 10

    def loop(self,weight):
        '''
        agent should move in a corkscrew manner
        '''
        target = self.get_turnpoint(degrees=1)
        # make a target directly in front of beakball
        # dir = self.get_direction()
        # target_x = 3 if dir.x > 1 else -3
        # target_y = 3 if dir.y > 1 else -3
        # target = Vector(target_x, target_y)

        desired_direction = (self.p - target).normalize()
        max_speed = self.speedlimit.length()
        desired_velocity = desired_direction * max_speed
        self.steering += [(desired_velocity - self.v)*weight]
        # print(self.get_direction())

    def freeze(self,weight):
        '''
        stop, hammertime
        '''
        self.v = Vector(0,0,0,0)
        # self.a = Vector(0.0,0.0)
        self.leaving_wall = True



def dot(vA:Vector, vB:Vector):
    return (vA.x*vB.x)+(vA.y*vB.y)

def ang(lineA, lineB):
    # Get nicer vector form
    vA = Vector( (lineA[0].x - lineA[1].x), (lineA[0].y - lineA[1].y))
    vB = Vector( (lineB[0].x - lineB[1].x), (lineB[0].y - lineB[1].y))

    # Get dot prod
    dot_prod = dot(vA, vB)
    # Get magnitudes
    magA = dot(vA, vA)**0.5
    magB = dot(vB, vB)**0.5
    # Get cosine value
    cos_ = dot_prod/magA/magB
    # Get angle in radians and then convert to degrees
    angle = math.acos(dot_prod/magB/magA)
    # Basically doing angle <- angle mod 360
    ang_deg = math.degrees(angle) % 360
    
    if ang_deg-180>=0:
        # As in if statement
        return 360 - ang_deg
    else: 
        
        return ang_deg

