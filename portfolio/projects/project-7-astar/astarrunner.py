from heapq import heappush, heappop
from gridworld import GridWorld
import pygame
import time

## Most Recent Changes:
## JR - Fall 2022

## Description: This file contains everything needed to run a-star on a grid world

class HeapNode:
    ''' The nodes that we are storing in our open and closed nodes
    lists. They record their g, h, and f value.
    '''
    def __init__ (self, f, g, h, p, path_from_start):
        self.f = f # priority in the queue
        self.g = g # cost to get to this node from start
        self.h = h # estimate of cost to goal from here
        self.p = p # location
        self.path = path_from_start

    def __str__ (self):
        return str(self.p) +" f="+str(self.f)+" g="+str(self.g)+" h="+str(self.h)

    def __eq__(self,other):
            '''allows for comparison of nodes, for use in the "is in" list comprehension'''
            #where p is a tuple (x,y)
            return self.p == other.p

    ## JR - these are needed for maintaining heap order evidently
    def __le__(self,other):
        return self.f < other.f

    def __gt__(self,other):
        return self.f > other.f



class AStarRunner:

    def __init__ (self, grid:GridWorld):

        self.grid = grid

        self.open_nodes = [] #nodes we have found but not explored - the priority queue
        self.closed_nodes = [] #nodes we have explored
        self.current = None
        self.goal = None
        self.already_seen = []
        self.verbose = False
        self.method = "astar"
        
    ## note to self: make this less ugly -- JR
    def handle_events(self,keymap):
            if (pygame.K_r in keymap) and keymap[pygame.K_r]:
                    print("resetting")
                    self.reset()
            if (pygame.K_v in keymap) and keymap[pygame.K_v]:
                    self.verbose = True
                    print("verbose: ",self.verbose)
                    print("WARNING WILL RUN VERY SLOW")
            if (pygame.K_p in keymap) and keymap[pygame.K_p]:
                    self.verbose = False
                    print("verbose: ",self.verbose)
            if (pygame.K_a in keymap) and keymap[pygame.K_a]:
                    self.method = "astar"
                    print("using astar")
            if (pygame.K_b in keymap) and keymap[pygame.K_b]:
                    self.method = "breadth"
                    print("using breadth first")
            if (pygame.K_d in keymap) and keymap[pygame.K_d]:
                    self.method = "depth"
                    print("using depth first")
            if (pygame.K_t in keymap) and keymap[pygame.K_t]:
                    self.method = "bestfirst"
                    print("using best first")
            


    def reset (self):

        self.open_nodes = []
        self.closed_nodes = []
        self.current = None
        self.goal = None
        self.already_seen = []
        self.start = None


    def are_we_done_yet (self):

        return self.current.p == self.goal


    def search (self, start_loc, end_loc, displayWin = None, world = None):
        '''
        start_node and end_node should be names of two nodes in
        the graph.
        '''

        self.reset()

        self.start = start_loc

        # initialize
        start_g = 0 #cost to get here
        start_h = self.grid.estimate_distance (start_loc, end_loc)
        start_f = start_g + start_h #cost to get here plus estimate to end
        path_so_far = []
        heapnode = HeapNode (start_f, start_g, start_h, start_loc, path_so_far)
        heappush (self.open_nodes, (heapnode.f,heapnode))

        self.already_seen = [heapnode]
        self.goal = end_loc

        # search
        (val,self.current) = heappop(self.open_nodes)
        
        while not self.are_we_done_yet() :

            

            for neighbor in self.grid.neighbors(self.current.p):

                #put neighbor into heapnode
                #which just stores location alongside
                #f,g,h and the path to that location
                neighbornode = HeapNode (0, 0, 0, neighbor, [])

                if neighbornode not in self.already_seen:
  
                    # g is the cost to get from start to here
                    # note: valueAtPoint is the "terrain cost" of entering the neighbor
                    neighbornode.g = self.current.g + self.grid.valueAtPoint(neighbor)
                    #h is an estimate of distance from here to end point
                    neighbornode.h = self.grid.estimate_distance(neighbor, self.goal)
                  
                    #different graph search algorithms only differ on
                    #how to prioritize where to look next
                    if self.method == "astar": #f = g+h
                        neighbornode.f = neighbornode.g + neighbornode.h
                    elif self.method == "breadth": #f = g
                        neighbornode.f = neighbornode.g
                    elif self.method == "depth": #f = -1*g
                        neighbornode.f = -1*neighbornode.g
                    elif self.method == "bestfirst": #f = h
                        neighbornode.f = neighbornode.h
                    

                    # store locations, not node data in path
                    path_so_far = self.current.path + [neighbor]

                    neighbornode.path = path_so_far
                   
                    #python asks us to implement priority queues
                    # of custom objects as tuples (p,obj)
                    # which leads to this (somewhat inelegant) syntax
                    heappush (self.open_nodes, (neighbornode.f,neighbornode))
                    self.already_seen.append(neighbornode)
                    
            #closed nodes contains nodes we've visited and expanded
            self.closed_nodes.append(self.current)

            #total abuse of pygame game loop
            #pretend this isn't here
            #these aren't the drones you're looking for
            
            if self.verbose:
                world.draw(displayWin)
                self.draw(world,displayWin)
                pygame.display.update()

                time.sleep(1)
                #v = input("<return> for next")
                
                
             #get the next node to look at
             #from the front of the priority queue
            (val,self.current) = heappop (self.open_nodes)

        # Loop has ended: we must be done
        print("I visited", len(self.already_seen), "nodes")
        return self.current.path + [self.current.p]


    def print_astar_info (self):
        """ Just for debugging: prints out all the relevant
        information about a particular state of A-star search."""

        print("==============")
        print("current", self.current)
        print("goal", self.goal)
        print("already seen")
        for n in self.already_seen:
                print(n)
        print("open nodes")
        for v,n in self.open_nodes:
            print(n)
       # print "closed"
       # for n in self.closed_nodes:
       #     print n
        print("path:", self.current.path)
        print("==============")



    def draw(self,world,win):
        scale = world.gridsize
        myfont= pygame.font.SysFont("Impact", int(20*scale/100))
        nudge = int(10*scale/100)
        
        if (self.current):

                # draw the closed list 
                for pt in self.already_seen:
                        (x,y) = pt.p
                        centerx = x*scale + scale/2
                        centery = y*scale + scale/2
                        rad = scale/3
                        pygame.draw.circle(win,pygame.color.Color("yellow"),(centerx,centery),rad)
                        valstring = "%0.1f" % pt.f
                        label = myfont.render(valstring,1,pygame.color.Color("black"))
                        win.blit(label,(centerx-nudge,centery-nudge))
                        
                        #pygame.draw.rect(win,pygame.color.Color("yellow"),pygame.Rect(x*scale,y*scale,world.gridsize,world.gridsize))

                # draw closed nodes
                for pt in self.closed_nodes:
                    (x,y) = pt.p
                    centerx = x*scale + scale/2
                    centery = y*scale + scale/2
                    rad = scale/3
                    pygame.draw.circle(win,pygame.color.Color("orange"),(centerx,centery),rad)
                    valstring = "%0.1f" % pt.f
                    label = myfont.render(valstring,1,pygame.color.Color("black"))

                    win.blit(label,(centerx-nudge,centery-nudge))
                # draw closed nodes
                for pt in self.current.path:
                    (x,y) = pt
                    centerx = x*scale + scale/2
                    centery = y*scale + scale/2
                    rad = scale/3
                    pygame.draw.circle(win,pygame.color.Color("red"),(centerx,centery),rad)
                    #pygame.draw.rect(win,pygame.color.Color("red"),pygame.Rect(x*scale,y*scale,world.gridsize,world.gridsize))
                
                #draw endpoint
                (x,y) = self.goal
                centerx = x*scale + scale/2
                centery = y*scale + scale/2
                rad = scale/3 
                pygame.draw.circle(win,pygame.color.Color("green"),(centerx,centery),rad)

                
                (x,y) = self.start
                centerx = x*scale + scale/2
                centery = y*scale + scale/2
                rad = scale/3 
                pygame.draw.circle(win,pygame.color.Color("green"),(centerx,centery),rad)
