This study aims to define the ideal pixel size for the AstroPix project.

The basic geopmetry is composed of
    - 50 layers (1mx1m) of voxel detectors
    - ideal calorimeter
    - (passive material on top of each tkr layer)
    
We want to build a routine to build and test different geometries changing some parameters:
   - Voxel size:
		* 10 mm
		* 5 mm
		* 3 mm
		* 1 mm
		* 0.5 mm
		* ... (enough to see the plateau)
   - Si thickness:
		* 300 um
		* 500 um
		* 700 um 
   - passive material:
		* 1%
   		* 2%
		* 5%
		* 10%

We want to test the different configurations for different energies:
   	   	* 100 keV
		* 662 keV
		* 1000 keV



Description of the files:
-------------------------

 * config.py -> where we declare the parameters we want to study

 * mkGeometries.py -> builds all the geometry configurations starting from base files located in the geometry/geo_base/ folder.
 
 * mkSimulations.py -> Creates .source files from a base file located in the source/ folder and produce a sh file with the list of the commands to run the simulations (for now the simulations have to be run manually).
 
 * mkRecon.py -> Runs the reconstruction of the events with revan (according to the configuration file declared in the config file).
 
 * mkARM.py -> Takes the revan output and produces .root files with the ARM histograms.
 
 * mkARManalysis.py -> Runs analysis routine.



How to run the routines:
------------------------

 >>> python mkGeometries.py -c config.py
 >>> python mkSimulations.py -c config.py -sim True
 >>> python mkRecon.py -c config.py
 >>> python mkARM.py -c config.py --show True
 >>> python mkARManalysis.py -c config.py
