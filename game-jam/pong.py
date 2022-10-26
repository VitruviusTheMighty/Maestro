import pygame, sys
from pygame.locals import *
import os
import random

DIRNAME = os.path.dirname(__file__)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Pong:

    def __init__(self, display:pygame.Surface, speed=1):
        
        self.bg = pygame.image.load(os.path.join(DIRNAME, "assets//bg.png"))
        self.FPS = 120  
        self.default_speed = speed
        self.SPEED = self.default_speed

        self.PAD_SPEED = 0.5
        
        # paddle and line dimensions
        self.PADDLE_SIZE = 50 # Thickness of paddle
        self.PADDLE_XCOORD = 20 # x coordinate
        self.FPSCLOCK = pygame.time.Clock() # for custom frame rate

        self.BASICFONTSIZE = 15
        self.BASICFONT = pygame.font.Font(os.path.join(DIRNAME, "assets/font.ttf"), self.BASICFONTSIZE)

        self.DISPLAYSURF = display

        self.WIN_H = display.get_height()
        self.WIN_W = display.get_width()

        self.EDGE_W = 10

        self.INFLUENCED = False

        # draws out the window with center and side lines
    def draw_board(self):
        self.DISPLAYSURF.fill(BLACK) # fill screen with black
        self.DISPLAYSURF.blit(self.bg, (0,0))
        # 
        # outline
        # pygame.draw.rect(self.DISPLAYSURF, WHITE, ((0, 0), (WIN_W, WIN_H)), LINE_WIDTH * 2)
        # center
        # pygame.draw.line(self.DISPLAYSURF, WHITE, ((WIN_W / 2), 0), ((WIN_W / 2), WIN_H), int(LINE_WIDTH / 4))

    # draws the paddle on the board
    def place_paddle(self, paddle:pygame.Rect):
        if paddle.bottom > self.WIN_H - self.EDGE_W: # can't go beyond bottom of window
            paddle.bottom = self.WIN_H - self.EDGE_W
        elif paddle.top < self.EDGE_W: # can't go beyond top
            paddle.top = self.EDGE_W
        pygame.draw.rect(self.DISPLAYSURF, WHITE, paddle)

    # draws the ball
    def place_ball(self, ball:pygame.Rect):
        pygame.draw.rect(self.DISPLAYSURF, WHITE, ball)

    # increments the ball's coordinates based on direction
    def move_ball(self, ball, dir_x, dir_y): # ball is a Pygame rect
        ball.x += (dir_x * self.SPEED)
        ball.y += (dir_y * self.SPEED)
        return ball

    # makes the ball bounce at window boundaries
    def bounce(self, ball, dir_x, dir_y):
        if (ball.top <= self.EDGE_W) or (ball.bottom >= (self.WIN_H - self.EDGE_W)):
            dir_y *= -1 # change dir if hit upper or lower bound
        if (ball.left <= self.EDGE_W) or (ball.right >= self.WIN_W - self.EDGE_W):
            dir_x *= -1
        return dir_x, dir_y

    # ball hitting the paddles
    def hit_board(self, ball:pygame.Rect, paddle1:pygame.Rect, paddle2:pygame.Rect, dir_x):
        if (dir_x == -1) and (paddle1.right == ball.left) and (paddle1.top < ball.top) and (paddle1.bottom > ball.bottom):
            return -1
        elif (dir_x == 1) and (paddle2.left == ball.right) and (paddle2.top < ball.top) and (paddle2.bottom > ball.bottom):
            return -1
        else:
            return 1

    # the AI 
    def comp(self, ball:pygame.Rect, dir_x, paddle2:pygame.Rect):
        if dir_x == -1: # ball moving left, comp returns to center
            if paddle2.centery < (self.WIN_H / 2): # paddle center at upper half
                paddle2.y += self.SPEED * random.uniform(0.5, 1.5)
            elif paddle2.centery > (self.WIN_H / 2):
                paddle2.y -= self.SPEED * random.uniform(0.5, 1.5)
        elif dir_x == 1: # ball moving right, comp follows
            # Oh my god its cheating
            # TODO: Add a randomization function in here
            if paddle2.centery < ball.centery:
                paddle2.y += self.SPEED * random.uniform(0.5, 1.5)
            elif paddle2.centery > ball.centery:
                paddle2.y -= self.SPEED * random.uniform(0.5, 1.5)
        return paddle2

    # update score
    def has_scored(self, paddle1, paddle2, ball, score1, score2, dir_x):
        if ball.left == self.EDGE_W: # p1 lost, p2 scored
            ball.x = (self.WIN_W / 2) - (self.EDGE_W / 2)
            ball.y = (self.WIN_H / 2) - (self.EDGE_W / 2)
            dir_x = 1
            return ball, dir_x, score1, score2 + 5
        # p1 touches ball, gains a pt
        elif (dir_x == -1) and (paddle1.right == ball.left) and (paddle1.top < ball.top) and (paddle1.bottom > ball.bottom):
            return ball, dir_x, score1 + 1, score2
        elif (dir_x == 1) and (paddle2.left == ball.right) and (paddle2.top < ball.top) and (paddle2.bottom > ball.bottom):
            return ball, dir_x, score1, score2 + 1
        elif (ball.right == self.WIN_W - self.EDGE_W): # p1 scores! +5
            ball.x = (self.WIN_W / 2) - (self.EDGE_W / 2)
            ball.y = (self.WIN_H / 2) - (self.EDGE_W / 2)
            dir_x = -1
            return ball, dir_x, score1 + 5, score2
        else: # nothing yet
            return ball, dir_x, score1, score2 

    # displays score on board
    def print_score(self, score1, score2):
        # p1 score
        display_surf = self.BASICFONT.render('Score: %s' %(score1), True, WHITE)
        display_rect = display_surf.get_rect() # generate rect
        display_rect.topleft = (10, 25) # position rect
        # blit updates just the part of screed specified by resultRect
        self.DISPLAYSURF.blit(display_surf, display_rect)

        # p2 score
        display_surf2 = self.BASICFONT.render('Score: %s' %(score2), True, WHITE)
        display_rect2 = display_surf2.get_rect()
        display_rect2.topleft = (self.WIN_W - 140, 25)
        self.DISPLAYSURF.blit(display_surf2, display_rect2) 

    # determines if keyboard input is valid
    def keydown_paddle(self, event):
        if event.key == K_DOWN or event.key == K_s:
            return 8
        elif event.key in (K_UP, K_w):
            return -8
        else:
            return 0

    def keydown_ball(self, dir, event):
        if dir==-1: self.SPEED = self.default_speed

        if event.key == pygame.K_SPACE and dir==1:
            self.SPEED *= 2
            self.INFLUENCED = True
        else:
            self.INFLUENCED = False
                

        


    def play(self):

        
        # self.DISPLAYSURF = pygame.display.set_mode((self.WIN_W, self.WIN_H)) # set win size
        pygame.display.set_caption('PSYCHIC PONG') # window name

        # ball starting position
        ball_x = (self.WIN_W / 2) - (self.EDGE_W / 2)
        ball_y = (self.WIN_H / 2) - (self.EDGE_W / 2)
        
        # paddle positions (only care about height)
        p1_pos = p2_pos = (self.WIN_H - self.PADDLE_SIZE) / 2

        # direction ball is going
        dir_x = -1 # -1 is left
        dir_y = -1 # -1 is up

        # score
        p1_score = 0
        p2_score = 0

        # ball and paddle coordinates
        paddle1 = pygame.Rect(self.PADDLE_XCOORD, p1_pos, self.EDGE_W, self.PADDLE_SIZE)
        paddle2 = pygame.Rect(self.WIN_W - self.PADDLE_XCOORD - self.EDGE_W, p2_pos, self.EDGE_W, self.PADDLE_SIZE)
        ball = pygame.Rect(ball_x, ball_y, self.EDGE_W, self.EDGE_W)

        self.draw_board()
        self.place_paddle(paddle1)
        self.place_paddle(paddle2)
        self.place_ball(ball)

        

        pygame.mouse.set_visible(0) # cursor gone

        key = 0 # determines keyboard input

        while True: # game loop
            for event in pygame.event.get():
                if event.type == QUIT: # quitting the game
                    pygame.quit()
                    sys.exit()
                # elif event.type == MOUSEMOTION: # mouse / touchpad controls p1
                #     mouse_x, mouse_y = event.pos
                #     paddle1.y = mouse_y
                elif event.type == KEYDOWN: # pressed key 
                    if event.key == pygame.K_ESCAPE: 
                        pygame.quit()
                        sys.exit()
                    key = self.keydown_paddle(event)

                    self.keydown_ball(dir_x, event)

                elif event.type == KEYUP: # lifted key
                    key = 0
                    self.SPEED = self.default_speed
            
            paddle1.y += key
            
            
            

            # draw everything
            self.draw_board()
            self.place_paddle(paddle1)
            self.place_paddle(paddle2)
            self.place_ball(ball)

            # move ball
            ball = self.move_ball(ball, dir_x, dir_y)
            
            # check score
            ball, dir_x, p1_score, p2_score = self.has_scored(paddle1, paddle2, ball, p1_score, p2_score, dir_x)

            # check direction
            dir_x, dir_y = self.bounce(ball, dir_x, dir_y)        
            dir_x = dir_x * self.hit_board(ball, paddle1, paddle2, dir_x)

            # p2 responds
            paddle2 = self.comp(ball, dir_x, paddle2)

            self.print_score(p1_score, p2_score)

            if self.INFLUENCED:
                display_text = self.BASICFONT.render("INFLUENCING BALL", True, (255,255,0))
                display_rect = display_text.get_rect() # generate rect
                display_rect.center = (350, 350) # position rect
                self.DISPLAYSURF.blit(display_text, display_rect)
            

            pygame.display.update() # refresh screen
            self.FPSCLOCK.tick(self.FPS) # set framerate

if __name__ == "__main__":
    
    pygame.init()
    display = pygame.display.set_mode((600, 600))
    p = Pong(display)
    p.play()