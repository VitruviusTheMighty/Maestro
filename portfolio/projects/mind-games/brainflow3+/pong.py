
import pygame, sys
from pygame.locals import *

''' game constants '''

# Frames per second 
FPS = 200

# Ball speed
SPEED = 1

# Window dimensions
WIN_W = 600
WIN_H = 600

# paddle and line dimensions
LINE_WIDTH = 10
PADDLE_SIZE = 50 # Thickness of paddle
PADDLE_XCOORD = 20 # x coordinate

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


''' functions '''

# draws out the window with center and side lines
def draw_board():
    DISPLAYSURF.fill(BLACK) # fill screen with black
    # outline
    # pygame.draw.rect(DISPLAYSURF, WHITE, ((0, 0), (WIN_W, WIN_H)), LINE_WIDTH * 2)
    # # center
    # pygame.draw.line(DISPLAYSURF, WHITE, ((WIN_W / 2), 0), ((WIN_W / 2), WIN_H), int(LINE_WIDTH / 4))

# draws the paddle on the board
def place_paddle(paddle):
    if paddle.bottom > WIN_H - LINE_WIDTH: # can't go beyond bottom of window
        paddle.bottom = WIN_H - LINE_WIDTH
    elif paddle.top < LINE_WIDTH: # can't go beyond top
        paddle.top = LINE_WIDTH
    pygame.draw.rect(DISPLAYSURF, WHITE, paddle)

# draws the ball
def place_ball(ball):
    pygame.draw.rect(DISPLAYSURF, WHITE, ball)

# increments the ball's coordinates based on direction
def move_ball(ball, dir_x, dir_y): # ball is a Pygame rect
    ball.x += (dir_x * SPEED)
    ball.y += (dir_y * SPEED)
    return ball

# makes the ball bounce at window boundaries
def bounce(ball, dir_x, dir_y):
    if (ball.top <= LINE_WIDTH) or (ball.bottom >= (WIN_H - LINE_WIDTH)):
        dir_y *= -1 # change dir if hit upper or lower bound
    if (ball.left <= LINE_WIDTH) or (ball.right >= WIN_W - LINE_WIDTH):
        dir_x *= -1
    return dir_x, dir_y

# ball hitting the paddles
def hit_board(ball, paddle1, paddle2, dir_x):
    if (dir_x == -1) and (paddle1.right == ball.left) and (paddle1.top < ball.top) and (paddle1.bottom > ball.bottom):
        return -1
    elif (dir_x == 1) and (paddle2.left == ball.right) and (paddle2.top < ball.top) and (paddle2.bottom > ball.bottom):
        return -1
    else:
        return 1

# the AI 
def comp(ball, dir_x, paddle2):
    if dir_x == -1: # ball moving left, comp returns to center
        if paddle2.centery < (WIN_H / 2): # paddle center at upper half
            paddle2.y += SPEED
        elif paddle2.centery > (WIN_H / 2):
            paddle2.y -= SPEED
    elif dir_x == 1: # ball moving right, comp follows
        if paddle2.centery < ball.centery:
            paddle2.y += SPEED
        elif paddle2.centery > ball.centery:
            paddle2.y -= SPEED
    return paddle2

# update score
def has_scored(paddle1, paddle2, ball, score1, score2, dir_x):
    if ball.left == LINE_WIDTH: # p1 lost, p2 scored
        ball.x = (WIN_W / 2) - (LINE_WIDTH / 2)
        ball.y = (WIN_H / 2) - (LINE_WIDTH / 2)
        dir_x = 1
        return ball, dir_x, score1, score2 + 5
    # p1 touches ball, gains a pt
    elif (dir_x == -1) and (paddle1.right == ball.left) and (paddle1.top < ball.top) and (paddle1.bottom > ball.bottom):
        return ball, dir_x, score1 + 1, score2
    elif (dir_x == 1) and (paddle2.left == ball.right) and (paddle2.top < ball.top) and (paddle2.bottom > ball.bottom):
        return ball, dir_x, score1, score2 + 1
    elif (ball.right == WIN_W - LINE_WIDTH): # p1 scores! +5
        ball.x = (WIN_W / 2) - (LINE_WIDTH / 2)
        ball.y = (WIN_H / 2) - (LINE_WIDTH / 2)
        dir_x = -1
        return ball, dir_x, score1 + 5, score2
    else: # nothing yet
        return ball, dir_x, score1, score2 

