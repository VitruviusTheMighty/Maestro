import pygame

class Sprite:

    img = None
    x = 0
    y = 0
    w = 0
    h = 0

    def __init__ (self, img, x, y):

        self.img = img
        self.x = x
        self.y = y
        self.w = img.get_width()
        self.h = img.get_height()


    def draw (self, window):

        window.blit (self.img, (self.x-self.w/2, self.y-self.h/2))
