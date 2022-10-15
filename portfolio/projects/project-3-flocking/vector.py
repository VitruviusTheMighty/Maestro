##
## Author: Kristina Striegnitz
## Author: Matt Anderson 
## Author: John Rieffel 
##
## Version: Fall 2022 
##
## A very simple vector class.

import math

class Vector:

    x = 0
    y = 0

    def __init__ (self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __str__ (self):
        return "["+str(self.x)+", "+str(self.y)+"]"

    def __add__(self,v2):
        return Vector(self.x + v2.x, self.y + v2.y)

    def __sub__(self,v2):
        return Vector(self.x - v2.x, self.y - v2.y)

    #when multiplying against a scalar
    def __rmul__(self,scalar):
        return Vector(self.x*scalar, self.y*scalar)
    def __mul__(self,scalar):
        return Vector(self.x*scalar, self.y*scalar)

    def __truediv__(self,scalar):
        return self * (1/scalar)

    def length (self):
        """ Length of the vector in pixels.
        """
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        """ Make the vector be one unit in length. I am using 10
        pixels as my unit.
        """
        l = float(self.length())
        self.x = self.x/l
        self.y = self.y/l
        return self

    def get_unit_vector(self):
        l = float(self.length())
        return Vector(self.x/l,self.y/l)


    def dot (self, v2):
        """
        The dot product.
        """
        return self.x * v2.x + self.y * v2.y

    def getPerpendicularUnit(self):
        perp = Vector(-1*self.y,self.x)
        perp.normalize()
        return perp

        
if __name__ == "__main__":
    v1 = Vector(3,1)
    v2 = v1.getPerpendicularUnit()
    print(v1,v2)