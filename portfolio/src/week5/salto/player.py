"""
Derived from code provided at
http://programarcadegames.com/
"""
from tkinter.tix import DisplayStyle
from numpy import disp
import pygame
import os
from spritesheet_functions import SpriteSheet
from vector import Vector
from termcolor import colored
import datetime

class Player(pygame.sprite.Sprite):
    """
    Models a player sprite
    """
    def __init__(self, display:pygame.Surface):
        """ Constructor function """
        pygame.sprite.Sprite.__init__(self)

        # Constants
        self.display = display
        self.display_size = Vector(display.get_size()[0], display.get_size()[1])
        self.ground = self.display_size.y
        
        self.v = Vector(0, 0) # Initial Velocity

        # Sprite appearance
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "sprite/mr_salto.png")
        sprite_sheet = SpriteSheet(filename)
        
        size = Vector(14, 23)
        self.load_mrsalto(sprite_sheet, size.x, size.y)

        self.image = self.walking_frames[0] # starter image
        self.rect = self.image.get_rect()

        # Variables
        self.facing = 1 # 1 indicates right, 0 is left
        
        # Constants
        self.maxh = size.y * 3

    def load_mrsalto(self, spritesheet:SpriteSheet, size_x, size_y, padding=5, scale=1):
        
        p = padding

        self.walking_frames = []
        self.walking_reverse_frames = []
        # self.jumping_frames = []
        self.crouching_frames = []
        self.crouch_walk = []
        self.crouch_walk_left = []


        # self.size = Vector(14, 23) # TBD will need to be updated

        # regular walk sequence
        img = spritesheet.get_image(0, 0, size_x+p, size_y+p)
        # img.set_colorkey(color=white)
        if scale > 1: img = pygame.transform.scale(img.convert_alpha(), ((size_x)*scale, (size_y)*scale))
        self.walking_frames.append(img.convert_alpha())
        self.walking_reverse_frames.append(pygame.transform.flip(img.convert_alpha(), flip_x=True, flip_y=False))

        img = spritesheet.get_image(28, 46, size_x+p, size_y+p)
        # # img.set_colorkey(color="white")
        if scale > 1: img = pygame.transform.scale(img.convert_alpha(), ((size_x)*scale, (size_y)*scale))
        self.walking_frames.append(img.convert_alpha())
        self.walking_reverse_frames.append(pygame.transform.flip(img.convert_alpha(), flip_x=True, flip_y=False))
        

        
        # Crouching frames
        img = spritesheet.get_image(size_x*6, size_y*6, size_x+p, size_y+p)
        # img.set_colorkey(color="white")
        if scale > 1: img = pygame.transform.scale(img.convert_alpha(), ((size_x)*scale, (size_y)*scale))
        self.crouching_frames.append(img.convert_alpha())

        img = spritesheet.get_image(size_x*5, size_y*5, size_x+p, size_y+p)
        # img.set_colorkey(color="white")
        if scale > 1: img = pygame.transform.scale(img.convert_alpha(), ((size_x)*scale, (size_y)*scale))
        self.crouching_frames.append(img.convert_alpha())

        img = spritesheet.get_image(size_x*9, size_y*9, size_x+p, size_y+p)
        # img.set_colorkey(color="white")
        if scale > 1: img = pygame.transform.scale(img.convert_alpha(), ((size_x)*scale, (size_y)*scale))
        self.crouching_frames.append(img.convert_alpha())

        # Crouching walk
        img = spritesheet.get_image(size_x*9, size_y*9, size_x+p, size_y+p)
        # img.set_colorkey(color="white")
        if scale > 1: img = pygame.transform.scale(img.convert_alpha(), ((size_x)*scale, (size_y)*scale))
        self.crouch_walk.append(img.convert_alpha())

        img = spritesheet.get_image(size_x*10, size_y*10, size_x+p, size_y+p)
        # img.set_colorkey(color="white")
        if scale > 1: img = pygame.transform.scale(img.convert_alpha(), ((size_x)*scale, (size_y)*scale))
        self.crouch_walk.append(img.convert_alpha())
        self.crouch_walk_left.append(pygame.transform.flip(img.convert_alpha(), flip_x=True, flip_y=False))

        self.walking_reverse_frames.reverse()
        self.crouch_walk_left.reverse()

    
        self.size = Vector(size_x, size_y)

    def update(self):
        self.simulate()

    def simulate(self):
        self.applyGravity()
        self.rect.x += self.v.x
        self.rect.y += self.v.y  

    def aboveGround(self):
        return self.rect.y < self.ground + 2

    def belowGround(self):
        return self.rect.y >= self.ground + 1

    def applyGravity(self):
        if self.aboveGround():
            self.change_yv(mode=0, val=1, msg="falling")
        elif self.belowGround():
            self.rect.y = (self.ground - self.size.y)
        else:
            self.change_yv(1, self.v.y, msg="At ground")

    # Changer
    def change_yv(self, mode=1, val=0, msg=""):
        """
        mode 0: add
        mode 1: set
        """
        if mode>0:self.v.y = val
        else: self.v.y = val
        if msg!="":
            self.debugmsg(msg, "green")

    def change_xv(self, mode=1,val=0, msg=""):
        """
        mode 0: add
        mode 1: set
        """
        if mode>0: self.v.x = val
        else: self.v.x += val
        if msg!="":
            self.debugmsg(msg, "yellow")

    def debugmsg(self, msg, color="white"):
        """
        Prints a color coded message for debugging
        """
        d = datetime.datetime.now()
        dt = d.strftime("%m|%d|%Y::%H:%M:%S")
        timestamp = colored(text=f"[{dt}]", color="blue")
        file_opener = colored(text="[player]:", color="cyan")
        message = colored(text=msg, color=color)
        print(f"{timestamp}{file_opener} {message}")
            




        
        



