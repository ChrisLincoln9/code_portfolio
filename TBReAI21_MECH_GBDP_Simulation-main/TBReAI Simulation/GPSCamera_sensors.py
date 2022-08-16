import cv2
import matplotlib.pyplot as plt
import numpy as np
import time
import sim
import PIL.Image as Image
import io
from skimage.util import img_as_ubyte
import track_generation_functions as tg
import CL_processing_funcs as Process
from generalHelperFunctions import globalData
from generalHelperFunctions import PlotSelect
#-----------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------
#Callback Functions
def posCB(msg):
    return_code = msg[0]
    globalData.abs_pos = msg[1]
    pos_entry = Process.gps_pos_noise(True, msg[1])
    if return_code and msg[1] and globalData.time:
        pos_entry = [globalData.time[-1]] + pos_entry
        globalData.pos.append(pos_entry)
    else:
        print('No position data')

def velCB(msg):
    return_code = msg[0]
    globalData.abs_vel = msg[1]
    vel_entry = Process.gps_vel_noise(msg[1])
    if return_code and msg[1] and globalData.time:
        vel_entry = [globalData.time[-1]] + vel_entry
        globalData.vel.append(vel_entry)
    else:
        print('No velocity data')

def rightcameraCB(msg):
    return_code = msg[0]
    if return_code and msg[1]:
        new_camera_signal = np.array(sim.simxUnpackFloats(msg[1]), dtype=np.float64)
        new_camera_signal = new_camera_signal.reshape(256,512,3)
        new_camera_signal = img_as_ubyte(new_camera_signal)
        globalData.current_right_image = new_camera_signal
        #plt.figure(2)
        #plt.imshow(abs(new_camera_signal), origin='lower')
        #plt.show()

    else:
        print('No Camera data')


def simStepDoneCB(msg):
    globalData.time.append(msg[1][b'simulationTime'])
    globalData.doNextStep = True

#-----------------------------------------------------------------------------------------------------------------

#Velocity and Position plot function
class GpsVelPosPlot:
    def initialise(self):
        #Get cone positions
        start_cones, left_cones, right_cones = tg.Acceleration_Positions(track_length=100, track_width=3,cone_distance=3)# get global cones

        self.fig = plt.figure()
        if not PlotSelect.suppress_vel_plot:
            #Velocity Figure
            self.vel_ax = self.fig.add_subplot(211)
            self.vel_ax.set_title('GPS Velocity')
            self.vel_ax.set_xlabel('Simulation time / s')
            self.vel_ax.set_ylabel('Velocity / ms^-1')
            self.vel_ax.set_xlim(0, 20)
            self.vel_ax.set_ylim(-1, 10)
            self.vel_lineX, = self.vel_ax.plot([], [])
            self.vel_lineY, = self.vel_ax.plot([], [])
            self.vel_lineX.set_label('X Velocity')
            self.vel_lineY.set_label('Y Velocity')
            self.vel_ax.legend()
        if not PlotSelect.suppress_pos_plot:
            #Position Figure
            self.pos_ax = self.fig.add_subplot(212)
            self.pos_ax.set_title('GPS Position')
            self.pos_ax.set_xlabel('X position(m)')
            self.pos_ax.set_ylabel('Y position(m)')
            self.pos_lineX, = self.pos_ax.plot([], [])
            self.pos_lineY, = self.pos_ax.plot([], [])
            self.pos_lineX.set_label('X Position')
            self.pos_lineY.set_label('Y Position')
            self.pos_ax.legend()
            #Plot cones
            left_xy = Process.extract_coords(left_cones)
            right_xy = Process.extract_coords(right_cones)
            self.pos_ax.scatter(left_xy[0],left_xy[1], linewidths=0.01) #add color
            self.pos_ax.scatter(right_xy[0], right_xy[1],linewidths=0.01)  #add color
            self.pos_ax.scatter(start_cones[0].x, start_cones[0].y,linewidths=0.02)  # add color
            self.pos_ax.scatter(start_cones[1].x, start_cones[1].y, linewidths=0.02)  # add color






def updateLivePlot(livePlot):
    if globalData.vel and globalData.time and not PlotSelect.suppress_vel_plot:
        # Convert to array to allow multidimensional slicing, and update live plot
        vel_data_array = np.array(globalData.vel)
        livePlot.vel_lineX.set_data(vel_data_array[:,0], vel_data_array[:,1])
        livePlot.vel_lineY.set_data(vel_data_array[:,0], vel_data_array[:,2])
    if globalData.pos and globalData.time and not PlotSelect.suppress_pos_plot:
        # Convert to array to allow multidimensional slicing, and update live plot
        pos_data_array = np.array(globalData.pos)
        livePlot.pos_lineX.set_data(pos_data_array[:,1], pos_data_array[:,2])
    plt.draw()
    plt.waitforbuttonpress(0.05)
#-----------------------------------------------------------------------------------------------------------------






















