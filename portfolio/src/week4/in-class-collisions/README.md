# csc245-starter-collisions

# Week 3 In-Class: Collisions

In these in-class assignments you'll be given an opportunity to practice several of the collision Algorithms that we have covered in lecture.  Specifically:

* AABB bounding box collisions
* momentum/energy preserving collisions between balls
* ball-vs-AABB collision
* ball and (non-axis aligned) collision


## Setup and code overview

You'll find the following files:

* `vector.py` - the Vector class 
* `ball_2d.py` - the base 2D Ball class
* `moving_ball_sprite_2d.py` - elaborates on the 2D ball
* `box_sprite.py`- a very simple box class
* `collision_game.py` - (note that I'm appending `_game` to all my "main" python programs)

Take a look at all the files.  Notice that I've 
Notice also that I've added some very rudimentary keyboard input to show you how to handle keyboard/mouse events (for more info, read the documentation).

## AABB Bounding Box Collissions

Save a copy of `collision_game.py` as `AABB_collision_game.py`

Start by adding a second box to the game.  You can choose to either have this box move independently and bounce around, or else be player controlled (it's easier to test the latter)  You can get rid of the ball if you want to.

Complete the `collidesWithAABB()` method in the Box class (`box_sprite.py`).

Add all remaining necessary code to have the moving box be green when it is not colliding with the stationary box, and red when it is.

I recommend also adding a `draw()` method to the vector class, so that you can draw the speed vectors assoicated with objects.  You'll thank me in a couple of weeks.

## Ball Collisions

Save a copy of `AABB_collision_game.py` as `Ball_collision_game.py`

1. Implement the `collide()` method in `moving_ball_sprite.py` and test it.  Read the function description carefully.
2. Now implement the `getResponse()` and the `bounce()` methods.  You'll need to update the `simulate()` method appropriately.  Test your code.
3. Finally add many balls to the game, and test that your bounce code still works.

## Ball-vs-AABB  Collisions

Repeat the pattern above to detect collision between boxes and AABBs.

## Challenge: Ball-vs-Segments

Finally, repeat the pattern above to detect when a ball intersects with a non-axis-aligned line segment.

## Hand in

Hand in all files associated with your project.  Name the main file breakout-game.py when I run this file in Python it should start your game.



