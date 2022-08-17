% Changes made: Added global variable 'tilenumber'
% - Added the Dufort-Frankel and Crank-Nicolson methods'
% - Added an average of all methods at a point of smallest error between
% methods to refer to.

global tilenumber
i=0; 
nx = 21; 
thick = 0.05; 
tmax = 4000; 
for nt = 41:20:1001 
    i=i+1; 
    dt(i) = tmax/(nt-1); 
    disp (['nt = ' num2str(nt) ', dt = ' num2str(dt(i)) ' s']) 
    [~, ~, u] = shuttle(tmax, nt, thick, nx, 'Forward', false, tilenumber); 
    uf(i) = u(end, 1);
    [~, ~, u] = shuttle(tmax, nt, thick, nx, 'Backward', false, tilenumber); 
    ub(i) = u(end, 1);
       [~, ~, u] = shuttle(tmax, nt, thick, nx, 'Dufort-Frankel', false, tilenumber); 
    udf(i) = u(end, 1);
       
    [~, ~, u] = shuttle(tmax, nt, thick, nx, 'Crank-Nicolson', false, tilenumber); 
    ucn(i) = u(end, 1);
end 
% Calculate the converging result through averaging.
Converging_Result = (uf(end)+ub(end)+udf(end)+ucn(end))/4;
Converging_Result(1:length(dt)) = Converging_Result;

% Plot results

plot(dt, [uf; ub; udf; ucn]) 
hold on
plot(dt, Converging_Result, '--')
hold off
xlabel('Time Step (s)')
ylabel('End Tile Temperature (C)')
ylim([100 200]) 
legend ('Forward', 'Backward', 'Dufort-Frankel','Crank-Nicolson','Converging result')