##
## Author: Kristina Striegnitz
## Author: John Rieffel
##
## Version: Fall 2022
##
## This character has an FSM that allows it to go back and forth
## between two states: waiting and following a given path. The path is
## specified as a sequence of points and the character uses seek
## behavior to get from one point to the next.
##



try:
    from steering_character import SteeringBall 
    from fsm import FSM
    from target import Target
    from vector import Vector

except ModuleNotFoundError:
    try:
        from path.vector import Vector
        from path.steering_character import SteeringBall 
        from path.fsm import FSM
        from path.target import Target

    except:
        from games.path.vector import Vector
        from games.path.steering_character import SteeringBall 
        from games.path.fsm import FSM
        from games.path.target import Target

class NaviBeakBall (SteeringBall):

    def __init__ (self, x, y, r, m, color):

        SteeringBall.__init__(self, x, y, r, m, color, 0, 0)

        self.route = []
        self.goal = None
        self.target = None
        
        self.fsm = FSM()
        self.fsm.add_states ([('waiting', lambda:self.freeze (1.0)), \
                              ('pathfollowing', lambda:self.follow_path (1.0))])

        self.fsm.add_transitions ('waiting', [(self.test_got_route, 'pathfollowing')])
        self.fsm.add_transitions ('pathfollowing', [(self.test_at_goal, 'waiting')])


    def execute_actions (self):

        self.steering = []

        action = self.fsm.states[self.fsm.current_state]
        action()

        self.apply_steering ()


    def set_route (self, route):
        self.route = route
        x,y = route[0]
        self.target = Target(x, y)
        self.goal = route[-1]
        self.route = self.route[1:]


    def test_got_route (self, world):

        return self.route != []


    def test_at_goal (self, world):
        (x,y) = self.goal
        goalVec = Vector(x,y)
        distance_goal = (self.p -  goalVec).length()
        return distance_goal < 20


    def follow_path (self, weight):
        """ If we are close to our current target. Take the next point
        on our route and make that the new current target.
        """

        if self.target and self.route:
            distance_target = (self.p - self.target.p).length()
            if distance_target < 20:
                x,y = self.route[0]
                #target is the first item in the route  
                self.target = Target(x, y)
                #route is the remainder of the route
                self.route = self.route[1:]

        self.seek (self.target,weight)

