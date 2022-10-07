import pygame
BLACK = (0,0,0)

class Paddle(pygame.sprite.Sprite):
    #This class represents a paddle. It derives from the "Sprite" class in Pygame.
    
    def __init__(self, color, width, height, display):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        # Pass in the color of the paddle, its width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
 
        # Draw the paddle (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

        self.right_boundry = 

        self.speed = 10

    def moveLeft(self):
        """
        Move paddle left by speed
        """
        self.rect.x -= self.speed
        if self.rect.x < 0:
          self.rect.x = 0

    def moveRight(self):
        """
        Move paddle right by speed
        """
        self.rect.x += self.speed
        if self.rect.x > self.right_boundry-self.width:
          self.rect.x = self.right_boundry-self.width