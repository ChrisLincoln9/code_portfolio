%This script runs the simulation using the selected tile and the
%Crank-Nicolson method for a given range and number of thicknesses,
%plotting the results of maximum internal temperature against thickness.


%Fetch global variables
global Ntiletests minthickness maxthickness tilenumber


% initialize variables
i=0; 
nt = 500; 
nx = 21;
tmax = 4000; 
dthick = (maxthickness-minthickness) / (Ntiletests-1);

%Run shuttle.m for the specified thicknesses
for thick = minthickness:dthick:maxthickness
i = i+1;
thickness(i) = thick;
[~, ~, u] = shuttle(tmax, nt, thick, nx, 'Crank-Nicolson', false, tilenumber); 
umax(i) = max(u(1:end, 1));
end
threshtemp(1:length(thickness)) = 176;
%Findthickness close to 176

[a,nth]=min(abs(umax-threshtemp));
MinimumThickness = thickness(nth);
% Plot results onto GUI graph
plot(thickness,umax);
hold on
plot(thickness,threshtemp,'--')
hold off
xlabel('Tile thickness')
ylabel('Maximum tile temperature at internal boundary (C)')
txt = ['Tile' tilenumber];
legend(txt,'Acceptable temperature')
txt2 = ['\downarrow Thickness = ', num2str(MinimumThickness,3)];
text(MinimumThickness,194,txt2,'FontSize',13)
