import random
import math
import numpy as np
import track_functions.track_universal_functions as tuf
import track_classes.track_point as tp
import track_classes.track_chicane as tc
import track_classes.track_slalom as ts
import track_classes.track_hairpin as th

def random_track_generation(cone_distance=1,track_width=4):
    '''
    Description
    -----------
    Randomly generates a track to simulate the Trackdrive event
    
    Parameters
    -----------
    cone_distance: int
        distance between cones
    track_width: int
        width of the track

    Returns
    -----------
    start_cones: list of Point object
        coordinates for start cones
    left_cones: list of Point object
        coordinates for left cones
    right_cones: list of Point object
        coordinates for right cones
    '''

    # Ensure that the convex hull calculated from the random points are not too close to each other
    while True:
        random_points = generate_random_points()
        convex_hull = jarvismarch_convex_hull(random_points)

        if check_validity(convex_hull,cone_distance):
            break

    # Add midpoints to convex hull to add more variety to polygon shapes
    polygon_points = add_convex_hull_midpoints(convex_hull)
    
    # Insert track features if certain parameters are met between polygon points
    updated_polygon = add_track_features(polygon_points,cone_distance)
    
    # Connect polygon points with a straight line that is fairly consistent
    track_points = add_points(updated_polygon,cone_distance)
    
    # Uses track points to calculate cone positions and type
    start_cones,left_cones,right_cones = calculate_cone_positions(track_points,updated_polygon,track_width)

    # Removes any cones which are too close to track points due to strange polygon point positioning
    left_cones,right_cones  = remove_erroneous_cones(left_cones,right_cones,track_points,track_width)
    
    return start_cones,left_cones,right_cones

def generate_random_points(num_points=12,square_size=70):
    '''
    Description
    -----------
    Generates random points within dimensions of given square
    
    Parameters
    -----------
    num_points: int
        number of random points to generate
    square_size: float
        size allocation for random number generator

    Returns
    -----------
    random_points: list of Point object
        coordinates for generated random points
    '''
    
    random_points=[]
    
    # Generate the random points between given square size above the x-axis
    for i in range(num_points):
        single_point = tp.Point(random.randint(-square_size/2,square_size/2),random.randint(0,square_size))
        random_points.append(single_point)
        
    # Add origin point for the start line
    origin = tp.Point(0,0)    
    random_points.append(origin)
    
    return random_points

def jarvismarch_convex_hull(random_points):
    '''
    Description
    -----------
    Algorithm to find the convex hull of a list of points
    
    Parameters
    -----------
    random_points: list of Point object
        unordered list of random coordinates

    Returns
    -----------
    convex_hull: list of Point object
        coordinates for calculated convex hull
    '''
    
    convex_hull = []
    
    # Find the top-leftmost point
    left_index = tuf.find_left_index(random_points)
                
    p = left_index
    q = 0
    n = len(random_points)
    while True:
          
        # Add current point to result 
        convex_hull.append(random_points[p])
        
        q = (p + 1) % n
  
        for i in range(n):
              
            # If i is more counterclockwise than current q, then update q
            if tuf.find_orientation(random_points[p], random_points[i], random_points[q]) == 2:
                q = i
        p = q
  
        # While we don't come to first point
        if p == left_index:
            break
    
    return convex_hull

def check_validity(convex_hull,cone_distance):
    '''
    Description
    -----------
    Checks whether the distance between points are not too small
    
    Parameters
    -----------
    convex_hull: list of Point object
        coordinates for calculated convex hull
    cone_distance: float
        distance between cones

    Returns
    -----------
    False: list of Point object
        points are too close
    True: bool
        points are not too close
    '''

    for i in range(len(convex_hull)):
        prev,current,nxt = tuf.get_3_consecutive_elements(convex_hull,i)
        if tuf.calculate_distance(current,nxt) < 6*cone_distance:
            return False

    return True

def add_convex_hull_midpoints(convex_hull,variation=6):
    '''
    Description
    -----------
    Generates random midpoints, within a specified radius, using the list of convex hull points
    
    Parameters
    -----------
    convex_hull: list of Point object
        coordinates for calculated convex hull
    variation: int
        radius of random variation allowed in the midpoints

    Returns
    -----------
    new_convex_hull: list of Point object
        polygon with more varied points and shape
    '''

    new_convex_hull = []

    for i in range(len(convex_hull)):
        
        prev,current,nxt = tuf.get_3_consecutive_elements(convex_hull,i)
        new_convex_hull.append(current)
        
        if tuf.calculate_distance(current,nxt) > 6 * variation:     
            mid_x = (current.x + nxt.x)/2
            mid_y = (current.y + nxt.y)/2
            midpoint = tp.Point(mid_x + random.randint(-variation,variation), mid_y + random.randint(-variation,variation))
            new_convex_hull.append(midpoint)
        
    return new_convex_hull

