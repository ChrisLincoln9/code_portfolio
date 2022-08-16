import track_classes.track_point as tp
import track_functions.track_universal_functions as tuf

class Chicane():
    "Track feature that contains functions to find its midpoints"
    def __init__(self,current,nxt,cone_distance):
        self.current = current
        self.nxt = nxt
        self.interval = 3*cone_distance
    
    def chicane_point_calculation(self,prev_chicane_point,nxt,change_x,change_y):
        '''
        Description
        -----------
        Works out the chicane point closest to the next major polygon point
        
        Parameters
        -----------
        self: Chicane object
            Chicane object
        prev_chicane_point: Point object
            previous chicane point to use to calcluate the next
        nxt: Point object
            next polygon point using current index
        change_x: float
            required change in the x-axis
        change_y: float
            required change in the y-axis

        Returns
        -----------
        chicane_point: Point object
            next point to simulate chicane
        '''

        point_a = tp.Point(prev_chicane_point.x + change_x, prev_chicane_point.y + change_y)
        point_b = tp.Point(prev_chicane_point.x - change_x, prev_chicane_point.y - change_y)
 
        distance_a = tuf.calculate_distance(nxt,point_a)
        distance_b = tuf.calculate_distance(nxt,point_b)
        
        distance_data = [(point_a,distance_a),(point_b,distance_b)]
        distance_data.sort(key=lambda tup:tup[1])

        return distance_data[0][0]

    def get_chicane_points(self):
        '''
        Description
        -----------
        Calculates the points required to simulate a chicane
        
        Parameters
        -----------
        self: Chicane object
            Chicane object

        Returns
        -----------
        chicane: list of Point object
            3 points required to simulate chicane
        '''

        chicane = []
        dy = self.nxt.y - self.current.y
        dx = self.nxt.x - self.current.x
        
        if dx == 0:
            point1 = tp.Point(self.current.x, self.current.y + self.interval)    
            point2 = tp.Point(self.current.x + self.interval, self.current.y + self.interval)
            point3 = self.chicane_point_calculation(point2, self.nxt, 0, self.interval)
            chicane.append(point1)
            chicane.append(point2)
            chicane.append(point3)
                
        elif dy == 0:
            point1 = tp.Point(self.current.x + self.interval, self.current.y)
            point2 = tp.Point(self.current.x + self.interval, self.current.y + self.interval)
            point3 = self.chicane_point_calculation(point2, self.nxt, self.interval, 0)
            chicane.append(point1)
            chicane.append(point2) 
            chicane.append(point3)
                        
        else:
            dy_original,dx_original,dy_reciprocal,dx_reciprocal = tuf.calculate_changes_gradient_reciprocal(dy,dx,self.interval)
            point1 = self.chicane_point_calculation(self.current, self.nxt, dx_original, dy_original)
            point2 = self.chicane_point_calculation(point1, self.nxt, dx_reciprocal, dy_reciprocal)
            point3 = self.chicane_point_calculation(point2, self.nxt, dx_original, dy_original)
            chicane.append(point1)
            chicane.append(point2)
            chicane.append(point3) 
        
        return chicane