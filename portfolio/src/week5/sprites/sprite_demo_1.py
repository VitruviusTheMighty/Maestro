"""

Author: John Rieffel

Based off of 

Simpson College Computer Science Material

Game art from Kenney.nl:
http://opengameart.org/content/platformer-art-deluxe

"""

import pygame

from player import Player
from simple_platform import Box

class Game:

    def __init__(self, width=1200, height=480):
        pygame.init()

        # Instance VARS
        self.HEIGHT = height
        self.WIDTH = width

        # Generate SPRITES


    def handle_collisions(self, player:Player, obj1:pygame.sprite.Sprite):
        collision = pygame.sprite.collide_mask(player,obj1)
        player.is_above(obj1)

        if collision:
            player.is_colliding = True
            # print(collision)
            if collision[1] > player.size.y - 11:
                print(f"Collision y: {player.size.y - 11}")
                player.floor = self.HEIGHT - obj1.rect.h 
            else: 
                if not player.above_ground():
                    # player.floor = HEIGHT
                    player.stop(x=True, y=False)
        else:
            player.is_colliding = False
            player.floor = self.HEIGHT


    def handle_key_events(self, event:pygame.event.Event, player:Player):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.go_left()
            if event.key == pygame.K_RIGHT:
                player.go_right()
            if event.key == pygame.K_ESCAPE:
                pygame.quit()

            if event.key == pygame.K_UP:
                if player.at_ground():
                    player.jump()
                else:
                    player.descend()
            if event.key == pygame.K_DOWN:
                if not player.below_ground():
                    player.descend()

            if player.above_ground() and player.above_jump_height():
                player.descend()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT: 
                player.stop()
            if event.key == pygame.K_RIGHT:
                player.stop()
            
            if player.above_ground():
                if not player.falling: 
                    player.descend()
                    player.falling = True

    def run(self):
        size = [self.WIDTH, self.HEIGHT]
        screen = pygame.display.set_mode(size)

        pygame.display.set_caption("demo with sprite sheets")

        active_sprite_list = pygame.sprite.Group()
        # Create the player
        player = Player(screen)
        platform = Box(pygame.color.Color("blue"),50,50) 
        platform.rect.x = 400
        platform.rect.y = self.HEIGHT - platform.rect.h

        # Create all the levels

        player.rect.x = 100 
        player.rect.y = self.HEIGHT - player.rect.height
        active_sprite_list.add(player,platform)

        #Loop until the user clicks the close button.
        done = False

        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()

        # -------- Main Program Loop -----------
        while not done:

            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    done = True # Flag that we are done so we exit this loop

                self.handle_key_events(event, player)

            # Update the player.
            active_sprite_list.update()

            self.handle_collisions(player, platform)

            # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
            #current_level.draw(screen)
            screen.fill(pygame.color.Color("gray14")) 
            active_sprite_list.draw(screen)

            # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

            clock.tick(120)

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    
    g = Game()
    g.run()
