Game Dev Log
============

**A collection of all dev-logs from making games during the production of this portfolio**

project-1:baselines
-------------------

NA

project-2:breakout
------------------

Handling Collisions
~~~~~~~~~~~~~~~~~~~~

- The is the method we learned in class of detecting collisions - I want to see if pygame has a way to achieve this for any shape
- After some tweaking with trying to create an interface for objects that can be collided with, I found pygame already has this... **A sprite**
- I have now reimplemented every object that can be collided with as a pygame sprite child class
- This has the added beenfit of allowing me to interact with all sprites using the same global methods.
- I also found how to add music

Some Bugs
~~~~~~~~~

- the sprite handle collisions acts on in certain cases. It is not fool - proof

New Knowledge thus far
~~~~~~~~~~~~~~~~~~~~~~

- Pygame Sprites classes and functions

Old knowledge used thus far
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Pygame, object orienting python, text displaying

Most fun
~~~~~~~~

- Given the way I implemented / object oriented the balls, being able to toggle between square and circle balls is cool.
- also the background music implementing was fun too

Struggling
~~~~~~~~~~

- Having proper collisions using the inital methods is the tricker part for me


project-3:collisions
--------------------

NA

project-4:joust
---------------

See :ref:`project-2-joust-documentation`

project-5:flocking
------------------

See :ref:`project-3-flocking-documentation`

project-6:fsm
-------------

project-7:astar
---------------

project-8:networking
---------------------

maestro
-------

ctrl 
----