def add_track_features(polygon_points,cone_distance):
    '''
    Description
    -----------
    Adds track features where possible within the polygon points
    
    Parameters
    -----------
    polygon_points: list of Point object
        polygon with more varied points and shape
    cone_distance: float
        distance between cones

    Returns
    -----------
    updated_polygon: list of Point object
        polygon with pre-defined track features
    '''

    updated_polygon=[]
    
    for i in range(len(polygon_points)):
        
        prev,current,nxt = tuf.get_3_consecutive_elements(polygon_points,i)
        rad_angle = tuf.calculate_angle(prev,current,nxt)
        deg_angle = rad_angle * (180/math.pi)
        
        updated_polygon.append(current)
        
        distance = tuf.calculate_distance(current,nxt)
        
        # 25% chance of a feature being inserted if possible
        if random.choice([True, False]):
            if random.choice([True, False]):
                for each in insert_feature(distance,deg_angle,cone_distance,prev,current,nxt):
                    updated_polygon.append(each)               
    
    return updated_polygon

def insert_feature(distance,angle,cone_distance,prev,current,nxt):
    '''
    Description
    -----------
    Determines which features can be inserted given the position of the points
    
    Parameters
    -----------
    distance: list of Point object
        absolute distance between the current and next polygon point
    angle: float
        angle between 2 vectors in degrees
    cone_distance: float
        distance between cones
    prev: Point object
            previous polygon point using current index
    current: Point object
            current polygon point using current index
    nxt: Point object
            next polygon point using current index

    Returns
    -----------
    track_feature: list of Point object
        points to simulate a pre-defined track feature
    '''

    track_feature = []
    features_available = []
    
    # Each features contains requirements for the angle between the 3 points and the distance between the current and next
    if distance > 6*cone_distance:
        if angle > 140:
            features_available.append('chicane')
        
    if distance > 10*cone_distance:
        if angle > 140:
            features_available.append('slalom')
            
    if distance > 6*cone_distance:
        if 80 < angle < 100:
            features_available.append('hairpin')
            
    # Features compatibile are randomly chosen for generation
    if len(features_available) > 0:
        feature = random.choice(features_available) 
        if feature == 'chicane':
            track_feature = tc.Chicane(current,nxt,cone_distance).get_chicane_points()
        elif feature == 'slalom':
            track_feature = ts.Slalom(current,nxt,cone_distance).get_slalom_points()
        elif feature == 'hairpin':
            track_feature = th.Hairpin(prev,current,nxt,cone_distance).get_hairpin_points()            

    return track_feature
 
def add_points(updated_polygon,cone_distance):
    '''
    Description
    -----------
    Adds points between the polygon points and tries to maintain even spacing
    
    Parameters
    -----------
    updated_polygon: list of Point object
        polygon with pre-defined track features
    cone_distance: float
        distance between cones

    Returns
    -----------
    track_points: list of Point object
        normalised points in polygon with pre-defined track features
    '''

    track_points = []
    
    for i in range(len(updated_polygon)):
        
        prev,current,nxt = tuf.get_3_consecutive_elements(updated_polygon,i)
        track_points.append(current)
                    
        distance = tuf.calculate_distance(current,nxt)
        num_cones=round(distance/cone_distance)
        
        x_vals = np.linspace(current.x,nxt.x,num_cones+2)
        y_vals = np.linspace(current.y,nxt.y,num_cones+2)
        
        point1 = tp.Point(x_vals[-1],y_vals[-1])
        point2 = tp.Point(x_vals[-2],y_vals[-2])
        distance = tuf.calculate_distance(point1,point2)
        
        if distance < 0.6*cone_distance:
            cones_to_add = num_cones
        else:
            cones_to_add = num_cones+1
        
        for j in range(1,cones_to_add):
            new_point = tp.Point(x_vals[j],y_vals[j])
            track_points.append(new_point)
        
    return track_points

