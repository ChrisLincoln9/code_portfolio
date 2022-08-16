import matplotlib.pyplot as plt
import numpy as np
from generalHelperFunctions import globalData
import generalHelperFunctions as General
import CL_processing_funcs as Process
from skimage.util import img_as_ubyte
import math
from scipy.spatial.transform import Rotation as R

class SensorPlotFigures:
    """
    Initialises plots for output data from LiDAR, accelerometer, gyroscope, 
    and GPS. These may then be updated in real-time.
    
    Parameters
    ----------
    None

    Returns
    -------
    None. 
    """
    def __init__(self):
        self.suppress_live_plot = False
        self.suppress_lidar_plot = False
        self.suppress_accel_plot = False
        self.suppress_gyro_plot = False
        self.suppress_pos_plot = False
        self.suppress_vel_plot = False
        self.suppress_camera_data = True
        self.suppress_cone_distance = False

        self.start_cones = globalData.start_cones
        self.right_cones = globalData.right_cones
        self.left_cones = globalData.left_cones

    def create_figure(self):
        self.fig = plt.figure(3)
        if not self.suppress_lidar_plot:
            # Axes for LiDAR ouput
            self.lidarAx = self.fig.add_subplot(231, projection='polar')
            self.lidarAx.set_title('LiDAR output')
            self.lidarAx.set_rlim(0, 5500)
            self.lidarAx.set_yticklabels([])
            self.lidarAx.set_theta_zero_location('N')
            self.lidarAx.set_theta_direction(-1)
            self.lidarScatter, = self.lidarAx.plot([], [], marker=".", ls="")
        if not self.suppress_accel_plot:
            # Axes for accelerometer output
            self.accelAx = self.fig.add_subplot(233)
            self.accelAx.set_title('Acclerometer output')
            self.accelAx.set_xlabel('Simulation time / s')
            self.accelAx.set_ylabel('Acceleration / ms^-2')
            self.accelAx.set_xlim(0, 20)
            self.accelAx.set_ylim(-10, 10)
            self.accelLineX, = self.accelAx.plot([], [])
            self.accelLineY, = self.accelAx.plot([], [])
            self.accelLineX.set_label('X acceleration')
            self.accelLineY.set_label('Y acceleration')
            self.accelAx.legend()
        if not self.suppress_gyro_plot:
            self.gyroAx = self.fig.add_subplot(232, projection='3d')
            self.gyroAx.set_title('Gyro output')
            self.gyroAx.set_xlim(-1,1)
            self.gyroAx.set_ylim(-1,1)
            self.gyroAx.set_zlim(-1,1)
            self.gyroAx.set_xticks([])
            self.gyroAx.set_yticks([])
            self.gyroAx.set_zticks([])
            self.gyroAx.xaxis.pane.set_alpha(1)
            self.gyroAx.yaxis.pane.set_alpha(1)
            self.gyroAx.zaxis.pane.set_alpha(1)
            self.gyroAx.xaxis.pane.set_edgecolor('#000000')
            self.gyroAx.yaxis.pane.set_edgecolor('#000000')
            self.gyroAx.zaxis.pane.set_edgecolor('#000000')
            self.rollAxisCoords = np.array([[1,0,0],[-1,0,0],[-0.9,-0.05,0],[-1,0,0],[-0.9,0.05,0]])
            self.pitchAxisCoords = np.array([[0,-1,0],[0,1,0]])
            self.yawAxisCoords = np.array([[0,0,-1], [0,0,1]])
            self.gyroAx.rollAxis, = self.gyroAx.plot(self.rollAxisCoords[:,0], self.rollAxisCoords[:,1], self.rollAxisCoords[:,1], color='k', linewidth=2)
            self.gyroAx.pitchAxis, = self.gyroAx.plot(self.pitchAxisCoords[:,0], self.pitchAxisCoords[:,1], self.pitchAxisCoords[:,2], color='k')
            self.gyroAx.yawAxis, = self.gyroAx.plot(self.yawAxisCoords[:,0], self.yawAxisCoords[:,1], self.yawAxisCoords[:,2], color='b', linestyle='--')
            self.gyroAx.label = self.fig.text(x=0.42, y=0.52, s='yaw = 0°, \npitch = 0°, \nroll = 0°', fontsize=9,transform=self.fig.transFigure)

        if not self.suppress_vel_plot:
            #Velocity Figure
            if not self.suppress_accel_plot:
                self.vel_ax = self.fig.add_subplot(236, sharex = self.accelAx)
            if self.suppress_accel_plot:
                self.vel_ax = self.fig.add_subplot(236)
            self.vel_ax.set_title('Velocity output')
            self.vel_ax.set_title('Speed')
            self.vel_ax.set_xlabel('Time')
            self.vel_ax.set_ylabel('Speed(m/s)')
            self.vel_ax.set_ylim(0, 10)
            self.vel_ax.set_xlim(0, 20)
            self.speed_text = self.vel_ax.text(1,1, str('0'), c = 'Red', fontsize = '12')
            self.vel_line, = self.vel_ax.plot([], [])
        if not self.suppress_pos_plot:
            #Position Figure
            self.pos_ax = self.fig.add_subplot(223)
            self.pos_ax.set_title('GPS Position')
            self.pos_ax.set_xlabel('X position(m)')
            self.pos_ax.set_ylabel('Y position(m)')
            self.pos_line, = self.pos_ax.plot([], [])


            #Plot cones
            left_xy = Process.extract_coords(self.left_cones)
            right_xy = Process.extract_coords(self.right_cones)
            print(left_xy[0])
            self.pos_ax.scatter(left_xy[0],left_xy[1], c = 'blue', linewidths=0.01) #add color
            self.pos_ax.scatter(right_xy[0], right_xy[1], c = 'yellow', linewidths=0.01)  #add color
            self.pos_ax.scatter(self.start_cones[0].x, self.start_cones[0].y, c = 'orange', linewidths=0.02)  # add color
            self.pos_ax.scatter(self.start_cones[1].x, self.start_cones[1].y, c = 'orange',  linewidths=0.02)  # add color

