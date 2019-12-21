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
    
def run_mkRecon(**kwargs):
	assert(kwargs['config'].endswith('.py'))
	get_var_from_file(kwargs['config'])
	
	passive = data.PASSIVE
	thickness = data.THICKNESS
	voxelsize = data.VOXELSIZE
	geo_base = data.GEO_BASE
	src_base = data.SRC_BASE
	energy = data.ENERGY
	revan_cfg = data.REVAN_CFG
	
	geos_list, sims_list, outs_list, outlog_list = [], [], [], []
	for i, p in enumerate(passive):
		print('PASSIVE %i: %i%%' %(i, p*100))
		for j, t in enumerate(thickness):	
			print('THICKNESS %i: %.2f cm' %(j, t/10000))
			for k, v in enumerate(voxelsize): 
				print('VOXEL SIZE %i: %.2f mm' %(k, v))
				geo_new = geo_base.replace('base', '%.2f_%i_%.2f' %(p, t, v))
				for n, e in enumerate(energy):
					print('ENERGY: %i keV'%e)
					sim_new = 'simres/'+os.path.basename(src_base).replace('base', 
													'%.2f_%i_%.2f_en%i' %(p, t, v, e))+\
													'.inc1.id1.sim'
					out_root = 'simres/arm_%.2f_%i_%.2f_en%i' %(p, t, v, e)
					geos_list.append(geo_new)
					sims_list.append(sim_new)	
					outs_list.append(out_root)
					outlog_list.append('simres/revan-log_%.2f_%i_%.2f_en%i.txt' %(p, t, v, e))
		print('\n')
	for i, s in enumerate(sims_list):
		os.system('revan -f %s -g %s -c %s -a  > %s &' %(s, geos_list[i], 
														 revan_cfg, outlog_list[i]))
	print('---> done ...!')
						
if __name__ == '__main__':
	args = PARSER.parse_args()
	
	print("--------------------")
	print("---- Start  Run ----")
	print("--------------------")
	print('\n')
	
	run_mkRecon(**args.__dict__)
	
	print("--------------------")
	print("----- End  Run -----")
	print("--------------------")