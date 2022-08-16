import random

class Point:
    "Point with x and y coordinates"
    def __init__(self,x,y):
        self.x = x
        self.y = y       

    def apply_noise(self,radius):
        '''
        Description
        -----------
        Random variations in the x and y coordinates
        
        Parameters
        -----------
        self: Point object
            Point object
        radius: float
            radius of possible random variation of position
        '''
        
        self.x = self.x + random.uniform(-radius,radius)
        self.y = self.y + random.uniform(-radius,radius)