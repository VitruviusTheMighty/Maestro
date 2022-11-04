

class FSM:

    def __init__ (self):

        self.current_state = None
        self.states = {}
        self.transitions = {}


    def add_states (self, state_specs):
        """ Expecting a list of tuples, where each tuple provides a
        name for a state and the name of a python method that should
        be run while the character is in that state."""

        for (name, action) in state_specs:

            self.states[name] = action

        if state_specs != []:
            self.current_state = state_specs[0][0]


    def make_start (self, name):

        self.current_state = name


    def add_transitions (self, from_name, transitions):
        """ transitions is a list of tuples, with each tuple providing
        the name of a method testing a condition and the name of the
        next state that the character goes into if the condition is
        true"""

        self.transitions[from_name] = transitions


    def update (self, world):

        if self.current_state in self.transitions:
            for (test, next_state) in self.transitions[self.current_state]:
                if test(world):
                    self.current_state = next_state