class AGLNoise:
    """
    Holds data for the noise parameters of the accelerometer, gyroscope, and
    LiDAR. These parameters have been taken from the technical specifications
    of the relevant sensors.
    Parameters
    ----------
    None

    Returns
    -------
    None. 
    """
    def __init__(self):
        self.ignore = True
        self.accel_bias = np.zeros((1,3))
        self.accel_gain = np.ones((1,3))
        self.accel_random_walk_density = 57e-6 # g / sqrt(Hz)
        self.accel_bias_stability = 5e-3 # g
        self.accel_gain_stability = 1e-3 # Unitless (gain)
        
        self.gyro_bias = np.zeros((1,3))
        self.gyro_gain = np.ones((1,3))
        self.gyro_random_walk = np.zeros((1,3))
        self.gyro_random_walk_density = 0.025 # deg / sqrt(s). Given as 0.15 deg / sqrt(hr)
        self.gyro_bias_stability = 0.2 # deg / s
        self.gyro_gain_stability = 5e-4 # Unitless (gain)
        self.gyro_angle_tolerance = 0.2 # deg
        
        self.lidar_shot_coefficient = 7e-3
        self.lidar_angle_tolerance = 0.225 # deg
        
AGL_noise_data = AGLNoise() 

def fetch_lidar_data(msg):
    """
    Fetches packed LiDAR data from CoppeliaSim, unpacks it into original x-y-z
    components, and converts into polar coordinates. Noise is applied, and
    outputs are stored in the global data class.
    
    Polar coordinates output units:
        r: mm
        theta: degrees
    These units align with those that are output from the SLAMTEC RPLIDAR A3.
    
    Parameters
    ----------
    msg : list
        msg[0] : bool
            Whether the function was successfully called on the server side
        msg[1] : string
            Return data. Consists of x-y-z coords of detected points in m, 
            packed into a string.

    Returns
    -------
    None.

    """

    # Check for valid return data
    if msg[0] and msg[1]:
        # Unpack string signal to individual floats, use slicing to split
        # into 3-column x-y-z array, and store in global data class
        new_lidar_signal = General.unpackFloats(msg[1])
        new_lidar_signal = np.array([new_lidar_signal[0::3], new_lidar_signal[1::3], new_lidar_signal[2::3]])
        globalData.lidar.append(new_lidar_signal)

        # Convert signal to polar coords in mm and degrees, apply noise, and
        # store in global data class
        new_lidar_data_polar = np.empty((len(new_lidar_signal[0]), 2))
        new_lidar_data_polar[:, 0] = np.arctan2(new_lidar_signal[0], new_lidar_signal[1]) * 180 / np.pi
        new_lidar_data_polar[:, 1] = np.sqrt(np.square(new_lidar_signal[0]) + np.square(new_lidar_signal[1])) * 1000
        if not AGL_noise_data.ignore:
            new_lidar_data_polar = add_lidar_noise(new_lidar_data_polar)
        globalData.lidar_polar.append(new_lidar_data_polar)


