from pickle import FALSE
import pygame

from box import Box
from player import Player


class Game:

    def __init__(self, width=1200, height=480):
            pygame.init()

            # Instance VARS
            self.HEIGHT = height
            self.WIDTH = width

    def handle_keypress_events(self, event:pygame.event.Event, player:Player):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.go_left()
            if event.key == pygame.K_RIGHT:
                player.go_right()
    
            if event.key == pygame.K_ESCAPE:
                pygame.quit()

            if event.key == pygame.K_UP:
                # player jump
                pass
            if event.key == pygame.K_DOWN:
                # player down
                pass

        if event.type == pygame.KEYUP:
            player.stop_x()

    def run(self):
        Game_size = [self.WIDTH, self.HEIGHT]
        Game_screen = pygame.display.set_mode(Game_size)
        pygame.display.set_caption("SALTO!")

        # Create sprites
        active_sprite_list = pygame.sprite.Group()
        player = Player(Game_screen)

        active_sprite_list.add(player)

        ACTIVE = True
        clock = pygame.time.Clock()

        while ACTIVE:

            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    ACTIVE = False # Flag that we are done so we exit this loop

                self.handle_keypress_events(event, player)
            
            # handle collisions
            active_sprite_list.update() # update

            Game_screen.fill(pygame.color.Color("gray14")) 
            active_sprite_list.draw(Game_screen)

            clock.tick(30)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    g = Game()
    g.run()
