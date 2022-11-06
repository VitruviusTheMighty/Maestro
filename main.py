"""
Leonardo Ferrisi 23'
"""

import pygame
import os
import sys
from assets.button import Button
# Import all other loops here. 
# TODO: EVERY game should have a loop that can be imported

DIRNAME = os.path.dirname(__file__)

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font(os.path.join(DIRNAME, "assets/font.ttf"), size)

class Porfolio:
    """
    A central executable for running all games made in CSC 245
    """

    def __init__(self, width, height):
        
        self.load_win_dimensions(width, height)

        self.prep_portfolio()

    def load_win_dimensions(self, x, y):
        """
        Given an x, y input - load them as the instance variables for window height and width
        """
        self.win_height = y # y
        self.win_width  = x  # x
        self.center_win_height = y // 2
        self.center_win_width  = x // 2

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
            self.SCREEN.blit(self.background, self.bg_coords)
        else:
            self.SCREEN.fill("black")

    def gen_text(self, text="", size=45, color="#b68f40", pos=(0,0)):
        TEXT = get_font(size=size).render(text, True, color)
        TEXT_RECT = TEXT.get_rect(center=pos)
        return TEXT, TEXT_RECT

    def display_text(self, text="", size=45, color="#b68f40", pos=(0,0)):
        text, text_rect = self.gen_text(text=text, size=size, pos=pos, color=color)
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
        self.load_background(use_center=True)

        while True:
            pygame.display.set_caption("Portfolio - Main Menu")
            self.render_background()

            MOUSE_POS = pygame.mouse.get_pos()

            GAME_SELECT = Button(image=pygame.image.load(os.path.join(DIRNAME, "assets//Play Rect.png")), pos=(self.center_win_width, 250), 
                                text_input="GAME SELECT", font=get_font(30), base_color="#d7fcd4", hovering_color="#b68f40")


            self.display_text(text="Portfolio", size=50, pos=(self.center_win_width,100))

            for button in [GAME_SELECT]:
                button.changeColor(MOUSE_POS)
                button.update(self.SCREEN)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if GAME_SELECT.checkForInput(MOUSE_POS):
                        # self.playgame()
                        # TODO: Do a thing
                        pass
                    # if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    #     self.options()
                    # if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    #     pygame.quit()
                        # sys.exit()
            pygame.display.update()


            

    def switch_screen(self):
        pass

if __name__ == "__main__":

    p = Porfolio(1280, 1080)
    p.portfolio_loop()