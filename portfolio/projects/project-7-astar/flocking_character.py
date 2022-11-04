
import pygame
from moving_ball_2d import MovingBall
from vector import Vector


class BeakBall (MovingBall):

    beak_tip = Vector(0,20)
    max_acceleration = 200.0

    speedlimit = Vector(500,500)

    steering = []

    def draw (self, window):
        pygame.draw.circle(window, self.color, (int(self.p.x),int(self.p.y)),self.r)
        speed = self.v.length()
        if speed != 0:
            self.beak_tip = self.v.normalize().times(20)
        pygame.draw.line(window,self.color,(int(self.p.x),int(self.p.y)),(self.p.x+self.beak_tip.x,self.p.y+self.beak_tip.y), 3)

        for vec in self.steering:
            arrowvec = Vector(0,0)
            arrowvec = arrowvec.plus(vec)
            arrowvec = arrowvec.plus(self.p)
            pygame.draw.line(window,pygame.color.Color("red"),(int(self.p.x),int(self.p.y)),(arrowvec.x,arrowvec.y),2)


    def __str__ (self):
        return str(self.p)+", "+str(self.v)+", "+str(self.a) 


    def apply_steering (self):
        for s in self.steering:
            self.v = self.v.plus(s)



    def cohesion (self, others, weight):
        """ The direction of the desired velocity is toward the center
        of all the swarm, i.e. toward the average position of all the
        other swarm members."""

        if len(others) > 1:
            center = Vector(0,0)
            for o in others:
                if o != self:
                    center = center.plus(o.p)
            num_of_others = len(others)-1
            center = center.times(1.0/num_of_others)

            desired_velocity = center.minus(self.p)
            velocity_adjustment = desired_velocity.minus(self.v) 

            self.steering += [velocity_adjustment.times(weight)]


    def separation (self, others, weight):
        """ FILL IN THIS METHOD. The goal is to find the velocity
        adjustment, i.e. the amount that we need to add to the
        velocity of our boid to make it move away from all other boids
        that are getting close. To do that, start out by creating an
        0-vector for the velocity adjustment. Then look at every other
        boid (i.e., all boids that are different from the one whose
        velocities we are currently adjusting). If we find another
        boid that gets closer than a certain threshold (e.g., 50
        pixels), then compute the difference between the other boid's
        position and this boid's position and subtract that amount
        from the velocity adjustment.
        """
    
        velocity_adjustment = Vector (0,0)    

        personalSpace = 50;

        if len(others) > 1:
            for o in others:
                if o!= self:
                    otherpos = o.p
                    diffvec = o.p.minus(self.p)
                    if diffvec.length() < personalSpace:
                        velocity_adjustment = velocity_adjustment.minus(diffvec)
                        
            

        #print velocity_adjustment
        
        self.steering += [velocity_adjustment.times(weight)]


    def align (self, others, weight):
        """ FILL IN THIS METHOD. The goal is to adjust a given boids
        velocity so that it gets more similar to the velocity of the
        other boids in the group. So, calculate the average velocity
        of all other boids. Then calculate the difference between the
        average velocity and our boids velocity.
        """

        velocity_adjustment = Vector (0,0)
        if len(others) > 1:
            for o in others:
                if o!=self:
                    velocity_adjustment = velocity_adjustment.plus(o.v)
            velocity_adjustment.x = velocity_adjustment.x/(len(others) - 1)
            velocity_adjustment.y = velocity_adjustment.y/(len(others) - 1)
                    
                
            

        self.steering += [velocity_adjustment.times(weight)]

    def seek (self, target, weight):
        
        desired_direction = target.p.minus(self.p).normalize()
        max_speed = self.speedlimit.length()
        desired_velocity = desired_direction.times(max_speed)

        self.steering += [desired_velocity.minus(self.v).times(weight)]


    def arrive (self, target, weight):

        target_distance = target.p.minus(self.p).length()
        max_speed = self.speedlimit.length()
        slow_radius = 4 * (target.r + self.r)

        if target_distance > slow_radius:

            self.seek(target, weight)

        else:

            desired_speed = max_speed * (target_distance / slow_radius)
            if desired_speed > max_speed:
                desired_speed = max_speed
            
            desired_direction = target.p.minus(self.p).normalize()
            desired_velocity = desired_direction.times(desired_speed/target_distance)

            self.steering += [desired_velocity.minus(self.v).times(weight)]




