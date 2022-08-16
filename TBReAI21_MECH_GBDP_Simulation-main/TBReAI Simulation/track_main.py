from dependencies import b0RemoteApi
import track_classes.track_point as tp
import terrain_functions.terrain_generation_functions as teg
import os

def track_initialise(start_cones,left_cones,right_cones,cone_texture,terrain,terrain_texture,terrain_height,puddles,max_puddle_depth):
    '''
    Description
    -----------
    Generates the environment within CoppeliaSim, both the track and terrain
    
    Parameters
    -----------
    start_cones: list of Point object
        list of Point for start cones
    left_cones: list of Point object
        list of Point for left cones
    right_cones: list of Point object
        list of Point for right cones
    cone_texture: string
        determines level of noise of cone texture
    terrain_texture: string
        determines type of terrain texture
    terrain_height: float
        defines height variance of terrain
    puddles: boolean
        defines whether puddles will generate
    max_puddle_depth: float
        defines max height of water
    '''

    current_working_directory = os.getcwd().replace("/","\\") 
    model_position = tp.Point(0,0)

    print(f'There are {len(start_cones + left_cones + right_cones)} cones to insert')

    if terrain == True:
        (terrain_data, puddle_data) = teg.terrain_initialise(
            start_cones,left_cones,right_cones,
            terrain_texture_num=terrain_texture,
            height=terrain_height,generate_puddle=puddles,
            puddle_depth=max_puddle_depth)

    with b0RemoteApi.RemoteApiClient('b0RemoteApi_pythonClient','b0RemoteApi') as client:
        print ('Connected to BlueZero API')

        # Generate terrain
        if terrain == True:
            teg.create_terrain(client,terrain_data,puddle_data)
        else: 
            cone_positions = start_cones + left_cones + right_cones
            teg.Create_Floor(client,cone_positions)

        # Place the loaded start cones
        for index,value in enumerate(start_cones):
            cone_file_name = current_working_directory + "\\models\\Start" + cone_texture + ".ttm"
            cone_data = ([value.x,value.y,0.67],f'StartCone{index+1}',cone_file_name)
            client.simxCallScriptFunction('placeModel_function@remoteApiCommandServer','sim.scripttype_customizationscript',cone_data,client.simxServiceCall())

        # Place the loaded left cones
        for index,value in enumerate(left_cones):
            cone_file_name = current_working_directory + "\\models\\Left" + cone_texture + ".ttm"
            cone_data = ([value.x,value.y,0.67],f'LeftCone{index+1}',cone_file_name)
            client.simxCallScriptFunction('placeModel_function@remoteApiCommandServer','sim.scripttype_customizationscript',cone_data,client.simxServiceCall())

        # Place the loaded right cones
        for index,value in enumerate(right_cones):
            cone_file_name = current_working_directory + "\\models\\Right" + cone_texture + ".ttm"
            cone_data = ([value.x,value.y,0.67],f'RightCone{index+1}',cone_file_name)   
            client.simxCallScriptFunction('placeModel_function@remoteApiCommandServer','sim.scripttype_customizationscript',cone_data,client.simxServiceCall())

        # Place the loaded vehicle
        vehicle_name = 'TBReAI_21_vm.ttm'
        file_name = current_working_directory + "\\models\\" + vehicle_name
        vehicle_data = ([model_position.x,model_position.y,1],'Model',file_name)
        client.simxCallScriptFunction('placeModel_function@remoteApiCommandServer','sim.scripttype_customizationscript',vehicle_data,client.simxServiceCall())