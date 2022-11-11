
import pygame
import math
import random
import time

try:
    from vector import Vector
    from moving_ball_2d import MovingBall
except ModuleNotFoundError:
    try:
        from vector import Vector
        from moving_ball_2d import MovingBall
    except:
        from games.fsm.vector import Vector
        from games.fsm.moving_ball_2d import MovingBall

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

    def loop(self,weight):
        '''
        agent should move in a corkscrew manner
        '''        
        if self.v.isZero(): self.v = Vector(50,50)

        desired_velocity = Vector(self.v.y*-1, self.v.x) * self.speedlimit.length()
        self.v = desired_velocity
        self.steering += [(desired_velocity)*weight]

    def freeze(self,weight):
        '''
        stop, hammertime
        '''
        # self.a = Vector(0.0,0.0)
        # self.v = Vector(self.v.y*-1, self.v.x*-1)

        self.v = Vector(0,0)



