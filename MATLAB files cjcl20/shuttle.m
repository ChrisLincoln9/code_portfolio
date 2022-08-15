function [x, t, u] = shuttle(tmax, nt, xmax, nx, method, doplot, tilenumber)
% Function for modelling temperature in a space shuttle tile
% D N Johnston  30/1/19
%
% Input arguments:
% tmax   - maximum time
% nt     - number of timesteps
% xmax   - total thickness
% nx     - number of spatial steps
% method - solution method ('forward', 'backward' etc)
% doplot - true to plot graph; false to suppress graph.
%
% Return arguments:
% x      - distance vector
% t      - time vector
% u      - temperature matrix
%
% For example, to perform a  simulation with 501 time steps
%   [x, t, u] = shuttle(4000, 501, 0.05, 21, 'forward', true);
%

% Set tile properties
thermcon = 0.141; % W/(m K)
density  = 351;   % 22 lb/ft^3
specheat = 1259;  % ~0.3 Btu/lb/F at 500F

% Load data from plottempauto
file = ['temp',tilenumber,'.mat'];
load(file)

% Initialise everything.
dt = tmax / (nt-1);
t = (0:nt-1) * dt;
dx = xmax / (nx-1);
x = (0:nx-1) * dx;
u = zeros(nt, nx);
alpha = (thermcon)/(density*specheat);
p = alpha * dt / dx^2;
u = zeros(nt, nx);
ivec = 2:nx-1;

% set initial conditions to 16C throughout.
% Do this for first two timesteps.
u([1 2], :) = 16;
L = 1;
% Main timestepping loop.
for n = 2:nt - 1
    
    % RHS boundary condition: outer surface. 
    % Use interpolation to get temperature R at time t(n+1).
    R = interp1(timedatacorrected, tempdatacorrectedC, t(n+1), 'linear', 16);
    %Changed last entry from extrap to '16'
    u(n+1,nx) = R;
    % Select method.
    switch method
        case 'Forward'

    % calculate internal values using forward differencing
    %*Neumann boundary:
    u(n+1,L) = (1 - 2 * p) * u(n,L) + p * 2* (u(n,L+1)); 

    u(n+1,ivec) = (1 - 2 * p) * u(n,ivec) + p * (u(n,ivec-1) + u(n,ivec+1));

        case 'Dufort-Frankel'
     %*Neumann boundary:
    u(n+1,L) = ((1 - 2 * p) * u(n-1,L) + 4 * p * (u(n,L+1)))/(1 + 2 * p);
    
    u(n+1,ivec) = ((1 - 2 * p) * u(n-1,ivec) + 2 * p * (u(n,ivec-1) + u(n,ivec+1)))/(1 + 2 * p); 
        case 'Backward' 
            u(1,:) = min(x, xmax-x);
     %*Neumann boundary
    L = u(n,1);
    
    b(1)      = 1+2*p;
    c(1)      = -2*p;
    d(1)      = L;
    a(ivec) = -p;
    b(ivec) = 1 + 2*p;
    c(ivec) = -p;
    d(ivec) = u(n, ivec);
    a(nx) = 0;
    b(nx) = 1;
    d(nx)     = R;
    u(n+1,:) =  tdm(a,b,c,d);
        case 'Crank-Nicolson'
      %*Neumann boundary
    L = (1-p)*u(n,1)+p*u(n,2);
    
    b(1)      = 1+p;
    c(1)      = -p;
    d(1)      = L;
    a(nx) = 0;
    b(nx) = 1;
    d(nx)     = R;
 a(2:nx-1) = -p/2; 
 b(2:nx-1) = 1 + p; 
 c(2:nx-1) = -p/2; 
 d(2:nx-1) = p/2*u(n,1:nx-2) + (1-p)*u(n,2:nx-1) + p/2*u(n,3:nx);
 
 u(n+1,:) = tdm(a,b,c,d);
           
        otherwise
            error (['Undefined method: ' method])
            return
    end
end

if doplot
% contour plot
surf(x,t,u)
% comment out the next line to change the surface appearance
shading interp  
% Rotate the view
view(-60,30)

%label the axes
xlabel('\itx\rm - m')
ylabel('\itt\rm - s')
zlabel('\itu\rm - deg C')
% title('method')
% End of shuttle function
end
end


    