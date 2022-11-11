try:
    from steering_character import BeakBall
    from fsm import FSM

except ModuleNotFoundError:
    try:
        from fsm.steering_character import BeakBall
        from fsm.fsm import FSM
    except:
        from games.fsm.steering_character import BeakBall
        from games.fsm.fsm import FSM

class FSMBeakBall (BeakBall):

    def __init__ (self, x, y, r, m, color, xv, yv):

        BeakBall.__init__(self, x, y, r, m, color, xv, yv)

        self.fsm = FSM()

        # green - wander; red - run
        self.fsm.add_states ([('wandering', lambda:self.wander(1.0/30)), \
                              ('looping', lambda:self.loop(1.0/30)), \
                              ('freezing', lambda:self.freeze(1.0/30))])

        self.fsm.add_transitions ('wandering', [(self.test_on_red, 'looping')])
        self.fsm.add_transitions ('looping', [(self.test_on_green, 'wandering')])

        # self.fsm.add_transitions ('wandering', [(self.test_collide, 'freezing')])
        # self.fsm.add_transitions ('looping', [(self.test_collide, 'freezing')])



    def execute_actions (self):

        self.steering = []

        action = self.fsm.states[self.fsm.current_state]
        action()

        self.apply_steering()


    def test_on_red (self, world):

        if self.p.x > world.width/2:

            # if self.test_collide(world):
            #     self.freeze()
            return True
        else:
            return False

    def test_on_green (self, world):

        if self.p.x < world.width/2:
            # if self.test_collide(world):
            #     self.freeze()
            return True
        else:
            return False


    def test_collide (self, world):

        if self.isColliding(world, self.r):
            return True
        else:
            return False


