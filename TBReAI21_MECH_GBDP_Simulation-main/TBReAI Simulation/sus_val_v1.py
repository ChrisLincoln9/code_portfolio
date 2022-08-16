# -*- coding: utf-8 -*-
"""
Created on Thu May  6 15:51:13 2021

@author: Akif Jabir
"""

import math

def sus_handles(client):
    """
    Retrives suspension relevant object handles and then computes suspension 
    constants to be applied into an equation

    Parameters
    ----------
    client : RemoteApiClient
        b0 python API connection line

    Returns
    -------
    Shock1 : int
        Shock absorber no. 1 object handle.
    Shock2 : int
        Shock absorber no. 2 object handle.
    Shock3 : int
        Shock absorber no. 3 object handle.
    Shock4 : int
        Shock absorber no. 4 object handle.
    Front_wheel : int
        Front wheel object handle.
    Rear_wheel : int
        Rear wheel object handle.
    Lf : float
        Front hub wheel displacment from the centre of gravity.
    Lr : float
        Rear hub wheel displacment from the centre of gravity.
    Mb : float
        Model mass.
    Iyy : float
        Model Moment of Inertia about the y-axis.
    kf : int
        Front suspension effective spring constant.
    kr : int
        Rear suspension effective spring constant.
    cf : int
        Front suspension resulting damping coefficient.
    cr : int
        Rear suspension resulting damping coefficient..
    g : int
        Acceleration due to gravity.
    hf_std : float
        Front hub displacement from ground at t = 0.
    hr_std : float
        Rear hub displacement from ground at t = 0..
    a : int
        Right hub displacment from the centre of gravity.
    b : int
        Left hub displacment from the centre of gravity.

    """
    # Get suspension shock absorber object handles
    Shock1 = client.simxGetObjectHandle('Shock_1',client.simxServiceCall())[1] 
    Shock2 = client.simxGetObjectHandle('Shock_2',client.simxServiceCall())[1]
    Shock3 = client.simxGetObjectHandle('Shock_3',client.simxServiceCall())[1]
    Shock4 = client.simxGetObjectHandle('Shock_4',client.simxServiceCall())[1]
    
    # Get main body handle
    Main_body = client.simxGetObjectHandle('Model',client.simxServiceCall())[1]
    
    # Get wheel handles
    Front_wheel = client.simxGetObjectHandle('Wheel_FSR',client.simxServiceCall())[1]
    Rear_wheel = client.simxGetObjectHandle('Wheel_RSR',client.simxServiceCall())[1]
    Front_wheel_left = client.simxGetObjectHandle('Wheel_FSL',client.simxServiceCall())[1]
    
    Lf = client.simxGetObjectPosition(Front_wheel, -1, client.simxServiceCall())[1][1]*-1;    # front hub displacement from body gravity center (m)
    Lr = client.simxGetObjectPosition(Rear_wheel, -1, client.simxServiceCall())[1][1];        # rear hub displacement from body gravity center (m)
    
    a = client.simxGetObjectPosition(Front_wheel_left, -1, client.simxServiceCall())[1][1]*-1; # Right hub displacment from the centre of gravity (m)
    b = Lr;                                                                                    # Left hub displacment from the centre of gravity (m)
    
    Mb = client.simxGetObjectFloatParameter(Main_body, 3005, client.simxServiceCall())[1];   # body mass (kg)
    
    # Lenght of the main body along the x-direction (m)
    w = (client.simxGetObjectFloatParameter(Main_body, 21, client.simxServiceCall())[1])-(client.simxGetObjectFloatParameter(Main_body, 24, client.simxServiceCall())[1]); 
    # Lenght of the main body along the z-direction (m)
    d = (client.simxGetObjectFloatParameter(Main_body, 25, client.simxServiceCall())[1])-(client.simxGetObjectFloatParameter(Main_body, 22, client.simxServiceCall())[1]); 
    
    Iyy = 1/12*Mb*(w**2+d**2) # body moment of inertia about y-axis in (kg m^2)
     
    kf = client.simxGetObjectFloatParameter(Shock1, 2018, client.simxServiceCall())[1]; # front suspension stiffness in (N/m)
    kr = client.simxGetObjectFloatParameter(Shock2, 2018, client.simxServiceCall())[1];  # rear suspension stiffness in (N/m)
    
    zeeta = 1;    # Damping ratio
    Muf = 35;   # Mass of the front suspension (kg)
    Mur = 38;   # Mass of the rear suspension (kg)
    cf = zeeta*2*math.sqrt(Muf*kf);     # Damping Coefficient front suspension (Ns/m)
    cr = zeeta*2*math.sqrt(Mur*kr);     # Damping Coefficient rear suspension (Ns/m)
    
    g = 9.81;    # Acc. due to gravity
    
    hf_std = client.simxGetObjectPosition(Front_wheel, -1, client.simxServiceCall())[1][2]*-1;    # front hub displacement from ground at t = 0 (m)
    hr_std = client.simxGetObjectPosition(Rear_wheel, -1, client.simxServiceCall())[1][2];        # rear hub displacement from ground at t = 0 (m)
    
    return Shock1,Shock2,Shock3,Shock4,Front_wheel, Rear_wheel, Lf, Lr, Mb, Iyy, kf, kr, cf, cr, g, hf_std, hr_std, a, b 

