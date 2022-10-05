# Game 2: Breakout

Implement an homage to the classic Atari game Breakout.  This game has spawned many clones and imitators.

We will play test your games  once they have been turned in.

Required Features:

* A player controlled paddle
* A bouncing ball
* Destructable blocks
* A score keeping mechanism
* Object-oriented implementation
* A README.md (replacing this one) with a description of the game.
* A GameDev Diary on your process that includes:
   * what new knowledge you learned 
   * what old knowledge you dusted off
   * what was easiest/most fun
   * where did you struggle?
  

Optional Features:

* Splash and Game Over screens
* Power ups / Negative effects
* Multiple balls
* Multiple game modes
* Additional paddles
* More advanced physics / collisions
* Art assets / animation
* Sound effects / music

Hints:

Start from the code in this repository! 

Note that our ball-wall collision and bounce code does not require that the wall be axis aligned.  

## Hand in

Hand in all files associated with your project.  Name the main file breakout-game.py when I run this file in Python it should start your game.



## DEV LOG:

# Handling Collisions:

- The is the method we learned in class of detecting collisions - I want to see if pygame has a way to achieve this for any shape

    ## pygame.sprites.Sprite
        - After some tweaking with trying to create an interface for objects that can be collided with, I found pygame already has this...
            - A sprite

        I have now reimplemented every object that can be collided with as a pygame sprite child class

        This has the added beenfit of allowing me to interact with all sprites using the same global methods.

        - I also found how to add music

# Some Bugs:

- the sprite handle collisions acts on in certain cases. It is not fool - proof

# New Knowledge thus far:

- Pygame Sprites classes and functions

# Old knowledge used thus far

- Pygame, object orienting python, text displaying

# Most fun

- Given the way I implemented / object oriented the balls, being able to toggle between square and circle balls is cool.
- also the background music implementing was fun too

# Struggling

- Having proper collisions using the inital methods is the tricker part for me