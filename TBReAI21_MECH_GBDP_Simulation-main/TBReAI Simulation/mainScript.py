from dependencies import b0RemoteApi
import sensorHelperFunctions as sensors
import generalHelperFunctions as general
from powertrain_final import *
import sus_val_v1 as sus
import pickle

f_r = []  # Front Reaction Force Array
t_ult = []  # Time Step array
r_r = []  # Rear Reaction Force Array

'''
Description
-----------
Runs Simulation onto pre-generated track environment
'''


def main():
    with open('cone_locations.pkl', 'rb') as f:
        general.globalData.start_cones, general.globalData.left_cones, general.globalData.right_cones = pickle.load(f)

    # Initial Conditions
    velocity = []
    torque = []
    position = []  # Suspension position array
    y0 = [0, 0, 0, 0]

    # USER-SPECIFIED INPUT #
    duration = 120
    print('Program started')

    with b0RemoteApi.RemoteApiClient('b0RemoteApi_pythonClient', 'b0RemoteApi') as client:

        # Get everything ready
        subs, live_plot, cones, camera = general.initialise(client)
        client.simxStartSimulation(client.simxServiceCall())
        # Uncomment line below to not render simulation on CoppeliaSim #
        #client.simxSetBoolParameter('sim.boolparam_display_enabled', False, client.simxServiceCall())
        global u0

        motorLeft = client.simxGetObjectHandle('RSL2_3_Motor_Enabled', client.simxServiceCall())[1]
        # Calling left wheel motor in CoppeliaSim
        motorRight = client.simxGetObjectHandle('RSR2_3_Motor_Enabled', client.simxServiceCall())[1]
        # Calling right wheel motor in CoppeliaSim

        # Import suspension parameters'
        Shock1, Shock2, Shock3, Shock4, Front_wheel, Rear_wheel, Lf, Lr, Mb, Iyy, kf, kr, cf, cr, g, hf_std, hr_std, a, b = sus.sus_handles(client)

        # Main loop
        client.simxSynchronous(True)
        startTime = time.time()
        while time.time() - startTime < duration and general.globalData.simState:
            if general.globalData.doNextStep and general.globalData.time:
                general.globalData.doNextStep = False

                # Suspension Code
                hf = client.simxGetObjectPosition(Front_wheel, -1, client.simxServiceCall())[1][2] * -1  # front hub displacement from ground (m)
                hr = client.simxGetObjectPosition(Rear_wheel, -1, client.simxServiceCall())[1][2]  # rear hub displacement from from ground (m)

                h = (hf - hf_std + hr - hr_std) / 2  # Avg height of the tyres from the ground

                acc_xyzg = np.array(general.globalData.accel)  # Import vehicle body acceleration data into array
                accz = acc_xyzg[-1, 2]  # Call acceleration in the z-axis
                accy = acc_xyzg[-1, 1]  # Call acceleration in the y-axis

                t_new = time.time()  # Get universal current time

                # Input required arguments into suspension equation solver to receive suspension suspension
                # characteristics
                y0, normal_force, r, t_ulti, y0_cornering = sus.sus_mod(y0, [general.globalData.time[-1], t_new], accz,h, Lf, Lr, Mb, Iyy, kf, kr, cf, cr, g, a, b,accy)

                # Store new values into respective arrays
                position.append(y0)
                f_r.append(normal_force)
                r_r.append(r)
                t_ult.append(t_ulti)

                # Set target velocity of each shock absorber
                client.simxSetJointTargetVelocity(Shock1, position[-1][1], client.simxServiceCall())
                client.simxSetJointTargetVelocity(Shock2, position[-1][1], client.simxServiceCall())
                client.simxSetJointTargetVelocity(Shock3, position[-1][1], client.simxServiceCall())
                client.simxSetJointTargetVelocity(Shock4, position[-1][1], client.simxServiceCall())

                # Powertrain code
                [_, t_step] = client.simxGetSimulationTimeStep(client.simxServiceCall())
                powertrain_instance = Powertrain(u0, general.globalData.time[-1], t_step, error, normal_force)
                new_torque, new_u0 = powertrain_instance.run()
                torque.append(new_torque)
                velocity.append(new_u0[7])
                rotational_velocity = 0.8 * -new_u0[5]
                u0 = new_u0

                client.simxSetJointTargetVelocity(motorLeft, rotational_velocity, client.simxServiceCall())
                client.simxSetJointTargetVelocity(motorRight, rotational_velocity, client.simxServiceCall())

                client.simxSynchronousTrigger()
            client.simxSpinOnce()

            # Camera and GPS and LiDAR code

            if not live_plot.suppress_live_plot:
                sensors.update_live_plot(live_plot)

            if not live_plot.suppress_cone_distance:
                cones.check_cam_fov(general.globalData.abs_pos, general.globalData.gyro[-1, 3])

            if not live_plot.suppress_camera_data:
                camera.gaussian_blur(general.globalData.current_right_image)

        # Clean up
        general.finish(client, subs)
        client.simxStopSimulation(client.simxDefaultPublisher())

    print('Program ended')
    '''
    Input & Output Graph Plots
    ---------------
    Powertrain: Velocity-Time Graph (Input)
    
    Powertrain: Torque-Time Graph (Input)
    
    Suspension: Acceleration-Time Graph (Output)
        -Vertical Acceleration felt on Model
    '''
    plt.figure(1)
    plt.grid()
    plt.plot(general.globalData.time[0:len(velocity)], velocity)
    plt.xlabel('Time (s)')
    plt.ylabel('Rear wheel linear velocity (m/s)')

    plt.figure(2)
    plt.grid()
    plt.plot(general.globalData.time[0:len(torque)], torque)
    plt.xlabel('Time (s)')
    plt.ylabel('Torque (Nm)')

    # position = np.array(position)
    # plt.figure(2)
    # plt.plot(general.globalData.time[0:len(position)], position[:, 1])
    # plt.xlabel('Time (s)')
    # plt.ylabel('Acceleration (m/s^2)')

    plt.show()


if __name__ == '__main__':
    main()

