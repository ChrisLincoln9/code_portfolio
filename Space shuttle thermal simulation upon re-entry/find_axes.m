function [ox,oy,maxx,maxy] = find_axes(name)
%The following function locates the pixel coordiantions of the origin
%[ox,oy] and the ends of the x and y axes, maxx, maxy respectively.

%Load the image.
i=imread([name '.jpg']);
figure (4);
image(i);

%Load each color group.
imagered = i(:,:,1);
imagegreen = i(:,:,2);
imageblue = i(:,:,3);

%Create a matrix of which pixels are black with a '1', and which are not with
% a '0'.
findblackindex = (imagered < 150 & imagegreen < 150  & imageblue < 150);
%Find which coloum and row contain the most black values, as this is always
%occurs at the axis.
Sx = sum(findblackindex);
Sy = sum(transpose(findblackindex));

%Find origin coordinates with max Sx and max Sy.
ox = find(Sx==max(Sx));
oy = find(Sy==max(Sy));
[x,y] = find(findblackindex == 1);




%Find the last black pixel of each axis.
maxx = 73+find(~findblackindex(oy,75:end),1); 
maxy = 1 + find(~findblackindex(1:75,ox),1,'last');
%The use of '75' is specific to the resolution of the colleciton of graph
%photos, this may be edited if applied to a different group a graphs.

