# A test in creating title screens

# To use multiple title screens in a game, use multiple game loop

import pygame
import sys
import os
import brainflow
import time
from pygame import mixer

try:
    from pong import Pong
    from button import Button
    from espr import ESPPong
    from train import PsychicTraining
except ModuleNotFoundError:
    try:
        from ctrl.pong import Pong
        from ctrl.button import Button
        from ctrl.espr import ESPPong
        from ctrl.train import PsychicTraining
    except:
        from games.ctrl.pong import Pong
        from games.ctrl.button import Button
        from games.ctrl.espr import ESPPong
        from games.ctrl.train import PsychicTraining

from simplepygamemenus.menu import Menu

DIRNAME = os.path.dirname(__file__)

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font(os.path.join(DIRNAME, "assets/font.ttf"), size)

class Game:

    def __init__(self, width=1400, height=900, world=None):

        pygame.init()
        mixer.init()

        if not world:
            self.SCREEN = pygame.display.set_mode((width, height))
            self.width  = width
            self.height = height
            self.cx = width // 2
            self.cy = height // 2
        else:
            self.SCREEN = world
            self.width  = world.get_width()
            self.height = world.get_height()
            self.cx     = self.width // 2
            self.cy     = self.height // 2

        bg_path = os.path.join(DIRNAME, f"assets//bg_large.png")
        self.background_path = bg_path
        self.MENUBG = pygame.image.load(bg_path)

        # self.optionsbg = pygame.image.load(os.path.join(DIRNAME, f"assets//options.png"))
        self.optionsbg = self.MENUBG


        pygame_icon = pygame.image.load(os.path.join(DIRNAME, "assets//icon.png"))
        pygame.display.set_icon(pygame_icon)

        self.vol_on = False

        # self.start_audio()

        # self.mainmenu = None

        self.primarymenu = None

        self.create_menus()

    def start_audio(self):
        mixer.music.load(os.path.join(DIRNAME, "assets//ost.mp3"))
        self.audio_toggle()
    
    

    def create_menus(self):

        # Main Menu
        self.variant_main_menu = Menu(caption="CTRL", world=self.SCREEN, background=self.background_path, displaytitle=False)
        self.variant_main_menu.add_text(text="CTRL", x=self.cx, y=100, size=70)

        # Options Menu
        self.variant_options_menu = Menu(caption="Options", world=self.SCREEN, background=self.background_path, main=self.variant_main_menu, displaytitle=False)
        self.variant_options_menu.add_text(text="OPTIONS", x=self.cx, y=100, size=45)
        self.variant_options_menu.add_button(label="TOGGLE AUDIO", function=self.audio_toggle, x=self.cx, y=300, fontsize=25, basecolor=(255,255,255), hovercolor=(0,255,0))
        self.variant_options_menu.add_button(label="BACK", function=self.variant_main_menu.run_menu, x=self.cx, fontsize=25, y=600, basecolor=(255,255,255), hovercolor=(0,255,0))
        

        # Game Select Menus
        self.variant_mode_select = Menu(caption="CTRL - SELECT MODE", world=self.SCREEN, background=self.background_path, main=self.variant_main_menu, displaytitle=False)
        self.variant_mode_select.add_text(text="SELECT MODE", x=self.cx, y=100, size=45)
        self.variant_mode_select.add_button(label="ESPR", function=self.train, x=self.cx, y=300, fontsize=40, basecolor=(255,255,255), hovercolor=(0,255,0))
        self.variant_mode_select.add_button(label="KEYS", function=self.playkeys, x=self.cx, fontsize=40, y=450, basecolor=(255,255,255), hovercolor=(0,255,0))
        
        self.psychicTrain = PsychicTraining(display=self.SCREEN)
        self.psychicTrain.mod_ESC_behavior(function=self.variant_main_menu.run_menu)
        self.variant_mode_select.add_button(label="TRAIN", function=self.psychicTrain.run_TRAINGING_MENU, x=self.cx, y=600, fontsize=40, basecolor=(255,255,255), hovercolor=(0,255,0) )

        self.variant_main_menu.add_button(label="PLAY", function=self.variant_mode_select.run_menu, x=self.cx, y=250, basecolor=(255,255,255), hovercolor=(182,143, 64))
        self.variant_main_menu.add_button(label="OPTIONS", function=self.variant_options_menu.run_menu, x=self.cx, y=400, basecolor=(255,255,255), hovercolor=(0,255,0))
        self.variant_main_menu.add_button(label="QUIT", function=self.quit_CTRL, x=self.cx, y=550, basecolor=(255,255,255), hovercolor=(182,143, 64))

    def audio_toggle(self):
        if self.vol_on:
            mixer.music.set_volume(0.0)
            self.vol_on = False
        else:
            mixer.music.set_volume(0.5)
            self.vol_on = True
        mixer.music.play()


    def load_game_select(self, menu_select_func):
        self.primarymenu = menu_select_func
        self.variant_main_menu.modify_ESC_behavior(function=self.primarymenu)

    def load_all_images(self):
        pass

    def switch_screen(self):
        self.SCREEN.fill("black")

    def gen_text(self, text="", size=45, color="#b68f40", pos=(0,0)):
        TEXT = get_font(size=size).render(text, True, color)
        TEXT_RECT = TEXT.get_rect(center=pos)
        return TEXT, TEXT_RECT

    def display_text(self, text="", size=45, color="#b68f40", pos=(0,0)):
        text, text_rect = self.gen_text(text=text, size=size, pos=pos, color=color)
        self.SCREEN.blit(text, text_rect)
    
    def do_intro_sequence(self):
        self.SCREEN.blit(self.MENUBG, (0,0))

    def run_training_session(self):

        pass
    
    def quit_CTRL(self):
        if self.primarymenu is not None:
            self.primarymenu()
        else:
            pygame.quit()
            sys.exit()

    def train(self):
        self.SCREEN.fill("black")

        self.SCREEN.blit(self.MENUBG, (0,0))    
        pygame.display.update()
        # display some info text
        self.display_text(text="Welcome to the CTRL Program", size=40, pos=(self.cx,350))
        pygame.display.update()
        time.sleep(3)

        self.SCREEN.blit(self.MENUBG, (0,0))    
        pygame.display.update()
        self.display_text(text="Please connect your device now", size=40, pos=(self.cx,350))
        pygame.display.update()

        time.sleep(3)

        self.connected = False

        while not self.connected:

            MOUSE_POS = pygame.mouse.get_pos()

            self.SCREEN.blit(self.MENUBG, (0,0))   
            self.display_text(text="Please connect your device now", size=30, pos=(self.cx,100))

            CONNECT_MUSE = Button(image=pygame.image.load(os.path.join(DIRNAME, "assets//Play Rect.png")), pos=(self.cx, 300), 
                                text_input="MUSE", font=get_font(30), base_color="#d7fcd4", hovering_color="#b68f40")

            # CONNECT_OBCI = Button(image=pygame.image.load(os.path.join(DIRNAME, "assets//Play Rect.png")), pos=(self.cx, 450), 
            #                     text_input="ULTRACORTEX", font=get_font(30), base_color="#d7fcd4", hovering_color="#b68f40")

            
            
            BACK = Button(image=None, pos=(self.cx, 600), text_input="BACK", font=get_font(25), base_color="Grey", hovering_color="Green")
            
            for button in [CONNECT_MUSE, BACK]:
                button.changeColor(MOUSE_POS)
                button.update(self.SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if CONNECT_MUSE.checkForInput(MOUSE_POS):
                        MUSE_ID = 38
                        p = ESPPong(self.SCREEN)
                        p.mod_ESC_behavior(function=self.variant_main_menu.run_menu)
                        p.perform_preflight(board=MUSE_ID)

                        p.play()
                    if BACK.checkForInput(MOUSE_POS):
                        self.start_ctrl()
            pygame.display.update()
    
    def playkeys(self):
        
        p = Pong(self.SCREEN)
        p.load_game_select(self.variant_mode_select.run_menu)
        p.play()

    def start_ctrl(self):
        self.variant_main_menu.run_menu()

if __name__ == "__main__":

    g = Game()
    #  g.main_menu()
    g.start_ctrl()