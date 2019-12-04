#*******************************************************************#
#-------------------------------------------------------------------#
#---------------------------- AstroPix -----------------------------#
#-------------------------------------------------------------------#
#------------- Michela Negro - GSFC/UMBC - 2019/2020 ---------------#
#-------------------------------------------------------------------#
#*******************************************************************#

import os
import sys
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
    
def run_mkARManalysis(**kwargs):
	assert(kwargs['config'].endswith('.py'))
	get_var_from_file(kwargs['config'])
	
	passive = data.PASSIVE
	thickness = data.THICKNESS
	voxelsize = data.VOXELSIZE
	geo_base = data.GEO_BASE
	src_base = data.SRC_BASE
	energy = data.ENERGY
	
	outs_list = []
	for i, p in enumerate(passive):
		print('PASSIVE %i: %i%%' %(i, p*100))
		for j, t in enumerate(thickness):	
			print('THICKNESS %i: %.2f cm' %(j, t/10000))
			for k, v in enumerate(voxelsize): 
				print('VOXEL SIZE %i: %.2f mm' %(k, v))
				geo_new = geo_base.replace('base', '%.2f_%i_%.2f' %(p, t, v))
				for n, e in enumerate(energy):
					print('ENERGY: %i keV'%e)
					out_root = 'simres/arm_%.2f_%i_%.2f_en%i.root' %(p, t, v, e)
					outs_list.append(out_root)
		print('\n')
	for i, o in enumerate(outs_list):
		print('PyRoot needed')	
						
if __name__ == '__main__':
	args = PARSER.parse_args()
	
	print("--------------------")
	print("---- Start  Run ----")
	print("--------------------")
	print('\n')
	
	run_mkARManalysis(**args.__dict__)
	
	print("--------------------")
	print("----- End  Run -----")
	print("--------------------")