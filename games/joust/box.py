from re import S
import pygame
import random

try:
    from vector import Vector
except:
    from salto.vector import Vector

class Box(pygame.sprite.Sprite):

    def __init__(self, color, height, width, posx, posy):
        super().__init__()
  
        self.image = pygame.Surface([width, height])


        if type(color) == str: color = pygame.color.Color(color)

        self.image.fill(color)
  
        pygame.draw.rect(self.image,
                         color,
                         pygame.Rect(0, 0, width, height))

        self.v = Vector(0,0)
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy
        self.id = str(''.join(["{}".format(random.randint(0, 9)) for num in range(0, 10)]))

    def isColliding(self, obj:pygame.sprite.Sprite):
        """
        Checks if self is colliding with sprite obj

        Args:
            obj (pygame.sprite.Sprite): Object we can collide with
        Returns:
            bool: True if mask is colliding, False if no
        """
        if pygame.sprite.collide_mask(self, obj):
            return True
        return False


    def objOnTop(self, obj:pygame.sprite.Sprite):
        """
        Checks if self is colliding with sprite obj

        Args:
            obj (pygame.sprite.Sprite): Object we can collide with
        Returns:
            bool: True if mask is colliding, False if no
        """
        if self.isColliding(obj):
            bottom_object_y = obj.rect.y + obj.rect.h
            return bottom_object_y <= self.rect.y + self.rect.h

    # Velocity methods
    def set_xv(self, val):
        self.v.x = val

    def set_yv(self, val):
        self.v.y = val

    def change_xv(self, val):
        self.v.x += val

    def change_yv(self, val):
        self.v.y += val

    def stop_x(self):
        if self.v.x > 0:
            self.v.x = 0
    
    def stop_y(self):
        if self.v.y > 0:
            self.v.y = 0
    
    def stop(self):
        self.v = Vector(0,0)

    def update(self):
        self.simulate()

    def simulate(self):
        self.rect.x += self.v.x
        self.rect.y += self.v.y

if __name__ == "__main__":
    b = Box(color="red", height=10, width=10)
    print(type(b))

    print(isinstance(b, Box))