import pygame
# from ball import Ball

class Paddle(pygame.sprite.Sprite):
    """
    a Paddle for breakout
    """    
    def __init__(self, color, width, height, speed=1):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        pygame.draw.rect(self.image, color, [0, 0, width, height])        
        self.rect = self.image.get_rect()
        self.speed = speed

    def update_boundry(self, new_width):
        """
        Add information about the right boundry
        """
        self.right_boundry = new_width

    def speedUp(self):
        """
        Speed paddle up
        """
        self.speed += 0.1

    def slowDown(self):
        """
        Slow paddle down
        """
        self.speed -= 0.1

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

    # def isMakingContact(self, display, ball):

    #     r = ball.radius
        
    #     pos_x = self.rect.x
    #     pos_y = self.rect.y

    #     # print(f"Pos: {pos_x, pos_y}")
        
    #     self.sides = {
    #         "left": ((pos_x, pos_y), (pos_x, pos_y+self.height)),
    #         "top": ((pos_x, pos_y), (pos_x+self.width, pos_y)),
    #         "right": ((pos_x+self.width, pos_y), (pos_x+self.width, pos_y+self.height)),
    #         "bottom": ((pos_x, pos_y+self.height), (pos_x+self.width, pos_y+self.height))
    #     }

    #     self.bounds = {
            
    #         "left": ((pos_x-r, pos_y-r), (pos_x-r, pos_y+self.height+r)),
    #         "top": ((pos_x-r, pos_y-r), (pos_x+self.width+r, pos_y-r)),
    #         "right": ((pos_x+self.width+r, pos_y-r), (pos_x+self.width+r, pos_y+self.height+r)),
    #         "bottom": ((pos_x-r, pos_y+self.height+r), (pos_x+self.width+r, pos_y+self.height+r))

    #     }

    

    #     # x = ball.position.x
    #     # y = ball.position.y




        



        