def fetch_accel_data(msg):
    """
    Fetches packed accelerometer data from CoppeliaSim, and unpacks it into a
    list of x-y-z acceleration components. Noise is applied, and this is
    stored in the global data class with the current simulation time, to
    ensure that there is no mismatch of data when plotting due to missed
    signals from CoppeliaSim.
    
    Acceleration output units:
        x, y, z : ms^-2

    Parameters
    ----------
    msg : list
        msg[0] : bool
            Whether the function was successfully called on the server side
        msg[1] : string
            Return data. Consists of x-y-z components of acceleration in
            ms^-2, packed into a string.

    Returns
    -------
    None.

    """

    # Check for valid return data. Must also check that time data has begun
    # streaming, to avoid plotting errors
    if msg[0] and msg[1] and globalData.time:
        # Unpack string signal to x-y-z components, apply noise, and store in
        # global data class with current simulation time
        new_accel_data = np.array([General.unpackFloats(msg[1])])
        if not AGL_noise_data.ignore:
            new_accel_data = add_accel_noise(new_accel_data)
        new_accel_data = np.append(np.array([[globalData.time[-1]]]), new_accel_data, axis=1)
        globalData.accel = np.append(globalData.accel, new_accel_data, axis=0)


def fetch_gyro_data(msg):
    """
    Fetches orientation data from the IMU in radians, and converts to degrees.
    Noise is applied, and this is stored in the global data class with the
    current simulation time, to ensure there is no mismatch of data when
    plotting due to missed signals from CoppeliaSim.
    
    Orientation output units:
        pitch, roll, yaw : degrees
    
    Parameters
    ----------
    msg : list
        msg[0] : bool
            Whether the function was successfully called on the server side
        msg[1] : list
            Return data. Consists of rotations about the absolute (global)
            x-y-z axes as floats in radians

    Returns
    -------
    None.

    """
    # Check for valid return data. Must also check that time data has begun
    # streaming, to avoid plotting errors
    if msg[0] and msg[1] and globalData.time:
        # Convert orientation to degrees, apply noise, and store in global
        # data class with current simulation time
        new_gyro_data = np.array([msg[1]]) * 180 / np.pi
        if not AGL_noise_data.ignore:
            new_gyro_data = add_gyro_noise(new_gyro_data)
        new_gyro_data = np.append(np.array([[globalData.time[-1]]]), new_gyro_data, axis=1)
        globalData.gyro = np.append(globalData.gyro, new_gyro_data, axis=0)


def add_lidar_noise(lidar_data_polar):
    """
    Applies 2 noise parameters to the raw LiDAR data: to the magnitude 
    data, sunlight shot noise in the form of a \ero-mean normal distribution
    with standard deviation according to the data assigned in the AGLNoise class

    Parameters
    ----------
    lidar_data_polar : Numpy array
        Most recent LiDAR input data in polar coordinates
        (theta=degrees, r=mm) as floats

    Returns
    -------
    lidar_data_polar : Numpy array
        Input data with noise added elementwise

    """
    # Apply sunlight shot noise
    noise_array = np.empty((np.size(lidar_data_polar, 0), np.size(lidar_data_polar, 1)))
    for i in range(np.size(lidar_data_polar, 0)):
        noise_array[i,0] = np.random.uniform(AGL_noise_data.lidar_angle_tolerance/2, AGL_noise_data.lidar_angle_tolerance/2)
        noise_array[i,1] = np.random.normal(0, AGL_noise_data.lidar_shot_coefficient*np.sqrt(abs(lidar_data_polar)[i,1]))
    lidar_data_polar = np.add(lidar_data_polar, noise_array)
        
    return lidar_data_polar

