
import pygame
import math

from vector import Vector

class GridWorld:


        gravity = Vector(0,10) #useless here, but required for compatability
        grass = 0
        water = 1
        wall = 2
        #use terrain type to index colors
        colors = [pygame.color.Color("white"),pygame.color.Color("blue"),pygame.color.Color("black")]
        #float("inf") returns infinity! (well not really)

        costs = [1,4,float("inf")]


        def __init__(self,wid,hi,scale):

                self.width = wid
                self.height = hi
                self.gridsize = scale
                self.timescale = 1/1000
                #value at a grid location is the "terrain cost"
                self.grid = [[self.grass for _ in range(self.width)] for _ in range(self.height)]

                for i in range(0,self.height//2):
                        self.grid[i][self.width//2] = self.wall

                for i in range(0,int(self.width//2)):
                        self.grid[self.height//2][self.width//2 - i] = self.wall

        def handle_events(self,keymap):
                mpos = pygame.mouse.get_pos()
                x,y = self.find_closest_gridloc(mpos)
                if pygame.K_w in keymap and keymap[pygame.K_w]:
                        self.grid[y][x] = self.wall                                 
                if pygame.K_m in keymap and keymap[pygame.K_m]:
                        self.grid[y][x] = self.water
                if pygame.K_g in keymap and keymap[pygame.K_g]:
                        self.grid[y][x] = self.grass
                   
            

                

        def draw(self,window):
                window.fill(pygame.color.Color("green"))
                for row in range(0,self.height):
                        for col in range(0,self.width):
                                xcoord = col*self.gridsize
                                ycoord = row*self.gridsize
                                terrain = self.grid[row][col]
                                groundcolor = self.colors[terrain]
                                pygame.draw.rect(window,groundcolor,pygame.Rect(xcoord,ycoord,self.gridsize,self.gridsize))


        def inbounds(self,p):
          (x,y) = p
          return (x >= 0) and (x < self.width) and (y >= 0) and (y < self.height)
                  

        def isLegitimate(self,p):
                '''if out of bounds or wall, return false'''
                (x,y) = p
                if self.inbounds(p):
                        return self.grid[int(y)][int(x)] != self.wall
                else:
                        return False
                        

        def valueAtPoint(self,p):
                '''return the terrain cost of a point in the grid'''
                (x,y) = p
                if self.inbounds(p):
                        index = self.grid[int(y)][int(x)]
                        return self.costs[index]
                else:
                        return None

        def neighbors(self,p):
                '''given a point p, return a vector of all the neighboring points'''
                (x,y) = p
                outvec = []
                north = (x,y - 1)
                south = (x,y + 1)
                east = (x + 1, y)
                west = (x - 1,y)
                coords = [north,south,east,west]
                #only put something in the outvec if it is a legitimate point
                #i.e. don't return walls or out-of-bounds
                outvec = [loc for loc in coords if self.isLegitimate(loc)]
                return outvec



        def distance(self,startp,endp):
                (endx,endy) = endp
                (startx,starty) = startp

                return math.sqrt(pow(endx - startx,2) + pow(endy - starty,2))
                                  
        def manhattan(self,startp,endp):
                '''given two points, return manhattan distance of two points'''
                pass
        
        def estimate_distance(self,start,end):
#                return self.manhattan(start,end)
                 return self.distance(start,end)

        def find_closest_gridloc(self,p):
                '''given a point in (high resolution) game space, return the closest grid point'''
                x,y = p
                xval = int(x/self.gridsize)
                yval = int(y/self.gridsize)
                #print "endpoint is :",x,y, "(",xval,",",yval,")"
                return (xval,yval)
                                                 
                
