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
        
        size = Vector(16, 21)
        self.load_mrsalto(sprite_sheet, size.x, size.y)

        self.image = self.walking_frames[0] # starter image
        self.rect = self.image.get_rect()

        # Variables
        self.facing = 1 # 1 indicates right, 0 is left
        self.jumping = False

        # Constants
        self.maxh = size.y * 3

    def load_mrsalto(self, spritesheet:SpriteSheet, size_x, size_y, padding=5, scale=10):
        
        p = padding

        self.walking_frames = []
        self.walking_reverse_frames = []
        # self.jumping_frames = []
        self.crouching_frames = []
        self.crouch_walk = []
        self.crouch_walk_left = []

        white = (255,255,255)
        green = (0, 255, 110)

        # self.size = Vector(14, 23) # TBD will need to be updated

        # regular walk sequence
        img = spritesheet.get_image(0, 0, size_x+p, size_y+p)
        img.set_colorkey(green)
        if scale > 1: img = pygame.transform.scale(img.convert_alpha(), ((size_x)*scale, (size_y)*scale))
        self.walking_frames.append(img.convert_alpha())
        self.walking_reverse_frames.append(pygame.transform.flip(img.convert_alpha(), flip_x=True, flip_y=False))

        img = spritesheet.get_image(size_x+p*2, size_y+p, size_x+p, size_y+p)
        img.set_colorkey(green)
        if scale > 1: img = pygame.transform.scale(img.convert_alpha(), ((size_x)*scale, (size_y)*scale))
        self.walking_frames.append(img.convert_alpha())
        self.walking_reverse_frames.append(pygame.transform.flip(img.convert_alpha(), flip_x=True, flip_y=False))

        img = spritesheet.get_image(0, 0, size_x+p*3, size_y+p)
        img.set_colorkey(green)
        if scale > 1: img = pygame.transform.scale(img.convert_alpha(), ((size_x)*scale, (size_y)*scale))
        self.walking_frames.append(img.convert_alpha())
        self.walking_reverse_frames.append(pygame.transform.flip(img.convert_alpha(), flip_x=True, flip_y=False))

        img = spritesheet.get_image(size_x+p*3, size_y+p, size_x+p, size_y+p)
        img.set_colorkey(green)
        if scale > 1: img = pygame.transform.scale(img.convert_alpha(), ((size_x)*scale, (size_y)*scale))
        self.walking_frames.append(img.convert_alpha())
        self.walking_reverse_frames.append(pygame.transform.flip(img.convert_alpha(), flip_x=True, flip_y=False))
        

        
        # Crouching frames
        img = spritesheet.get_image(size_x*6, size_y*6, size_x+p, size_y+p)
        img.set_colorkey(green)
        if scale > 1: img = pygame.transform.scale(img.convert_alpha(), ((size_x)*scale, (size_y)*scale))
        self.crouching_frames.append(img.convert_alpha())

        img = spritesheet.get_image(size_x*5, size_y*5, size_x+p, size_y+p)
        img.set_colorkey(green)
        if scale > 1: img = pygame.transform.scale(img.convert_alpha(), ((size_x)*scale, (size_y)*scale))
        self.crouching_frames.append(img.convert_alpha())

        img = spritesheet.get_image(size_x*9, size_y*9, size_x+p, size_y+p)
        img.set_colorkey(green)
        if scale > 1: img = pygame.transform.scale(img.convert_alpha(), ((size_x)*scale, (size_y)*scale))
        self.crouching_frames.append(img.convert_alpha())

        # Crouching walk
        img = spritesheet.get_image(size_x*9, size_y*9, size_x+p, size_y+p)
        img.set_colorkey(green)
        if scale > 1: img = pygame.transform.scale(img.convert_alpha(), ((size_x)*scale, (size_y)*scale))
        self.crouch_walk.append(img.convert_alpha())

        img = spritesheet.get_image(size_x*10, size_y*10, size_x+p, size_y+p)
        img.set_colorkey(green)
        if scale > 1: img = pygame.transform.scale(img.convert_alpha(), ((size_x)*scale, (size_y)*scale))
        self.crouch_walk.append(img.convert_alpha())
        self.crouch_walk_left.append(pygame.transform.flip(img.convert_alpha(), flip_x=True, flip_y=False))

        self.walking_reverse_frames.reverse()
        self.crouch_walk_left.reverse()

    
        self.size = Vector(size_x, size_y)

    def update(self):
        self.simulate()

        frame = (self.rect.x // 5) % len(self.walking_frames)
        if self.facing == 1: self.image = self.walking_frames[frame]
        elif self.facing == 0: 
            try:
                self.image = self.walking_reverse_frames[frame]
            except:
                raise IndexError(f"List Index out of range. Tried to find image at index: {frame}. List len is: {len(self.walking_reverse_frames)}")
        self.mask = pygame.mask.from_surface(self.image)

    def simulate(self):
        self.applyGravity()
        self.rect.x += self.v.x
        self.rect.y += self.v.y  

    def aboveGround(self):
        return self.rect.y + self.rect.h <= self.ground - 1

    def belowGround(self):
        return self.rect.y + self.rect.h >= self.ground 

    def applyGravity(self):

        if not self.jumping:
            if self.aboveGround():
                self.change_yv(mode=0, val=1, msg="falling")

            elif self.belowGround():
                self.rect.y = self.ground - self.rect.h
                self.change_yv(0, 1)
            else:
                # self.change_yv(1, self.v.y, msg="At ground")
                self.change_yv(0, 1, msg="At ground")

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

    # Orient
    def flip(self, str):
        if str=='right' and self.facing==0:
            self.facing = 1
        elif str=='left' and self.facing==1:
            self.facing = 0
        else:
            pass
    # Movement

    def stop(self):
        self.change_xv(1, 0)
        self.change_yv(1, 0)


    def go_right(self):
        self.flip('right')
        self.change_xv(0, 1, "moving right")

    def go_left(self):
        self.flip('left')
        self.change_xv(0, -1, "moving left")

    def jump(self):

        # if not self.aboveGround():
        self.jumping = True
        print("JMP")
        self.change_yv(1, -1, "jumping")



        
        



