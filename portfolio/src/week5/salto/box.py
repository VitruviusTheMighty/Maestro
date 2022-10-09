import pygame

class Box(pygame.sprite.Sprite):

    def __init__(self, color, height, width):
        super().__init__()
  
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
  
        pygame.draw.rect(self.image,
                         color,
                         pygame.Rect(0, 0, width, height))
  
        self.rect = self.image.get_rect()

    
    def playerAbove(self, player):
        """
        Check if play is above self
        """
        # Get player top left and top right

        # If either is above the platform, player is above platform
        pass
    