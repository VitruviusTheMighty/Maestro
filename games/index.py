"""
INDEX's all the games
"""
# from joust.joust import Game as JOUST_GAME 
# from 
try:
    from joust.joust import Game as JOUST_GAME
    from breakout.breakout_game import Breakout3000 as BREAKOUT_GAME
    from flocking.steering_game import FlockingGame as FLOCKING_GAME
    from fsm.fsm_demo_game import FSM_GAME as FSM_GAME
    from path.navigating_demo_game import PathPlanning as PATH_GAME
    from ctrl.CTRL import Game as CTRL_GAME
except:
    from games.joust.joust import Game as JOUST_GAME
    from games.breakout.breakout_game import Breakout3000 as BREAKOUT_GAME
    from games.flocking.steering_game import FlockingGame as FLOCKING_GAME
    from games.fsm.fsm_demo_game import FSM_GAME as FSM_GAME
    from games.path.navigating_demo_game import PathPlanning as PATH_GAME
    from games.ctrl.CTRL import Game as CTRL_GAME

BREAKOUT = BREAKOUT_GAME # we would import something here
JOUST = JOUST_GAME
FLOCK = FLOCKING_GAME
FSM   = FSM_GAME
CTRL =  CTRL_GAME
PATH = PATH_GAME

if __name__ == "__main__":
    pass