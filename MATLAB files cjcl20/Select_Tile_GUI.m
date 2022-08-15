%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%TOP LEVEL FUNCTION - START HERE%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% This GUI function displays an image of the shuttle and graphs with
% buttons to select the desired graph to run  the simulation on. This takes
% the user to a second GUI where simulations can be configured and ran.




function varargout = Select_Tile_GUI(varargin)
% Initialisation code
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @Select_Tile_GUI_OpeningFcn, ...
                   'gui_OutputFcn',  @Select_Tile_GUI_OutputFcn, ...
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
% End initialization code - DO NOT EDIT


% --- Executes just before Select_Tile_GUI is made visible.
function Select_Tile_GUI_OpeningFcn(hObject, eventdata, handles, varargin)
% Plot image on axes
axes(handles.axes1)
i=imread(['Shuttlewithdiag.jpg']);
image(i)

%Get rid of ticks
set(gca,'Yticklabel',[]) 
set(gca,'Xticklabel',[])
% Choose default command line output for Select_Tile_GUI
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);


% --- Outputs from this function are returned to the command line.
function varargout = Select_Tile_GUI_OutputFcn(hObject, eventdata, handles) 

varargout{1} = handles.output;


% Exit button closes everything
function Exit_Button_Callback(hObject, eventdata, handles)
close all






%The following push buttons will set the name variable to the respective
%image, and input it into the plottemp function.
%Additionally, the action is displayed in the console to notify the user
function pushbutton2_Callback(hObject, eventdata, handles)
name = 'temp502';
disp(['Loading ', name])
plottempauto(name)

% --- Executes on button press in pushbutton3.
function pushbutton3_Callback(hObject, eventdata, handles)
name = 'temp590';
disp(['Loading ', name])
plottempauto(name)

% --- Executes on button press in pushbutton4.
function pushbutton4_Callback(hObject, eventdata, handles)
name = 'temp468';
disp(['Loading ', name])
plottempauto(name)

% --- Executes on button press in pushbutton5.
function pushbutton5_Callback(hObject, eventdata, handles)
name = 'temp597';
disp(['Loading ', name])
plottempauto(name)

% --- Executes on button press in pushbutton6.
function pushbutton6_Callback(hObject, eventdata, handles)
name = 'temp480';
disp(['Loading ', name])
plottempauto(name)

% --- Executes on button press in pushbutton7.
function pushbutton7_Callback(hObject, eventdata, handles)
name = 'temp850';
disp(['Loading ', name])
plottempauto(name)


% --- Executes on button press in pushbutton8.
function pushbutton8_Callback(hObject, eventdata, handles)
name = 'temp711';
disp(['Loading ', name])
plottempauto(name)

% --- Executes on button press in pushbutton9.
function pushbutton9_Callback(hObject, eventdata, handles)
name = 'temp730';
disp(['Loading ', name])
plottempauto(name)
