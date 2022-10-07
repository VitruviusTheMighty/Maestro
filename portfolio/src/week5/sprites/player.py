"""
Derived from code provided at
http://programarcadegames.com/
"""
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
    def __init__(self, display):
        """ Constructor function """
        pygame.sprite.Sprite.__init__(self)

        self.display = display
        x, y = display.get_size()
        self.floor = y

        self.v = Vector(0,0)

        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "l_spritesheet.png")

        sprite_sheet = SpriteSheet(filename)

        god_dimensions = (220, 306)
        self.gdv = Vector(god_dimensions[0], god_dimensions[1])
        gd = god_dimensions

        self.walking_frames = []
        self.walking_reverse_frames = []

        img = sprite_sheet.get_image(0, 0, gd[0], gd[1])
        self.walking_frames.append(img)
        self.walking_reverse_frames.append(pygame.transform.flip(img.convert_alpha(), flip_x=True, flip_y=False))

        for i in range(1,31):
            image = sprite_sheet.get_image((gd[0]*i)+5, 0, gd[0], gd[1])
            self.walking_frames.append(image)
            self.walking_reverse_frames.append(pygame.transform.flip(image.convert_alpha(), flip_x=True, flip_y=False))
            self.image = self.walking_frames[0]
        self.walking_reverse_frames.reverse()
        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

        self.facing = 1 # 1 indicates right, 0 is left
        self.jump_height = self.floor - (self.gdv.y // 2)
        self.falling = False
        self.rising = False
        self.is_colliding = False


    def update(self):
        """ Move the player. """
        # Gravity etc
        self.simulate()

        # Move left/right
        # What is the division thing?
        frame = (self.rect.x // 5) % len(self.walking_frames)
        if self.facing == 1: self.image = self.walking_frames[frame]
        elif self.facing == 0: 
            # if frame < 0: frame = len(self.walking_reverse_frames) - frame
            try:
                self.image = self.walking_reverse_frames[frame]
            except:
                raise IndexError(f"List Index out of range. Tried to find image at index: {frame}. List len is: {len(self.walking_reverse_frames)}")
        self.mask = pygame.mask.from_surface(self.image)
            
        
        # print(f"Frame: {frame}. Facing: {self.facing}")

    def at_ground(self):
        bottom_corner = self.rect.y+self.gdv.y
        return bottom_corner+1 >= self.floor

    def apply_gravity(self):
        pass
    
    def above_jump_height(self)->bool:
        bottom_corner = self.rect.y+self.gdv.y
        return self.above_ground() and bottom_corner <= self.jump_height

    def above_ground(self)->bool:
        """
        Check if is above ground
        """
        bottom_corner = self.rect.y+self.gdv.y
        return (bottom_corner < self.floor)

    def below_ground(self)->bool:
        bottom_corner = self.rect.y+self.gdv.y
        return (bottom_corner >= self.floor-1)

    def simulate(self):
        """ Calculate effect of gravity. """
        self.rect.x += self.v.x
        self.rect.y += self.v.y
        
        # Check if above ground
        if self.above_ground():
            
            # if self.above_jump_height() and not self.falling:
            #     self.falling = True
            #     self.descend()

            if self.rising and self.above_jump_height():
                self.descend()

            if self.falling:
                if self.below_ground():
                    self.rect.y = self.floor - self.gdv.y

                    self.stop(x=False, y=True)
                    self.falling = False

        self.debugmsg(f"{self.gdv.y + self.rect.y -1}, {self.floor}")

    def jump(self):
        """ Called when user hits 'jump' button. """
        # modify gravity temporarily
        if not self.above_jump_height():
            self.v.y -= 1
            self.rising = True
        else:
            self.v.y += 1
            self.falling = True
            self.rising = False
        self.debugmsg("JMP", "red")

    def flip(self, desired_direction):
        if self.facing != desired_direction: 
            # self.image = pygame.transform.flip(surface=self.image.convert_alpha() ,flip_y=True, flip_x=False)
            self.facing = desired_direction

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """

        self.flip(0)
        self.v = Vector(-1, 0)

    def go_right(self):
        """ Called when the user hits the right arrow. """
        
        self.flip(1)
        self.v = Vector(1,0)
        # pass
    
    def fly(self):
        self.v = Vector(self.v.x, -1)

    def descend(self):
        if not self.is_colliding:
            if self.rising: self.rising = False
            self.debugmsg("DESCENDING", "red")
            if self.above_ground():
                self.stop(x=False, y=True)
                self.v.y += 1
        # self.v = Vector(self.v.x, 1)

    def stop(self, x=True, y=True):
        """ Called when the user lets off the keyboard. """
        if x and y:
            self.v = Vector(0,0)
            self.falling = False
        elif x and not y:
            self.v = Vector(0, self.v.y)
        elif not x and y:
            self.v = Vector(self.v.x, 0)
            self.falling = False
        else:
            self.v = self.v
        
    
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
        


if __name__ == "__main__":
    size = (640,480)
    screen = pygame.display.set_mode(size)
    p = Player(screen)