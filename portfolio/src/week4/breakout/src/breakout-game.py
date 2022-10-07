import pygame
from paddle import Paddle
from ball import Ball
from vector import Vector
from brick import Brick
import math
import os

class Breakout3000:
    """
    A python implementation for BREAKOUT 
    
    - Leonardo Ferrisi
    """
    def __init__(self, width=1000, height=800, fullscreen=False, cheats=False, multiball=False, useSquares=False, sfx=True, music=False):
        pygame.init()
        
        self.score = 0
        self.lives = 3
        self.header_floor = 40
        self.paddle_speed = 10
        self.cheats = cheats
        info = pygame.display.Info()

        self.useSquares = useSquares

        self.WIDTH = width
        self.HEIGHT = height

        dirname = os.path.dirname(__file__)

        if cheats: 
            self.lives = math.inf
            self.paddle_speed = 10
        if fullscreen: 
            info = pygame.display.Info()
            # print(f"Screen is {info.current_w} x {info.current_h}")
            self.display = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
        else: self.display = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption("Breakout3000")

        if sfx:
            bounce_sound = os.path.join(dirname, f"music{os.sep}vine-boom.mp3")
            self.bounce_sound = pygame.mixer.Sound(bounce_sound)

            brick_hit_sound = os.path.join(dirname, f"music{os.sep}taco-bell-bong-sfx.mp3")
            self.brick_hit_sound = pygame.mixer.Sound(brick_hit_sound)
            pygame.mixer.init()

        if music:
            ost = os.path.join(dirname, f"music{os.sep}amogus.mp3")
            pygame.mixer.music.load(ost)
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(3)

        self.center_coords = ( self.display.get_width() // 2, self.display.get_height() // 2 )

        self.font = pygame.font.SysFont(None, size=74)

        self.sprites = pygame.sprite.Group()
        self.balls = []

        self.createPaddle(length=100, height=20)

        self.addBall(color="cyan", radius=10, position=Vector(0,0), velocity=Vector(2, 2))

        if multiball:
            self.addBall(color="green", radius=5, position=Vector(0,0), velocity=Vector(-8, 2))
            self.addBall(color="blue", radius=20, position=Vector(0,0), velocity=Vector(3, 4))
            self.addBall(color="yellow", radius=30, position=Vector(0,0), velocity=Vector(10, 10))

        self.sprites.add(self.paddle)

        self.max_score = 80 # should be divisible by 4 for now if each brick is 1 pt
        self.create_bricks(self.max_score)

        self.keepPlaying=False

    def createPaddle(self, length, height, color="white"):
        """
        Create a paddle and add it to the game
        """
        #Create the Paddle
        self.paddle = Paddle(pygame.color.Color(color), length, height, speed=self.paddle_speed)
        self.paddle.rect.x = self.display.get_width() // 2
        self.paddle.rect.y = self.display.get_height() - 100
        self.paddle.update_boundry(self.display.get_width())

    def addBall(self, color, radius, position, velocity):
        """
        Add a ball to the game
        """
        ball = Ball(color=pygame.color.Color(color), mass=10, position=position, radius=radius, velocity=velocity, asSquare=self.useSquares)
        ball.load_display_info(self.display)
        ball.load_header_info(self.header_floor)
        
        ball.update_position(Vector(self.display.get_width() // 2,
                                    self.display.get_height() // 2))

        ball.load_clock(pygame.time.Clock())
        
        self.sprites.add(ball)
        self.balls.append(ball)

    def create_bricks(self, num_bricks):
        """
        Creates an even number of bricks
        """
        assert num_bricks % 2 == 0 
        self.bricks = pygame.sprite.Group()
        
        self.brick_size = (int(self.display.get_width() // (num_bricks//4)), 50)
        bricks_per_row = num_bricks // 4
        for i in range(bricks_per_row): # top row
            brick = Brick(color="red", width=self.brick_size[0], height=self.brick_size[1])
            brick.rect.x = i * self.brick_size[0]
            brick.rect.y = 100
            self.sprites.add(brick)
            self.bricks.add(brick)
        for i in range(bricks_per_row):
            brick = Brick(color="orange", width=self.brick_size[0], height=self.brick_size[1])
            brick.rect.x =  i * self.brick_size[0]
            brick.rect.y = 150
            self.sprites.add(brick)
            self.bricks.add(brick)
        for i in range(bricks_per_row):
            brick = Brick(color="yellow", width=self.brick_size[0], height=self.brick_size[1])
            brick.rect.x = i * self.brick_size[0]
            brick.rect.y = 200
            self.sprites.add(brick)
            self.bricks.add(brick)
        for i in range(bricks_per_row*2):
            brick = Brick(color="green", width=self.brick_size[0], height=self.brick_size[1])
            brick.rect.x = i * self.brick_size[0]
            brick.rect.y = 250
            self.sprites.add(brick)
            self.bricks.add(brick)

    def display_text(self, position:Vector, text, color, delay=0):
        """
        Display text on the screen
        """
        text_surface = self.font.render(text, False, pygame.color.Color(color))
        text_rect = text_surface.get_rect()
        text_rect.center = (position.x, position.y)
        self.display.blit(text_surface, text_rect)
        pygame.display.flip()

        if delay > 0:
            pygame.time.wait(1000)
    
    def process_ball_brick_collisions(self):
        """
        Check for and process any ball - brick collisions
        """
        for ball in self.balls:
            self.bricks_collisions = pygame.sprite.spritecollide(ball, self.bricks, False)
        

            for brick in self.bricks_collisions:                
                pygame.mixer.Sound.play(self.brick_hit_sound)
                ball.bounce()
                self.score += 1
                brick.kill()

    def process_paddle_ball_collisions(self):
        for ball in self.balls:
            if pygame.sprite.collide_mask(ball, self.paddle):
                pygame.mixer.Sound.play(self.bounce_sound)
                ball.rect.x -= ball.velocity.x
                ball.rect.y -= ball.velocity.y
                ball.bounce()

    def draw_header(self):
        """
        Draw the header on top of the screen to keep score
        """
        pygame.draw.line(self.display, pygame.color.Color("white"), [0, self.header_floor], [self.display.get_width(), self.header_floor], 2)
        #Display the score and the number of lives at the top of the screen
        font = pygame.font.Font(None, 34)
        text = font.render("Score: " + str(self.score), 1, pygame.color.Color("white"))
        self.display.blit(text, (20,10))
        if self.cheats:
            text = font.render("CHEATS ENABLED", 1, pygame.color.Color("PURPLE"))
            self.display.blit(text, (self.center_coords[0],10))
        text = font.render("Lives: " + str(self.lives), 1, pygame.color.Color("white"))
        self.display.blit(text, (self.display.get_width() - 110 ,10))

    def check_game_end_cases(self):
        """
        Checks if the game has ended
        """

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                self.keepPlaying = False 
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: 
                    self.keepPlaying=False

        if self.score == self.max_score:
                self.display_text(position=Vector(self.display.get_width()//2, self.display.get_height()//2 ), text="YOU WIN!", color="white")
                pygame.time.delay(1000)
                self.keepPlaying = False

        for ball in self.balls:
            if ball.position.y >= self.display.get_height()-ball.radius:
                ball.bounce()
                self.lives -= 1

        if self.lives == 0:
            self.display_text(position=Vector(self.center_coords[0],self.center_coords[1]), text="YOU DIED", color="red")
            pygame.time.wait(3000)
            self.keepPlaying = False

    def _evaluate_positions(self):
        """
        Evaluate the positions of the paddle relative to the size of window in the event of resizing
        """
        self.paddle.update_boundry(self.display.get_width())
        self.paddle.rect.y = self.display.get_height() - 100

    def update_paddle(self):
        """
        Update the paddles position as according to key commands
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.paddle.moveLeft()
        if keys[pygame.K_RIGHT]:
            self.paddle.moveRight()

    def run(self):  
        """
        Run Breakout3000
        """
        self.keepPlaying = True
        clock = pygame.time.Clock() # define fps

        while self.keepPlaying:

            self.check_game_end_cases()
            self._evaluate_positions()
            
            self.update_paddle()

            self.sprites.update()

            # CHECK COLLISIONS
            self.process_paddle_ball_collisions()
            self.process_ball_brick_collisions()

            # DRAW AND COLOR IN EVERYTHING =============
            
            # Update display and header
            self.display.fill(pygame.color.Color("black"))
            self.draw_header()

            # DRAW SPRITES
            self.sprites.draw(self.display)

            pygame.display.flip()
            clock.tick(120)

        pygame.quit()

if __name__ == "__main__":
    b3k = Breakout3000(fullscreen=False, cheats=False, multiball=False, useSquares=False, sfx=True, music=False)
    b3k.run()