def add_accel_noise(accel_data):
    """
    Applies 3 noise parameters to the accelerometer data: a velocity random 
    walk, which manifests in the acceleration data as simple white noise, 
    a bias instability, and a gain instability. Each is modelled as a 
    zero-mean normal distribution with standard deviation according to the 
    data assigned in the AGLNoise class. 

    Parameters
    ----------
    accel_data : Numpy array
        The most recent set of acceleration data, consisting of x-y-z 
        coordinates in ms^-2

    Returns
    -------
    accel_data : Numpy array
        Acceleration data with the noise model applied, consisting of x-y-z 
        coordinates in ms^-2

    """
    # Apply velocity random walk
    # (Derivative of velocity random walk appears as acceleration white noise)
    white_noise = np.random.normal(0, AGL_noise_data.accel_random_walk_density, (1,3))
    
    # Apply bias instability to current bias
    AGL_noise_data.accel_bias = np.append(AGL_noise_data.accel_bias, [AGL_noise_data.accel_bias[-1]], axis=0)
    AGL_noise_data.accel_bias[-1] = np.add(AGL_noise_data.accel_bias[-1], \
                                           np.random.normal(0, AGL_noise_data.accel_bias_stability, (1,3)))
    
    # Apply gain to current gain
    AGL_noise_data.accel_gain = np.append(AGL_noise_data.accel_gain, [AGL_noise_data.accel_gain[-1]], axis=0)
    AGL_noise_data.accel_gain[-1] = np.multiply(AGL_noise_data.accel_gain[-1], \
                                                np.random.normal(1, AGL_noise_data.accel_gain_stability, (1,3)))
    
    # Measured Acceleration = Gain * (True Acceleration + Random Walk) + Bias
    accel_data = np.add(np.multiply(np.add(accel_data[-1], white_noise), AGL_noise_data.accel_gain[-1]), AGL_noise_data.accel_bias[-1])
    return accel_data.reshape((1,3))

def add_gyro_noise(gyro_data):
    """
    Applies 3 noise parameters to the gyroscope data: an angle random walk, 
    a bias instability, and a gain instability. Each is modelled as a 
    zero-mean normal distribution with standard deviation according to the 
    data assigned in the AGLNoise class

    Parameters
    ----------
    gyro_data : Numpy array
        The most recent set of orientation data, consisting of x-y-z 
        rotational coordinates in degrees
        

    Returns
    -------
    gyro_data : Numpy array
        Orientation data with the noise model applied, consisting of x-y-z 
        rotational coordinates in degrees

    """
    # Apply angle random walk
    AGL_noise_data.gyro_random_walk = np.append(AGL_noise_data.gyro_random_walk, [AGL_noise_data.gyro_random_walk[-1]], axis=0)
    AGL_noise_data.gyro_random_walk[-1] = np.add(AGL_noise_data.gyro_random_walk[-1], \
                                                 np.random.normal(0, AGL_noise_data.gyro_random_walk_density*np.sqrt(globalData.time[-1]), (1,3)))
        
    # Apply bias instability to current bias
    AGL_noise_data.gyro_bias = np.append(AGL_noise_data.gyro_bias, [AGL_noise_data.gyro_bias[-1]], axis=0)
    AGL_noise_data.gyro_bias[-1] = np.add(AGL_noise_data.gyro_random_walk[-1], \
                                                 np.random.normal(AGL_noise_data.gyro_bias_stability*(globalData.time[-1]), (1,3)))

        
    # Apply gain instability to current gain
    AGL_noise_data.gyro_gain = np.append(AGL_noise_data.gyro_gain, [AGL_noise_data.gyro_gain[-1]], axis=0)
    AGL_noise_data.gyro_gain[-1] = np.multiply(AGL_noise_data.gyro_gain[-1], \
                                                np.random.normal(1, AGL_noise_data.gyro_gain_stability, (1,3)))   
    
    # Measured Rotation = Gain * (True Rotation + Random Walk) + Bias
    noisy_data = np.add(np.multiply(np.add(gyro_data[-1], AGL_noise_data.gyro_random_walk[-1]), AGL_noise_data.gyro_gain[-1]), AGL_noise_data.gyro_bias[-1])
    
    # Clip noise at gyroscope's error tolerance to account for assumption of random walk model in bias stability
    gyro_data = np.add(gyro_data, np.subtract(noisy_data, gyro_data) % AGL_noise_data.gyro_angle_tolerance)
    return gyro_data.reshape((1,3))


