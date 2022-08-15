function dz = A2stateDeriv(t,z,k1,k2)
% Calculate the state derivative for the shuttlecock's flight.
% 
%     DZ = stateDeriv(T,Z) computes the derivative DZ = [V; A] of the 
%     state vector Z = [P; V], where X is displacement, V is velocity,
%     and A is acceleration.
%Set physical conditions
M = 0.005;
g = 9.81;
% k1 and k2 compress the terms for the forward travelling and
% backwards travelling drag on the shuttlecock
%They have been calculated earlier in train of functions to prevent
%needless repeated computation.

%Assigning easily identifiable variable names to the vector z elements
Px = z(1,1);
Vx = z(2,1);
Py = z(3,1);
Vy = z(4,1);

if Py>0
V = sqrt(Vx^2 +Vy^2);
%shuttle angle is based on Vx and Vy
theta = atan2(Vy,Vx);
%Absolute velocity is needed for drag force calculation


if t<0.050
    F = k1*V^2;
else
    F = k2*V^2;
end


dzy1 = Vy; 
dzy2 = (-M*g-sin(theta)*F)/M; %This is the expression for acceleration


dzx1 = Vx;
dzx2 = -(F*cos(theta))/M; %This is the expression for acceleration
dz = [dzx1;dzx2;dzy1;dzy2]; %dz = [Vx;Ax;Vy;Ay]
else

dz = [0;0;0;0]; %prevents further calculation after shuttle cock reaches ground
end
end

