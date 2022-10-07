import pygame
from _paddle import Paddle

def update_paddle(self):
        """
        Update the paddles position as according to key commands
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.paddle.moveLeft()
        if keys[pygame.K_RIGHT]:
            self.paddle.moveRight()

if __name__ == "__main__":

    pygame.init()



    # Define some colors
    WHITE = (255,255,255)
    DARKBLUE = (36,90,190)
    LIGHTBLUE = (0,176,240)
    RED = (255,0,0)
    ORANGE = (255,100,0)
    YELLOW = (255,255,0)

    score = 0
    lives = 3

    size = (800, 600)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Breakout Game")

    all_sprites_list = pygame.sprite.Group()

    paddle = Paddle(LIGHTBLUE, 100, 10, screen)
    paddle.rect.x = 350
    paddle.rect.y = 560

    all_sprites_list.add(paddle)

    carryOn = True

    clock = pygame.time.Clock()

    while carryOn:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                carryOn = False # Flag that we are done so we exit this loop

        all_sprites_list.update()

        screen.fill(DARKBLUE)
        pygame.draw.line(screen, WHITE, [0, 38], [800, 38], 2)

        font = pygame.font.Font(None, 34)
        text = font.render("Score: " + str(score), 1, WHITE)
        screen.blit(text, (20,10))
        text = font.render("Lives: " + str(lives), 1, WHITE)
        screen.blit(text, (650,10))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.moveLeft()
        if keys[pygame.K_RIGHT]:
            paddle.moveRight()


        all_sprites_list.draw(screen)



        pygame.display.flip()

        clock.tick(60)

    #Once we have exited the main program loop we can stop the game engine:
    pygame.quit()