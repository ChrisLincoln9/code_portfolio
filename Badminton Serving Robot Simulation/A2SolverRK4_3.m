function [theta] = A2SolverRK4_3(Target_Distance,N)
tic % A2SolverRK4_3 takes a Target_Distance between x = 0 and x = 2.45, and
% finds the launch angle, theta, to N decimal places
t0=0; 
% Intial angle guesses
a1=90;   %90 gives min distance
a2=19.5; %19.5 gives ~max distance
         %This means all solutions can lie between these two angles

Toggle = 0; % A toggle between two 'if' statements will be used during 
% the while loop below,each toggle deals with changing a different angle
% guess.

 i=0;
while i<1000
i=i+1;
% Intial guess landing positions
if a1 == 90
    Rounded_L1 = -2.1; %This saves some time in the inital iterations
else
Rounded_L1 = ShootSolver_2(t0,(a1),N);
end
Rounded_L2 = ShootSolver_2(t0,(a2),N);
Toggle = (-1)^i;
if Rounded_L2 == (Target_Distance)
           i=1000;
           String1 =['Pitch angle (2d.p.) = '];
           disp(String1)
           target_angle = sprintf('%0.2f', a2); % makes 2 decimal places
           disp(target_angle)
           global combinedString
           combinedString = [String1, target_angle,char(176)];

elseif Toggle == -1
       linear_ratio1 = (Target_Distance - Rounded_L1) / (Rounded_L2 - Rounded_L1);
       a2prev=a2;
       a2 = a2 + ((a1-a2)*(1-linear_ratio1)); %Clever angle guess by assuming
%        linear relationship between angle and land position 
       
elseif Toggle == 1
       linear_ratio2 =  (Rounded_L2 - Target_Distance) / (Rounded_L2 - Rounded_L1);
       
   if i>10 % gives time for a2 to become close to target
       a1 = a2 + (-a2prev+a2)+3; %attempt to get a1 as close to the target angle
%        without becoming less than it (this is what the +3 helps with)
   end

end

end

theta = a2;

toc %tic and toc used to time the length of the operation, and see if changes have increased efficiency  
disp('The shuttlecock will land at x=') % This is for the purpose of console commentary
disp(Target_Distance)
end
