TBReAI Simulation Team - Simulation Instructions 
------------------------------------------------
https://github.com/TBReAI/TBReAI21_MECH_GBDP_Simulation
-------------------------------------------------------

Introduction:
------------
Simulation in CoppeliaSim to test the TBReAI AI-Pipeline in an accurate 3d Environment

Requirements:
------------
1. CoppeliaSim EDU 4.1.0
	-("CoppeliaSim_Player_V4_1_0_Setup.exe" provided in Working Directory)
	-( If sourced on GitHub download from: https://www.coppeliarobotics.com/files/CoppeliaSim_Player_V4_1_0_Setup.exe )

2. Python 3.9
	-Additional Python Modules
  	 -pygame
  	 -scipy
  	 -opencv-python
	 -Numpy
	 -pickle
	 
3. Simulation CoppeliaSim Scene
	- https://drive.google.com/file/d/1pZVAoPw1aStRCaVtAg9OKV1qoI4eqbxd/view?usp=sharing
	
Instructions:
-------------
1. Extract all Zipped folders and keep them in the original folder they are held in.

2. Load "simulation_scene.ttt" in CoppeliaSim.
	-Ensure all child scripts are active (Do not have a red cross next to them).

3. Run "track_ui.py"
	- Open "surface&texture_key.pdf" for a key of cone and surface textures.
	- Choose desired scene environment vairables.
	- "Terrain - False" will generatea flat basic testing environment.
	- Click "Generate Track" for a 2D plot of desired track design.
	- Click "Generate in Sim" to load environment into CoppeliaSim scene.
	
4.Select desired plots at the top of the SensorPlotFigures class within sensorHelperFunctions

5. Run "mainScript.py"

Any further questions email: dec34@bath.ac.uk

      2021-05-14
