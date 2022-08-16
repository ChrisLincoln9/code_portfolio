import csv
import pickle
import CL_processing_funcs as Process
import sensorHelperFunctions as sensors
import numpy as np
from struct import unpack
class ParameterSettings:
    kernel_length = 10
    gsigma = 2.5
    camera_resolution = [512,256]


class globalData:
    curr_time_step = []
    time = []
    abs_pos = []
    abs_vel = []
    pos= []
    vel = []
    current_left_image = []
    current_right_image = []
    camera_resolution = []
    lidar = []
    lidar_polar = []
    accel = np.empty((0,4))
    start_cones = []
    left_cones = []
    right_cones = []
    camera_depth = []
    speed = []
    gyro = np.empty((0,4))
    doNextStep = True
    simState = 16
    
def simulationStepStarted(msg):
    """
    Detects if CoppeliaSim has started simulating the next timestep, 
    and records the current simulation time.

    Parameters
    ----------
    msg : list
        msg[0] bool
            Whether the function was successfully called on the server side
        msg[1] : dict
            Return data. b-strings are encoded in utf-8
            msg[1][0] : {byte-encoded string : byte-encoded string)}
                Key : b'simulationState'
                Value: code indicating if simulation is running, paused,
                stopped etc
            msg[1][1] : {byte-encoded string : float}
                Key : b'simulationTime'
                Value : time at end of last simulated time step
            msg[1][2] : {byte-encoded string : float}
                Key : b'simulationTimeStep'
                Value : length of last simulated time step

    Returns
    -------
    None.

    """
    simTime=msg[1][b'simulationTime'];
    print('Simulation step started. Simulation time: ',simTime)


def simStepDone(msg):
    """
    Detects if CoppeliaSim has finished simulating the current timestep,
    records the current simulation time, and triggers the next timestep in
    synchronous operation
    Parameters
    ----------
    msg : list
        msg[0] : bool
            Whether the function was successfully called on the server side
        msg[1] : dict
            Return data. b-strings are encoded in utf-8
            msg[1][0] : {byte-encoded string : byte-encoded string)}
                Key : b'simulationState'
                Value: code indicating if simulation is running, paused,
                stopped etc
            msg[1][1] : {byte-encoded string : float}
                Key : b'simulationTime'
                Value : time at end of last simulated time step
            msg[1][2] : {byte-encoded string : float}
                Key : b'simulationTimeStep'
                Value : length of last simulated time step
    Returns
    -------
    None.
    """
    if msg[0]:
        globalData.time.append(msg[1][b'simulationTime'])
        globalData.doNextStep = True


def simulationState(msg):
    """
    Detects the state of the simulation (running, stopped, paused etc) and
    stores this in the global data class
    Parameters
    ----------
    msg : list
        msg[0]: bool
            Whether the function was successfully called on the server side
        msg[1] : int
            Code indicating simulation state at end of last time step
    Returns
    -------
    None.
    """
    if msg[0]:
        globalData.simState = msg[1]


def unpackFloats(packedFloats):
    """
    Receives a data string and unpacks it into a list of its constituent
    float values
    Parameters
    ----------
    packedFloats : string
        List of floats packed into a single string
    Returns
    -------
    b : list
        Unpacked floats
    """
    b = []
    for i in range(int(len(packedFloats) / 4)):
        b.append(unpack('<f', packedFloats[4 * i:4 * (i + 1)])[0])
    return b

def initialise(client):
    """
    Prepares for start of simulation by creating object handles and opening
    subscriber topics

    Parameters
    ----------
    client : CoppeliaSim client
        The client to which the server is currently connected.

    Returns
    -------
    subs : list
        List of subscribed topics.
    live_plot : SensorPlotFigures class
        Handle of the live plot window.
    cones : cone object
        Locations of cones that are placed by the track initialisation functions.
    camera : camera object
        Handle of stereo camera.

    """
    live_plot = sensors.SensorPlotFigures()
    # User settings

    ## Prepare figure for live-updating plot and start data streaming ##
    
    # Prepare live plot
    if not live_plot.suppress_camera_data:
        camera = Process.CameraNoise(ParameterSettings.kernel_length,ParameterSettings.gsigma)
    else:
        camera = None
    if not live_plot.suppress_cone_distance:
        cones = Process.CalculateConeDistance(globalData.left_cones, globalData.right_cones)
    else:
        cones = None
    if not live_plot.suppress_live_plot:
        live_plot.create_figure()


    #Get handles
    gps_handle = list(client.simxGetObjectHandle('GPS', client.simxServiceCall()))
    left_camera_handle = list(client.simxGetObjectHandle('anaglyphStereoSensor_leftSensor', client.simxServiceCall()))
    right_camera_handle = list(client.simxGetObjectHandle('anaglyphStereoSensor_rightSensor', client.simxServiceCall()))
    _, gyro_handle = client.simxGetObjectHandle('Accelerometer_mass', client.simxServiceCall())
    #dummy_camera_handle = list(client.simxGetObjectHandle('Dummy_sensor', client.simxServiceCall()))
    # Open subscriber channels for time, accelerometer, and LiDAR data

    sub1 = client.simxGetStringSignal('newLidarData', client.simxDefaultSubscriber(sensors.fetch_lidar_data))
    sub2 = client.simxGetStringSignal('newAccelData', client.simxDefaultSubscriber(sensors.fetch_accel_data))
    sub3 = client.simxGetSimulationStepDone(client.simxDefaultSubscriber(simStepDone))
    sub4 = client.simxGetObjectOrientation(gyro_handle, -1, client.simxDefaultSubscriber(sensors.fetch_gyro_data))
    sub5 = client.simxGetObjectPosition(gps_handle[1], '-1', client.simxDefaultSubscriber(sensors.posCB))
    sub6 = client.simxGetObjectVelocity(gps_handle[1], client.simxDefaultSubscriber(sensors.velCB))
    sub7 = client.simxGetSimulationState(client.simxDefaultSubscriber(simulationState))
    subs = [sub1, sub2, sub3, sub4, sub5, sub6, sub7]
    if not live_plot.suppress_camera_data:
        # depth buffer deactivated because not currently in use
        #sub6 = client.simxGetVisionSensorDepthBuffer(dummy_camera_handle, True, False, client.simxDefaultSubscriber(sensors.depthCB))
        sub8 = client.simxGetStringSignal("newCameraData", client.simxDefaultSubscriber(sensors.rightcameraCB))
        subs = [sub1, sub2, sub3, sub4, sub5, sub6, sub7, sub8]

    return subs, live_plot, cones, camera


def finish(client, subs):
    """
    Prepares for programme termination by unsubscribing from all topics, and pickling global data 

    Parameters
    ----------
    client : CoppeliaSim client
        The client to which the server is currently connected.
        
    subs : list
        Subscriber topics to be removed.

    Returns
    -------
    None.

    """
    ## Unsubscribe from data streaming and write data to csv file if specified ##
    
    # Remove subscriber channels to avoid performance loss
    for sub in subs:
        client.simxRemoveSubscriber(sub)
    
    data_to_pickle = [globalData.abs_pos, globalData.abs_vel, globalData.pos, globalData.vel, globalData.lidar, \
                      globalData.lidar_polar, globalData.accel, globalData.start_cones, globalData.left_cones, \
                      globalData.right_cones, globalData.speed, globalData.gyro]

    with open('globalData.pkl', 'wb') as f:
        pickle.dump(data_to_pickle, f)
