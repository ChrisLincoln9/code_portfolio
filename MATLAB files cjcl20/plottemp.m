%The calibration process begins by entering known axis values and pointing
%them out to the software by clicking on the points in the instructed
%order.


% Script to plot image of measured temperature, and trace it using the mouse.
%
% Image from http://www.columbiassacrifice.com/techdocs/techreprts/AIAA_2001-0352.pdf
% Now available at 
% http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.26.1075&rep=rep1&type=pdf
%
% D N Johnston 30/01/19
function plottemp(name)
img=imread([name '.jpg']);

figure (4);
image(img);
hold on
% You can adapt the following code to enter data interactively or automatically.

yaxismax = input('Enter the max value within the y axis labels: ');
xaxismax = input('Enter the max value within the x axis labels: ');
originposition = questdlg('Is the origin of the axis at 0,0?',...
    'Specify origin',...
    'Yes', 'No', 'No');
    switch originposition 
        case 'Yes'
            origin = [0,0];
        case 'No'
            xstart = input('What value does the time axis start at?');
            origin(1) = xstart;
            ystart = input('What value does the temperature axis start at?');
            origin(2) = ystart;
    end
timedata_axis_ends = [origin(1),origin(1),xaxismax];
tempdata_axis_ends = [origin(2),yaxismax,origin(2)];
% save temp597.mat timedata_axis_ends tempdata_axis_ends
 timedatascale = zeros(3,2);
 tempdatascale = zeros(3,2);

instruct = questdlg('In order to calibrate picture axis, please click on these three points in the following order: Origin, Max temp value on temp axis, Max time value on time axis',...
    'Instructions',...
    'I understand these instructions','I do not understand', 'I understand these instructions');
switch instruct
    case 'I understand these instructions'
        
   
    count = 0;
    a=0;
while 1>a % infinite loop
    [x, y, button] = ginput(1); % get one point using mouse
     if button
         count = count+1;
     end
    if button ~= 1 % break if anything except the left mouse button is pressed
        break
    end
    
    plot(x, y, 'og') % 'og' means plot a green circle.
    
    % Add data point to vectors. Note that x and y are pixel coordinates.
    % You need to locate the pixel coordinates of the axes, interactively
    % or otherwise, and scale the values into time (s) and temperature (F, C or K).
    timedatascale(count,1) = [timedata_axis_ends(count)];
    timedatascale(count,2) = [x];
    tempdatascale(count,1) = [tempdata_axis_ends(count)];
    tempdatascale(count,2) = [y];
    if count>2
        close all
         a=2;
    end
end
hold off

% sort data and remove duplicate points.
[timedata_axis_ends, index] = unique(timedata_axis_ends);
tempdata_axis_ends = tempdata_axis_ends(index);
tempindexmax = max(tempdatascale);
tempindexmin = min(tempdatascale);
gradienttemp = -1/((tempindexmax(1) - tempindexmin(1))/(tempindexmax(2)-tempindexmin(2)));
xintercepttemp = tempdatascale(1,2);

timeindexmax = max(timedatascale);
timeindexmin = min(timedatascale);
gradienttime = (timeindexmax(2)-timeindexmin(2))/(timeindexmax(1)-timeindexmin(1));
yintercepttime = timedatascale(1,2);

a=0;

    i=imread([name '.jpg']);
imagered = i(:,:,1);
imagegreen = i(:,:,2);
imageblue = i(:,:,3);
findredindex = (imagered>(2*imagegreen+2*imageblue));
[x,y] = find(findredindex == 1);
n=1;
for small = (5:length(x)-5);
xshort(n) = sum(x(small-4:small+5))/10;
yshort(n) = sum(y(small-4:small+5))/10;
n=n+1;
end
% convert to Celsius


   

h = 0;
for h = 1 : (length(xshort))
    timedatacorrected(h) = (yshort(h)- yintercepttime)/gradienttime ;
    tempdatacorrected(h) = -(xintercepttemp - xshort(h))/gradienttemp;
end
% convert to Celsius
tempdatacorrectedC = (tempdatacorrected-32)*5/9;
%Plot results
plot(timedatacorrected, tempdatacorrectedC)
%save data to .mat file with same name as image file
save(name, 'timedatacorrected', 'tempdatacorrectedC')
case 'I do not understand'
     help plottemp
end