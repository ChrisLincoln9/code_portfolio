'''
Module used to store constants for the powertrain model

'''

import numpy as np
import matplotlib.pyplot as plt
import time
import scipy as sp
import scipy.integrate
from math import sin, atan, tan, asin, pi, exp, tanh, log

## Material parameters
steel_density = 7850 # kg/m^3
aluminium_density = 2700 # kg/m^3
steel_shear_modulus = 79300000000 # kg/m^2
aluminium_shear_modulus = 28000000000 # kg/m^2

## DC motor data
motor_inductance = 7.7e-05 # H
motor_inertia = 0.0416 # kgm^2
motor_damping = 0.0006899 # Nm/(rad/s)
motor_kt = 0.9437 # Torque constant
motor_ke = 0.8668 # Back emf constant
motor_resistance = 1.887 # Ohms
motor_efficiency = 0.95

## Transmission data
radius_drive = 0.024 # m
thickness_drive = 0.0059 # m
length_drive = 0.075 # m
radius_driven = 0.0945 # m
thickness_driven = 0.005 # m
length_driven = 0.5 # m
bearing_1_cfd = 0.12 # Coefficient of dynamic friction
bearing_1_cfs = 0.16 # Coefficient of static friction
drive_shaft_mass = 0.119 # kg
drive_shaft_radius = 0.011 # m
transmission_efficiency = 0.98
inertia_drive = 0.5 * steel_density * pi * (radius_drive ** 4) * thickness_drive # kgm^2
inertia_driven = 0.5 * aluminium_density * pi * (radius_driven ** 4) * thickness_driven # kgm^2
second_moment_area_drive = pi * (radius_drive ** 4) * 0.5 # m^4
second_moment_area_driven = pi * (radius_driven ** 4) * 0.5 # m^4
torsional_stiffness_drive = (steel_shear_modulus*second_moment_area_drive)/length_drive # Nm/rad
torsional_stiffness_driven = (aluminium_shear_modulus*second_moment_area_driven)/length_driven # Nm/rad

## Traction parameters
bearing_2_cfd = 0.12 # Coefficient of dynamic friction
bearing_2_cfs = 0.16 # Coefficient of static friction
driven_shaft_mass = 0.585 # kg
driven_shaft_radius = 0.0088 # m

## Tire Parameters
tire_b =  10 # Magic formula
tire_c = 1.9 # Magic formula
tire_d = 1 # Magic formula
tire_e = 0.97 # Magic formula
rear_tire_dia = 18 * 0.0254 # m
front_tire_dia = 16 * 0.0254 # m
tire_inertia = 1e-3   # kg*m^2
roll_resist = 0.015
tire_pressure = 28 # bar

# Frictional parameters
w_brk = 0.1 # rad/s
f = 0 # viscous friction coefficient
w_st = w_brk*((2)**(1/2)) # rad/s
w_coul = w_brk/10 # rad/s

## Vehicle Parameters
driver_mass = 68     # kg
vehicle_mass = 215  # kg
combined_mass = driver_mass + vehicle_mass # kg
CG_height = 320     # mm
drag_coeff = 0.54
front_axle = 1520   # mm
rear_axle = 1400    # mm
front_area = 0.56   # m^2
wheel_inertia = 0.5 * 20 * (rear_tire_dia/2)**2 # kg*m^2

# Simulation parameters
u0 = [0,0,0,0,0,0,0,0,0]
error = 0.05
demand_velocity = 1000 # rad/s

# Controller parameters
kp = 4.61
ki = 2.30
kd = 0
sat_lim = 500 # V
