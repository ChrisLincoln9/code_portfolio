function varargout = GUI(varargin)
%Defualt gui code:
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @GUI_OpeningFcn, ...
                   'gui_OutputFcn',  @GUI_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end

function GUI_OpeningFcn(hObject, eventdata, handles, varargin)
%Unedited default gui function
global starting_velocity A1 A2
  A1 = 0.012;
  A2 = 0.009;
  starting_velocity = 75;
handles.output = hObject;
guidata(hObject, handles);

function varargout = GUI_OutputFcn(hObject, eventdata, handles) 
varargout{1} = handles.output;

function GO_Callback(hObject, eventdata, handles)
global Target_Distance combinedString Impact_Velocity %Global variables taken from A2SolverRK4
Rounded_target_distance = round(Target_Distance*10^2)/10^2; %Rounds to 2 dp
N = 2;
theta = A2SolverRK4_3(Rounded_target_distance,N);
axes(handles.axes1) %Plots on big axes
PlotResults(0,theta,0.0001,3,N);
axes(handles.axes2) %Plots on small axes (X-Y)
PlotResults(0,theta,0.0001,3,N);
view(2)
legend(handles.axes2,'off')
axes(handles.axes3) %Plots on small axes (X-Z)
PlotResults(0,theta,0.0001,3,N);
view(0,0)
legend(handles.axes3,'off')
set(handles.answerstring, 'string',combinedString)
set(handles.text15, 'string',Impact_Velocity)

guidata(hObject,handles);

% --- Executes on slider movement.
function Slider_XDistance_Callback(hObject, eventdata, handles)
global Target_Distance
Target_Distance = get(hObject,'value');
set(handles.enterdistance,'string',num2str(Target_Distance));
guidata(hObject,handles);
%Communications with enterdistance edit text box

% --- Executes during object creation, after setting all properties.
function Slider_XDistance_CreateFcn(hObject, eventdata, handles)
%Unedited default gui function
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end

function enterdistance_Callback(hObject, eventdata, handles)
editdistance = get(hObject,'string');
global Target_Distance
Target_Distance = str2num(editdistance);
disp(Target_Distance)
set(handles.Slider_XDistance,'value',str2num(editdistance));
guidata(hObject,handles);
%Communications with Slider_XDistance

% --- Executes during object creation, after setting all properties.
function enterdistance_CreateFcn(hObject, eventdata, handles)
%Unedited default gui function
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in Clearaxesbutton.
function Clearaxesbutton_Callback(hObject, eventdata, handles)
axes(handles.axes1)
close all
GUI %Restart gui to clear axes
global Launch_Yaw_Angle
Launch_Yaw_Angle=0; %Prevents Launch_Yaw_ANgle to start undefined



% --- Executes during object creation, after setting all properties.
function answerstring_CreateFcn(hObject, eventdata, handles)
%Unedited default gui function


function answerstring_Callback(hObject, eventdata, handles)
%Unedited default gui function

% --- Executes on selection change in colorselect.
function colorselect_Callback(hObject, eventdata, handles)
global colorshortname
contents = cellstr(get(hObject,'String'));
colorchoice = contents(get(hObject,'value'));
if (strcmp(colorchoice,'Yellow'))
    colorshortname = 'y';
elseif (strcmp(colorchoice,'Magenta'))
    colorshortname = 'm';
elseif (strcmp(colorchoice,'Cyan'))
    colorshortname = 'c';
elseif (strcmp(colorchoice,'Red'))
    colorshortname = 'r';
elseif (strcmp(colorchoice,'Green'))
    colorshortname = 'g';
elseif (strcmp(colorchoice,'Blue'))
    colorshortname = 'b';
elseif (strcmp(colorchoice,'White'))
    colorshortname = 'w';
elseif (strcmp(colorchoice,'Black'))
    colorshortname = 'k';
end  
%List of all 3 bit colors, global variable used by A2SolverRK4 plotting.

% --- Executes during object creation, after setting all properties.
function colorselect_CreateFcn(hObject, eventdata, handles)
%Unedited default gui function
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


function editYawAngle_Callback(hObject, eventdata, handles)
editangle = get(hObject,'string');
global Launch_Yaw_Angle
Launch_Yaw_Angle = str2num(editangle);
disp(Launch_Yaw_Angle)
set(handles.Slider_YawAngle,'value',str2num(editangle));
guidata(hObject,handles);

% --- Executes during object creation, after setting all properties.
function editYawAngle_CreateFcn(hObject, eventdata, handles)
%Unedited default gui function
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on slider movement.
function Slider_YawAngle_Callback(hObject, eventdata, handles)
global Launch_Yaw_Angle
Launch_Yaw_Angle = get(hObject,'value')
set(handles.editYawAngle,'string',num2str(Launch_Yaw_Angle));
guidata(hObject,handles);


% --- Executes during object creation, after setting all properties.
function Slider_YawAngle_CreateFcn(hObject, eventdata, handles)
%Unedited default gui function
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes on button press in togglebutton1.
function togglebutton1_Callback(hObject, eventdata, handles)
global starting_velocity A1 A2
a = get(hObject,'Value');
if a == 1
    starting_velocity = 50;
    A1 = 0.00283;
    A2 = 0.00283;
 set(handles.Slider_XDistance,'max',8);
else
  A1 = 0.012;
  A2 = 0.009;
  starting_velocity = 75;
  set(handles.Slider_XDistance,'Value',0)
  set(handles.enterdistance,'string',0)
  set(handles.Slider_XDistance,'max',2.45);
end
