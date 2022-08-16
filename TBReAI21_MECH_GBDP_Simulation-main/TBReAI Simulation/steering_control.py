import numpy as np
from math import atan, sin, cos

def desired_position(theta_r,theta_l,d_r,d_l):#

    x_r_coords = []
    x_l_coords = []
    y_r_coords = []
    y_l_coords = []

    # convert cones into x,y
    for i in range(0,len(theta_r)):
        x_r_coords.append(sin(theta_r[i])*d_r[i])
        y_r_coords.append(cos(theta_r[i])*d_r[i])

    for i in range(0,len(theta_l)):
        x_l_coords.append(sin(theta_l[i])*d_l[i])
        y_l_coords.append(cos(theta_l[i])*d_l[i])

    #Find line algorithm
    #fitted_r_polar = np.polyfit(theta_r,d_r, 3)
    #fitted_l_polar = np.polyfit(theta_l,d_l, 3)

    fitted_r_cartesian = np.polyfit(x_r_coords,y_r_coords, 3)
    fitted_l_cartesian = np.polyfit(x_l_coords,y_l_coords, 3)

    #theta_r_fit = np.linspace(min(theta_r),max(theta_r),10)
    #d_r_fit = np.polyval(fitted_r_polar, theta_r_fit)

    #theta_l_fit = np.linspace(min(theta_l),max(theta_l),10)
    #d_l_fit = np.polyval(fitted_l_polar, theta_l_fit)

    x_r_fit = np.linspace(min(x_r_coords),max(x_r_coords),10)
    y_r_fit = np.polyval(fitted_r_cartesian, x_r_fit)

    x_l_fit = np.linspace(min(x_l_coords),max(x_l_coords),10)
    y_l_fit = np.polyval(fitted_l_cartesian, x_l_fit)

    x_middle = (x_r_fit + x_l_fit)/2
    y_middle = (y_r_fit + y_l_fit)/2

    target_position = [x_middle[1],y_middle[1]]

    return target_position

def steering_run(theta_old,theta_r_new,theta_l_new,d_r_new,d_l_new):

    # Get desired local position
    [x_des,y_des] = desired_position(theta_r_new,theta_l_new,d_r_new,d_l_new)


    # Get desired local angle
    theta_des = atan(x_des/y_des)

    #theta_des.append(desired_angle(theta_r,theta_l,d_r,d_l))

    #Get steering response
    theta_new = theta_old + (theta_des) * 0.1
    #theta.append(theta_des[-1])

    return theta_new
