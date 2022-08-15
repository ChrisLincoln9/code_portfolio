% Very similar code to dt_stability test, bu the for loop variable is nx
% instead of nt.
% Same changes made: Added global variable 'tilenumber'
% - Added the Dufort-Frankel and Crank-Nicolson methods'
% - Did not plot converging result due to number of timesteps being a
% favorable test of method
global tilenumber

i=0; 
nt = 800; 
thick = 0.05; 
tmax = 4000; 
for nx = 5:3:200
    i=i+1; 
    xlength(i) = thick/(nx-1); 
    disp (['nx = ' num2str(nx) ', xlength = ' num2str(xlength(i)) ' m']) 
    [~, ~, u] = shuttle(tmax, nt, thick, nx, 'Forward', false, tilenumber); 
    uf(i) = u(end-1, 1);
    [~, ~, u] = shuttle(tmax, nt, thick, nx, 'Backward', false, tilenumber); 
    ub(i) = u(end-1, 1);
       [~, ~, u] = shuttle(tmax, nt, thick, nx, 'Dufort-Frankel', false, tilenumber); 
    udf(i) = u(end-1, 1);
       
    [~, ~, u] = shuttle(tmax, nt, thick, nx, 'Crank-Nicolson', false, tilenumber); 
    ucn(i) = u(end-1, 1);

end 
% Plot results
plot(xlength, [uf; ub; udf; ucn]) 
xlabel('Thickness Step')
ylabel('End Tile Temperature (C)')
xlim([0.00125 0.0125])
ylim([120 185])
legend ('Forward', 'Backward', 'Dufort-Frankel','Crank-Nicolson')