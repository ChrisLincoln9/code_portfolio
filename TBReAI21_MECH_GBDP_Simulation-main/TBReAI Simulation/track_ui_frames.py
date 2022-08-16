import tkinter as tk

class AccelerationPage(tk.Frame):
    "Track options for the Acceleration track"
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.track_length = tk.IntVar(self, value=100)
        self.track_width = tk.IntVar(self, value=3)
        self.cone_distance = tk.IntVar(self, value=3)

        self.columnconfigure(0, pad=3)
        self.columnconfigure(1, pad=3, weight=1)

        tk.Label(self, text="Track Length").grid(row=0,column=0)
        tk.Label(self, text="Track Width").grid(row=1,column=0)
        tk.Label(self, text="Cone Distance").grid(row=2,column=0)

        tk.Entry(self, textvariable = self.track_length).grid(row=0,column=1,sticky="nsew")
        tk.Entry(self, textvariable = self.track_width).grid(row=1,column=1,sticky="nsew")
        tk.Entry(self, textvariable = self.cone_distance).grid(row=2,column=1,sticky="nsew")

class SkidpadPage(tk.Frame):
    "Track options for the Skidpad track"
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.radius = tk.DoubleVar(self, value=9.125)
        self.track_width = tk.IntVar(self, value=3)
        self.num_cones = tk.IntVar(self, value=16)
        self.start_excess = tk.IntVar(self, value=1)

        self.columnconfigure(0, pad=3)
        self.columnconfigure(1, pad=3, weight=1)

        tk.Label(self, text="Radius").grid(row=0,column=0)
        tk.Label(self, text="Track Width").grid(row=1,column=0)
        tk.Label(self, text="Number of Cones").grid(row=2,column=0)
        tk.Label(self, text="Start Distance").grid(row=3,column=0)

        tk.Entry(self, textvariable = self.radius).grid(row=0,column=1,sticky="nsew")
        tk.Entry(self, textvariable = self.track_width).grid(row=1,column=1,sticky="nsew")    
        tk.Entry(self, textvariable = self.num_cones).grid(row=2,column=1,sticky="nsew")     
        tk.Entry(self, textvariable = self.start_excess).grid(row=3,column=1,sticky="nsew")

class FixedCircuitPage(tk.Frame):
    "Track options for the Fixed Circuit track"
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.straight_length = tk.IntVar(self, value=60)
        self.bend_radius = tk.IntVar(self, value=12)
        self.track_width = tk.IntVar(self, value=3)
        self.cone_distance = tk.IntVar(self, value=3)

        self.columnconfigure(0, pad=3)
        self.columnconfigure(1, pad=3, weight=1)

        tk.Label(self, text="Straight Length").grid(row=0,column=0)
        tk.Label(self, text="Bend Radius").grid(row=1,column=0)
        tk.Label(self, text="Track Width").grid(row=2,column=0)
        tk.Label(self, text="Cone Distance").grid(row=3,column=0)

        tk.Entry(self, textvariable = self.straight_length).grid(row=0,column=1,sticky="nsew")  
        tk.Entry(self, textvariable = self.bend_radius).grid(row=1,column=1,sticky="nsew")     
        tk.Entry(self, textvariable = self.track_width).grid(row=2,column=1,sticky="nsew")       
        tk.Entry(self, textvariable = self.cone_distance).grid(row=3,column=1,sticky="nsew")  

class RandomTrackPage(tk.Frame):
    "Track options for the Random Trackdrive track"
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.cone_distance = tk.IntVar(self, value=2)
        self.track_width = tk.IntVar(self, value=4)

        self.columnconfigure(0, pad=3)
        self.columnconfigure(1, pad=3, weight=1)

        tk.Label(self, text="Cone Distance").grid(row=0,column=0)  
        tk.Label(self, text="Track Width").grid(row=1,column=0)  

        tk.Entry(self, textvariable = self.cone_distance).grid(row=0,column=1,sticky="nsew")   
        tk.Entry(self, textvariable = self.track_width).grid(row=1,column=1,sticky="nsew")  