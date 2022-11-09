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
except ModuleNotFoundError:
    try:
        from ctrl.pong import Pong
        from ctrl.button import Button
        from ctrl.espr import ESPPong
    except:
        from games.ctrl.pong import Pong
        from games.ctrl.button import Button
        from games.ctrl.espr import ESPPong



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
        self.MENUBG = pygame.image.load(bg_path)

        # self.optionsbg = pygame.image.load(os.path.join(DIRNAME, f"assets//options.png"))
        self.optionsbg = self.MENUBG


        pygame_icon = pygame.image.load(os.path.join(DIRNAME, "assets//icon.png"))
        pygame.display.set_icon(pygame_icon)

        self.vol_on = False

        self.start_audio()

        # self.mainmenu = None

        self.primarymenu = None

    def start_audio(self):
        mixer.music.load(os.path.join(DIRNAME, "assets//ost.mp3"))
        self.audio_toggle()
    

    def audio_toggle(self):
        if self.vol_on:
            mixer.music.set_volume(0.0)
            self.vol_on = False
        else:
            mixer.music.set_volume(0.5)
            self.vol_on = True
        mixer.music.play()


    def load_game_select(self, menu_select_func):

        # self.mainmenu = menu_select_func
        self.primarymenu = menu_select_func

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

    def train(self):
        self.SCREEN.fill("black")

        self.SCREEN.blit(self.MENUBG, (0,0))    
        pygame.display.update()
        # display some info text
        self.display_text(text="Welcome to the CTRL Program", size=10, pos=(350,350))
        pygame.display.update()
        time.sleep(3)

        self.SCREEN.blit(self.MENUBG, (0,0))    
        pygame.display.update()
        self.display_text(text="Please connect your device now", size=10, pos=(350,350))
        pygame.display.update()

        time.sleep(3)

        self.connected = False

        while not self.connected:

            MOUSE_POS = pygame.mouse.get_pos()

            self.SCREEN.blit(self.MENUBG, (0,0))   
            self.display_text(text="Please connect your device now", size=10, pos=(350,100))

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

                        p.perform_preflight(board=MUSE_ID)

                        p.play()
                    # if CONNECT_OBCI.checkForInput(MOUSE_POS):
                    #     self.options()
                    if BACK.checkForInput(MOUSE_POS):
                        self.main_menu()
            # Show buttons
            pygame.display.update()
        # get user to connect a board
    

    def main_menu(self):

        while True:
            pygame.display.set_caption("Main Menu")

            
            self.SCREEN.blit(self.MENUBG, (0,0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            PLAY_BUTTON = Button(image=pygame.image.load(os.path.join(DIRNAME, "assets//Play Rect.png")), pos=(self.cx, 250), 
                                text_input="PLAY", font=get_font(30), base_color="#d7fcd4", hovering_color="#b68f40")

            OPTIONS_BUTTON = Button(image=pygame.image.load(os.path.join(DIRNAME, "assets/Options Rect.png")), pos=(self.cx, 400), 
                                text_input="OPTIONS", font=get_font(30), base_color="#d7fcd4", hovering_color="#b68f40")
            QUIT_BUTTON = Button(image=pygame.image.load(os.path.join(DIRNAME, "assets/Quit Rect.png")), pos=(self.cx, 550), 
                                text_input="QUIT", font=get_font(30), base_color="#d7fcd4", hovering_color="#b68f40")

            self.display_text(text="CTRL", size=70, pos=(self.cx,100))
            
            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.SCREEN)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.playgame()
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.options()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        if not self.primarymenu:
                            pygame.quit()
                            sys.exit()
                        else:
                            self.primarymenu()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.primarymenu != None:
                            self.primarymenu()
                        else:
                            pygame.quit()
                            sys.exit()

            pygame.display.update()

    def options(self):
        while True:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            self.SCREEN.fill("black")
            
            self.SCREEN.blit(self.optionsbg, (0, 0))

            self.display_text(text="OPTIONS", size=45, pos=(self.cx,100))

            AUDIOTOGGLE = Button(image=None, pos=(self.cx, 300), text_input="TOGGLE AUDIO", font=get_font(25), base_color="White", hovering_color="Green")
            OPTIONS_BACK = Button(image=None, pos=(self.cx, 600), text_input="BACK", font=get_font(25), base_color="White", hovering_color="Green")

            AUDIOTOGGLE.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)

            OPTIONS_BACK.update(self.SCREEN)
            AUDIOTOGGLE.update(self.SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        self.main_menu()
                    if AUDIOTOGGLE.checkForInput(OPTIONS_MOUSE_POS):
                        self.audio_toggle()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.main_menu()

            pygame.display.update()
    
    def playkeys(self):
        
        p = Pong(self.SCREEN)
        p.load_game_select(self.playgame)
        p.play()


    def playgame(self):
        while True:
            PLAY_MOUSE_POS = pygame.mouse.get_pos()

            self.SCREEN.fill("black")

            self.display_text(text="SELECT MODE", size=45, pos=(self.cx,100))
            BACK  = Button(image=None, pos=(self.cx, 600), text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")
            PLAY_ESPER  = Button(image=None, pos=(self.cx, 300), text_input="ESPR", font=get_font(75), base_color="White", hovering_color="Yellow")
            PLAY_ANALOG = Button(image=None, pos=(self.cx, 400), text_input="KEYS", font=get_font(75), base_color="White", hovering_color="Grey")

            PLAY_ESPER.changeColor(PLAY_MOUSE_POS)
            PLAY_ANALOG.changeColor(PLAY_MOUSE_POS)
            BACK.changeColor(PLAY_MOUSE_POS)

            PLAY_ESPER.update(self.SCREEN)
            PLAY_ANALOG.update(self.SCREEN)
            BACK.update(self.SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK.checkForInput(PLAY_MOUSE_POS):
                        self.main_menu()
                    elif PLAY_ANALOG.checkForInput(PLAY_MOUSE_POS):
                        self.playkeys()
                    elif PLAY_ESPER.checkForInput(PLAY_MOUSE_POS):
                        self.train()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.main_menu()

            pygame.display.update()

if __name__ == "__main__":

 g = Game()
 g.main_menu()