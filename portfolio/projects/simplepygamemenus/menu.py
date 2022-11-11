"""
SIMPLE PYGAME MENU

A python package for simplifying the process of importing your pygame menus

Some Rules:

    - Make the main menu first!
    - If you want to be able to switch back to the previous menu, set the main parameter in Menu() to the previous menu

"""
from button import Button
import os
import pygame
import sys

DIRNAME = os.path.dirname(__file__)

def get_font(size, font_path=None): # Returns Press-Start-2P in the desired size
    if font_path is not None: return pygame.font.Font(os.path.join(DIRNAME, font_path), size)
    else: return pygame.font.Font(os.path.join(DIRNAME, "font.ttf"), size)

class Menu:
    """
    A constructor for menus
    """
    
    def __init__(self, caption="A Simple Pygame Menu", title="MENU", world:pygame.Surface=None, background=None, displaytitle=True, main=None, showESCKEYhint=True):
        """
        Parameters:
            caption            (str):
            title              (str):
            world   (pygame.Surface): The pygame surface object
            background         (str): The local path to a background file
            displaytitle      (bool): Display the title?
            main              (Menu): Add a main menu to return to with escape
        """
        self.caption         = caption
        self.title           = title
        self.buttons         = []
        self.text_to_display = []
        
        if world is not None:
            self.SCREEN = world
            self.load_win_dimensions(world.get_width(),world.get_height())
        else:
            self.load_win_dimensions(500,500)
            if background is not None: background_path = os.path.join(DIRNAME, background)
            else: background_path=None
            self.prepSCREEN(background_filepath=background_path)
        self.add_text(text=self.title, x=self.center_win_width, y=80, size=30, color=(255,255,255))

        if main is not None:
            if not isinstance(main, self.__class__): raise ValueError("Main Menu must be instance of Menu object")
            self.main = main
            if showESCKEYhint: self.add_text(text="Press ESC to return to the previous menu", x=self.center_win_width, y=10, size=10, color=(255,255,255))
        else: self.main = None
                
    def load_win_dimensions(self, x, y):
        """
        Given an x, y input - load them as the instance variables for window height and width
        """
        self.win_height = y # y
        self.win_width  = x  # x
        self.center_win_height = y // 2
        self.center_win_width  = x // 2

    def default_func(self):
        print("[DEFAULT FUNC] I should do something")

    def add_button(self, label="button", function=None, x=0, y=0, font=None, fontsize=30, basecolor=(0,0,255), hovercolor=(255,255,0)):
        if function is None: function = self.default_func
        if font is None: font = get_font(fontsize)
        img = pygame.image.load(os.path.join(DIRNAME, "rect.png"))
        b = Button(image=img, pos=(x,y), text_input=label, font=font, base_color=basecolor, hovering_color=hovercolor)
        self.buttons.append((b, function))

    def add_text(self, text="fortnite", x=0, y=0, size=45, color="#b68f40"):
        """
        Add text to render for the menu
        """
        display = (text, (x,y), size, color)
        self.text_to_display.append(display)
    
    def prepSCREEN(self, background_filepath=None):
        """
        Runs the portfolio
        """
        pygame.init()
        self.SCREEN = pygame.display.set_mode((self.win_width, self.win_height))
        self.background = pygame.image.load(os.path.join(DIRNAME, background_filepath)) if background_filepath is not None else None  

    def run_menu(self):
        """
        Runs the menu as a loop

            Parameters:
                world (pygame.Surface): The world/screen you import
        """
        
        while True:
            pygame.display.set_caption(self.caption)
            self.render_background()
            self.render_display_texts()

            MOUSEPOS = pygame.mouse.get_pos()

            self.render_buttons(MOUSEPOS=MOUSEPOS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        if self.main is None: 
                            pygame.quit()
                            sys.exit()
                        else:
                            self.main.run_menu()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Handle button press
                    for button_set in self.buttons:
                        button = button_set[0]
                        func  = button_set[1]
                        if button.checkForInput(MOUSEPOS):
                            func()
            pygame.display.update() # ESSENTIAL FOR CHANING MENUS!


    def render_background(self):
        if self.background is not None:
            self.SCREEN.fill("black")
            self.SCREEN.blit(self.background, self.background_coords)
        else:
            self.SCREEN.fill("black")

    def render_buttons(self, MOUSEPOS=None):
        if MOUSEPOS is None: raise ValueError("MOUSEPOS cannot be None")
        assert self.SCREEN is not None
        for button_set in self.buttons:
            button = button_set[0]
            button.changeColor(MOUSEPOS)
            button.update(self.SCREEN)

    def render_display_texts(self):
        assert self.SCREEN is not None
        for text_set in self.text_to_display:
            text, pos, size, color = text_set
            self.display_text(text=text, size=size, pos=pos, color=color, custom_font=None)

    def load_background(self, use_center=True):
        
        self.background_coords = (0,0)
        if self.background is not None:
            bg_x = self.background.get_width()
            bg_y = self.background.get_height()

            cbg_x = bg_x // 2
            cbg_y = bg_y // 2
            
            if use_center: 
                coords = ((self.center_win_width-cbg_x),(self.center_win_height-cbg_y))   
                self.background_coords = coords

    def gen_text(self, text="", size=45, color="#b68f40", pos=(0,0), custom_font=None):
        TEXT = get_font(size=size, font_path=custom_font).render(text, True, color)
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

    def go_back(self):
        if self.main is not None: 
            self.main.run_menu()

if __name__ == "__main__":

    main = Menu()
    main.add_text(text="TEST", x=250, y=20, size=30)
    b_menu = Menu(main=main, title="other menu", showESCKEYhint=True)
    main.add_button(label="Fortnite", x=250, y=250, fontsize=30, function=b_menu.run_menu)
    b_menu.add_button(label="exit", x=250, y=250, fontsize=30, function=sys.exit)

    next_menu = Menu(title="NEXT",main=b_menu)
    b_menu.add_button(label="next menu", x=250, y=400, fontsize=30, basecolor=(0,255,0), hovercolor=(255,255,255), function=next_menu.run_menu)

    
    main.run_menu()

    

