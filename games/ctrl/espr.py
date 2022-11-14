import pygame, sys
from pygame.locals import *
import os
import random
import numpy as np

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds,BrainFlowError
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowFunctions, DetrendOperations
from brainflow.ml_model import MLModel, BrainFlowMetrics, BrainFlowClassifiers, BrainFlowModelParams
from brainflow.exit_codes import *

import time

from simplepygamemenus.menu import Button

DIRNAME = os.path.dirname(__file__)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class ESPPong:

    def __init__(self, display:pygame.Surface, speed=1, esp_threshold=0.8):
        
        self.background = pygame.image.load(os.path.join(DIRNAME, "assets//bg_large.png"))
        self.bg = pygame.image.load(os.path.join(DIRNAME, "assets//bg_large.png"))
        self.FPS = 120  
        self.default_speed = speed
        self.SPEED = self.default_speed

        self.PAD_SPEED = 0.5
        
        # paddle and line dimensions
        self.PADDLE_SIZE = 100 # Thickness of paddle
        self.PADDLE_XCOORD = 20 # x coordinate
        self.FPSCLOCK = pygame.time.Clock() # for custom frame rate

        self.BASICFONTSIZE = 15
        self.BASICFONT = pygame.font.Font(os.path.join(DIRNAME, "assets/font.ttf"), self.BASICFONTSIZE)

        self.DISPLAYSURF = display

        self.WIN_H = display.get_height()
        self.WIN_W = display.get_width()
        self.cx = self.WIN_W//2
        self.cy = self.WIN_H//2
        self.load_background_coords(use_center=True)


        self.EDGE_W = 10

        self.INFLUENCED = False

        self.FOCUS_THRES = esp_threshold
        
        self.connected = False
        self.ml_prepped = False
        self.streaming = False
        self.primary_menu_call = None

    # ==============================
    def get_font(self, size, font_path=None): # Returns Press-Start-2P in the desired size
        if font_path!=None: return pygame.font.Font(os.path.join(DIRNAME, font_path), size)
        else: return pygame.font.Font(os.path.join(DIRNAME, "assets/font.ttf"), size)

    def gen_text(self, text="", size=45, color="#b68f40", pos=(0,0), custom_font=None):
        TEXT = self.get_font(size=size, font_path=custom_font).render(text, True, color)
        TEXT_RECT = TEXT.get_rect(center=pos)
        return TEXT, TEXT_RECT

    def display_text(self, text="", size=45, color="#b68f40", pos=(0,0), custom_font=None, line_spacing=10):
        if "\n" in text:
            text = text.split("\n")
            for i, line in enumerate(text):
                y_pos = pos[1]+((size+line_spacing)*i)
                line, text_rect = self.gen_text(text=line, size=size, pos=(pos[0], y_pos ), color=color, custom_font=custom_font)
                self.DISPLAYSURF.blit(line, text_rect)
        else:
            text, text_rect = self.gen_text(text=text, size=size, pos=pos, color=color, custom_font=custom_font)
            self.DISPLAYSURF.blit(text, text_rect)
    
    def load_background_coords(self, use_center=True) -> None:
        """
        Loads the background coordinates

            Parameters:
                `use_center` (bool): Default is True. Declares whether to center background or not
        """
    
        self.background_coords = (0,0)
        if self.background is not None:
            bg_x = self.background.get_width()
            bg_y = self.background.get_height()

            cbg_x = bg_x // 2
            cbg_y = bg_y // 2
            
            if use_center: 
                coords = ((self.cx-cbg_x),(self.cy-cbg_y))   
                self.background_coords = coords
    # ==========================================
    # Brainflow methods

    def perform_preflight(self, board, serial_port=''):

        self.DISPLAYSURF.blit(pygame.image.load(os.path.join(DIRNAME, f"assets//bg_large.png")), self.background_coords)
        self.display_text("Connecting. Please Hold..", size=30, pos=(self.cx, self.cy))
        pygame.display.update()

        self.prep_brainflow()
        print("Brainflow prepped")

        if board==38:
            self.connect_muse()
        elif board==0:
            if serial_port != '':
                self.connect_cyton(serial_port=serial_port)
            else:
                raise TypeError("Expected Serial Port, but got '' ")

        print(f"Board {board} connected")
        self.DISPLAYSURF.blit(pygame.image.load(os.path.join(DIRNAME, f"assets//bg_large.png")), self.background_coords)
        self.display_text("Connected", size=30, pos=(self.cx, self.cy))
        pygame.display.update()
        time.sleep(1)

        try:
            self.prep_ml()
        except:
            self.concentration.release_all()
            self.prep_ml()

        print("ML Prep completed")
        self.start_stream()
        print("Successfully streaming")

    def prep_brainflow(self):
        BoardShim.enable_board_logger ()
        DataFilter.enable_data_logger ()
        MLModel.enable_ml_logger ()
        self.EEG_WIN_SIZE = 5

    def end_session(self):
        if self.connected:
            self.board.stop_stream()
            self.board.release_session()
            time.sleep(1)
            self.board.release_all_sessions()
            time.sleep(1)

    def mod_ESC_behavior(self, function):
        # self.training_main_menu.modify_ESC_behavior(function=function)
        self.primary_menu_call = function

    def connect_muse(self):
        params = BrainFlowInputParams ()
        self.DISPLAYSURF.blit(pygame.image.load(os.path.join(DIRNAME, f"assets//bg_large.png")), self.background_coords)

        self.display_text("Attempting Connection...", size=30, pos=(self.cx, 350))
        pygame.display.update()


        try:
            self.board = BoardShim(BoardIds.MUSE_2_BOARD.value, params)
            self.master_board_id = self.board.get_board_id ()
            self.sampling_rate = BoardShim.get_sampling_rate (self.master_board_id)
            try:
                self.board.prepare_session ()
            except:
                self.board.release_all_sessions()
                self.board.prepare_session()
            print("connected successfully")
            self.connected = True
            time.sleep(1)
            self.DISPLAYSURF.blit(pygame.image.load(os.path.join(DIRNAME, f"assets//bg_large.png")), self.background_coords)
            self.display_text("Connected to MUSE", size=30, pos=(self.cx, 350))
            pygame.display.update()


        except:
            self.DISPLAYSURF.blit(pygame.image.load(os.path.join(DIRNAME, f"assets//bg_large.png")), self.background_coords)
            print("Failed to find muse...")
            self.display_text("Couldnt find any boards. Exiting...", size=30, pos=(self.cx, 350))
            self.board.release_all_sessions()
            pygame.display.update()
            time.sleep(2)
            if self.primary_menu_call is not None: self.primary_menu_call()
            else:
                pygame.quit()
                sys.exit()

    def connect_cyton(self, serial_port="COM4"):
        params = BrainFlowInputParams ()
        params.serial_port = serial_port # get some way to specify this

        self.board = BoardShim(BoardIds.CYTON_BOARD.value, params)
        self.master_board_id = self.board.get_board_id ()
        self.sampling_rate = BoardShim.get_sampling_rate (self.master_board_id)
        self.board.prepare_session()
        self.connected = True

        self.DISPLAYSURF.blit(pygame.image.load(os.path.join(DIRNAME, f"assets//bg.png")), self.background_coords)
        self.display_text("Connected to CYTON", size=30, pos=(self.cx, self.cy))
        pygame.display.update()

    def prep_ml(self):
        print("\nPrepping ML...\n")
        # calc concentration
        concentration_params = BrainFlowModelParams (BrainFlowMetrics.CONCENTRATION.value, BrainFlowClassifiers.REGRESSION.value)
        self.concentration = MLModel(concentration_params)
        self.concentration.prepare()
        self.ml_prepped = True
        print("\nML Prepped\n")
    
    def start_stream(self):
        self.board.start_stream (45000, '')
        self.streaming = True
        BoardShim.log_message (LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')
        if not self.ml_prepped:
            self.prep_ml()
        self.DISPLAYSURF.blit(pygame.image.load(os.path.join(DIRNAME, f"assets//bg_large.png")), self.background_coords)
        self.display_text("STREAM STARTED. WELCOME.", size=30, pos=(self.cx, 300))
        pygame.display.update()
        time.sleep(2)
        self.DISPLAYSURF.blit(pygame.image.load(os.path.join(DIRNAME, f"assets//bg.png")), self.background_coords)
        self.display_text("PLEASE ALLOW ANOTHER FEW SECONDS FOR THE RINGBUFFER TO FILL", size=10, pos=(self.cx, 300))
        pygame.display.update()
        time.sleep(2)

    

    def board_connected(self):
        return self.connected
        # draws out the window with center and side lines
    
    def get_current_data(self, seconds):
        data = self.board.get_current_board_data(self.sampling_rate*seconds)
        return data

    def get_focus_val(self):
        assert self.ml_prepped
        current_data = self.get_current_data(self.EEG_WIN_SIZE)
        eeg_channels = BoardShim.get_eeg_channels (int (self.master_board_id))
        bands = DataFilter.get_avg_band_powers (current_data, eeg_channels, self.sampling_rate, True)
        feature_vector = np.concatenate ((bands[0], bands[1]))

        prediction = self.concentration.predict (feature_vector)
        print ('Concentration: %f' % prediction)
        return prediction

    # ========================================================================================================


    def draw_board(self):
        self.DISPLAYSURF.fill(BLACK) # fill screen with black
        self.DISPLAYSURF.blit(self.bg, self.background_coords)

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
                

    def esp_ball(self, dir):

        # if int(round(time.time())) % int(15) == 0:  # Only read 15 times a minutes, every 4 seconds
        focus_val = self.get_focus_val()
        print(f"Focus Val: {focus_val}")

        if dir==-1: self.SPEED = self.default_speed

        if focus_val >= self.FOCUS_THRES:
            self.SPEED = self.default_speed*2
            self.INFLUENCED = True
        else:
            self.INFLUENCED = False


        


    def play(self):

        assert self.connected
        assert self.ml_prepped
        assert self.streaming

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

        

        # pygame.mouse.set_visible(0) # cursor gone

        key = 0 # determines keyboard input

        while True: # game loop
            

            MOUSE_POS = pygame.mouse.get_pos()

            
                
            self.esp_ball(dir_x)

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
                display_rect.center = (self.cx, self.cy) # position rect
                self.DISPLAYSURF.blit(display_text, display_rect)
            

            self.display_text("THRES", pos=(self.cx, self.WIN_H-70), size=20)

            UP = Button(image=None, pos=(self.cx-100, self.WIN_H-30), 
                                text_input="▲", font=self.get_font(30), base_color="#d7fcd4", hovering_color="#b68f40")

            self.display_text(f"{round(self.FOCUS_THRES,2)}", pos=(self.cx, self.WIN_H-30))

            DOWN = Button(image=None, pos=(self.cx+100, self.WIN_H-30), 
                                text_input="▼", font=self.get_font(30), base_color="#d7fcd4", hovering_color="#b68f40")

            for button in [UP, DOWN]:
                button.changeColor(MOUSE_POS)
                button.update(self.DISPLAYSURF)

            for event in pygame.event.get():
                if event.type == QUIT: # quitting the game
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN: # pressed key 
                    if event.key == pygame.K_ESCAPE: 
                        
                        self.end_session()

                        if self.primary_menu_call is not None: self.primary_menu_call()
                        else:
                            pygame.quit()
                            sys.exit()
                    key = self.keydown_paddle(event)
                if event.type == KEYUP: # lifted key
                    key = 0
                    self.SPEED = self.default_speed
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if UP.checkForInput(MOUSE_POS):
                        self.FOCUS_THRES += 0.1
                    if DOWN.checkForInput(MOUSE_POS):
                        self.FOCUS_THRES -= 0.1

            pygame.display.update() # refresh screen
            self.FPSCLOCK.tick(self.FPS) # set framerate



if __name__ == "__main__":
    
    MUSE_ID = 38

    pygame.init()
    display = pygame.display.set_mode((600, 600))
    p = ESPPong(display)

    p.perform_preflight(board=MUSE_ID)

    p.play()