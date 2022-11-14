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

from simplepygamemenus.menu import Menu, Button

DIRNAME = os.path.dirname(__file__)

class PsychicTraining:

    def __init__(self, display:pygame.Surface, threshold=0.8):
        
        pygame.init()
        self.SCREEN = display
        self.width  = self.SCREEN.get_width()
        self.height = self.SCREEN.get_height()
        self.cx     = self.width // 2
        self.cy     = self.height // 2

        # self.connected = False

        # self.connect_muse(doExitBehavior=False)

        # FPS
        self.FPS = 60
        self.FPSCLOCK = pygame.time.Clock() # for custom frame rate

        # Background
        self.background = pygame.image.load(os.path.join(DIRNAME, "assets//bg_large.png")) 
        self.load_background_coords(use_center=True)

        self.primary_menu_call = None

        # Text
        self.FONTSIZE = 45
        self.FONT = pygame.font.Font(os.path.join(DIRNAME, "assets/font.ttf"), self.FONTSIZE)
        
        # other
        self.crux_val = 1.0

        # Brainflow
        self.THRESHOLD = threshold
        self.streaming = False
        self.ml_prepped = False
        self.connected  = False

        self.create_TRAINING_MENU()


    # Text Methods ===================================

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
                self.SCREEN.blit(line, text_rect)
        else:
            text, text_rect = self.gen_text(text=text, size=size, pos=pos, color=color, custom_font=custom_font)
            self.SCREEN.blit(text, text_rect)

    # Brainflow Methods ==============================

    def perform_preflight(self, board, serial_port=''):

        self.SCREEN.blit(pygame.image.load(os.path.join(DIRNAME, f"assets//bg_large.png")), (0,0))
        self.display_text("Connecting. Please Hold..", size=10, pos=(self.cx, 350))
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
            self.board.release_all_sessions()
            self.concentration.release_all()

    def minimal_muse_connect(self):
        BoardShim.enable_board_logger ()
        DataFilter.enable_data_logger ()
        MLModel.enable_ml_logger ()
        self.EEG_WIN_SIZE = 5
        params = BrainFlowInputParams ()
        params.serial_port = 'COM3'
        try:
            self.board = BoardShim(22, params)
            self.master_board_id = self.board.get_board_id ()
            self.sampling_rate = BoardShim.get_sampling_rate (22)
            self.board.prepare_session()
            print("connected")
            self.connected = True
        except:
            self.board.release_all_sessions()
            print("EXITING")        
            pygame.quit()
            sys.exit()

    def connect_muse(self, doExitBehavior=False):

        self.prep_brainflow()
        print("brainflow prepped")

        params = BrainFlowInputParams ()
        self.SCREEN.blit(pygame.image.load(os.path.join(DIRNAME, f"assets//bg_large.png")), (0,0))

        self.display_text("Attempting Connection...", size=30, pos=(self.cx, 350))
        pygame.display.update()

        if not self.connected:
            try:
                self.board = BoardShim(38, params)
                self.master_board_id = self.board.get_board_id ()
                self.sampling_rate = BoardShim.get_sampling_rate (38)
                try:
                    self.board.prepare_session ()
                except:
                    self.board.release_all_sessions()
                    self.board.prepare_session()

                self.connected = True
                self.SCREEN.blit(pygame.image.load(os.path.join(DIRNAME, f"assets//bg_large.png")), (0,0))
                self.display_text("Connected to MUSE", size=30, pos=(self.cx, 350))
                pygame.display.update()
            except:
                self.SCREEN.blit(pygame.image.load(os.path.join(DIRNAME, f"assets//bg_large.png")), (0,0))
                self.display_text("Couldnt find any boards. Exiting...", size=30, pos=(self.cx, 350))
                self.board.release_all_sessions()
                pygame.display.update()
                time.sleep(2)
                print("EXITING")
                if not doExitBehavior:
                    if self.primary_menu_call is not None: self.primary_menu_call()
                    else:
                        pygame.quit()
                        sys.exit()
            try:
                self.prep_ml()
            except:
                self.concentration.release_all()
                self.prep_ml()
            print("ML Prep completed")

            self.start_stream()
            print("Successfully streaming")
        else:
            self.SCREEN.blit(pygame.image.load(os.path.join(DIRNAME, f"assets//bg_large.png")), (0,0))
            self.display_text("Connected to MUSE", size=30, pos=(self.cx, 350))
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
        self.SCREEN.blit(pygame.image.load(os.path.join(DIRNAME, f"assets//bg_large.png")), (0,0))
        self.display_text("STREAM STARTED. WELCOME.", size=30, pos=(self.cx, 300))
        pygame.display.update()
        time.sleep(2)
        self.SCREEN.blit(pygame.image.load(os.path.join(DIRNAME, f"assets//bg_large.png")), (0,0))
        self.display_text("PLEASE ALLOW ANOTHER FEW SECONDS FOR THE RINGBUFFER TO FILL", size=15, pos=(self.cx, 300))
        pygame.display.update()
        time.sleep(2)
    
    def is_board_connected(self):
        return self.connected
    
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

    def create_TRAINING_MENU(self):
        
        self.training_main_menu = Menu(caption="Cognition and Telepathy Retrieval Learning Program", world=self.SCREEN, background=os.path.join(DIRNAME, "assets//bg_large.png"), displaytitle=False)

        self.training_main_menu.add_text(text="TRAIN", x=self.cx, y=150)
        
        if not self.connected:

            def run_muse_then_play():
                self.connect_muse()
                # self.minimal_muse_connect()
                self.run_psychic_training()

            self.training_main_menu.add_button("Connect MUSE", x=self.cx, y=self.cy-200, function=run_muse_then_play, basecolor=(255,255,255), hovercolor=(182,143, 64))

        else:
            self.training_main_menu.add_button("PLAY", x=self.cx, y=250, function=self.run_psychic_training, basecolor=(255,255,255), hovercolor=(182,143, 64))

        self.training_main_menu.add_button(label="TESTRUN", function=self.run_psychic_training, x=self.cx, y=self.cy, basecolor=(255,255,255), hovercolor=(182,143, 64))


    def run_TRAINGING_MENU(self):

        self.training_main_menu.run_menu()
        

    def mod_ESC_behavior(self, function):
        self.training_main_menu.modify_ESC_behavior(function=function)
        self.primary_menu_call = function

    def draw_background(self):
        
        # draw background
        self.SCREEN.fill((0,0,0))
        self.SCREEN.blit(self.background, self.background_coords)

    def draw_UI(self, value):
        """
        Value (float): A value between 0 and 1 that determines the intensity of a color
        """
        # assert self.ml_prepped
        
        if value > 1.0: raise ValueError("value should not be greater than max value 1.0")

        stimuli_color = (255, 255, 255*(1.0 - value))

        
        # draw stimuli
        a,b,c = (self.cx-200,self.cy+150), (self.cx, self.cy-200), (self.cx+200,self.cy+150)
        pygame.draw.polygon(surface=self.SCREEN, color=stimuli_color, points=[a,b,c])

    def raise_threshold(self):
        if self.THRESHOLD < 1.0:
            self.THRESHOLD += 0.1
    
    def lower_threshold(self):
        if self.THRESHOLD > 0.0:
            self.THRESHOLD -= 0.1

    def render_concentration_metric(self, value):

        if value >= self.THRESHOLD:
            self.display_text("MENTAL ENERGY ACKNOWLEDGED", pos=(self.cx, self.height - 100))
        else:
            self.display_text("[ + ]", pos=(self.cx, self.height - 100))

        if self.crux_val > 0.0:
            self.display_text("+", pos=(self.cx,self.cy+10), color=(0,0,0))
        else:
            self.display_text("+", pos=(self.cx,self.cy+10), color=(255,255,255))
        
    

    def render_texts(self):
        
        self.display_text("CTRL\nCognition and Telepathy Retrieval Learning", size=30, pos=(self.cx, 80))



    def run_psychic_training(self):
        #TODO: Add some checkers here
        # assert self.connected
        # assert self.ml_prepped
        # assert self.streaming

        self.alive = True

        concentration_prediction = 0.0
        self.draw_background()
        pygame.display.update() # refresh screen

        self.draw_UI(value=concentration_prediction)
        pygame.display.update() # refresh screen



        start_time = time.time()

        wait_time = 1.0

        while self.alive:
            
            # concentration_prediction = self.get_focus_val()
            MOUSE_POS = pygame.mouse.get_pos()

            self.draw_background()
            self.render_texts()

            if (time.time() - start_time) > wait_time:
                # concentration_prediction = random.uniform(0.0,1.0)

                # print(f"Running at {time.time() - start_time}")
                print(f"Concentration: {concentration_prediction}")

                if not self.connected:
                    concentration_prediction = random.uniform(0.0,1.0)
                else:
                    concentration_prediction = self.get_focus_val()

                self.crux_val *= -1

                start_time = time.time()

            self.draw_UI(value=concentration_prediction)
            


            self.render_concentration_metric(concentration_prediction)

            self.display_text("THRES", pos=(110, self.cy-200), size=20)

            UP = Button(image=None, pos=(110, self.cy-100), 
                                text_input="▲", font=self.get_font(30), base_color="#d7fcd4", hovering_color="#b68f40")

            self.display_text(f"{round(self.THRESHOLD,2)}", pos=(110, self.cy))

            DOWN = Button(image=None, pos=(110, self.cy+100), 
                                text_input="▼", font=self.get_font(30), base_color="#d7fcd4", hovering_color="#b68f40")

            for button in [UP, DOWN]:
                button.changeColor(MOUSE_POS)
                button.update(self.SCREEN)

            for event in pygame.event.get():
                if event.type == QUIT: # quitting the game
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:

                        if self.connected: self.end_session()

                        self.run_TRAINGING_MENU()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if UP.checkForInput(MOUSE_POS):
                        self.raise_threshold()
                    if DOWN.checkForInput(MOUSE_POS):
                        self.lower_threshold()

            pygame.display.update() # refresh screen
            self.FPSCLOCK.tick(self.FPS) # set framerate


if __name__ == "__main__":
    screen = pygame.display.set_mode((1400,900))
    p = PsychicTraining(display=screen)
    # p.run_psychic_training()
    p.run_TRAINGING_MENU()
    # BoardShim.enable_board_logger ()
    # DataFilter.enable_data_logger ()
    # MLModel.enable_ml_logger ()
    # # self.EEG_WIN_SIZE = 5
    # params = BrainFlowInputParams ()
    # try:
    #     board = BoardShim(38, params)
    #     master_board_id = board.get_board_id ()
    #     sampling_rate = BoardShim.get_sampling_rate (38)
    #     board.prepare_session()
    #     connected = True
    # except:
    #     board.release_all_sessions()
    #     print("EXITING")        
    #     pygame.quit()
    #     sys.exit()

