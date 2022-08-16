import track_classes.track_point as tp
import track_functions.track_universal_functions as tuf

class Hairpin():
    "Track feature that contains functions to find its midpoints"
    def __init__(self,prev,current,nxt,cone_distance):
        self.prev = prev
        self.current = current
        self.nxt = nxt
        self.interval = 2.5*cone_distance

    def hairpin_point_1(self,prev,current,change_x,change_y):
        '''
        Description
        -----------
        Calculates the first point of the hairpin
        
        Parameters
        -----------
        self: Hairpin object
            Hairpin object
        prev: Point object
            previous polygon point using current index
        current: Point object
            current polygon point using current index
        change_x: float
            change required in the x-axis
        change_y: float
            change required in the y-axis

        Returns
        -----------
        point1: Point object
            first point to simulate hairpin
        '''

        point1 = tp.Point(current.x + change_x, current.y + change_y)

        if tuf.calculate_distance(prev,point1) < tuf.calculate_distance(prev,current):  
            point1 = tp.Point(current.x - change_x, current.y - change_y)
            
        return point1

    def hairpin_point_2(self,hairpin_point1,current,nxt,change_x,change_y):       
        '''
        Description
        -----------
        Calculates the second point on the tip of the hairpin
        
        Parameters
        -----------
        self: Hairpin object
            Hairpin object
        hairpin_point1: Point object
            first point of the hairpin
        current: Point object
            current polygon point using current index
        nxt: Point object
            next polygon point using current index
        change_x: float
            change required in the x-axis
        change_y: float
            change required in the y-axis

        Returns
        -----------
        point2: Point object
            second point to simulate hairpin
        '''

        point_a = tp.Point(hairpin_point1.x + change_x, hairpin_point1.y + change_y)
        point_b = tp.Point(hairpin_point1.x - change_x, hairpin_point1.y - change_y)
        point_c = tp.Point(hairpin_point1.x + change_x, hairpin_point1.y - change_y)
        point_d = tp.Point(hairpin_point1.x - change_x, hairpin_point1.y + change_y)
        
        current_distance_a = tuf.calculate_distance(point_a,current)
        current_distance_b = tuf.calculate_distance(point_b,current)
        current_distance_c = tuf.calculate_distance(point_c,current)
        current_distance_d = tuf.calculate_distance(point_d,current)

        current_distance_data = [(point_a,current_distance_a),(point_b,current_distance_b),(point_c,current_distance_c),(point_d,current_distance_d)]
        
        current_distance_data.sort(key=lambda tup:tup[1], reverse=True)
        
        # Get the 2 points with the largest distance to the current point
        while len(current_distance_data) > 2:
            current_distance_data.pop()

        nxt_distance_data = []
        for point,distance in current_distance_data:
            point_distance = tuf.calculate_distance(point,nxt)
            nxt_distance_data.append([point,point_distance])
            
        # Return the minimum distance from next point from the 2 filtered points
        min_nxt_distance = min([each[1] for each in nxt_distance_data])
        for point,point_distance in nxt_distance_data:
            if point_distance == min_nxt_distance:
                return point    

    def hairpin_point_3(self,hairpin_point2,current,nxt,change_x,change_y):        
        '''
        Description
        -----------
        Calculates the final point of the hairpin which is symmetrical to point1 along the axis of point2

        Parameters
        -----------
        self: Hairpin object
            Hairpin object
        hairpin_point2: Point object
            second point of the hairpin
        current: Point object
            current polygon point using current index
        nxt: Point object
            next polygon point using current index
        change_x: float
            change required in the x-axis
        change_y: float
            change required in the y-axis

        Returns
        -----------
        point3: Point object
            final point to simulate hairpin
        '''

        point_a = tp.Point(hairpin_point2.x + change_x, hairpin_point2.y + change_y)
        point_b = tp.Point(hairpin_point2.x - change_x, hairpin_point2.y - change_y)
        point_c = tp.Point(hairpin_point2.x + change_x, hairpin_point2.y - change_y)
        point_d = tp.Point(hairpin_point2.x - change_x, hairpin_point2.y + change_y)
        
        nxt_distance_a = tuf.calculate_distance(point_a,nxt)
        nxt_distance_b = tuf.calculate_distance(point_b,nxt)
        nxt_distance_c = tuf.calculate_distance(point_c,nxt)
        nxt_distance_d = tuf.calculate_distance(point_d,nxt)
        
        nxt_distance_data = [(point_a,nxt_distance_a),(point_b,nxt_distance_b),(point_c,nxt_distance_c),(point_d,nxt_distance_d)]
        nxt_distance_data.sort(key=lambda tup:tup[1])

        # Get the 2 points with the smallest distance to the next point
        while len(nxt_distance_data) > 2:
            nxt_distance_data.pop()

        current_distance_data = []
        for point,distance in nxt_distance_data:
            point_distance = tuf.calculate_distance(point,current)
            current_distance_data.append([point,point_distance])
            
        # Return the minimum distance from current point from the 2 filtered points
        min_current_distance = min([each[1] for each in current_distance_data])
        for point,point_distance in current_distance_data:
            if point_distance == min_current_distance:
                return point   

    def get_hairpin_points(self):
        '''
        Description
        -----------
        Calculates the points required to simulate a hairpin
        
        Parameters
        -----------
        self: Hairpin object
            Hairpin object

        Returns
        -----------
        hairpin: list of Point object
            3 points required to simulate hairpin
        '''

        hairpin=[]
        dy = self.current.y - self.prev.y
        dx = self.current.x - self.prev.x
        
        if dx == 0:        
            point1 = self.hairpin_point_1(self.prev,self.current,0,2*self.interval)
            point2 = self.hairpin_point_2(point1,self.current,self.nxt,self.interval,self.interval)
            point3 = self.hairpin_point_3(point2,self.current,self.nxt,self.interval,self.interval)
            hairpin.append(point1)
            hairpin.append(point2)
            hairpin.append(point3)
            
        elif dy == 0:
            point1 = self.hairpin_point_1(self.prev, self.current, 2*self.interval,0)
            point2 = self.hairpin_point_2(point1,self.current,self.nxt,self.interval,self.interval)
            point3 = self.hairpin_point_3(point2,self.current,self.nxt,self.interval,self.interval)
            hairpin.append(point1)
            hairpin.append(point2)
            hairpin.append(point3)
            
        else:
            dy_original,dx_original,dy_reciprocal,dx_reciprocal = tuf.calculate_changes_gradient_reciprocal(dy,dx,self.interval)
            point1 = self.hairpin_point_1(self.prev, self.current,2*dx_original,2*dy_original)
            point2 = self.hairpin_point_2(point1,self.current,self.nxt, dx_reciprocal + dx_original, dy_reciprocal + dy_original)
            point3 = self.hairpin_point_3(point2, self.current,self.nxt, dx_reciprocal + dx_original, dy_reciprocal + dy_original)
            hairpin.append(point1)
            hairpin.append(point2)
            hairpin.append(point3)
        
        return hairpin