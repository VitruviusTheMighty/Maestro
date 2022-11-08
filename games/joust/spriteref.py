import pygame
from pygame.transform import scale

try:
    from spritesheet_functions import SpriteSheet
    from vector import Vector
except:
    from salto.spritesheet_functions import SpriteSheet
    from salto.vector import Vector

import time
import os


WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0, 255, 0)

class CatParams:

    def __init__(self, spritesheet="catsheet_b.png", scale=10, extend=1):
        
        dirname = os.path.dirname(__file__)
        sheet = os.path.join(dirname, spritesheet)
        self.spritesheet = SpriteSheet(sheet)

        self.size = Vector(17, 17)

        self.padding = 15
        self.spacing = self.padding + self.size.x

        self.scale = scale

        # Load all
        self.load_idle(extend)
        self.load_walk(extend-2)

    def load_idle(self, extend=1):
        
        self.idle = []
        self.idle_reverse = []

        posx = 6
        posy = 15

        img = self.spritesheet.get_image(posx, posy, self.size.x, self.size.y)
        img.set_colorkey(GREEN)
        self.idle.append(  scale( img.convert_alpha(), size=(self.size.x*self.scale, self.size.y*self.scale) )  )
        self.idle_reverse.append(  scale( pygame.transform.flip(img.convert_alpha(), flip_x=True, flip_y=False) , size=(self.size.x*self.scale, self.size.y*self.scale) ) )

        img = self.spritesheet.get_image(38, posy, self.size.x, self.size.y)
        img.set_colorkey(GREEN)
        self.idle.append(  scale( img.convert_alpha(), size=(self.size.x*self.scale, self.size.y*self.scale) )  )
        self.idle_reverse.append(  scale( pygame.transform.flip(img.convert_alpha(), flip_x=True, flip_y=False) , size=(self.size.x*self.scale, self.size.y*self.scale) ) )

        img = self.spritesheet.get_image(70, posy, self.size.x, self.size.y)
        img.set_colorkey(GREEN)
        self.idle.append(  scale( img.convert_alpha(), size=(self.size.x*self.scale, self.size.y*self.scale) )  )
        self.idle_reverse.append(  scale( pygame.transform.flip(img.convert_alpha(), flip_x=True, flip_y=False) , size=(self.size.x*self.scale, self.size.y*self.scale) ) )

        img = self.spritesheet.get_image(102, posy, self.size.x, self.size.y)
        img.set_colorkey(GREEN)
        self.idle.append(  scale( img.convert_alpha(), size=(self.size.x*self.scale, self.size.y*self.scale) )  )
        self.idle_reverse.append(  scale( pygame.transform.flip(img.convert_alpha(), flip_x=True, flip_y=False) , size=(self.size.x*self.scale, self.size.y*self.scale) ) )

        if extend > 1:
            sub_idle = []
            sub_idle_reverse = []

            for img in self.idle:
                for i in range(extend):
                    sub_idle.append(img)
            self.idle = sub_idle

            for img in self.idle_reverse:
                for i in range(extend):
                    sub_idle_reverse.append(img)
            self.idle_reverse = sub_idle_reverse

        return self.idle, self.idle_reverse

    def load_walk(self, extend=1):
        self.walk = []
        self.walk_reverse = []
        
        # posx = 6
        # posy = 144

        posx = 6
        posy = 143

        for i in range(0, 8):
            img = self.spritesheet.get_image(posx+(self.spacing*i), posy, self.size.x, self.size.y)
            img.set_colorkey(GREEN)
            self.walk.append(  scale( img.convert_alpha(), size=(self.size.x*self.scale, self.size.y*self.scale) )  )
            self.walk_reverse.append(  scale( pygame.transform.flip(img.convert_alpha(), flip_x=True, flip_y=False) , size=(self.size.x*self.scale, self.size.y*self.scale) ) )

        if extend > 1:
            sub_walk = []
            sub_walk_reverse = []

            for img in self.walk:
                for i in range(extend):
                    sub_walk.append(img)
            self.walk = sub_walk

            for img in self.walk_reverse:
                for i in range(extend):
                    sub_walk_reverse.append(img)
            self.walk_reverse = sub_walk_reverse

        return self.walk, self.walk_reverse

if __name__ == "__main__":
    screen = pygame.display.set_mode([400, 400])

    c = CatParams()
    mode = 'walk'

    clock = pygame.time.Clock()
    while True:
        
        

        for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    done = True # Flag that we are done so we exit this loop
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()

        if mode == 'idle':
            screen.blit(c.idle[0],(150,150))
            pygame.display.flip()
            screen.fill(BLACK)
            time.sleep(0.1)

            screen.blit(c.idle[1],(150,150))
            pygame.display.flip()
            screen.fill(BLACK)
            time.sleep(0.1)

            screen.blit(c.idle[2],(150,150))
            pygame.display.flip()
            screen.fill(BLACK)
            time.sleep(0.1)

            screen.blit(c.idle[3],(150,150))
            pygame.display.flip()
            screen.fill(BLACK)
            time.sleep(0.1)

        elif mode == 'walk':
            
            for frame in c.walk:
                screen.blit(frame,(150,150))
                pygame.display.flip()
                screen.fill(BLACK)
                time.sleep(0.1)

        clock.tick(60)

        pygame.display.flip()
            
            # time.sleep(1)
        # time.sleep(1)