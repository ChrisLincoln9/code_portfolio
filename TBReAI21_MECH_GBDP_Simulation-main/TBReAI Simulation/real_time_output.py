import pickle
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class lidarAccelPlot:
    def initialise(self):
        self.fig = plt.figure()
        
        # Axes for LiDAR ouput
        self.lidarAx = self.fig.add_subplot(211, projection='polar')
        self.lidarAx.set_title('LiDAR output')
        self.lidarAx.set_rlim(0, 5.5)
        self.lidarAx.set_theta_zero_location('N')
        self.lidarAx.set_theta_direction(-1)
        self.lidarScatter, = self.lidarAx.plot([], [], marker=".", ls="")
        
        # Axes for accelerometer output
        self.accelAx = self.fig.add_subplot(212)
        self.accelAx.set_title('Acclerometer output')
        self.accelAx.set_xlabel('Simulation time / s')
        self.accelAx.set_ylabel('Acceleration / ms^-2')
        self.accelAx.set_xlim(0, 40)
        self.accelAx.set_ylim(-10, 10)
        self.accelLineX, = self.accelAx.plot([], [])
        self.accelLineY, = self.accelAx.plot([], [])
        self.accelLineX.set_label('X acceleration')
        self.accelLineY.set_label('Y acceleration')
        self.accelAx.legend()

# Load data
with open('globalData.pkl', 'rb') as f:
    lidarData, lidarDataPolar, accelData = pickle.load(f)

filename1 = '1 - Test.csv'
filename2 = '2 - Test.csv'

# Write data to csv
accelHeaders = ['Time (s)', 'X acceleration (ms^-2)', 'Y acceleration (ms^-2)', 'Z acceleration (ms^-2)']
a = pd.DataFrame(accelData)
a.to_csv(filename1, index=False, header=accelHeaders)
print('Data written to file: ', filename1)


c = pd.DataFrame()
for row in lidarDataPolar:
    d = pd.DataFrame(row.transpose())
    c = c.append(d)
c.to_csv(filename2, index=False)
print('Data written to file: ', filename2)

# Read data from csv
b = pd.read_csv(filename1)
t = b['Time (s)']
x = b['X acceleration (ms^-2)']
y = b['Y acceleration (ms^-2)']


e = pd.read_csv(filename2)

myplot = lidarAccelPlot()
myplot.initialise()

def animate(i):
        
    t_vals = t[0:i]
    y_vals = y[0:i]
    x_vals = x[0:i]
    
    theta_vals = e.iloc[2*i]
    r_vals = e.iloc[2*i+1]
    
    # plt.cla()
    # plt.plot(x_vals, y_vals)
    myplot.accelLineX.set_data(t_vals, x_vals)
    myplot.accelLineY.set_data(t_vals, y_vals)
    myplot.lidarScatter.set_data(theta_vals, r_vals)                

    return myplot.accelLineX, myplot.lidarScatter, myplot.accelLineY
    
ani = FuncAnimation(plt.gcf(), animate, frames = int(max(len(x),(len(e)/2))), interval = 50, repeat = False, blit = True)
plt.show()