# CSC 245 - The Computer Science of Computer Games
### A journey in game development using python, pygame and other stuff too..
##### **by** *Leonardo Ferrisi* '23

---------------------------

#### Portfolio Site:

Associated with this class, I have made a site using **readthedocs**
available at: (https://csc245-maestro.readthedocs.io/en/latest/)

This Portfolio page functions as a manifest, guide, documentation page, dev-log source

### Contract:

Access Contract [**HERE**](./portfolio/contract.md)

### Projects

##### Baseline Projects

- [Baselines](https://github.com/VitruviusTheMighty/Maestro/tree/main/portfolio/projects/project-1-baselines)
- [Collisions](https://github.com/VitruviusTheMighty/Maestro/tree/main/portfolio/projects/project-3-collisions)

##### Actual Projects

- [Breakout](https://github.com/VitruviusTheMighty/Maestro/tree/main/portfolio/projects/project-2-breakout)
- [Joust](https://github.com/VitruviusTheMighty/Maestro/tree/main/portfolio/projects/project-4-joust)
- [Flocking](https://github.com/VitruviusTheMighty/Maestro/tree/main/portfolio/projects/project-5-flocking)
- [Finite State Machines](https://github.com/VitruviusTheMighty/Maestro/tree/main/portfolio/projects/project-6-fsm)
- [Path Planning](https://github.com/VitruviusTheMighty/Maestro/tree/main/portfolio/projects/project-7-astar)
- [Networking](https://github.com/VitruviusTheMighty/Maestro/tree/main/portfolio/projects/project-8-networking)

### Final Projects

- [*MAESTRO* the collection of all games detailed in this portfolio](https://csc245-maestro.readthedocs.io/en/latest/maestro.html)
- [CTRL: A Pong Game to train your psychic abilites with!](https://github.com/VitruviusTheMighty/Maestro/blob/main/games/ctrl/CTRL.py)
- [simple-pygame-menus](https://github.com/LeonardoFerrisi/simplepygamemenus-gitrepo)

# KWL (Know, Want to Know, Learned) Chart

| Topic                       | Know    | Want to Know | Learned |
| ----------------------------| ------- | ------------ | ------- |
| Git                         |    x    |              |         |
| Linux  Terminal             |    x    |              |         |
| Markdown                    |    x    |              |         |
| ReStructuredText            |    x    |              |    x    |
| ReadTheDocs Documentation   |    x    |              |    x    |
| Object Oriented Python      |    x    |              |         |
| List Comprehensions         |    x    |              |         |
| SSH and SSH Keys            |    x    |              |         |
| Vector Math                 |    x    |              |         |
| Flocking Agents             |    x    |              |    x    |
| Finite State Machines       |         |       x      |         |
| Path Planning               |    x    |              |    x    |
| Sprites                     |    x    |              |    x    |
| Sprite Sheets and Animation |    x    |              |    x    |
| Pygame API for Collisions   |    x    |              |    x    |
| Pygame API for Music        |    x    |              |         |
| Making Game Menus in Pygame |    x    |              |    x    |
| Standards for Game Design   |    x    |              |    x    |
| Alternative Inputs for Games|    x    |              |         |
| Using Bio Activity as Input |    x    |              |         |

##### Currently Completed: 19/20 (**95%**)

---------------------------------

### Final Grade Bid

Based on the completed KWL objectives and the grading rubric detailed in my [contract](./portfolio/contract.md)

----------------

### Postmortem

The final project(s) *CTRL*, *MAESTRO*, *simplepygamemenus*

All demonstrated different aspects of the skillset I spent this term expanding upon in game development.

CTRL - the primary "main" final game project involved bioactivity training and control of a ping pong ball in a python version of *pong* with an AI-opponent

*There were a few things that could have been improved*

1. In terms of training, the training mode only gives the user and idea of what works and what doesnt - it would be cool if it saved a configuration and imported that into the pong game such that threshold changes are saved across modes. Also the pong ball does not slow down when the user is concentrating on it which would be a nice features.

2. If I were to start this project again, I would try implementing a two player version of this game using python's socket module and two computers allowing a truly telepathic
game to exist between two individuals playing with brain activity.

3. If I had some more time with this project, I would probably implement some of the features detailed in *2* and also would improve the connection interface as there are times the program needs to be restarted because it wont re-connect to the headset. Bluetooth connections are pain.

4. I learned a lot about game design both in terms of appearance and functionality. CTRL demonstrates the culmination of my side projects such as menu design, sound, asthetic, and of course alternative user inputs.

MAESTRO - my portfolio, gamified

1. This project is mainly a cherry on top to my final submissions. I wanted to use what I had learned about menu design to put all of my games in one place. Unfortunatley I was unable to successfully add the networking game in time for the final sumbission as having python code open up additional programs can be flagged as a security risk on some machines and I was unable to find optimal ways around that in the given time frame.

2. If I could start this component again, I would build it from the ground up using my python package **simplepygamemenus**. The package makes it incredibly easy to make custom menus for pygame - games. I was able to convert a good chunk of maestro to simplepygamemenus after I completed the package - however I did not have enough time to convert the entire program. I would also implment some sort of game-garbage collection as currently there is a bug where switching menus many times actually results the games being drawn over eachother and thus system RAM begins filling up. This is not ideal and if the games were any heftier would result in significant issues.

3. If I had more time with this project, I would complete the conversion and figure out how to use gifs as pyamee backgrounds.

4. This side project taught me a lot about menu design and running other games on the same screen. It's especially satisfying to play *most* of my games through the same interface.


simplepyamemenus

1. No real issues I have with this one, it's a fantastic package that lets you easily make some simple pygame menus

2. If I had more time, I would implement a backend to handle importing gifs as a background. This task is significantly harder than it sounds and it would be cool if the package did all the grunt work in figuring out how to animate a background.


----------------

### Meme 
![Game Dev Meme](./assets/meme.jpg "No place like home")
