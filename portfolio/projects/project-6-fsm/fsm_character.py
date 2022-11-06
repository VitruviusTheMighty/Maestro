

from steering_character import BeakBall
from fsm import FSM

class FSMBeakBall (BeakBall):

    def __init__ (self, x, y, r, m, color, xv, yv):

        BeakBall.__init__(self, x, y, r, m, color, xv, yv)

        self.fsm = FSM()

        # green - wander; red - run
        self.fsm.add_states ([('wandering', lambda:self.wander(1.0/30)), \
                              ('looping', lambda:self.loop(1.0/30)), \
                              ('freezing', lambda:self.freeze(1.0/30))])

        self.fsm.add_transitions ('wandering', [(self.test_on_red, 'looping')])


    def execute_actions (self):

        self.steering = []

        action = self.fsm.states[self.fsm.current_state]
        action()

        self.apply_steering ()


    def test_on_red (self, world):

        if self.p.x > world.width/2:
            return True
        else:
            return False


