import pygame

from sprite import Sprite

class SpriteMoving (Sprite):

    xv = 0.0
    yv = 0.0
    bbox = (0,0,0,0)

    # Idea: bounding box is a rectangle contained in the image. The
    # argument bounding_box indicates the x and y offset of the
    # bounding box from the top left corner of the image and the width
    # and height of the bounding box.
    def __init__ (self, img, x, y, xv, yv, bounding_box):
        Sprite.__init__(self, img, x, y)
        self.xv = float(xv)
        self.yv = float(yv)
        self.bbox = bounding_box


    def move (self, millisecs):

        self.x += self.xv * float(millisecs)/1000
        self.y += self.yv * float(millisecs)/1000


    def bounce (self, width, height):

        if (self.x + self.w/2) > width:
            self.x = width - self.w/2
            self.xv *= -1
        elif (self.x - self.w/2) < 0:
            self.x = 0 + self.w/2
            self.xv *= -1
        if (self.y + self.h/2) > height:
            self.y = height - self.h/2
            self.yv *= -1
        elif (self.y - self.h/2) < 0:
            self.y = 0 + self.h/2
            self.yv *= -1


    def simulate (self, millisecs, width, height):
        self.move(millisecs)
        self.bounce(width, height)

    
    def get_bbox (self):
        """
        Calculates the screen coordinate of the bounding box.
        """
        top_left_x = self.x-self.w/2
        top_left_y = self.y-self.h/2
        return pygame.Rect(top_left_x + self.bbox[0], top_left_y + self.bbox[1], self.bbox[2], self.bbox[3])
        

    def collide (self, s2):
        """
        Uses pygame's built in collision detection to check whether
        two sprites collide based on their bounding boxes.
        """
        return self.get_bbox().colliderect(s2.get_bbox())