def calculate_cone_positions(track_points,updated_polygon,track_width):
    '''
    Description
    -----------
    Works out cone positions given the track points
    
    Parameters
    -----------
    track_points: list of Point object
        normalised points in polygon with pre-defined track features
    updated_polygon: list of Point object
        polygon with pre-defined track features
    cone_distance: float
        distance between cones

    Returns
    -----------
    start_cones: list of Point object
        coordinates for start cones
    left_cones: list of Point object
        coordinates for left cones
    right_cones: list of Point object
        coordinates for right cones
    '''

    start_cones = []
    left_cones = []
    right_cones = []
    
    for i in range(len(track_points)):
               
        prev,current,nxt = tuf.get_3_consecutive_elements(track_points,i)

        next_midpoint = tp.Point((nxt.x + current.x)/2,((nxt.y + current.y)/2))
        prev_midpoint = tp.Point((prev.x + current.x)/2,((prev.y + current.y)/2))
        
        dy = next_midpoint.y - prev_midpoint.y
        dx = next_midpoint.x - prev_midpoint.x
        
        if dx == 0:
            point1 = tp.Point(current.x + track_width/2, current.y)
            point2 = tp.Point(current.x - track_width/2, current.y)
            
            # Checks if point1 is inside polygon to differentiate between left and right
            if tuf.check_inside(point1,updated_polygon):
                if current.x == 0 and current.y == 0:
                    start_cones.append(point2)
                    start_cones.append(point1)
                else:
                    left_cones.append(point2)
                    right_cones.append(point1)
            else:
                if current.x == 0 and current.y == 0:
                    start_cones.append(point1)
                    start_cones.append(point2)
                else:
                    left_cones.append(point1)
                    right_cones.append(point2)

        elif dy == 0:
            point1 = tp.Point(current.x, current.y + track_width/2)
            point2 = tp.Point(current.x, current.y - track_width/2)
            
            # Checks if point1 is inside polygon to differentiate between left and right
            if tuf.check_inside(point1,updated_polygon):
                if current.x == 0 and current.y == 0:
                    start_cones.append(point1)
                    start_cones.append(point2)
                else:
                    left_cones.append(point1)
                    right_cones.append(point2)
            else:
                if current.x == 0 and current.y == 0:
                    start_cones.append(point2)
                    start_cones.append(point1)
                else:
                    left_cones.append(point2)
                    right_cones.append(point1)
                
        else:
            dy_original,dx_original,dy_reciprocal,dx_reciprocal = tuf.calculate_changes_gradient_reciprocal(dy,dx,track_width/2)
            point1 = tp.Point(current.x + dx_reciprocal, current.y + dy_reciprocal)
            point2 = tp.Point(current.x - dx_reciprocal, current.y - dy_reciprocal)
            
            # Checks if point1 is inside polygon to differentiate between left and right
            if tuf.check_inside(point1,updated_polygon) == True:
                if current.x == 0 and current.y == 0:
                    start_cones.append(point1)
                    start_cones.append(point2)
                else:
                    left_cones.append(point1)
                    right_cones.append(point2)
            else:
                if current.x == 0 and current.y == 0:
                    start_cones.append(point2)
                    start_cones.append(point1)
                else:
                    left_cones.append(point2)
                    right_cones.append(point1)
    
    return start_cones,left_cones,right_cones

def remove_erroneous_cones(left_cones,right_cones,track_points,track_width):
    '''
    Description
    -----------
    Removes cones that are within the width of the track multiplied by multiplier
    
    Parameters
    -----------
    left_cones: list of Point object
        coordinates for left cones
    right_cones: list of Point object
        coordinates for right cones
    track_points: list of Point object
        normalised points in polygon with pre-defined track features
    track_width: float
        width of the track

    Returns
    -----------
    new_left_cones: list of Point object
        coordinates for left cones with erroneous ones removed
    new_right_cones: list of Point object
        coordinates for right cones with erroneous ones removed
    '''

    new_left_cones = []
    new_right_cones = []
    
    left_indexes_remove = []
    right_indexes_remove = []
    
    for i in range(len(left_cones)):
        for j in range(len(track_points)):
            if tuf.calculate_distance(left_cones[i],track_points[j]) < (track_width/2) * 0.5:
                left_indexes_remove.append(i)
                break

    for i in range(len(left_cones)):
        if i not in left_indexes_remove:
            new_left_cones.append(left_cones[i])


    for i in range(len(right_cones)):
        for j in range(len(track_points)):
            if tuf.calculate_distance(right_cones[i],track_points[j]) < (track_width/2) * 0.5:
                right_indexes_remove.append(i)
                break

    for i in range(len(right_cones)):
        if i not in right_indexes_remove:
            new_right_cones.append(right_cones[i])

    return new_left_cones,new_right_cones