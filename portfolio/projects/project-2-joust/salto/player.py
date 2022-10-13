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

        self.possible_actions = ['idle', 'walking', 'jumping']

        self.action = 'idle'

        self.idle = c.idle
        self.idle_r = c.idle_reverse

        self.walk = c.walk
        self.walk_r = c.walk_reverse
        
        self.current_frame = (0, self.idle[0])

        # create sprite
        self.image = self.current_frame[1]
        self.rect = self.image.get_rect()

        # spawn player pos at ground
        self.pos = Vector(display.get_size()[0] // 2, self.main_floor - self.rect.h)
        self.update_pos() # initialize all storage


        self.speed   = 5
        self.facing  = 'right'
        self.jumping = False
        self.jump_decay = 1
        self.gravitational_acceleration = 10
        
        self.on_obj         = False
        self.on_obj_id      = None
        self.platform_floor = None
        self.platform       = None
    # Loading methods

    def set_speed(self, val):
        self.speed = val

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
        self.change_xv(self.speed)

    def go_left(self):
        if self.facing!='left':self.flip()
        self.change_xv(-self.speed)

    def jump(self):
        if self.onGround() or self.onPlatform():
            self.jumping = True
            self.change_yv(-30)
        
    # Position cases

    def onObject(self, obj):
        pass

    def onGround(self):
        return self.bottom >= self.main_floor 

    def onPlatform(self):
        if self.platform!=None: 
            return (self.pos.y == self.platform.rect.y - self.rect.h) and self.platform.isColliding(self)
        else: 
            return False

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

        elif self.action == 'walking':
            if self.facing == 'right':
                if self.current_frame[0]+1 == len(self.walk): # If is at end
                    self.current_frame = (0, self.walk[0])
                else: # get next
                    index, img = self.current_frame[0], self.current_frame[1]
                    self.current_frame = (index+1, self.walk[index+1])
                self.image = self.current_frame[1]
            else:
                if self.current_frame[0]+1 == len(self.walk_r): # If is at end
                    self.current_frame = (0, self.walk_r[0])
                else: # get next
                    index, img = self.current_frame[0], self.current_frame[1]
                    self.current_frame = (index+1, self.walk_r[index+1])
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
        if self.v.x != 0:
            if self.action != 'walking':
                self.action = 'walking'
                if self.facing == 'right': self.current_frame = (0, self.walk[0])
                else: self.current_frame = (0, self.walk_r[0])
        else:
            if self.action != 'idle': self.action = 'idle'

        



    
    def gravitate(self):
        # print(f"Jumping? {self.jumping}")

        if self.onGround() and not self.jumping and self.platform == None: # If we are on the ground and not trying to jump stop at the floor
            self.set_yv(val=0)
            self.pos.y = self.main_floor - self.rect.h

        if self.platform != None:
            self.set_yv(val=0)
            self.on_obj == True
            self.pos.y = self.platform.rect.y - self.rect.h


        else:
            if self.jumping and self.v.y >= 0: 
                # print("Setting jump to false")
                self.jumping = False
            
            elif not self.jumping and not self.onPlatform():  # MAIN GRAVITY METHOD
                self.set_yv(val=self.gravitational_acceleration)

            else:
                if self.jumping and self.v.y < 0: # JUMP DECAY
                    self.change_yv(self.jump_decay) # Make this some change able variable called jump decay
                    # print(f"Decreasing, yv - {self.v.y}")

                
        

    

