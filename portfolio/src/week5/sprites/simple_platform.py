import pygame
from vector import Vector

class Box(pygame.sprite.Sprite):

    def __init__(self, color, height, width):
        super().__init__()
  
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
  
        pygame.draw.rect(self.image,
                         color,
                         pygame.Rect(0, 0, width, height))

        self.v = Vector(0,0)
        self.rect = self.image.get_rect()

    def isColliding(self, obj:pygame.sprite.Sprite):
        """
        Checks if self is colliding with sprite obj

        Args:
            obj (pygame.sprite.Sprite): Object we can collide with
        Returns:
            bool: True if mask is colliding, False if no
        """
        return pygame.sprite.collide_mask(self,obj)

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

    def change_xv(self, val):
        self.v.x += val

    def stop_x(self):
        if self.v.x > 0:
            self.v.x == 0
    
    def stop_y(self):
        if self.v.y > 0:
            self.v.y == 0
    
    def stop(self):
        self.v = Vector(0,0)

if __name__ == "__main__":
    b = Box(color="red", height=10, width=10)
    print(type(b))

    print(isinstance(b, Box))