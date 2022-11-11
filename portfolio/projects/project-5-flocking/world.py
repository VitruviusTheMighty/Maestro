
try:
    from vector import Vector
except ModuleNotFoundError:
    try:
        from fsm.vector import Vector
    except:
        from games.fsm.vector import Vector

class World:

    gravity = Vector (0,0)

    def __init__ (self, width, height):

        self.width = width
        self.height = height
        self.timescale = 1/1000

        
