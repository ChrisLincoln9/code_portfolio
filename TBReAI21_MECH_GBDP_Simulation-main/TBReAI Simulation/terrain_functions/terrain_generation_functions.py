import matplotlib.pyplot as plt
import numpy as np
import terrain_functions.perlin2d as perlin

def terrain_initialise(
        start_cones, left_cones, right_cones, terrain_texture_num='1',
        track_excess = 26, height = 0.2, generate_puddle = True,
        puddle_depth = 0.05, random_generation = True,
        noise_type = 'perlin', detail = 2, noise_res = 8):
    
    ''' terrain_initialise takes input from terrain variables and cone locations
    Parameters
    -----------
    
    start_cones, left_cones, right_cones: three tupeles of [x,y]
        Mark the locations of the cones for the generated track
    track_excess: float
        marks the additional width of the terrain beyond the track. Suggested 
        to be >= 16 as track size is rounded to a factor of 16
    height: float
        marks the height variance of the track. A height of 0.2 will create
        a terrain with variance of +- 0.2m
    puddle_generation: boolean
        if puddles are to be generated, mark True
    puddle_depth: float
        denotes the depth of the deepest puddle in the environment. A plane of
        water will be created at this level
    random_generation: boolean
        using numpy.random, a value of False will create a reproducable noise
        map. True will create a new noise map each execution
    noise_type: string
        two choises of noise (perlin and fractal), explained in file 'perlin2d'
    detail: integer
        higher detail will interpolate more of the noise map. Suggested value
        1(low detail) or 2(high detail)
        
    Returns
    ----------
        The output of this function is returned to the track_main file to generate
        the terrain in CoppeliaSim
    '''
    noise_options = [random_generation, noise_type, noise_res, detail]
    
    
    (terrain_dim, terrain_mid) = terrain_properties(start_cones,left_cones,right_cones, track_excess)

    cone_height = 0.425 - height
    #heightmap returns a list of heights for the generation of a heightfield in Coppelia
    heightmap = generate_noise(terrain_dim, height, noise_options)
    terrain_data = ([terrain_dim[0]*detail, terrain_dim[1]*detail, terrain_dim[0]],[terrain_mid[0],terrain_mid[1],cone_height],'Terrain', heightmap, f'Terrain_textureHolder{terrain_texture_num}')
    
    if generate_puddle:
        puddle_data = ([terrain_dim[0], terrain_dim[1], max(heightmap)-min(heightmap)], [terrain_mid[0], terrain_mid[1], cone_height + min(heightmap)], 'Puddle', puddle_depth)
    else:
        puddle_data = []
        
    return (terrain_data, puddle_data)

def terrain_properties(
        start_cones,left_cones,right_cones,track_excess):
    
    cone_positions = start_cones + left_cones + right_cones
    
    '''
    Using the cone positions and track_excess, terrain dimensions can be calculated
    
    terrain_dim provides the dimensions of the terrain, including excess
    
    Returns:
        terrain_mid provides the position of the terrain centre for repositioning in Coppelia
    '''
    max_x = (max(point.x for point in cone_positions))
    min_x = (min(point.x for point in cone_positions))
    size_x = (max_x - min_x) + track_excess
    terrain_x = int(round((size_x)/16)*16)
    midpoint_x = (max_x + min_x)/2
    
    max_y = (max(point.y for point in cone_positions))
    min_y = (min(point.y for point in cone_positions))
    size_y = (max_y - min_y) + track_excess
    terrain_y = int(round((size_y)/16)*16)
    midpoint_y = (max_y + min_y)/2
    
    terrain_dim = [terrain_x,terrain_y]
    terrain_mid = [midpoint_x,midpoint_y]
    
    return(terrain_dim, terrain_mid)

def generate_noise(terrain_dim, height, noise_options):
    
    '''
    Description
    -----------
        To encorporate the detail variable, the axis are scaled linearly in x and y. The 
        generated table is then scaled lenearly in the z-direction to account for height
    
    Parameters
    -----------
    terrain_dim: tuple
        dimensions of the terrain. [x dimension, y dimension]
    height: float
        defines height variance of terrain. +- height
    noise_options: list
        comprised of [random_generation, noise_type, noise_res, detail]
        see terrain_initialise for details

    Returns
    ------------
        generate_noise returns a heightmap of the generated terrain
    '''
    
    print("Generating ", terrain_dim[0], " x ", terrain_dim[1], " noise map")

    terrain_dim_scale = [terrain_dim[0]*noise_options[3], terrain_dim[1]*noise_options[3]]
    terrain_res = [int(terrain_dim[0]/noise_options[2]), int(terrain_dim[1]/noise_options[2])]
    
    if noise_options[0] == 0:
        np.random.seed(0)
    
    if noise_options[1] == 'perlin':
        noise = np.array(perlin.generate_perlin_noise_2d(terrain_dim_scale, terrain_res, (1, 1))) * height
    else:
        noise = np.array(perlin.generate_fractal_noise_2d(terrain_dim_scale, terrain_res, (1, 1))) * height
    
    plt.imshow(noise, cmap='gray', interpolation='lanczos')
    plt.colorbar()
    
    noise = noise.transpose()

    #CoppeliaSim requires a list of heights rather than a table, hence the flattening of the array
    heightMap = list(noise.flat)
    return(heightMap)

def create_terrain(client, terrain_data,
                   puddle_data = None):

    ''' Communicates with coppelia function to generate the terrain

    Parameters
    ----------
    client: coppelia object 
        For accessing CoppeliaSim b0 client
    terrain_data : list
        List of all variables relevant to terrain generation within coppelia
    puddle_data : list
        List of all variables relevant to puddle generation within coppelia.
        This variable is optional. If empty, no puddles will be generated 

    Returns
    -----------
    None
    '''
    
    client.simxCallScriptFunction('createTerrain_function@remoteApiCommandServer','sim.scripttype_customizationscript',terrain_data,client.simxServiceCall())
    
    if puddle_data:
        client.simxCallScriptFunction('placePuddle_function@remoteApiCommandServer','sim.scripttype_customizationscript',puddle_data,client.simxServiceCall())


def Create_Floor(client, cone_positions, track_excess=2):
    '''
    Description
    ----------
    Generates a flat floor for the track
    Parameters
    ----------
    client: coppelia object
        For accessing CoppeliaSim b0 client
    cone_positions : list of Point object
        coordinates of all the cones
    track_excess : float
        excess floor distance at the edges of the track
    '''

    max_x = (max(point.x for point in cone_positions))
    min_x = (min(point.x for point in cone_positions))
    size_x = (max_x - min_x) + 2 * track_excess
    midpoint_x = (max_x + min_x) / 2

    max_y = (max(point.y for point in cone_positions))
    min_y = (min(point.y for point in cone_positions))
    size_y = (max_y - min_y) + 2 * track_excess
    midpoint_y = (max_y + min_y) / 2

    floor_data = ([size_x, size_y, 0.5], [midpoint_x, midpoint_y, 0], 'Floor')
    client.simxCallScriptFunction('createFloor_function@remoteApiCommandServer', 'sim.scripttype_customizationscript',
                                  floor_data, client.simxDefaultPublisher())