from pickle import FALSE
import pygame
import os

DIRNAME = os.path.dirname(__file__)

try:
    from box import Box
    from player import Player
    from vector import Vector
except ModuleNotFoundError:
    try:
        from joust.box import Box
        from joust.player import Player
        from joust.vector import Vector
    except:
        from games.joust.box import Box
        from games.joust.player import Player
        from games.joust.vector import Vector

    # raise ImportError("Failed to import packages")




class Game:

    def __init__(self, width=1200, height=800, world:pygame.Surface=None):
            pygame.init()

            # Instance VARS
            self.HEIGHT = height
            self.WIDTH = width

            self.player_speed = 15

            self.boxes     = []
            self.platforms = pygame.sprite.Group()

            self.world = world

            self.menu = None

            self.background = None

    def handle_collisions(self, player:Player):
        
        
        hits = pygame.sprite.spritecollide(player , self.platforms, False)

        if hits:
            for box in self.boxes:
                collides = pygame.sprite.collide_mask(player, box)
                # print(f"collides? {collides}")
                if player.v.y > 0:
                    if collides:
                        if not player.onPlatform:  # TODO: Reimplement such that onPlatform is specific to box
                            player.v.y = 0
                            player.onPlatform = True
                        player.pos.y = box.rect.y - player.rect.h + 1 # keep them colliding

        else:
            player.onPlatform = False

    def handle_keypress_events(self, event:pygame.event.Event, player:Player):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.go_left()
            if event.key == pygame.K_RIGHT:
                player.go_right()
    
            if event.key == pygame.K_ESCAPE:
                if self.menu != None:
                    self.menu()
                else:
                    pygame.quit()

            if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                # player jump
                player.jump()

                

            if event.key == pygame.K_DOWN:
                # player down
                pass

        if event.type == pygame.KEYUP:
            player.stop_x()

    def addbox(self, color, size:Vector, pos:Vector):
        
        b = Box(color, size.y, size.x, pos.x, pos.y)
        # b.v.x = -1
        self.platforms.add(b)
        self.boxes.append(b)

    def load_game_select(self, menu_select_func):

        self.menu = menu_select_func

    def load_background(self, background_path="couch_background.png"):
        
        self.background = pygame.image.load(background_path)

    def run(self):

        if self.world == None:

            Game_size = [self.WIDTH, self.HEIGHT]
            Game_screen = pygame.display.set_mode(Game_size)
            pygame.display.set_caption("SALTO!")
        else:
            Game_screen = self.world
            pygame.display.set_caption("SALTO!")


        # Create sprites
        active_sprite_list = pygame.sprite.Group()
        player = Player(Game_screen)
        player.set_speed(self.player_speed)

        self.addbox('red', Vector(90, 20), Vector(500 ,750))
        self.addbox('blue', Vector(90, 20), Vector(850 ,650))
        self.addbox('green', Vector(90, 20), Vector(350 ,550))



        active_sprite_list.add(player)

        for box in self.boxes:
            active_sprite_list.add(box)


        ACTIVE = True
        clock = pygame.time.Clock()

        while ACTIVE:

            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    ACTIVE = False # Flag that we are done so we exit this loop

                
                self.handle_keypress_events(event, player)

            # handle collisions
            self.handle_collisions(player)
            
            # print(player.pos.y)

            active_sprite_list.update() # update

            
            if self.background != None: Game_screen.blit(self.background, (0,0))  
            else: Game_screen.fill(pygame.color.Color("gray14")) 

            active_sprite_list.draw(Game_screen)

            clock.tick(30)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    g = Game(width=1400, height=900)
    g.load_background(os.path.join(DIRNAME,"couch_background2.png"))
    g.run()
