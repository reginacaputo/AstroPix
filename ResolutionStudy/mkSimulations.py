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
PARSER.add_argument('-sim', '--simulate', type=bool, required=False, default=False,
                    help='True if you want to run the all the simulatios')

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
	src_base = data.SRC_BASE
	energy = data.ENERGY
	
	line_geometry = 1
	line_filename = 10
	line_energy = 16

	for i, p in enumerate(passive):
		print('PASSIVE %i: %i%%' %(i, p*100))
		for j, t in enumerate(thickness):	
			print('THICKNESS %i: %.2f cm' %(j, t/10000))
			for k, v in enumerate(voxelsize): 
				print('VOXEL SIZE %i: %.2f mm' %(k, v))
				geo_new = geo_base.replace('base', '%.2f_%i_%.2f' %(p, t, v))
				for n, e in enumerate(energy):
					print('ENERGY: %i keV'%e)
					src_new = src_base.replace('base', '%.2f_%i_%.2f_en%i' %(p, t, v, e))
					src_f = open(src_base, 'r')
					lines = src_f.readlines()
					if '.Spectrum' not in lines[line_energy]:
						print('ATT: line number for the energy parameter is not correct!')
						sys.exit()
					if 'Geometry' not in lines[line_geometry]:
						print('ATT: line number for the geometry is not correct!')
						sys.exit()
					if '.FileName' not in lines[line_filename]:
						print('ATT: line number for the file name is not correct!')
						sys.exit()
					line_list_e = lines[line_energy].split()
					line_list_e[-1] = str(e)+'\n'
					lines[line_energy] = ' '.join(line_list_e)
					line_list_g = lines[line_geometry].split()
					line_list_g[-1] = geo_new+'\n'
					lines[line_geometry] = ' '.join(line_list_g)
					line_list_f = lines[line_geometry].split()
					line_list_f[-1] = src_new+'\n'
					lines[line_filename] = ' '.join(line_list_f)
					src_f.close()
					with open(src_new, 'w') as f:
						for line in lines:
							f.write(line)
					f.close()
					
		print('\n')
	if kwargs['simulate'] == True:
		for s in os.listdir('source/'):
			print('---> Running %s...' %s)
			os.system('cosima source/%s' %s) 
			print('<--- done.')
		
						
if __name__ == '__main__':
	args = PARSER.parse_args()
	
	print("--------------------")
	print("---- Start  Run ----")
	print("--------------------")
	print('\n')
	
	run_mkGeometries(**args.__dict__)
	
	print("--------------------")
	print("----- End  Run -----")
	print("--------------------")