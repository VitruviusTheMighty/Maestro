"""
INDEX's all the games
"""
# from joust.joust import Game as JOUST_GAME 
# from 
try:
    from joust.joust import Game as JOUST_GAME
    from breakout.breakout_game import Breakout3000 as BREAKOUT_GAME
    from flocking.steering_game import FlockingGame as FLOCKING_GAME
except:
    from games.joust.joust import Game as JOUST_GAME
    from games.breakout.breakout_game import Breakout3000 as BREAKOUT_GAME
    from games.flocking.steering_game import FlockingGame as FLOCKING_GAME

BREAKOUT = BREAKOUT_GAME # we would import something here
JOUST = JOUST_GAME
FLOCK = FLOCKING_GAME

if __name__ == "__main__":
    pass