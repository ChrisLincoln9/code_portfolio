function [t,z] = PlotResults(t0,angle,dt,tend,N)
% PlotResults takes an initial value problem, with inputs defined as
% follows:
% t0: The start time of the calculations where t=0 is where the shuttlecock is served
% angle: The pitch angle of the shuttlecock launch
% dt: the time step used for the RK4 calculation
% N: the number of decimal places that the calculation rounds to.
% The function outputs the vector z, which contains all values for at each time step:
% [xpostion;xvelocity;xpostion;xvelocity]
  A1 = 0.012;
  A2 = 0.009;
  starting_velocity = 10000;
% Set initial conditions:

theta = angle*pi/180;
z(1,1) = -2.1;
z(2,1) = starting_velocity*cos(theta);
z(3,1) = 1;
z(4,1) = starting_velocity*sin(theta);
t(1) = t0;
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
xland = find(z(2,:),1,'last');
yland = find(z(4,:),1,'last');
global Impact_Velocity
ImpactV = sqrt(z(2,xland)^2 +z(4,yland)^2);
Impact_Velocity = sprintf('%0.2f', ImpactV);



L = (z(1,end));   % Finds landposition
global Rounded_L colorshortname Launch_Yaw_Angle %Global variables are for the GUI
Rounded_L = round(L*10^N)/10^N; % Rounds to N decimal places
colorshortname = 'c';
Launch_Yaw_Angle = 0;
%Net height = 5ft [REFERENCE]
%These vectors draw the floor and the net
NetX = [0,0,0,0,0,0,0];
NetY = [0,1.024,1.024,0,1.524,1.524,0];
NetZ = [-3.084,-3.084,3.084,3.084,3.084,-3.084,-3.084];
FloorX = [-6.7056,6.7056,6.7056,-6.7056,-6.7056];
FloorY = [0,0,0,0,0];
FloorZ = [3.084,3.084,-3.084,-3.084,3.084];
disp(z(1,500))
figure(1)
hold on
radlaunch_yaw_angle = Launch_Yaw_Angle*pi/180; %convert to radians
zpos = (z(1,:)- z(1)) * sin(radlaunch_yaw_angle); % z position vector
xpos = ((z(1,:)-z(1)) *cos(radlaunch_yaw_angle)) -2.1; % x position vector
plot3(xpos(500),zpos(500),z(3,500),'o')
plot3(xpos(end),zpos(end),z(3,end),'o')
%Plotting floor, net, and trajectory

xlabel('x')
ylabel('z')
zlabel('y')
axis equal
plot3(NetX,NetZ,NetY,'b')
plot3(FloorX,FloorZ,FloorY,'k')
plot3(xpos,zpos,z(3,:),colorshortname)
legend('Stable flight begins','Landing','Net','Ground','Trajectory')
if Launch_Yaw_Angle == 0
view(0,0) %Side view is used if no yaw angle
else
view(30,-25) %This viewing angle is found to be a good perspective
end
hold off