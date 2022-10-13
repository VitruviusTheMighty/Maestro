from pickle import FALSE
import pygame

from box import Box
from player import Player
from vector import Vector


class Game:

    def __init__(self, width=1200, height=800):
            pygame.init()

            # Instance VARS
            self.HEIGHT = height
            self.WIDTH = width

            self.player_speed = 15

            self.boxes = []

    def handle_collisions(self, player:Player):

        for box in self.boxes:
            if box.objOnTop(player):
                player.on_obj = True
                player.on_obj_id = box.id
                player.platform = box
                

                print(f"On platform floor? {player.onPlatform()}, {player.pos.y}, {player.rect.y}, {player.rect.h}, {box.rect.y}, {box.rect.y + box.rect.h}")
                
            else:   
                print(f"On platform floor? {player.onPlatform()}")

                if ( player.on_obj_id == box.id ) and not (player.onPlatform()):
                    # print(f"On platform floor? {player.onPlatform()}")
                    player.on_obj = False
                    player.platform_floor = None
                    player.on_obj_id = None
                    player.platform = None
            
        

    def handle_keypress_events(self, event:pygame.event.Event, player:Player):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.go_left()
            if event.key == pygame.K_RIGHT:
                player.go_right()
    
            if event.key == pygame.K_ESCAPE:
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
        
        self.boxes.append(Box(color, size.y, size.x, pos.x, pos.y))


    def run(self):
        Game_size = [self.WIDTH, self.HEIGHT]
        Game_screen = pygame.display.set_mode(Game_size)
        pygame.display.set_caption("SALTO!")

        # Create sprites
        active_sprite_list = pygame.sprite.Group()
        player = Player(Game_screen)
        player.set_speed(self.player_speed)

        self.addbox('red', Vector(90, 20), Vector(500 ,750))

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

            Game_screen.fill(pygame.color.Color("gray14")) 
            active_sprite_list.draw(Game_screen)

            clock.tick(30)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    g = Game()
    g.run()
