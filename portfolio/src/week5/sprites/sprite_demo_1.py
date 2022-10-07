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

def handle_collisions(player:Player, obj1):
    if pygame.sprite.collide_mask(player,obj1):
        player.is_colliding = True
        print(pygame.sprite.collide_mask(player,obj1))
        if player.above_ground() and player.v.y != 0: player.stop(x=False, y=True)
        else: 
            if not player.above_ground():
                player.stop(x=True, y=False)
    else:
        player.is_colliding = False

def handle_key_events(event:pygame.event.Event, player:Player):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            player.go_left()
        if event.key == pygame.K_RIGHT:
            player.go_right()

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

def main():
    """ Main Program """
    pygame.init()

    # Set the height and width of the screen
    HEIGHT = 480
    WIDTH = 1200
    size = [WIDTH,HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("demo with sprite sheets")

    active_sprite_list = pygame.sprite.Group()
    # Create the player
    player = Player(screen)
    platform = Box(pygame.color.Color("blue"),50,50) 
    platform.rect.x = 400
    platform.rect.y = HEIGHT - platform.rect.h

    # Create all the levels

    player.rect.x = 100 
    player.rect.y = HEIGHT - player.rect.height
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

            handle_key_events(event, player)

        # Update the player.
        active_sprite_list.update()

        handle_collisions(player, platform)


        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        #current_level.draw(screen)
        screen.fill(pygame.color.Color("gray14")) 
        active_sprite_list.draw(screen)

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        # Limit to 60 frames per second
        clock.tick(120)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()

if __name__ == "__main__":
    main()
