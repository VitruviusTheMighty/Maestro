"""
Leonardo Ferrisi 23'
"""

import pygame
import os
import sys
from assets.button import Button
from games.index import JOUST_GAME, BREAKOUT_GAME
# Import all other loops here. 
# TODO: EVERY game should have a loop that can be imported

DIRNAME = os.path.dirname(__file__)

def get_font(size, font_path=None): # Returns Press-Start-2P in the desired size
    if font_path!=None: return pygame.font.Font(os.path.join(DIRNAME, font_path), size)
    else: return pygame.font.Font(os.path.join(DIRNAME, "assets/font.ttf"), size)

class Porfolio:
    """
    A central executable for running all games made in CSC 245
    """

    def __init__(self, width, height, background_filepath=None, music_path=None):
        
        self.load_win_dimensions(width, height)

        self.prep_portfolio(background_filepath)

        self.load_background()
        
        self.load_music(music_path)

    def load_win_dimensions(self, x, y):
        """
        Given an x, y input - load them as the instance variables for window height and width
        """
        self.win_height = y # y
        self.win_width  = x  # x
        self.center_win_height = y // 2
        self.center_win_width  = x // 2

    def load_music(self, music_path):
        self.music_is_live = False

        if music_path != None:
            pygame.mixer.init()
            pygame.mixer.music.load(os.path.join(DIRNAME, music_path))
            pygame.mixer.music.play(loops=-1)

            self.music_is_live = True

    def toggle_music(self):
        if self.music_is_live: 
            pygame.mixer.music.set_volume(0.0)
            self.music_is_live = False
        else: 
            pygame.mixer.music.set_volume(5.0)
            self.music_is_live = True

    def load_background(self, use_center=True):
        
        if self.background != None:
            bg_x = self.background.get_width()
            bg_y = self.background.get_height()

            cbg_x = bg_x // 2
            cbg_y = bg_y // 2
            coords = (0,0) 
            if use_center: coords = ((self.center_win_width-cbg_x),(self.center_win_height-cbg_y))   
            self.bg_coords = coords

    def render_background(self):
        if self.background != None:
            self.SCREEN.fill("black")
            self.SCREEN.blit(self.background, self.bg_coords)
        else:
            self.SCREEN.fill("black")

    def gen_text(self, text="", size=45, color="#b68f40", pos=(0,0), custom_font=None):
        TEXT = get_font(size=size, font_path=custom_font).render(text, True, color)
        TEXT_RECT = TEXT.get_rect(center=pos)
        return TEXT, TEXT_RECT

    def display_text(self, text="", size=45, color="#b68f40", pos=(0,0), custom_font=None):
        text, text_rect = self.gen_text(text=text, size=size, pos=pos, color=color, custom_font=custom_font)
        self.SCREEN.blit(text, text_rect)

    def prep_portfolio(self, background_filepath=None):
        """
        Runs the portfolio
        """
        pygame.init()
        self.SCREEN = pygame.display.set_mode((self.win_width, self.win_height))
        self.background = pygame.image.load(os.path.join(DIRNAME, background_filepath)) if background_filepath!=None else None        

    def portfolio_loop(self):
        """
        Run the main portfolio loop
        """
        # self.load_background(use_center=True)
        while True:
            
            pygame.display.set_caption("Main Menu")

            self.render_background()

            self.display_text(text="LEONARDOS", size=50, color=(255,255,255), pos=(self.center_win_width,80), custom_font=r"assets\IBM-Logo.ttf")

            self.display_text(text="GAME PORTFOLIO", size=50, pos=(self.center_win_width,160))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            GAME_SELECT = Button(image=pygame.image.load(os.path.join(DIRNAME, "assets//Play Rect.png")), pos=(self.center_win_width, 350), 
                                text_input="GAME SELECT", font=get_font(30), base_color="#d7fcd4", hovering_color="#b68f40")

            OPTIONS = Button(image=pygame.image.load(os.path.join(DIRNAME, "assets//Play Rect.png")), pos=(self.center_win_width, 500), 
                                text_input="OPTIONS", font=get_font(30), base_color="#d7fcd4", hovering_color="#b68f40")

            QUIT = Button(image=pygame.image.load(os.path.join(DIRNAME, "assets//Play Rect.png")), pos=(self.center_win_width, 720), 
                                text_input="QUIT", font=get_font(30), base_color="#d7fcd4", hovering_color="#b68f40")

            for button in [GAME_SELECT, OPTIONS, QUIT]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.SCREEN)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE: 
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if GAME_SELECT.checkForInput(MENU_MOUSE_POS):
                        self.game_select_loop()
                    if OPTIONS.checkForInput(MENU_MOUSE_POS):
                        self.options_menu_loop()
                    if QUIT.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()
            pygame.display.update() # ESSENTIAL FOR CHANING MENUS!


    def game_select_loop(self):
        while True:
            pygame.display.set_caption("Portfolio - Game Select")
            self.render_background()
            self.display_text(text="GAME SELECT", size=50, pos=(self.center_win_width,50))
            self.display_text(text="Press ESC to return to Main Menu", size=10, color=(255,255,255), pos=(self.center_win_width,100))


            MOUSE_POS = pygame.mouse.get_pos()

            BREAKOUT = Button(image=pygame.image.load(os.path.join(DIRNAME, "assets//Play Rect.png")), pos=(self.center_win_width//2, 300), 
                                text_input="BREAKOUT", font=get_font(30), base_color="#d7fcd4", hovering_color="#b68f40")
            JOUST = Button(image=pygame.image.load(os.path.join(DIRNAME, "assets//Play Rect.png")), pos=(self.center_win_width//2, 450), 
                                text_input="JOUST", font=get_font(30), base_color="#d7fcd4", hovering_color="#b68f40")
            
            for button in [BREAKOUT, JOUST]:
                button.changeColor(MOUSE_POS)
                button.update(self.SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE: 
                        self.portfolio_loop()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BREAKOUT.checkForInput(MOUSE_POS):
                        # print("play breakout")
                        self.launch_breakout()
                    if JOUST.checkForInput(MOUSE_POS):
                        # print("play joust")
                        self.launch_joust()
                        
            pygame.display.update() # ESSENTIAL FOR CHANING MENUS!


    def options_menu_loop(self):
        while True:
            pygame.display.set_caption("Portfolio - Options")
            self.render_background()
            self.display_text(text="OPTIONS", size=50, pos=(self.center_win_width,50))
            self.display_text(text="Press ESC to return to Main Menu", size=10, color=(255,255,255), pos=(self.center_win_width,100))

            MOUSE_POS = pygame.mouse.get_pos()

            BACKTOMAIN = Button(image=pygame.image.load(os.path.join(DIRNAME, "assets//Play Rect.png")), pos=(self.center_win_width, 700), 
                                text_input="MAIN MENU", font=get_font(30), base_color="#d7fcd4", hovering_color="#b68f40")
            
            TOGGLE_MUSIC = Button(image=pygame.image.load(os.path.join(DIRNAME, "assets//Play Rect.png")), pos=(self.center_win_width, 350), 
                                text_input="TOGGLE MUSIC", font=get_font(30), base_color="#d7fcd4", hovering_color="#b68f40")

            for button in [TOGGLE_MUSIC, BACKTOMAIN]:
                button.changeColor(MOUSE_POS)
                button.update(self.SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE: 
                        self.portfolio_loop()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if TOGGLE_MUSIC.checkForInput(MOUSE_POS):
                        self.toggle_music()
                    if BACKTOMAIN.checkForInput(MOUSE_POS):
                        self.portfolio_loop()
            pygame.display.update() # ESSENTIAL FOR CHANING MENUS!

    def import_games(self):
        games = []
        
    def switch_screen(self):
        pass
    
    # Launch Games
    def launch_joust(self):
        j = JOUST_GAME(width=self.win_width, height=self.win_height, world=self.SCREEN) 
        j.load_game_select(menu_select_func=self.game_select_loop)
        j.run()

    def launch_breakout(self):
        b = BREAKOUT_GAME(width=self.win_width, height=self.win_height, cheats=False, multiball=False, useSquares=True, sfx=False, music=False, world=self.SCREEN)
        b.load_game_select(menu_select_func=self.game_select_loop)
        b.run()

if __name__ == "__main__":

    p = Porfolio(1400, 900, background_filepath=r"assets\neon_scanlines2.png", music_path=r"assets\Raving Energy.mp3")
    p.portfolio_loop()