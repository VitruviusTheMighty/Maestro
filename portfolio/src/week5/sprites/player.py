"""
Derived from code provided at
http://programarcadegames.com/
"""
import pygame


from spritesheet_functions import SpriteSheet
from vector import Vector

class Player(pygame.sprite.Sprite):

    # -- Attributes
    # Set speed vector of player

    # This holds all the images for the animated walk left/right
    # of our player
    

    # -- Methods
    def __init__(self, display):
        """ Constructor function """
        #This is ugly, but it came with the example code...

        self.gravity = 1.0

        self.display = display

        x, y = display.get_size()
        self.floor = y
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        self.v = Vector(0,0)

        sprite_sheet = SpriteSheet("l_spritesheet.png")

        # DEAR GOD ITS MAREVELOUS
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
        self.jumping = False
        self.jump_height = self.floor - 10

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
        
        print(f"Frame: {frame}. Facing: {self.facing}")


    def apply_gravity(self):
        pass

    def isAboveGround(self):
        pass

    def simulate(self):
        """ Calculate effect of gravity. """
        ## NOTE USE self.rect for position
        self.rect.x += self.v.x
        # self.rect.y += self.v.y

        if not self.jumping:
            if self.gdv.y + self.rect.y <= self.floor-5:
                self.rect.y += self.gravity
                print("sinking")
            elif self.gdv.y + self.rect.y > self.floor:
                self.rect.y = self.floor - self.gdv.y - 2
            else:
                self.rect.y += 0
        else:
            self.rect.y += 10

            if self.rect.y < self.jump_height:
                self.jumping = False
                self.gravity = 1.0

        print(f"{self.gdv.y + self.rect.y -1}, {self.floor}")

    def jump(self):
        """ Called when user hits 'jump' button. """
        # modify gravity temporarily
        self.jumping = True
        self.gravity = 0
        
    
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
        self.v = Vector(self.v.x, 1)
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.v = Vector(0,0)
        pass


if __name__ == "__main__":
    size = (640,480)
    screen = pygame.display.set_mode(size)
    p = Player()