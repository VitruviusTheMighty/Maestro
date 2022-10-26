
import pygame
from moving_ball_2d import MovingBall
from vector import Vector


class SteeringBall (MovingBall):

    beak_tip = Vector(0,20)

    speedlimit = Vector(500,500)

    # All steering inputs
    steering = []

    def draw (self, window):
        # draw the body
        pygame.draw.circle(window, self.color, (int(self.p.x),int(self.p.y)),self.r)
        # draw the beak
        speed = self.v.length()
        if speed != 0:
            self.beak_tip = self.v.normalize() * 20
        pygame.draw.line(window,self.color,(int(self.p.x),int(self.p.y)),(self.p.x+self.beak_tip.x,self.p.y+self.beak_tip.y), 3)

        if self.drawvec:
            for vec in self.steering:
                arrowvec = Vector(0,0)
                arrowvec = arrowvec + vec
                arrowvec = arrowvec + self.p
                pygame.draw.line(window,pygame.color.Color("red"),(int(self.p.x),int(self.p.y)),(arrowvec.x,arrowvec.y),2)


    def __str__ (self):
        return str(self.p)+", "+str(self.v)+", "+str(self.a) 


    def apply_steering (self):
        ## add all steering inputs to current velocity vector
        for s in self.steering:
            self.v += s


    def seek (self, target, weight):

        #find difference between my location and target location 
        desired_direction = (target.p - self.p).normalize()
        #multiply direction by max speed
        max_speed = self.speedlimit.length()
        desired_velocity = desired_direction * max_speed
        ## first find the "error" between current velocity and desired velocity, and then multiply that error 
        ## by the weight, and then add it to steering inputs
        self.steering += [(desired_velocity - self.v)*weight]


    def freeze(self, weight):
        '''
        write me.  Set character's speed to 0
        '''
        pass

    def wander(self,weight,wanderspeed=100):
        '''
        pick a random target and steer toward it
        '''



