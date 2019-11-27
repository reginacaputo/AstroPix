#*******************************************************************#
#-------------------------------------------------------------------#
#---------------------------- AstroPix -----------------------------#
#-------------------------------------------------------------------#
#------------- Michela Negro - GSFC/UMBC - 2019/2020 ---------------#
#-------------------------------------------------------------------#
#*******************************************************************#

import os
import argparse
import numpy as np
from importlib.machinery import SourceFileLoader

__description__ = 'Creates the AstroPix geometry configurations'

formatter = argparse.ArgumentDefaultsHelpFormatter
PARSER = argparse.ArgumentParser(description=__description__, formatter_class=formatter)
PARSER.add_argument('-c', '--config', type=str, required=True,
                    help='the input configuration file')

def get_var_from_file(filename):
    f = open(filename)
    global data
    data = SourceFileLoader('data', filename).load_module()
    f.close()
    
def run_mkGeometries(**kwargs):
	assert(kwargs['config'].endswith('.py'))
	get_var_from_file(kwargs['config'])
	passive = data.PASSIVE
	thickness = data.THICKNESS
	voxelsize = data.VOXELSIZE
	geo_base = data.GEO_BASE
	det_base = data.DET_BASE
	for i, p in enumerate(passive):
		print('PASSIVE %i: %i%%' %(i, p))
		for j, t in enumerate(thickness):	
			print('THICKNESS %i: %i um' %(j, t))
			for k, v in enumerate(voxelsize): 
				print('VOXEL SIZE %i: %.2f mm' %(k, v))
				
				folder_name = 'geo_%i_%i_%.2f'%(p, t, v)
				if not os.path.exists('geometry/%s' %folder_name):
					os.system('mkdir geometry/%s' %folder_name)
				geo_new = os.path.basename(geo_base).replace('base', 
												'%i_%i_%.2f'%(p, t, v))
				det_new = os.path.basename(det_base).replace('base', '%i_%i_%.2f'%(p, t, v))
				os.system('cp %s geometry/%s/.' %(geo_base, folder_name))
				os.system('mv geometry/%s/%s geometry/%s/%s' \
					%(folder_name, os.path.basename(geo_base), folder_name, geo_new))
				os.system('cp %s geometry/%s/.' %(det_base, folder_name))          
				os.system('mv geometry/%s/%s geometry/%s/%s' \
					%(folder_name, os.path.basename(det_base), folder_name, det_new))  
		print('\n')
				
				
				
if __name__ == '__main__':
	args = PARSER.parse_args()
	
	print("--------------------")
	print("---- Start  Run ----")
	print("--------------------")

	run_mkGeometries(**args.__dict__)
	
	print("--------------------")
	print("----- End  Run -----")
	print("--------------------")