# displays score on board
def print_score(score1, score2):
    # p1 score
    display_surf = BASICFONT.render('Score: %s' %(score1), True, WHITE)
    display_rect = display_surf.get_rect() # generate rect
    display_rect.topleft = (50, 25) # position rect
    # blit updates just the part of screed specified by resultRect
    DISPLAYSURF.blit(display_surf, display_rect)

    # p2 score
    display_surf2 = BASICFONT.render('Score: %s' %(score2), True, WHITE)
    display_rect2 = display_surf2.get_rect()
    display_rect2.topleft = (WIN_W - 100, 25)
    DISPLAYSURF.blit(display_surf2, display_rect2) 

# determines if keyboard input is valid
def keydown(event):
    if event.key == K_DOWN or event.key == K_s:
        return 8
    elif event.key in (K_UP, K_w):
        return -8

# facilitates game
def play():
    pygame.init()
    global DISPLAYSURF # global variable, main surface that Pygame draws on
    
    # FONT
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE = 15
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    FPSCLOCK = pygame.time.Clock() # for custom frame rate
    
    DISPLAYSURF = pygame.display.set_mode((WIN_W, WIN_H)) # set win size
    pygame.display.set_caption('Pong - wtingda') # window name

    # ball starting position
    ball_x = (WIN_W / 2) - (LINE_WIDTH / 2)
    ball_y = (WIN_H / 2) - (LINE_WIDTH / 2)
    
    # paddle positions (only care about height)
    p1_pos = p2_pos = (WIN_H - PADDLE_SIZE) / 2

    # direction ball is going
    dir_x = -1 # -1 is left
    dir_y = -1 # -1 is up

    # score
    p1_score = 0
    p2_score = 0

    # ball and paddle coordinates
    paddle1 = pygame.Rect(PADDLE_XCOORD, p1_pos, LINE_WIDTH, PADDLE_SIZE)
    paddle2 = pygame.Rect(WIN_W - PADDLE_XCOORD - LINE_WIDTH, p2_pos, LINE_WIDTH, PADDLE_SIZE)
    ball = pygame.Rect(ball_x, ball_y, LINE_WIDTH, LINE_WIDTH)

    draw_board()
    place_paddle(paddle1)
    place_paddle(paddle2)
    place_ball(ball)

    pygame.mouse.set_visible(0) # cursor gone

    key = 0 # determines keyboard input

    while True: # game loop
        for event in pygame.event.get():
            if event.type == QUIT: # quitting the game
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION: # mouse / touchpad controls p1
                mouse_x, mouse_y = event.pos
                paddle1.y = mouse_y
            elif event.type == KEYDOWN: # pressed key 
                key = keydown(event)
            elif event.type == KEYUP: # lifted key
                key = 0
        
        paddle1.y += key

        # draw everything
        draw_board()
        place_paddle(paddle1)
        place_paddle(paddle2)
        place_ball(ball)

        # move ball
        ball = move_ball(ball, dir_x, dir_y)
        
        # check score
        ball, dir_x, p1_score, p2_score = has_scored(paddle1, paddle2, ball, p1_score, p2_score, dir_x)

        # check direction
        dir_x, dir_y = bounce(ball, dir_x, dir_y)        
        dir_x = dir_x * hit_board(ball, paddle1, paddle2, dir_x)

        # p2 responds
        paddle2 = comp(ball, dir_x, paddle2)

        print_score(p1_score, p2_score)

        pygame.display.update() # refresh screen
        FPSCLOCK.tick(FPS) # set framerate


if __name__ == "__main__":
    play()