from scipy.integrate import odeint
from sus_val_v1 import sus_handles

def sus_mod(y0,t,accz,h, Lf, Lr, Mb, Iyy, kf, kr, cf, cr, g, a, b, accy):
    """
    Imports suspension parameters to solve for given timestep 't' to output
    suspension characteristics and reaction forces.

    Parameters
    ----------
    y0 : list
        Array with four suspension values, these are vertical velocity & 
        acceleration, angular velocity & acceleration (if first time step,
        initial condition y0 is [0,0,0,0]). 
    t : list
        Array of timer steps [last recorded time, current time].
    accz : float
        Acceleration in the z-axis.
    h : float
        Average height of the wheels from the ground at give time step.
    Lf : float
        Front hub wheel displacment from the centre of gravity.
    Lr : float
        Rear hub wheel displacment from the centre of gravity.
    Mb : float
        Model mass.
    Iyy : float
        Model Moment of Inertia about the y-axis.
    kf : int
        Front suspension effective spring constant.
    kr : int
        Rear suspension effective spring constant.
    cf : int
        Front suspension resulting damping coefficient.
    cr : int
        Rear suspension resulting damping coefficient.
    g : int
        Acceleration due to gravity.
    a : int
        Right hub displacment from the centre of gravity.
    b : int
        Left hub displacment from the centre of gravity.
    accy : float
        Acceleration in the y-axis.

    Returns
    -------
    y0 : list
        Array with four suspension values, these are vertical velocity & 
        acceleration and angular acceleration and velocity.
    y0_cornering : list
        Array with four suspension values, these are vertical velocity & 
        acceleration and angular acceleration and velocity while cornering.
    t : float
        Time step for which y0 was calculated.
    f : float
        Resultant front reaction  force.
    r : float
        Resultant rear reaction force.

    """

    def halfcar(z,t,My,h,Lf,Lr,Mb,Iyy,kf,kr,cf,cr,g,a,b):
        """
        Calculates the state variables of the suspension initial conditions by
        applying state space form of the governing suspension equations.

        Parameters
        ----------
        z : list
            Initial conditions.
        t : list
            Time step.
        My : float
            Moment of the vehicle along the y-axis with direction in the z-axis.
        h : float
            Average height of the wheels from the ground at give time step.
        Lf : float
            Front hub wheel displacment from the centre of gravity.
        Lr : float
            Rear hub wheel displacment from the centre of gravity.
        Mb : float
            Model mass.
        Iyy : float
            Model Moment of Inertia about the y-axis.
        kf : int
            Front suspension effective spring constant.
        kr : int
            Rear suspension effective spring constant.
        cf : int
            Front suspension resulting damping coefficient.
        cr : int
            Rear suspension resulting damping coefficient.
        g : int
            Acceleration due to gravity.
        a : int
            Right hub displacment from the centre of gravity.
        b : int
            Left hub displacment from the centre of gravity.

        Returns
        -------
        states : list
            Array of corresponding state variables.

        """
        # State variable
        q1,q2,q3,q4 = z
        
        # Coupled Equation  z_x = q1 & z_x_dot = q2 theta_x = q3 & theta_x_dot = q4
        q1dot = q2;
        q2dot = (2*kf*(Lf*q3-(q1+h))+2*cf*(Lf*q4-q2) - 2*kr*(Lr*q3+q1+h)-2*cr*(Lr*q4+q2))/Mb;
        q3dot = q4;
        q4dot = (-Lf*2*kf*(Lf*q3-(q1+h))-2*Lf*cf*(Lf*q4-q2) - 2*Lr*kr*(Lr*q3+q1+h)-2*Lr*cr*(Lr*q4+q2)+My)/Iyy;    
        
        # Store the calulated values in states array
        states = [q1dot, q2dot, q3dot, q4dot]        
        return states
    
    def cornering(z,t,h,Mb,Iyy,kf,kr,cf,cr,a,b):
        """
        Calculates the state variables of the suspension initial conditions by
        applying state space form of the governing suspension equations for 
        cornering.

        Parameters
        ----------
        z : list
            Initial conditions.
        t : list
            Time step.
        h : float
            Average height of the wheels from the ground at give time step.
        Mb : float
            Model mass.
        Iyy : float
            Model Moment of Inertia about the y-axis.
        kf : int
            Front suspension effective spring constant.
        kr : int
            Rear suspension effective spring constant.
        cf : int
            Front suspension resulting damping coefficient.
        cr : int
            Rear suspension resulting damping coefficient.
        a : int
            Right hub displacment from the centre of gravity.
        b : int
            Left hub displacment from the centre of gravity.

        Returns
        -------
        states : list
            Array of corresponding state variables.

        """
        # State variable
        q5,q6,q7,q8 = z
        
        # Coupled Equation  z_y = q5 & z_y_dot = q6 theta_y = yq7 & theta__dot = q8        
        q5dot = q6;
        q6dot = (((kf+kr)*(a*q7-(q5+h)))+((cf+cr)*(q8*a-q6)))/Mb;
        q7dot = q8;
        q8dot = (((a**2+b**2)*(q7*(kf+kr)+q8*(cf+cr)))-F_centripetal)/Iyy
        
        # Store the calulated values in states array
        states = [q5dot, q6dot, q7dot, q8dot]  
        return states
    
    # Approximate turning radius while cornering
    r = (13.5 + 10.5)/2
    
    My = accz*(Lf + Lr);            # Vertical acclertion of the vehicle
    F_centripetal = Mb*accy**2/r    # Cnetripetal force while cornering
    
    # ODE Integrator function, integrates for the fiven time step 't' with initial conditions 'y0' to output suspension characteristics in a straight line
    y0 = odeint(halfcar, y0, t,args=(My,h,Lf,Lr,Mb,Iyy,kf,kr,cf,cr,g,a,b)) [-1]
    
    # ODE Integrator function, integrates for the fiven time step 't' with initial conditions 'y0' to output suspension characteristics while cornering
    y0_cornering = odeint(cornering, y0, t,args=(h,Mb,Iyy,kf,kr,cf,cr,a,b)) [-1]
    
    # Function to give the vehicle reaction forces
    def front_reaction(My,h):
        """
        Calculates reaction forces of front and rear tyres for two conditions 
        - straight line and cornering

        Parameters
        ----------
        M  My : float
            Moment of the vehicle along the y-axis with direction in the z-axis.
        h : float
            Average height of the wheels from the ground at give time step.

        Returns
        -------
        f : float
        Resultant front reaction  force.
        r : float
            Resultant rear reaction force.

        """
        f = (2*kf*((Lf*y0[2])-(y0[0]+h)))+(2*cf*((Lf*y0[3])-y0[1]))+(Mb*g/2);   # Front reaction force
        r = (2*kr*((Lr*y0[2])+(y0[0]+h)))-(2*cr*((Lr*y0[3])+y0[1]))+(Mb*g/2);   # Rear reaction force
        
        return f,r
    
    f,r = front_reaction(My, h)     # Outputs front reaction as 'f' and rear reaction as 'r'
        
    return y0,f,r,t,y0_cornering