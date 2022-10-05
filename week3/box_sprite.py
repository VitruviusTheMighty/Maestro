import pygame


class Box:

    xv = 0.0
    yv = 0.0

    def __init__ (self, x, y, w, h):
        self.rect = pygame.Rect(x,y,w,h)
        self.color = pygame.color.Color("blue")

    def draw(self,window):
        pygame.draw.rect(window,self.color,self.rect)

    def move (self):

        self.rect.x += self.xv;
        self.rect.y += self.yv;

    def collidesWithAABB(self,other):
        '''
        given another box, return True if we collide, False otherwise
        '''
        pass


    def bounce (self, width, height):

        if (self.rect.x + self.rect.w/2) > width:
            self.rect.x = width - self.rect.w/2
            self.xv *= -1
        elif (self.rect.x - self.rect.w/2) < 0:
            self.rect.x = 0 + self.rect.w/2
            self.xv *= -1
        if (self.rect.y + self.rect.h/2) > height:
            self.rect.y = height - self.rect.h/2
            self.yv *= -1
        elif (self.rect.y - self.rect.h/2) < 0:
            self.rect.y = 0 + self.rect.h/2
            self.yv *= -1


    def simulate (self, width, height):
        self.move()
        self.bounce(width, height)

    
    def get_bbox (self):
        """
        Calculates the screen coordinate of the bounding box.
        """
        return self.rect
        
if __name__ == "__main__":
    b1 = Box(1,2,3,4)