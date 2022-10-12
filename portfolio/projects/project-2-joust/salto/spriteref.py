import pygame
from pygame.transform import scale

from spritesheet_functions import SpriteSheet
import time
import os

from vector import Vector

WHITE = (255,255,255)
BLACK = (0,0,0)

class CatParams:

    def __init__(self, spritesheet="catsheet.png", scale=10, extend=1):
        
        dirname = os.path.dirname(__file__)
        sheet = os.path.join(dirname, spritesheet)
        self.spritesheet = SpriteSheet(sheet)

        self.size = Vector(14, 14)

        self.padding = 18

        self.scale = scale

        # Load all
        self.load_idle(extend)
        self.load_walk()

    def load_idle(self, extend=1):
        
        self.idle = []
        self.idle_reverse = []

        posx = 7
        posy = 18

        img = self.spritesheet.get_image(posx, posy, self.size.x, self.size.y)
        img.set_colorkey(WHITE)
        self.idle.append(  scale( img.convert_alpha(), size=(self.size.x*self.scale, self.size.y*self.scale) )  )
        self.idle_reverse.append(  scale( pygame.transform.flip(img.convert_alpha(), flip_x=True, flip_y=False) , size=(self.size.x*self.scale, self.size.y*self.scale) ) )

        img = self.spritesheet.get_image(39, posy, self.size.x, self.size.y)
        img.set_colorkey(WHITE)
        self.idle.append(  scale( img.convert_alpha(), size=(self.size.x*self.scale, self.size.y*self.scale) )  )
        self.idle_reverse.append(  scale( pygame.transform.flip(img.convert_alpha(), flip_x=True, flip_y=False) , size=(self.size.x*self.scale, self.size.y*self.scale) ) )

        img = self.spritesheet.get_image(71, posy, self.size.x, self.size.y)
        img.set_colorkey(WHITE)
        self.idle.append(  scale( img.convert_alpha(), size=(self.size.x*self.scale, self.size.y*self.scale) )  )
        self.idle_reverse.append(  scale( pygame.transform.flip(img.convert_alpha(), flip_x=True, flip_y=False) , size=(self.size.x*self.scale, self.size.y*self.scale) ) )

        img = self.spritesheet.get_image(103, posy, self.size.x, self.size.y)
        img.set_colorkey(WHITE)
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

    def load_walk(self):
        self.walk = []
        self.walk_reverse = []

        posx = 10
        posy = 179

        for i in range(0, 4):
            img = self.spritesheet.get_image(posx+(self.padding*i), posy+(self.padding*i), self.size.x, self.size.y)
            self.walk.append(  scale( img.convert_alpha(), size=(self.size.x*self.scale, self.size.y*self.scale) )  )
            self.walk_reverse.append(  scale( pygame.transform.flip(img.convert_alpha(), flip_x=True, flip_y=False) , size=(self.size.x*self.scale, self.size.y*self.scale) ) )

        return self.walk, self.walk_reverse

if __name__ == "__main__":
    screen = pygame.display.set_mode([400, 400])

    c = CatParams()

    clock = pygame.time.Clock()
    while True:
        
        

        for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    done = True # Flag that we are done so we exit this loop
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
        print(len(c.idle))

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

        clock.tick(60)

        pygame.display.flip()
            
            # time.sleep(1)
        # time.sleep(1)