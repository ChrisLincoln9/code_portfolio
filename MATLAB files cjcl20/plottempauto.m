
function plottempauto(name)


[ox,oy,maxx,maxy] = find_axes(name);

%All axes are between 0 and 2000
timedata_axis_ends = [0,0,2000];
tempdata_axis_ends = [0,2000,0];

%Create matrices
 timedatascale = zeros(3,2);
 tempdatascale = zeros(3,2);
 
%the following 8 assingments set the 'datascale' variables to the same
%format as the non-automatic plottemp function. This is so that the rest of
%the code does not need to be modifdied.
    timedatascale(1,2) = [ox];
    timedatascale(2,2) = [ox];
    timedatascale(3,1) = [timedata_axis_ends(3)];
    timedatascale(3,2) = [maxx];
    
    tempdatascale(1,2) = [oy];
    tempdatascale(2,1) = [tempdata_axis_ends(2)];
    tempdatascale(2,2) = [maxy];
    tempdatascale(3,2) = [oy];

%Calculating gradient of pixels/temperature and
%the size of the translation needed to scale and correct the axis
tempindexmax = max(tempdatascale);
tempindexmin = min(tempdatascale);
gradienttemp = -1/((tempindexmax(1) - tempindexmin(1))/(tempindexmax(2)-tempindexmin(2)));
xintercepttemp = tempdatascale(1,2);

%Similarly, calculating gradient of pixels/time and
%the size of the translation needed to scale and correct the axis

timeindexmax = max(timedatascale);
timeindexmin = min(timedatascale);
gradienttime = (timeindexmax(2)-timeindexmin(2))/(timeindexmax(1)-timeindexmin(1));
yintercepttime = timedatascale(1,2);


%Load the image and find the coordiantes of red pixels.

i=imread([name '.jpg']);
imagered = i(:,:,1);
imagegreen = i(:,:,2);
imageblue = i(:,:,3);
findredindex = (imagered>(2*imagegreen+2*imageblue));
[x,y] = find(findredindex == 1);
n=1;
%The following for loop decreases the number of points by factor 10,
%while taking the 10 point moving average of the data to smooth it.
for small = (5:10:length(x)-5)
xshort(n) = sum(x(small-4:small+5))/10;
yshort(n) = sum(y(small-4:small+5))/10;
n=n+1;
end



%The following for loop scales the [x,y] pixel points into [time,temperature] data points.
h = 0;
for h = 1 : (length(xshort))
    timedatacorrected(h) = (yshort(h)- yintercepttime)/gradienttime ;
    tempdatacorrected(h) = -(xintercepttemp - xshort(h))/gradienttemp;
end

% convert to Celsius
tempdatacorrectedC =(tempdatacorrected-32)*5/9;
%Plot results
plot(timedatacorrected, tempdatacorrectedC)
xlabel ('Time (s)')
ylabel ('Temperature (C)')
%save data to .mat file with same name as image file
save(name, 'timedatacorrected', 'tempdatacorrectedC')

%Quest dialog for user interaction:

confirmgraph = questdlg('Would you like to continue with the graph generated?',...
    'Confirm graph',...
    'Yes', 'No, the graph looks incorrect!', 'No, I want to select a different tile' , 'Yes');
switch confirmgraph
    case 'Yes'
        global tilenumber
        %Set tile name
        tilenumber = name(end-2:end);
        %Open next GUI
        close all
        Shuttle_GUI
       
    case 'No, the graph looks incorrect!'
    %Resorts back to manual axis selection (Still automatic red graph
    %finder)
    close Figure 4
    plottemp(name)
    
    case 'No, I want to select a different tile'
        %Close figure to allow new selection
        close Figure 4
end
