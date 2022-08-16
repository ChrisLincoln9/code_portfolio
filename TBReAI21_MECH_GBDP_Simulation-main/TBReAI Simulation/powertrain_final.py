# -*- coding: utf-8 -*-
'''
powertrain_final()

Models the powertrain installed in the TBRe 2019 vehicle with a PI controlled response

This script enables the powertrain of the TBRe 2019 vehicle to be modelled
based on an input desired velocity. It models an EMRAX 228 DC motor, the
transmission system, bearing friction, and slip. It uses an LSODA algorithm to
solve multiple first-order ODEs.

Classes:

    Powertrain()

'''

from powertrain_constants_final import *

class Powertrain():
    '''
    A class to represent the powertrain installed in the TBRe 2019 vehicle with a PI controlled response.

    ...

    Attributes:
        u0 : object
            Initial values for variables.
        t : object
            Array of time values used in the ODE solver.
        error : float
            Error coefficient used in the ODE solver.

    Methods:
        run(self):
            Runs the powertrain model.

        calculate_torque(self,z):


        get_demand_velocity(self,t):
            Returns the demand velocity for the motor at a given time

        rotational_friction(self,cf_static,cf_dyn,mass,radius,w):
            Returns the rotational friction acting at a bearing at a specified speed

        rolling_resistance(self,v_hub):
            Returns the rolling resistance acting on the wheel

        step(self,u, t):
            Computes a step in the LSODA algorithm

        plot_data(self,current,motor_velocity,demand_velocity,rear_velocity):
            Plots data from the powertrain model

    '''

    def __init__(self,u0,current_time,t_step,error,normal_force):
        '''
        Constructs all the necessary attributes for the powertrain object.

        Parameters:
            u0 : object
                Initial values for variables
            current_time : float
                Current time
            t_step : float
                Current time step
            error : float
                Error coefficient used in the ODE solver
            normal_force : float
                Normal force acting upon one rear wheel tyre
        '''
        self.u0 = u0
        self.t = np.linspace(current_time, current_time + t_step, 10)
        self.error = error
        self.normal_force = normal_force

    def run(self):
        '''
        Runs the powertrain model

        Returns:
            rear_wheel_torque : float
                Torque acting on one rear wheel of the vehicle
            new_params : float
                List of new initial parameters for the next iteration
        '''

        # Run the LSODA ODE solver
        y = sp.integrate.odeint(self.step, self.u0, self.t, atol = self.error, rtol = self.error)

        new_params = y[-1]

        rear_wheel_torque = self.calculate_torque(new_params)

        return rear_wheel_torque,new_params

    def calculate_torque(self,new_params):
        '''
        Calculates the applied torque on the rear wheels

        Parameters:
            new_params : object
                List of new iniital parameters for the next iteration
        Returns:
            torque : float
                Torque acting on one rear wheel of the vehicle
        '''

        v_rh = -new_params[5] * (rear_tire_dia/2)

        # Slip equations
        if (v_rh > 0.1):
            kr = ((v_rh - new_params[7])/abs(new_params[7]+0.1))
        else:
            kr = ((v_rh - new_params[7])/abs(0.1))

        force = (self.normal_force * tire_d * sin(tire_c * atan(tire_b * kr - tire_e * (tire_b * kr - atan(tire_b * kr)))))
        torque = force * (rear_tire_dia/2)

        return torque

    def get_demand_velocity(self,t):
        '''
        Returns the demand velocity for the motor at a given time

            Parameters:
                t : int
                    The current time

            Returns:
                demand_velocity : int
                    The demand velocity for the motor
        '''

        if t < 1:
            return 0
        else:
            return demand_velocity

    def rotational_friction(self,cf_static,cf_dyn,mass,radius,w):
        '''
        Returns the rotational friction acting at a bearing at a specified speed

            Parameters:
                cf_static : float
                    Static coefficient of friction
                cf_dyn : float
                    Dynamic coefficient of friction
                mass : float
                    Mass of shaft
                radius : float
                    Radius of shaft
                w : float
                    Relative rotational velocity of the shaft

            Returns:
                friction : float
                    The rotational friction acting upon the shaft
        '''

        T_brk = cf_static * radius * mass * 9.81
        T_c = cf_dyn * radius * mass * 9.81
        friction = ((2*exp(1))**(1/2))*(T_brk - T_c)*exp(-(w/w_st)**2)*(w/w_st) + T_c*tanh(w/w_coul) + f*w

        return friction

    def rolling_resistance(self,v_hub):
        '''
        Returns the rolling resistance acting on the wheel

            Parameters:
                v_hub : float
                    The hub velocity of the rear wheels

            Returns:
                f_roll : float
                    The rolling resistance force at the rear wheels
        '''

        c_roll = 0.015 * tanh((4*v_hub)/0.001)
        f_roll = c_roll * self.normal_force * (rear_tire_dia/2)
        return f_roll

    def step(self,u,t):
        '''
        Computes a step in the LSODA algorithm

            Parameters:
                u : object
                    List of initial values of variables
                t : float
                    The current time value

            Returns:
                state_deriv : object
                    List of state derivatives
        '''

        # Initialise variables
        im,wm,am,w2,a2,w3,a3,vr,I = u

        # DC motor controller equations
        velocity_error = self.get_demand_velocity(t) - wm
        P = kp*velocity_error
        dI_dt = ki*velocity_error
        V = P + I
        if V >= sat_lim:
            V = sat_lim

        # DC motor electrical system equations
        dim_dt = (1/motor_inductance)*(V - (motor_ke*wm) - motor_resistance*im)

        # DC motor mechanical system equations
        dwm_dt = (1/motor_inertia)*((motor_kt * im * motor_efficiency)-(motor_damping*wm)+(torsional_stiffness_drive*(-((radius_driven/radius_drive)*(1/transmission_efficiency)*a2) - am)))
        dam_dt = wm

        # Transmission equations
        w1 = -(radius_driven/radius_drive)*(1/transmission_efficiency)*w2
        fr1 = self.rotational_friction(bearing_1_cfs,bearing_1_cfd,drive_shaft_mass,drive_shaft_radius,w1)
        fr2 = self.rotational_friction(bearing_2_cfs,bearing_2_cfd,driven_shaft_mass,driven_shaft_radius,w2)
        #fr3 = self.rolling_resistance(w3)
        fr3 = 0 # This is modelled in Coppeliasim

        # Transmission equations
        dw2_dt = (1/(inertia_driven + (inertia_drive/transmission_efficiency)*((radius_driven/radius_drive)**2)))*(-torsional_stiffness_drive*(((radius_driven/radius_drive)**2)*(1/transmission_efficiency)*a2 + am*(radius_driven/radius_drive)) + fr1*(radius_driven/radius_drive) + 2 * torsional_stiffness_driven * (a3 - a2) - fr2)
        da2_dt = w2

        # Traction equations
        dw3_dt = (1/wheel_inertia)*(-torsional_stiffness_driven*(a3 - a2) - fr3)
        da3_dt = w3
        v_rh = -w3 * (rear_tire_dia/2)

        # Slip equations
        if (v_rh > 0.1):
            kr = ((v_rh - vr)/abs(vr))
        else:
            kr = ((v_rh - vr)/abs(0.1))

        fx = (self.normal_force * tire_d * sin(tire_c * atan(tire_b * kr - tire_e * (tire_b * kr - atan(tire_b * kr)))))
        dvr_dt = (1/(combined_mass/4))*fx

        state_deriv = [dim_dt, dwm_dt, dam_dt, dw2_dt, da2_dt, dw3_dt, da3_dt, dvr_dt, dI_dt]

        return state_deriv

    def plot_data(self,current,motor_velocity,demand_velocity,rear_velocity):
        '''
        Plots data from the powertrain model

            Parameters:
                t : object
                    An array of time values
                current : object
                    A list of values of the motor current
                motor_velocity : object
                    A list of values of the motor velocity
                demand_velocity : object
                    A list of values of the demand velocity
                rear_velocity : object
                    A list of values of the rear wheel velocity

            Returns:
                state_deriv : object
                    List of state derivatives
        '''

        fig, axs = plt.subplots(2,2)
        fig.tight_layout(pad=3.0)
        axs[0,0].plot(self.t, current)
        axs[0,0].set_title('Current')
        axs[0,0].grid()
        axs[0,1].plot(self.t, motor_velocity, 'tab:orange')
        axs[0,1].set_title('Motor velocity')
        axs[0,1].grid()
        axs[1,0].plot(self.t, demand_velocity, 'tab:green')
        axs[1,0].set_title('Demand velocity')
        axs[1,0].grid()
        axs[1,1].plot(self.t, rear_velocity, 'tab:red')
        axs[1,1].set_title('Rear wheel velocity')
        axs[1,1].grid()
        plt.show()
