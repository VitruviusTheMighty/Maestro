import pygame
from vector import Vector
from spriteref import CatParams

class Player(pygame.sprite.Sprite):
    
    def __init__(self, display:pygame.Surface):
        pygame.sprite.Sprite.__init__(self)

        self.v = Vector(0,0)

        self.main_floor = display.get_size()[1] # Sets the main floor to the display's y val

        # Load sprite
        c = CatParams(extend=4)

        self.action = 'idle'
        self.idle = c.idle
        self.idle_r = c.idle_reverse
        
        self.current_frame = (0, self.idle[0])

        # create sprite
        self.image = self.current_frame[1]
        self.rect = self.image.get_rect()

        # spawn player pos at ground
        self.pos = Vector(display.get_size()[0] // 2, self.main_floor - self.rect.h)
        self.update_pos() # initialize all storage


        self.facing = 'right'
    # Loading methods

    
    # Velocity Methods
    def set_xv(self, val):
        self.v.x = val
    
    def set_yv(self, val):
        self.v.y = val

    def change_xv(self, val):
        self.v.x += val
    
    def change_yv(self, val):
        self.v.y += val

    def stop_x(self):
        self.v.x = 0
    
    def stop_y(self):
        self.v.y = 0
    
    def stop(self):
        self.stop_x()
        self.stop_y()
    
    # Movement methods
    def go_right(self):
        if self.facing!='right':self.flip()
        self.change_xv(5)

    def go_left(self):
        if self.facing!='left':self.flip()
        self.change_xv(-5)

    # Position cases

    def onObject(self, obj):
        pass

    def onGround(self):
        return self.bottom == self.main_floor

    def flip(self):
        if self.facing == 'right':
            idx = self.current_frame[0]
            self.current_frame = (idx, self.idle_r[idx])
            self.image = self.current_frame[1]
            self.facing = 'left'
        else:
            idx = self.current_frame[0]
            self.current_frame = (idx, self.idle[idx])
            self.image = self.current_frame[1]
            self.facing = 'right'

    def animate(self):
        # TODO: Reimplement
        if self.action == 'idle':

            if self.facing == 'right':
                if self.current_frame[0]+1 == len(self.idle): # If is at end
                    self.current_frame = (0, self.idle[0])
                else: # get next
                    index, img = self.current_frame[0], self.current_frame[1]
                    self.current_frame = (index+1, self.idle[index+1])
                self.image = self.current_frame[1]
            else:
                if self.current_frame[0]+1 == len(self.idle_r): # If is at end
                    self.current_frame = (0, self.idle_r[0])
                else: # get next
                    index, img = self.current_frame[0], self.current_frame[1]
                    self.current_frame = (index+1, self.idle_r[index+1])
                self.image = self.current_frame[1]


    def update_pos(self):
        self.pos.x += self.v.x
        self.pos.y += self.v.y
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        self.bottom = self.rect.y + self.rect.h

    def update(self):
        """
        Move the player
        """
        self.animate() # Updates current frame
        # Update player properties

        # Use self.current frame

        self.simulate()
        self.update_pos()


    def simulate(self):
        self.gravitate()


    
    def gravitate(self):

        if self.onGround():
            self.set_yv(val=0)
            self.pos.y = self.main_floor - self.rect.h
        else:
            self.change_yv(val=0.5)
        

    