def posCB(msg):
    """
    Fetches packed GPS position data from CoppeliaSim, and unpacks it into a
    list of x-y-z position components. This is the coordinates within the simulated environment
    Noise is applied, and this is stored in the global data class with the current simulation time, to
    ensure that there is no mismatch of data when plotting due to missed
    signals from CoppeliaSim.
    Position output units:
        x, y, z : meters
    Parameters
    ----------
    msg : list
        msg[0] : bool
            Whether the function was successfully called on the server side
        msg[1] : string
            Return data. Consists of x-y-z components of position in
            meters, packed into a string.
    Returns
    -------
    None.
    """

    return_code = msg[0]
    globalData.abs_pos = msg[1]
    # Add pos noise to the message
    pos_entry = Process.gps_pos_noise(True, msg[1])
    if return_code and msg[1] and globalData.time:
        # Append time data to new data, and append to global data arrays
        pos_entry = [globalData.time[-1]] + pos_entry
        globalData.pos.append(pos_entry)
    else:
        print('No position data')

def velCB(msg):
    """
    Fetches packed GPS velocity data from CoppeliaSim, and unpacks it into a
    list of x-y-z velocity components.
    Noise is applied, and this is stored in the global data class with the current simulation time, to
    ensure that there is no mismatch of data when plotting due to missed
    signals from CoppeliaSim.
    Position output units:
        x, y, z : ms^-1
    Parameters
    ----------
    msg : list
        msg[0] : bool
            Whether the function was successfully called on the server side
        msg[1] : string
            Return data. Consists of x-y-z components of velocity in
            meters, packed into a string.
    Returns
    -------
    None.
    """
    return_code = msg[0]
    globalData.abs_vel = msg[1]
    # Add velocity noise to the message
    msg[1] = Process.gps_vel_noise(msg[1])
    # Create entry for speed plot
    speed_entry = math.sqrt(msg[1][0]**2 + msg[1][0]**2)
    if return_code and msg[1] and globalData.time:
        # Append time data to new data, and append to global data arrays
        vel_entry = [globalData.time[-1]] + msg[1]
        speed_entry = [globalData.time[-1]] + [speed_entry]
        globalData.vel.append(vel_entry)
        globalData.speed.append(speed_entry)

    else:
        print('No velocity data')

def rightcameraCB(msg):
    """
    Fetches packed vision sensor image data from CoppeliaSim for the right camera and unpacks it into an RGB array.
    This is set to the globalData to be access from elsewhere, as the callback function cannot have a return.
    Array output format:
        A 3D array with size ResolutionX*ResolutionX*rgb (512x256)x3
    Parameters
    ----------
    msg : list
        msg[0] : bool
            Whether the function was successfully called on the server side
        msg[1] : string
            Return data. The packed string of the image data
    Returns
    -------
    None.
    """
    return_code = msg[0]
    if return_code and msg[1]:
        new_camera_signal = np.array(General.unpackFloats(msg[1]), dtype=np.float64)
        new_camera_signal = new_camera_signal.reshape(256,512,3)
        new_camera_signal = img_as_ubyte(new_camera_signal) # Convert image to readable formart
        globalData.current_right_image = new_camera_signal
        #plt.figure(2)
        #plt.imshow(abs(new_camera_signal), origin='lower')
        #plt.show()

    else:
        print('No Camera data')

def depthCB(msg):
    """
    Callback function for simxGetVisionSensorDepthBuffer function. This gets a depth map of the image, similar to what
    a stereo camera would output
    Array output format:
        A 2D array with size ResolutionX*ResolutionX (512x256) with a value in meters for the depth of each pixel
    Parameters
    ----------
    msg : list
        msg[0] : bool
            Whether the function was successfully called on the server side
        msg[1] : int
            The resolution of the depth buffer
        msg[2] : float
        The depth buffer. Values are in the range of 0-1 (0=on the near clipping plane, 1=on the far clipping plane).
         If toMeters was specified, then values represent the distance from the sensor's origin, in meters
    Returns
    -------
    None.
    """
    return_code = msg[0]
    if return_code and msg[2]:
        print(msg[2])
    else:
        print('No Camera data')

