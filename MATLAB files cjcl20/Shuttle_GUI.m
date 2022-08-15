%This GUI handles all the available simulations, using the selecteds tile
%from the previous GUI.
% Capabilities:
% -Plot temperature against thickness and time for given parameters
% -Test stability and accuracy of methods against eachother for thickness step and time step
% -Test the maximum internal temperature for safety of passengers/cargo.
function varargout = Shuttle_GUI(varargin)

gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @Shuttle_GUI_OpeningFcn, ...
                   'gui_OutputFcn',  @Shuttle_GUI_OutputFcn, ...
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

% --- Executes just before Shuttle_GUI is made visible.
function Shuttle_GUI_OpeningFcn(hObject, eventdata, handles, varargin)
%Fetch and declare global variables:
global tilenumber maxtime Ntimesteps tilethickness Ntilesteps method 
global Ntiletests minthickness maxthickness
% Default values
maxtime = 4000;
Ntimesteps = 801;
tilethickness = 0.0572;
Ntilesteps = 32;
Ntiletests = 50;
minthickness = 0.02;
maxthickness = 0.10;
method = 'Crank-Nicolson';

%Shows current tile selection:
txt = ['Current tile: ', tilenumber];
set(handles.currenttile,'string',txt);


% Choose default command line output for Shuttle_GUI
handles.output = hObject;
% Update handles structure
guidata(hObject, handles);


% --- Outputs from this function are returned to the command line.
function varargout = Shuttle_GUI_OutputFcn(hObject, eventdata, handles) 

varargout{1} = handles.output;


% --- Executes on selection change in popupmenu1.
function popupmenu1_Callback(hObject, eventdata, handles)
%Set global variable 'method'
global method
%Fetch string from cell
contents = cellstr(get(hObject,'String'));
methodchoice = contents(get(hObject,'value'));

%Set method name based on pop-up menu selection.
if (strcmp(methodchoice,'Forward Differencing'))
    method= 'Forward';
elseif (strcmp(methodchoice,'Backward Differencing'))
    method= 'Backward';
elseif (strcmp(methodchoice,'DuFort-Frankel'))
    method= 'Dufort-Frankel';
elseif (strcmp(methodchoice,'Crank-Nicolson'))
    method= 'Crank-Nicolson';
end


function popupmenu1_CreateFcn(hObject, eventdata, handles)

if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in simulatebutton.
function simulatebutton_Callback(hObject, eventdata, handles)
%This button runs the simulation using the following global variables,
%plotting it on axis 1.
global maxtime Ntimesteps tilethickness Ntilesteps method tilenumber
axes(handles.axes1)
shuttle(maxtime, Ntimesteps, tilethickness, Ntilesteps, method, true, tilenumber);


function editmaxtime_Callback(hObject, eventdata, handles)
%Fetch string from cell and set it as global variable for use elsewhere
edit = get(hObject,'string');
global maxtime
maxtime = str2num(edit);
disp(maxtime)


% --- Executes during object creation, after setting all properties.
function editmaxtime_CreateFcn(hObject, eventdata, handles)
%Default code
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function editNtimesteps_Callback(hObject, eventdata, handles)
%Fetch string from cell and set it as global variable for use elsewhere
edit = get(hObject,'string');
global Ntimesteps
Ntimesteps = str2num(edit);
disp(Ntimesteps)


% --- Executes during object creation, after setting all properties.
function editNtimesteps_CreateFcn(hObject, eventdata, handles)
%Default code
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edittilethickness_Callback(hObject, eventdata, handles)
%Fetch string from cell and set it as global variable for use elsewhere
edit = get(hObject,'string');
global tilethickness
tilethickness = str2num(edit);
disp(tilethickness)



% --- Executes during object creation, after setting all properties.
function edittilethickness_CreateFcn(hObject, eventdata, handles)
%Default code
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function editNtilesteps_Callback(hObject, eventdata, handles)
%Fetch string from cell and set it as global variable for use elsewhere
edit = get(hObject,'string');
global Ntilesteps
Ntilesteps = str2num(edit);
disp(Ntilesteps)


% --- Executes during object creation, after setting all properties.
function editNtilesteps_CreateFcn(hObject, eventdata, handles)
%Default code
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in reselect.
function reselect_Callback(hObject, eventdata, handles)
close all
Select_Tile_GUI


% --- Executes during object creation, after setting all properties.
function currenttile_CreateFcn(hObject, eventdata, handles)
%Default code

% --- Executes on button press in thicknesssteptestbutton.
function thicknesssteptestbutton_Callback(hObject, eventdata, handles)
%Run nx stability test on axes 2.
axes(handles.axes2)
nx_stability_test

function timesteptestbutton_Callback(hObject, eventdata, handles)
%Run nt stability test on axes 2.
axes(handles.axes2)
dt_stability_test
function timesteptestbutton_CreateFcn(hObject, eventdata, handles)


% --- Executes on button press in runsafteybutton.
function runsafteybutton_Callback(hObject, eventdata, handles)
%Run tile thickness safety test on axes 2.
axes(handles.axes2)
tilethicknesstest



function editmaxthickness_Callback(hObject, eventdata, handles)
%Fetch string from cell and set it as global variable for use elsewhere
edit = get(hObject,'string');
global maxthickness
maxthickness = str2num(edit);
disp(maxthickness)


% --- Executes during object creation, after setting all properties.
function editmaxthickness_CreateFcn(hObject, eventdata, handles)
% Default code
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function editminthickness_Callback(hObject, eventdata, handles)
%Fetch string from cell and set it as global variable for use elsewhere
edit = get(hObject,'string');
global minthickness
minthickness = str2num(edit);
disp(minthickness)


% --- Executes during object creation, after setting all properties.
function editminthickness_CreateFcn(hObject, eventdata, handles)
% Default code.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function editthickstepssaftey_Callback(hObject, eventdata, handles)
%Fetch string from cell and set it as global variable for use elsewhere
edit = get(hObject,'string');
global Ntiletests
Ntiletests = str2num(edit);
disp(Ntiletests)


% --- Executes during object creation, after setting all properties.
function editthickstepssaftey_CreateFcn(hObject, eventdata, handles)
% Default code
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in pushbutton6.
function pushbutton6_Callback(hObject, eventdata, handles)
%Close and re-open gui, useful incase of error.
close all
Shuttle_GUI
