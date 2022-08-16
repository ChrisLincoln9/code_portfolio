import numpy as np
import track_classes.track_point as tp

def acceleration_positions(track_length=100, track_width=3, cone_distance=3):
    '''
    Description
    -----------
    Returns the cone postions for the Acceleration track layout
    
    Parameters
    -----------
    track_length: int
        length of the track
    track_width: int
        width of the track
    cone_distance: int
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
    
    for i in range(0,track_length,cone_distance):
        
        point1 = tp.Point(i,track_width/2)
        point2 = tp.Point(i,-track_width/2)
        
        if i == 0:
            start_cones.append(point1)
            start_cones.append(point2)
        else:
            left_cones.append(point1)
            right_cones.append(point2)

    end_point1 = tp.Point(track_length,track_width/2)
    end_point2 = tp.Point(track_length,-track_width/2)
    start_cones.append(end_point1)
    start_cones.append(end_point2)

    return start_cones,left_cones,right_cones 

def skidpad_positions(radius=9.125,track_width=3,num_cones=16,start_excess=1):
    '''
    Description
    -----------
    Returns the cone postions for the Skidpad track layout
    
    Parameters
    -----------
    radius: float
        radius of the midpoint of the circles
    track_width: int
        width of the track
    num_cones: int
        number of cones for each circle
    start_distance: int
        distance start cones from circles

    Returns
    -----------
    start_cones: list of Point object
        coordinates for start cones
    left_cones: list of Point object
        coordinates for left cones
    right_cones: list of Point object
        coordinates for right cones
    '''

    start_cones= []
    left_cones = []
    right_cones = []
        
    inner_radius = radius - track_width/2
    outer_radius = radius + track_width/2
    
    # Cones that work out the figure of 8
    for i in np.linspace(0, 2*np.pi, num_cones, endpoint=False):
        
        x1 = inner_radius * np.cos(i) + inner_radius + start_excess/2 + track_width
        y1 = inner_radius * np.sin(i) + outer_radius - track_width/2
        point1 = tp.Point(x1,y1)
        point2 = tp.Point(x1,-y1)
        
        x2 = outer_radius * np.cos(i) + outer_radius + start_excess/2
        y2 = outer_radius * np.sin(i) + outer_radius - track_width/2
        point3 = tp.Point(x2,y2)
        point4 = tp.Point(x2,-y2)
        
        if abs(y1) >= track_width/2:      
            left_cones.append(point1)
            left_cones.append(point2)
        if abs(y2) > track_width/2:            
            right_cones.append(point3)   
            right_cones.append(point4) 
            

    # Placement of the cones to enter the Skidpad track        
    point5 = tp.Point(0, track_width/2)
    point6 = tp.Point(0, -track_width/2)
    point7 = tp.Point(2*outer_radius + start_excess, track_width/2)
    point8 = tp.Point(2*outer_radius + start_excess, -track_width/2)
    start_cones.append(point5)
    start_cones.append(point6)
    start_cones.append(point7)
    start_cones.append(point8)        
             
        
    return start_cones,left_cones,right_cones

def fixed_circuit_positions(straight_length=60, bend_radius=12, track_width=3, cone_distance=3):
    '''
    Description
    -----------
    Returns the cone postions for the Fixed Ring track layout
    
    Parameters
    -----------
    straight_length: int
        length of the straight
    bend_radius: int
        midpoint radius of the bend
    track_width: int
        width of the track
    cone_distance: int
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

    start_cones= []
    left_cones = []
    right_cones = []

    # Cones along the straights    
    for i in range(-int(straight_length/2) + cone_distance, int(straight_length/2), cone_distance):
        
        point1 = tp.Point(i,2*bend_radius + track_width/2)
        point2 = tp.Point(i,2*bend_radius - track_width/2)
        point3 = tp.Point(i, track_width/2)
        point4 = tp.Point(i, -track_width/2)
        
        if i == 0:
            start_cones.append(point3)     
            start_cones.append(point4)  
        else:
            left_cones.append(point3)
            right_cones.append(point4)
            
        right_cones.append(point1)
        left_cones.append(point2)
        
    # Cones along the inside of the bend    
    inner_radius = bend_radius - track_width/2
    inner_circumference = 2*np.pi*inner_radius
    for i in np.linspace(-0.5*np.pi, 0.5*np.pi, int(inner_circumference/(2*cone_distance)), endpoint=True):
        x_i = inner_radius * np.cos(i) + straight_length/2
        y_i = (inner_radius * np.sin(i) + inner_radius) + track_width/2
        
        point5 = tp.Point(x_i, y_i)
        point6 = tp.Point(-x_i ,y_i)

        left_cones.append(point5)
        left_cones.append(point6)
    
    # Cones along the outside of the bend
    outer_radius = bend_radius + track_width/2
    outer_circumference = 2*np.pi*outer_radius
    for i in np.linspace(-0.5*np.pi, 0.5*np.pi, int(outer_circumference/(2*cone_distance)), endpoint=True):
        x_o = outer_radius * np.cos(i) + straight_length/2
        y_o = (outer_radius * np.sin(i) + outer_radius) - track_width/2
        
        point7 = tp.Point(x_o,y_o)
        point8 = tp.Point(-x_o,y_o)
        
        right_cones.append(point7)
        right_cones.append(point8)

    return start_cones,left_cones,right_cones                                                                                                                   