def update_live_plot(live_plot):
    """
    This function is called on every time step, it updates all activated sensor figures with the incoming stream of
     information
    :param live_plot: The class instantiation containing the figure handles.
    :return:
    none
    """
    if np.size(globalData.accel, 0) and globalData.time and not live_plot.suppress_accel_plot:
        # Convert to array to allow multidimensional slicing, and update live plot
        live_plot.accelLineX.set_data(globalData.accel[:, 0], globalData.accel[:, 1])
        live_plot.accelLineY.set_data(globalData.accel[:, 0], globalData.accel[:, 2])

        # Dynamically extend x axis every 20 seconds
        _, upper_xlim = live_plot.accelAx.get_xlim()
        if globalData.time[-1] > upper_xlim:
            live_plot.accelAx.set_xlim(0, 20 * (int(upper_xlim / 20) + 1))

    if globalData.lidar_polar and not live_plot.suppress_lidar_plot:
        live_plot.lidarScatter.set_data(globalData.lidar_polar[-1][:,0]*np.pi/180, globalData.lidar_polar[-1][:,1])

    if globalData.vel and globalData.time and not live_plot.suppress_vel_plot:
        # Convert to array to allow multidimensional slicing, and update live plot
        speed_data_array = np.array(globalData.speed)
        live_plot.vel_line.set_data(speed_data_array[:,0], speed_data_array[:,1])
        speed = speed_data_array[-1][1]
        live_plot.speed_text.set_text('%.2f mph'%(speed*2.23694))
        # Increase axis limits if data is outside of plot
        _, upper_xlim = live_plot.vel_ax.get_xlim()
        if globalData.time[-1] > upper_xlim:
            live_plot.vel_ax.set_xlim(0, 20 * (int(upper_xlim / 20) + 1))
        _, upper_ylim = live_plot.vel_ax.get_ylim()
        if speed > upper_ylim:
            live_plot.vel_ax.set_ylim(0, speed)

    if globalData.pos and globalData.time and not live_plot.suppress_pos_plot:
        # Convert to array to allow multidimensional slicing, and update live plot
        pos_data_array = np.array(globalData.pos)
        live_plot.pos_line.set_data(pos_data_array[:,1], pos_data_array[:,2])

    if np.size(globalData.gyro, 0) and not live_plot.suppress_gyro_plot:
        live_plot.gyroAx.rollAxisCoords = np.array(
            [[1, 0, 0], [-1, 0, 0], [-0.9, -0.05, 0], [-1, 0, 0], [-0.9, 0.05, 0]])
        live_plot.gyroAx.pitchAxisCoords = np.array([[0, -1, 0], [0, 1, 0]])
        live_plot.gyroAx.yawAxisCoords = np.array([[0, 0, -1], [0, 0, 1]])

        rotationMatrix = R.from_euler('xyz', -np.array([globalData.gyro[-1, 1:5]]), degrees=True).as_matrix()[0, :, :]
        live_plot.gyroAx.rollAxisCoords = np.matmul(live_plot.gyroAx.rollAxisCoords, rotationMatrix)
        live_plot.gyroAx.pitchAxisCoords = np.matmul(live_plot.gyroAx.pitchAxisCoords, rotationMatrix)
        live_plot.gyroAx.yawAxisCoords = np.matmul(live_plot.gyroAx.yawAxisCoords, rotationMatrix)

        # print(livePlot.gyroAx.rollAxisCoords, livePlot.gyroAx.pitchAxisCoords, livePlot.gyroAx.yawAxisCoords)

        live_plot.gyroAx.rollAxis.set_data(live_plot.gyroAx.rollAxisCoords[:, 0], live_plot.gyroAx.rollAxisCoords[:, 1])
        live_plot.gyroAx.rollAxis.set_3d_properties(live_plot.gyroAx.rollAxisCoords[:, 2])
        live_plot.gyroAx.pitchAxis.set_data(live_plot.gyroAx.pitchAxisCoords[:, 0], live_plot.gyroAx.pitchAxisCoords[:, 1])
        live_plot.gyroAx.pitchAxis.set_3d_properties(live_plot.gyroAx.pitchAxisCoords[:, 2])
        live_plot.gyroAx.yawAxis.set_data(live_plot.gyroAx.yawAxisCoords[:, 0], live_plot.gyroAx.yawAxisCoords[:, 1])
        live_plot.gyroAx.yawAxis.set_3d_properties(live_plot.gyroAx.yawAxisCoords[:, 2])
        live_plot.gyroAx.label.set_text(f'yaw = {globalData.gyro[-1, 3]:.1f}°, \npitch = {globalData.gyro[-1, 2]:.1f}°, \nroll = {globalData.gyro[-1, 1]:.1f}°')

    plt.draw()
    plt.waitforbuttonpress(0.005)
