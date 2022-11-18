## MAESTRO, CTRL, and simplepygamemenus

# MAESTRO

## A demosntration of menus and interface design 

### Context and Genre

This project exists to display all other projects in this course's portfolio.
The general theme / genre is a retro / 80s esq look and feel.

### High - Level Description

MAESTRO at its core is a user interface for selecting other games

### Key Features

MAESTRO supports turning the global audio track on and off, as well as selecting between 9 different games.
You can also access documentation and the course contract from the menu

### Detailed Description

MAESTRO is a stylized user interface to have everything in py portfolio in one place

### Concept Art / Design

See https://csc245-maestro.readthedocs.io/en/latest/maestro.html

### Challenges

- Converting all games to be capable of being displayed from the same pygame surface.
- Converting two part games such as NETWORKING which requires a server and a client has been difficult as well

-----------

# CTRL

## A game demonstrating *menus*, *bioactivity*, and *pong*

### Context and Genre

This game is a spin on pong, except you play with the added input of concentration as interpreter through brain activity in real time.
The general theme / genre is a retro - terminal look and feel with an atmosphere of "top secret program" akin to stranger things or SCP foundation material.

### High - Level Description

CTRL at its core is a pong game that you play against an AI opponent with the added spin of using a Brain Computer Interface to influence the ball.
This functions using an EEG headset of some type, gather information of brain activity at mainly at the frontal lobe regions of the brain (front of head).
The brain activity from this region is read in real time, run through a fourier transform and then passed through a logistic regression model. From this, 
your predicted level of concentration is normalized and returned as a value between 0.0 and 1.0

### Key Features

- CTRL mode : Play pong using the up and down arrow keys. Concentrate harder on the ball to speed it up as it approaches your opponent
- KEYS mode : Play the same game as CTRL but instead of using concentration, use the SPACE key to influence the ball
- TRAIN mode: Play a training session to evaluate and train your ability to control your level of concentration consciously.

### Detailed Description

The main game of CTRL is CTRL. But the game sports three different modes to play around with your psychic abilities and of course, pong

### Concept Art / Design

See https://csc245-maestro.readthedocs.io/en/latest/ctrl.html

### Challenges

- Getting the value of concentration estimated in real time

# ====================================================================

# simplepygamemenus

## A package for making pygame menus simpler

### Context and Genre

This is not quite a game, rather a python package for simplifying a step in the design process for python games

### High - Level Description

This is a package on PYPI that can be installed using pip

### Key Features

Create a Pygame MENU object and add buttons or text. You can also import a BUTTON object to use in other pygame loops.

### Detailed Description

See https://pypi.org/project/simplepygamemenus/ for more details

### Concept Art / Design

### Challenges

- Having files other than .py files uploaded and accessible to the user