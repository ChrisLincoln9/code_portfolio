import math

def calculate_distance(point1,point2):
    '''
    Description
    -----------
    Calculates absolute distance between 2 points
    
    Parameters
    -----------
    point1: Point object
        first point
    point2: Point object
        second point

    Returns
    -----------
    distance: float
        absolute distance between both points
    '''
    
    return ((point1.x - point2.x)**2 + (point1.y - point2.y)**2)**0.5

def calculate_changes_gradient_reciprocal(dy,dx,interval):  
    '''
    Description
    -----------
    Calculates the change in y and x given both the gradient and reciprocal of a straight line
    
    Parameters
    -----------
    dy: Point object
        first point
    dx: Point object
        second point
    interval: float
        used to normalise final changes in y and x axes

    Returns
    -----------
    dy_original: float
        change in the y-axis using gradient
    dx_original: float
        change in the x-axis using gradient
    dy_reciprocal: float
        change in the y-axis using reciprocal of the gradient
    dx_reciprocal: float
        change in the x-axis using reciprocal of the gradient
    '''

    gradient= dy/dx
    reciprocal= -1/gradient
    
    dy_original = gradient * interval * (1/(1+gradient**2) ** 0.5)
    dx_original = (dy_original / gradient)
    
    dy_reciprocal = reciprocal * interval * (1/(1+reciprocal**2) ** 0.5)
    dx_reciprocal = (dy_reciprocal / reciprocal)

    return dy_original,dx_original,dy_reciprocal,dx_reciprocal

def get_3_consecutive_elements(a_list,index):
    '''
    Description
    -----------
    Returns the previous, current and next elements in a list given the index
    
    Parameters
    -----------
    a_list: list
        list to search
    index: int
        index for the current element

    Returns
    -----------
    prev: any
        previous element using current index in the list
    current: any
        element of current index in the list
    nxt: any
        next element using current index in the list
    '''

    if len(a_list) >= 3:
    
        if index != 0:
            prev = a_list[index-1]
        else:
            prev = a_list[-1]

        current = a_list[index]

        if index != len(a_list) - 1:
            nxt = a_list[index+1]
        else:
            nxt = a_list[0]
        
        return prev,current,nxt    

def calculate_angle(prev,current,nxt):
    '''
    Description
    -----------
    Calculates the angle between 3 points by assuming 2 vectors
    
    Parameters
    -----------
    prev: Point object
        previous coordinates using current index in the list
    current: Point object
        coordinates of current index in the list
    nxt: Point object
        next coordinates using current index in the list

    Returns
    -----------
    angle: float
        the angle of the 2 vectors in radians
    '''

    vector1 = [current.x - prev.x, current.y - prev.y]
    vector2 = [current.x - nxt.x, current.y - nxt.y]
    
    dot_prod = vector1[0] * vector2[0] + vector1[1] * vector2[1]
    vector1_mag = (vector1[0]**2 + vector1[1]**2)**0.5
    vector2_mag = (vector2[0]**2 + vector2[1]**2)**0.5

    return math.acos(dot_prod/(vector1_mag*vector2_mag))   

def find_left_index(track_points):
    '''
    Description
    -----------
    Finds the left most point within a list of points
    
    Parameters
    -----------
    track_points: list of Point object
        list with many points with coordinates

    Returns
    -----------
    left_index: int
        index of the list which contains left most point
    '''

    left_index=0
    
    for i in range(1,len(track_points)):
        if track_points[i].x < track_points[left_index].x:
            left_index=i
        elif track_points[i].x == track_points[left_index].x:
            if track_points[i].y > track_points[left_index].y: 
                left_index=i
                
    return left_index

def find_orientation(point1,point2,point3):
    '''
    Description
    -----------
    Finds orientation between 3 different points
    
    Parameters
    -----------
    point1: Point object
        coordinates of first point
    point2: Point object
        coordinates of second point
    point3: Point object
        coordinates of third point

    Returns
    -----------
    0: int
        colinear
    1: int
        clockwise
    2: int
        counterclockwise
    '''

    val = (point2.y - point1.y) * (point3.x - point2.x) - \
          (point2.x - point1.x) * (point3.y - point2.y)

    if val == 0: 
        return 0 #colinear
    elif val > 0: 
        return 1 #clockwise
    else:
        return 2 #counterclockwise

def check_inside(position,polygon_points):
    '''
    Description
    -----------
    Checks if a point lies inside a polygon
    
    Parameters
    -----------
    position: Point object
        coordinates of point to assess
    polygon_points: list of Point object
        consecutive points which make up the polygon

    Returns
    -----------
    False: bool
        does not lie in polygon
    True: bool
        lies in polygon
    '''

    intersections = 0
    
    for i in range(len(polygon_points)):
        
        current = polygon_points[i]
        
        if i != len(polygon_points) - 1:
            nxt = polygon_points[i+1]
        else:
            nxt = polygon_points[0]

        gradient,intercept = calculate_line_equation(current,nxt)
        
        if (position.y < gradient * position.x + intercept and gradient > 0) or (position.y > gradient * position.x + intercept and gradient < 0):
            if (current.y < position.y < nxt.y) or (nxt.y < position.y < current.y):
                
                intersections += 1
    
    if intersections % 2 == 0:
        return False
    else:
        return True

def calculate_line_equation(point1,point2):
    '''
    Description
    -----------
    Calculates equation of a line from 2 points
    
    Parameters
    -----------
    point1: Point object
        coordinates of first point
    point2: Point object
        coordinates of second point

    Returns
    -----------
    gradient: float
        gradient of the straight line
    intercept: float
        y-intercept of the straight line
    '''

    dy = point1.y - point2.y
    dx = point1.x - point2.x
    
    if dx != 0:
        gradient = dy/dx
    else:
        gradient = 0
        
    intercept = point1.y - gradient * point1.x

    return gradient,intercept