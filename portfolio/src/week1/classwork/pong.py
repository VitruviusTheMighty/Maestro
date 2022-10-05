# A simple pong game
# Author: Matthew Anderson, Kristina Striegnitz, John Rieffel
# Winter 2017 - BRUH DIS OLD, I was still worrying about my SATs back then
# Group B - Noah Lehman-Borer and Leo Ferrisi and Jiayong Song


import pygame
import time
import random

class BallContainer:

    def __init__(self):
        self.all_balls = []
        
class Ball:
    
    # TODO: Add x and y speed
    def __init__(self, x=300, y=300, speed=0.00001):
        self.x = x
        self.y = y
        self.__initalize()
        self.speed = speed
        self.direction = 0
        self.reverse = False
        
    def __initalize(self):
        self.radius = 10
        self.color = None
        self.__change_color()

    def add_edges(self, x, y):
        self.edge_x = x
        self.edge_y = y

    def draw(self, window:pygame.Surface):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

    def speed_up(self):
        self.speed = self.speed * 10

    
    def get_pos(self):
        return (self.x, self.y)
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

    def reflect(self):
        """
        Checks which axis ball needs to be reflected by and selects according subfunction
        """
        pass

    def __reflect_x(self):
        pass

    def __reflect_y(self):
        pass
    
    def move(self):
        """
        Right now is just horizontal
        """
        #TODO: Include edge case for top and bottom
        
        if self.reverse == False:
            if self.get_pos()[0] < self.edge_x - self.radius:
                self.x = self.x + 1
            else:
                self.reverse = True
                self.x = self.x - 1
                self.__change_color()
        else:
            if self.get_pos()[0] > 0 + self.radius:
                self.x = self.x - 1
            else:
                self.reverse = False
                self.x = self.x + 1
                self.__change_color()  
        time.sleep(self.speed)
                
    def __change_color(self):
        colors = ["Red", "Orange", "Yellow", "Green", " Blue", "Purple", "Magenta"]
        idx = random.randrange(len(colors))
        self.color = pygame.color.Color(colors[idx])

class Pong:

    def __init__(self):
        pygame.init()
        self.loop_game = True
        self.width = 840
        self.height = 680
        self.create_window()
        self.create_balls(random.randrange(0, 50))
        time.sleep(1)
        
    def create_window(self):
        self.my_win = pygame.display.set_mode((self.width, self.height))

    def add_edges_to(self, ball:Ball):
        ball.add_edges(x=self.width, y=self.height)
        
    def create_balls(self, quantity):
        print(f"Creating {quantity} balls")
        self.myBalls = []
        for i in range(quantity):
            speed = round(random.uniform(0.000000000000000001, 0.00009), 8)
            print(f"Speed is {speed}")
            ball = Ball(x=random.randrange(self.width), y=random.randrange(self.height), speed=speed)
            ball.add_edges(x=self.width, y=self.height)
            self.myBalls.append(ball)
            ball.draw(self.my_win)
    
    def update_my_BALLS(self):
        for ball in self.myBalls:
            ball.move()
            ball.draw(self.my_win)

    def draw_background(self):
        self.my_win.fill(pygame.color.Color("black"))

    def run_game(self):
        while (self.loop_game):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.loop_game = False
            self.draw_background()
            self.update_my_BALLS()
            pygame.display.update()
        pygame.quit()
        


if __name__ == "__main__":
    my_game = Pong()
    my_game.run_game()