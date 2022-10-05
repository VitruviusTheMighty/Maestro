import pygame
from pygame.locals import *
import random


def roll(sides:int):
        return random.randint(0, sides)

class Star:
    
    def __init__(self, window, width, height, color=(255,255,255)):
        self.win = window
        self.color = color
        self.radius = random.randint(0, 4)
        self.center_x = random.randint(0, width)
        self.center_y = random.randint(0, height)
        self.draw()

    def draw(self):
        pygame.draw.circle(self.win, self.color, center=(self.center_x, self.center_y), radius=self.radius)


class Comet:
    """
    A class modeling the occasional comet or shooting star darting across the sky
    Make a wish!
    """
    def __init__(self, window, width, height, color=[255,255,255]):
        self.win = window
        self.color = color
        self.radius = random.randint(0, 4)
        self.center_x = random.randint(0, width)
        self.center_y = random.randint(0, height)
        self.dead = False
        self.lifespan = 255
        self.draw()

    def draw(self):
        """
        Move the comet, fade it slightly everytime this is run, and of course, draw it
        """
        self.move()
        self.fade()
        if self.dead == False:
            pygame.draw.circle(self.win, self.color, center=(self.center_x, self.center_y), radius=self.radius)
        
    def move(self):
        """
        Move the comet's position
        """
        self.center_x += 1
        self.center_y += 1

    def fade(self):
        """
        Fade the star
        """
        self.lifespan = self.lifespan - 1
        if self.lifespan <= 0:
            self.dead = True
        self.color = [self.lifespan, self.lifespan, self.lifespan]

class NightSky:
    """
    An object modeling the twinkling sky above us every night
    """
    def __init__(self, width=800, height=800, color=(0,0,0)):
        pygame.init()
        self.color = color
        self.width = width
        self.height = height
        self.win = pygame.display.set_mode((width, height))
        self.win.fill(color)
        self.stars = []
        self.genStars()
        self.event = None

    def genStars(self, num_stars=random.randint(0, 600)):
        """
        Generates a random amount of stars
        """
        print(f"Num stars = {num_stars}")
        for i in range(num_stars):
            star = Star(window=self.win, width=self.width, height=self.height)
            self.stars.append(star)
    
    def try_randomEvent(self):
        """
        Attempts to start a random event
        """
        if self.event == None:
            # spawn comet on random event
            if roll(200) == 1:
                self.event = Comet(window=self.win, width=self.width, height=self.height)    
        else:
            # run comet
            if self.event.dead == False:
                self.event.draw()
            else:
                self.event = None

    def live_sky(self):
        """
        Displays a sky live with a random chance of Comets/Shooting stars
        """
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.win.fill(self.color)
            for star in self.stars:
                star.draw()
            self.try_randomEvent()
            pygame.display.flip()

if __name__ == "__main__":
    n = NightSky()
    n.live_sky()