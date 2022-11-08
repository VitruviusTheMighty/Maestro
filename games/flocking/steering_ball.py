
import pygame
try:
    from vector import Vector
    from moving_ball_2d import MovingBall

except ModuleNotFoundError:
    try:
        from flocking.vector import Vector
        from flocking.moving_ball_2d import MovingBall
    except:
        from games.flocking.vector import Vector
        from games.flocking.moving_ball_2d import MovingBall


class SteeringBall (MovingBall):

    beak_tip = Vector(0,20)

    def __init__ (self, x, y, r, m, color, xv, yv):

        super().__init__(x,y,r,m,color,xv,yv)
        self.speedlimit = Vector(500,500)
        self.defaultspeed = self.speedlimit
        self.fleespeed = Vector(5000,5000)
        self.fleeing = False


        
    # fleespeed = Vector(1000, 1000)
        
        
    
    # All steering inputs
    steering = []

    # def change_speed(self, mode):
    #     if mode > 1:
    #         speedlimit = Vector(1000, 1000)
    #     else:
    #         speedlimit

    def get_pos(self):
        return self.p

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

    def seek (self, target:MovingBall, weight):
        #find difference between my location and target location 
        desired_direction = (target.p - self.p).normalize()
        #multiply direction by max speed
        max_speed = self.speedlimit.length()
        desired_velocity = desired_direction * max_speed
        ## first find the "error" between current velocity and desired velocity, and then multiply that error 
        ## by the weight, and then add it to steering inputs
        self.steering += [(desired_velocity - self.v)*weight]

    def arrive(self, target:MovingBall, weight=1.0/30):
        """
        Alters the speed relative to distance
        """
        threshold = (target.r + self.r)*10

        if not self.fleeing:
            dist = self.getDistance(target)
            if dist < threshold:
                # print(f"should decrease speed: threshold: {threshold}")
                # self.speedlimit *= dist/threshold
                newspeed = self.speedlimit.x * ( (dist/threshold)**1.1 )
                ns = Vector(newspeed, newspeed)
                self.speedlimit = ns

                # print(f"New speed: {self.speedlimit}")
            self.seek (target, weight)

        else:
            pass

    def flee(self, target:MovingBall, weight, dt, world, dist_thres):
        """
        Evaluate the position and flee from a target
        """
        desired_direction = (self.p - target.p).normalize()
        max_speed = self.speedlimit.length()
        desired_velocity = desired_direction * max_speed
        self.steering += [(desired_velocity - self.v)*weight]

        # while self.getDistance(target) < dist_thres*2:
        self.move(dt, world)

        self.speedlimit *= 1.0125
        # self.speedlimit *= round(( dist_thres - (self.getDistance(target)) ) *  0.0125, 1)
        
    def cohesion(self, centeroid:Vector, weight):
        centeroid_pos = centeroid
        desired_direction = (centeroid_pos - self.p).normalize()
        max_speed = self.speedlimit.length()
        desired_velocity = desired_direction * max_speed

        self.steering += [(desired_velocity - self.v) * weight]

        
    def separation(self, flock:list, weight):
        """
        Separates the flock
        """
        velocity_adjustment = Vector(0,0)
        threshold_radius = self.r*5

        for boid in flock:
            if boid != self:
                dist = self.getDistance(boid)
                if dist <= threshold_radius:
                    desired_direction = (self.p - boid.p).normalize()
                    max_speed = self.speedlimit.length()
                    desired_velocity = desired_direction * max_speed
                    self.steering += [(desired_velocity - self.v)*weight]

    def align(self, flock_list):
        
        avg_v = Vector(0,0)

        for boid in flock_list:
            if boid != self:
                avg_v += boid.v
        self.v = avg_v / (len(flock_list) - 1)



