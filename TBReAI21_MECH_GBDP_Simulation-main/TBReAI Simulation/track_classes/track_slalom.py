import track_classes.track_point as tp
import track_functions.track_universal_functions as tuf

class Slalom():
    "Track feature that contains functions to find its midpoints"
    def __init__(self,current,nxt,cone_distance):
        self.current = current
        self.nxt = nxt
        self.interval = 2*cone_distance

    def slalom_point_calculation(self,prev_slalom_point, nxt, change_x, change_y):
        '''
        Description
        -----------
        Works out the slalom point closest to the next major polygon point
        
        Parameters
        -----------
        self: Slalom object
            Slalom object
        prev_slalom_point: Point object
            previous slalom point to use to calcluate the next
        nxt: Point object
            next polygon point using current index
        change_x: float
            required change in the x-axis
        change_y: float
            required change in the y-axis

        Returns
        -----------
        slalom_point: Point object
            next point to simulate slalom
        '''

        point_a = tp.Point(prev_slalom_point.x + change_x, prev_slalom_point.y + change_y)
        point_b = tp.Point(prev_slalom_point.x - change_x, prev_slalom_point.y - change_y)
        
        distance_a = tuf.calculate_distance(nxt,point_a)
        distance_b = tuf.calculate_distance(nxt,point_b)
        
        distance_data = [(point_a,distance_a),(point_b,distance_b)]
        distance_data.sort(key=lambda tup:tup[1])

        return distance_data[0][0]

    def get_slalom_points(self):
        '''
        Description
        -----------
        Calculates the points required to simulate a slalom
        
        Parameters
        -----------
        self: Slalom object
            Slalom object

        Returns
        -----------
        slalom: list of Point object
            4 points required to simulate slalom
        '''

        slalom=[]
        dy = self.nxt.y - self.current.y
        dx = self.nxt.x - self.current.x
        
        if dx == 0:
            point1 = tp.Point(self.current.x, self.current.y + self.interval)
            point2 = tp.Point(point1.x + self.interval, point1.y + self.interval)
            point3 = tp.Point(point2.x - 2*self.interval, point2.y + self.interval)
            point4 = tp.Point(point3.x + 2*self.interval, point3.y + self.interval)
            slalom.append(point1)
            slalom.append(point2)
            slalom.append(point3)
            slalom.append(point4)
            
        elif dy == 0:
            point1 = tp.Point(self.current.x + self.interval, self.current.y)
            point2 = tp.Point(point1.x + self.interval, point1.y + self.interval)
            point3 = tp.Point(point2.x + self.interval, point2.y - 2*self.interval)
            point4 = tp.Point(point3.x + self.interval, point3.y + 2*self.interval)
            slalom.append(point1)
            slalom.append(point2)
            slalom.append(point3)
            slalom.append(point4)
            
        else:
            dy_original,dx_original,dy_reciprocal,dx_reciprocal = tuf.calculate_changes_gradient_reciprocal(dy,dx,self.interval)
            point1 = self.slalom_point_calculation(self.current, self.nxt, dx_original, dy_original)
            point2 = self.slalom_point_calculation(point1, self.nxt, dx_original+dx_reciprocal, dy_original+dy_reciprocal)
            point3 = self.slalom_point_calculation(point2, self.nxt, -(dx_original+dx_reciprocal), dy_original+dy_reciprocal)
            point4 = self.slalom_point_calculation(point3, self.nxt,  (dx_original+dx_reciprocal), dy_original+dy_reciprocal)
            slalom.append(point1)
            slalom.append(point2)
            slalom.append(point3)
            slalom.append(point4)      
        
        return slalom