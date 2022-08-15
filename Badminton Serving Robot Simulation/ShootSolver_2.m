function [Rounded_L] = ShootSolver_2(t0,angle,N)
%This function is used by A2SolverRK4_3
global starting_velocity A1 A2
%Old Model
% starting_velocity = 75
%New Model
% starting_velocity = 50
%Very simialr code to 'PlotResult' however does not plot.
dt = 0.0001;                      % Timestep that satisfies high accuraccy and low calculation time
theta = angle*pi/180;             %Convert angle to radians
z(1,1) = -2.1;                    %Intial x positon
z(2,1) = starting_velocity*cos(theta);           %Intial x velocity
z(3,1) = 1;                       %Intial y positon
z(4,1) = starting_velocity*sin(theta);           %Intial y velocity
% Set initial conditions
t(1) = t0;
tend = 3; %3 seconds is enough time for shuttle to land from any launch angle that will get it over the net
Cd1 = 0.8;
Cd2 = 0.6;
RO = 1.225;
g = 9.81;
k1 = 0.5 * RO * A1 * Cd1;
k2 = 0.5 * RO * A2 * Cd2;
%Old Model
% A1 = 0.012;
% A2 = 0.009;
%New Model
% A1 = 0.00283;
% A2 = 0.00283;
% Continue stepping until the end time is exceeded
n=1;
while t(n) <= tend
    % Increment the time vector by one time step
    t(n+1) = t(n) + dt;
    
    % Apply RK4 method for one time step
    z(:,n+1) = A2stepRK4(t(n), z(:,n), dt,k1,k2);
    n = n+1;
end
%Round answer to N decimal places
Rounded_L = round(z(1,end)*10^N)/10^N;


