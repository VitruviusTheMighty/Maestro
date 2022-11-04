

from moving_ball_2d import MovingBall

class Target (MovingBall):

    def __init__ (self, x, y):

        MovingBall.__init__(self, x, y, 0, 0, (0,0,0), 0, 0)
