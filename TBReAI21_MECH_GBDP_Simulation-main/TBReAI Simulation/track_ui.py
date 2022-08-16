import tkinter as tk
from tkinter.ttk import Combobox
import track_main as tm
import track_functions.track_random_function as tr
import track_functions.track_generation_functions as tg
import matplotlib.pyplot as plt
import track_ui_frames as fr
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pickle

class MyWindow(tk.Tk):
    "Main window for the UI"
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('TBReAI Simulation Setup')
        self._frame = None
        self._figure = None
        self.cone_noise_radius = tk.DoubleVar(self, value=0.1)
        self.terrain_height = tk.DoubleVar(self, value=0.2)
        self.max_puddle_depth = tk.DoubleVar(self, value=0.05)
        self.start_cones = []
        self.left_cones = []
        self.right_cones = []

        # Configuration of the overall grid
        self.columnconfigure(0, pad=3)
        self.columnconfigure(1, pad=3)
        self.columnconfigure(2, pad=3, weight=1)
        self.rowconfigure(0, pad=3)
        self.rowconfigure(1, pad=3)
        self.rowconfigure(2, pad=3)
        self.rowconfigure(3, pad=3)
        self.rowconfigure(4, pad=3)
        self.rowconfigure(5, pad=3)
        self.rowconfigure(6, pad=3)
        self.rowconfigure(7, pad=3)
        self.rowconfigure(8, pad=3)
        self.rowconfigure(9, pad=3)
        self.rowconfigure(10, pad=3,weight=1)

        # Buttons to run generation functions
        self.btn_Generate = tk.Button(self, text='Generate in Sim', command=self.generate_environment, anchor='w').grid(row=0,column=0,columnspan=2,sticky="nsew")
        self.btn_Visualise = tk.Button(self, text='Generate Track', command=self.visualise_track, anchor='w').grid(row=1,column=0,columnspan=2,sticky="nsew")

        # Cone texture
        self.lbl_ConeTexture = tk.Label(self, text="Cone Texture").grid(row=2,column=0) 
        self.combo_ConeTexture = Combobox(self, values=('A', 'B', 'C', 'D'))
        self.combo_ConeTexture.current(0)
        self.combo_ConeTexture.grid(row=2,column=1)

        # Generate terrain?
        self.lbl_Terrain = tk.Label(self, text="Generate terrain?", anchor='w').grid(row=3,column=0)  
        self.combo_Terrain= Combobox(self, values=('True','False'))
        self.combo_Terrain.current(0)
        self.combo_Terrain.grid(row=3,column=1,sticky="nsew")

        # Terrain texture
        self.lbl_TerrainTexture = tk.Label(self, text="Terrain Texture", anchor='w').grid(row=4,column=0) 
        self.combo_TerrainTexture = Combobox(self, values=('1','2','3','4','5','6','7'))
        self.combo_TerrainTexture.current(0)
        self.combo_TerrainTexture.grid(row=4,column=1,sticky="nsew")

        # Terrain height variance
        self.lbl_TerrainHeight = tk.Label(self, text="Terrain Height", anchor='w').grid(row=5,column=0)  
        self.ent_TerrainHeight = tk.Entry(self, textvariable = self.terrain_height).grid(row=5,column=1,sticky="nsew")

        # Puddles?
        self.lbl_Puddle = tk.Label(self, text="Puddles?", anchor='w').grid(row=6,column=0)  
        self.combo_Puddle= Combobox(self, values=('True','False'))
        self.combo_Puddle.current(0)
        self.combo_Puddle.grid(row=6,column=1,sticky="nsew")

        # Puddle depth
        self.lbl_PuddleDepth = tk.Label(self, text="Puddle Depth", anchor='w').grid(row=7,column=0)  
        self.ent_PuddleDepth = tk.Entry(self, textvariable = self.max_puddle_depth).grid(row=7,column=1,sticky="nsew")   

        # Cone position noise
        self.btn_AddNoise = tk.Button(self, text='Add Cone Position Noise', command=self.add_cone_position_noise).grid(row=8,column=0)
        self.ent_AddNoise = tk.Entry(self, textvariable = self.cone_noise_radius).grid(row=8,column=1)

        # Track selection
        self.combo_Track = Combobox(self, values=('Acceleration', 'Skidpad', 'Fixed Circuit', 'Random Trackdrive'))
        self.combo_Track.current(0)
        self.combo_Track.bind("<<ComboboxSelected>>",self.track_combobox_change)
        self.combo_Track.grid(row=9,column=0,columnspan=2,sticky="nsew")

        # Initialise the user interface
        self.switch_frame(fr.AccelerationPage)
        self.visualise_track()
        self.plot_figure()

    def track_combobox_change(self,event):
        '''
        Description
        -----------
        Changes track settings depending on chosen track
        
        Parameters
        -----------
        self: MyWindow object
            MyWindow object
        '''

        selected_track = self.combo_Track.get()
        if selected_track == 'Acceleration':
            self.switch_frame(fr.AccelerationPage)
        elif selected_track == 'Skidpad':
            self.switch_frame(fr.SkidpadPage)
        elif selected_track == 'Fixed Circuit':
            self.switch_frame(fr.FixedCircuitPage)
        elif selected_track == 'Random Trackdrive':
            self.switch_frame(fr.RandomTrackPage)

    def switch_frame(self, frame_class):
        '''
        Description
        -----------
        Destroys current frame and replaces it with a new one
        
        Parameters
        -----------
        self: MyWindow object
            MyWindow object
        frame_class: track_ui_frames object
            settings to load up according to chosen track layout
        '''

        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid(row=10,column=0,columnspan=2,sticky="nsew")
        
    def generate_environment(self):
        '''
        Description
        -----------
        Generates environment within CoppeliaSim and then closes user interface
        
        Parameters
        -----------
        self: MyWindow object
            MyWindow object
        '''

        terrain = bool(self.combo_Terrain.get() == 'True')
        puddle = bool(self.combo_Puddle.get() == 'True')
        cone_texture = self.combo_ConeTexture.get()
        terrain_texture = self.combo_TerrainTexture.get()
        
        #try:
        tm.track_initialise(self.start_cones,self.left_cones,self.right_cones,cone_texture,terrain,terrain_texture,self.terrain_height.get(),puddle,self.max_puddle_depth.get())
        # except Exception as e:
        #     print(e)

        # Saves cone locations to be used by the main script
        with open("cone_locations.pkl", "wb") as f:
            pickle.dump([self.start_cones, self.left_cones, self.right_cones], f)

        self.destroy()

    def add_cone_position_noise(self):
        '''
        Description
        -----------
        Adds cone position noise to each cone
        
        Parameters
        -----------
        self: MyWindow object
            MyWindow object
        '''

        if len(self.start_cones) > 0 and len(self.left_cones) > 0 and len(self.right_cones) > 0:
            for each in self.start_cones:
                each.apply_noise(self.cone_noise_radius.get())   
            for each in self.left_cones:
                each.apply_noise(self.cone_noise_radius.get())
            for each in self.right_cones:
                each.apply_noise(self.cone_noise_radius.get())

        self.plot_figure()

    def visualise_track(self):
        '''
        Description
        -----------
        Updates the graph plot with new settings
        
        Parameters
        -----------
        self: MyWindow object
            MyWindow object
        '''

        selected_track = self.combo_Track.get()
        if selected_track == 'Acceleration':
            self.start_cones,self.left_cones,self.right_cones = tg.acceleration_positions(self._frame.track_length.get(),self._frame.track_width.get(),self._frame.cone_distance.get())
        elif selected_track == 'Skidpad':
            self.start_cones,self.left_cones,self.right_cones = tg.skidpad_positions(self._frame.radius.get(),self._frame.track_width.get(),self._frame.num_cones.get(),self._frame.start_excess.get())
        elif selected_track == 'Fixed Circuit':
            self.start_cones,self.left_cones,self.right_cones = tg.fixed_circuit_positions(self._frame.straight_length.get(),self._frame.bend_radius.get(),self._frame.track_width.get(),self._frame.cone_distance.get())
        elif selected_track == 'Random Trackdrive':
            self.start_cones,self.left_cones,self.right_cones = tr.random_track_generation(self._frame.cone_distance.get(),self._frame.track_width.get())

        self.plot_figure()

    def plot_figure(self):
        '''
        Description
        -----------
        Plots the track using matplotlib
        
        Parameters
        -----------
        self: MyWindow object
            MyWindow object
        '''

        # Separating lists into the correct format for plotting
        startX = list([point.x for point in self.start_cones])    
        startY = list([point.y for point in self.start_cones])   
        leftX = list([point.x for point in self.left_cones])     
        leftY = list([point.y for point in self.left_cones])  
        rightX = list([point.x for point in self.right_cones])    
        rightY = list([point.y for point in self.right_cones]) 

        # Plotting of graph
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.scatter(startX,startY, marker='X')
        ax.scatter(leftX,leftY, marker='x')
        ax.scatter(rightX,rightY, marker='+')
        ax.set_aspect('equal')  
        ax.set_xlabel('x (m)')
        ax.set_ylabel('y (m)')

        # Creation of Tkinter widget
        new_figure = FigureCanvasTkAgg(fig,self).get_tk_widget()
        if self._figure is not None:
            self._figure.destroy()
        self._figure = new_figure   
        self._figure.grid(row=0,column=2,rowspan=11)
    
app = MyWindow()
app.mainloop()