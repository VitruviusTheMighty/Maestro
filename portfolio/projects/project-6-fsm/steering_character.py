
import pygame
from moving_ball_2d import MovingBall
from vector import Vector
import math
import random
import time

class BeakBall (MovingBall):

    beak_tip = Vector(0,20)
    max_acceleration = 200.0

    speedlimit = Vector(500,500)

    steering = []
    
    def add_world_params(self, world):
        self.world = world

    def draw (self, window):
        pygame.draw.circle(window, self.color, (int(self.p.x),int(self.p.y)),self.r)
        speed = self.v.length()
        if speed != 0:
            self.beak_tip = self.v.normalize() * 20
        pygame.draw.line(window,self.color,(int(self.p.x),int(self.p.y)),(self.p.x+self.beak_tip.x,self.p.y+self.beak_tip.y), 3)

        for vec in self.steering:
            arrowvec = Vector(0,0)
            arrowvec = arrowvec + vec
            arrowvec = arrowvec + self.p
            pygame.draw.line(window,pygame.color.Color("red"),(int(self.p.x),int(self.p.y)),(arrowvec.x,arrowvec.y),2)

            self.direction = arrowvec


    def __str__ (self):
        return str(self.p)+", "+str(self.v)+", "+str(self.a) 

    def apply_steering (self):
        print(f"steering: {self.steering}")
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

    def seek(self, pos:Vector, weight):
        """
        Seeks something
        """
        desired_direction = (pos - self.p).normalize()
        #multiply direction by max speed
        max_speed = self.speedlimit.length()
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



    def get_direction(self):
        """
        Gets the direction returns a value in degrees
        """

        x = self.direction.x - self.p.x
        y = self.direction.y - self.p.y

        radians = math.atan2(y, x)
        degrees = math.degrees(radians)
        
        return degrees

    # def get_dir_point(self, degrees):
        
    #     dir = self.get_direction()

    #     if dir >0:
    #         desired_angle = dir+degrees
    #     else:
    #         desired_angle = dir-degrees

    #     dist = 10

    

    def get_turnpoint(self, degrees, distance=0):   
        """
        Finds a position that is n degrees at a distance x
        
        Params:
            degrees (int/float): Degrees to turn by
            distance (int/float): Amount to travel, can be 0
        """
        dir = self.get_direction()

        if dir >0:
            desired_angle = dir+degrees
        else:
            desired_angle = dir-degrees
    
        bx = (self.direction.x - self.p.x)
        by = (self.direction.y - self.p.y)

        if bx >= 0 and by >= 0:
            quad = 1
        elif bx <= 0 and by > 0:
            quad = 2
        elif bx < 0 and by <= 0:
            quad = 3
        elif bx > 0 and by < 0:
            quad = 4

        print(f"Beak: {self.direction.x},{self.direction.y}, Pos: {self.p.x}, {self.p.y} - Quad: {quad}")
        dist = (self.direction.distanceFrom(self.p)) + distance

        turnpoint_len = dist / math.cos(desired_angle)

        # Now get the x-dist and y-dist
        x_dist = math.sin(desired_angle) * turnpoint_len
        y_dist = math.cos(desired_angle) * turnpoint_len

        if quad == 1:
            tx = self.p.x + x_dist
            ty = self.p.y + y_dist
        elif quad == 2:
            tx = self.p.x - x_dist
            ty = self.p.y + y_dist
        elif quad == 3:
            tx = self.p.x - x_dist
            ty = self.p.y - y_dist
        elif quad == 4:
            tx = self.p.x + x_dist
            ty = self.p.y + y_dist



        target = Vector(tx, ty)
        return target


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



