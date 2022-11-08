import pygame

class Brick(pygame.sprite.Sprite):
    """
    A breakout brick
    """
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(pygame.color.Color("black"))
        self.image.set_colorkey(pygame.color.Color("black"))
        rect_object = pygame.Rect(0, 0, width, height) # drawn from top left corner
        pygame.draw.rect(self.image, pygame.color.Color(color), rect_object)

        self.rect = self.image.get_rect()
        
        # Switches

        isPowerup = False

    def update(self):
        pass
        # if isPowerup: updateColor, do something else