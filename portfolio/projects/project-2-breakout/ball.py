from paddle import Paddle
import pygame
from vector import Vector

class Ball(pygame.sprite.Sprite):
    """
    Models a ball
    """
    def __init__(self, color, mass, position:Vector, radius:int, velocity:Vector, background_color:str="white", asSquare=False):
        super().__init__()

        self.radius = radius
        self.diameter = radius*2
        self.mass = mass
        self.position = position
        self.ceiling = 0

        self.asBox=asSquare

        w, h = (self.diameter, self.diameter)
        self.image = pygame.Surface([w, h])
        self.image.fill(pygame.color.Color(background_color))
        self.image.set_colorkey(pygame.color.Color(background_color))

        center_of_image = (self.diameter//2, self.diameter//2)
        # # Using a square hitbox for now

        if self.asBox:
            rect_object = pygame.Rect(0, 0, w, h)
            pygame.draw.rect(self.image, pygame.color.Color(color), rect_object)
        else:
            pygame.draw.circle(self.image, pygame.color.Color(color), center=center_of_image, radius=radius)


        self.velocity = velocity

        self.rect = self.image.get_rect()

    def load_display_info(self, global_display:pygame.Surface):
        self.global_display = global_display

    def load_clock(self, clock:pygame.time.Clock):
        self.clock = clock

    def load_header_info(self, header_height):
        self.ceiling += header_height

    def update_position(self, pos:Vector):
        self.rect.x = pos.x
        self.rect.y = pos.y

    def update(self):
        self.simulate()

    def move(self):
        # print(f"Velocity: {self.velocity.x, self.velocity.y}, Position: {self.position.x, self.position.y}")
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        self.update_pos(self.rect.x, self.rect.y)
        
    def update_pos(self, x, y):
        self.position.x = x + self.radius
        self.position.y = y + self.radius

    def simulate(self):
        self.move()
        # print(self.global_display.get_width(), self.global_display.get_height())
        self.bounce_wall(self.global_display.get_width(), self.global_display.get_height())

    def bounce_wall(self, w, h):
        '''
        handle bounces and readjust to prevent penetration
        '''
        # print(f"Position: {w}, {h}")
        # print(f"Velocity: {self.velocity.x}, {self.velocity.y}")

        if self.position.x <= 0+self.radius: #Left boundry 
            self.position.x = self.radius
            self.velocity.x *= -1
            # print("passed boundry")
        elif self.position.x >= w-self.radius: #right boundry
            self.position.x = w-self.radius
            self.velocity.x *= -1
            # print("passed right boundry")
            
        if self.position.y <= self.ceiling+self.radius: # ceiling
            self.position.y = self.radius+self.ceiling
            self.velocity.y *= -1
        elif self.position.y > h-self.radius: # floor
            self.position.y = h-self.radius
            self.velocity.y *= -1

    # def isIntersectingPaddle(self, paddle):
    #     dist_y = self.position.y - paddle.y

    #     abs_dist_y = abs(dist_y)

        
    # def bounce_object(self):
    #     pass

    def isColliding(self, other):

        if type(other) == type(self):
            pass
        elif type(other) == Paddle():
            pass

    # def bounce(self):
    #     # TODO: Error in how ball reacts to sides
    #     self.velocity.x = self.velocity.x
    #     self.velocity.y = self.velocity.y*-1

    def bounce(self, axis=1):
        """
        Relects ball velocity across desired axis
        0 = x
        1 = y
        (0, 1) = x,y
        """

        if axis == 0: 
            self.velocity.x = self.velocity.x*-1

        if axis == 1:
            self.velocity.y = self.velocity.y*-1

        elif axis == (0, 1):
            self.velocity.y = self.velocity.y*-1
            self.velocity.x = self.velocity.x*-1


